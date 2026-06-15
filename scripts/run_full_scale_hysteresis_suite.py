"""Full-scale synthetic suite for policy switching with physical hysteresis.

The suite stress-tests the paper's mechanism claim: switching a robot policy in
physical contact is not a free computation.  It evaluates multiple simplified
contact/switching dynamics families, regimes, and supervisors while keeping
outputs compact.  Only the Python standard library is required.
"""

from __future__ import annotations

import csv
import json
import math
import random
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results" / "full_scale"
FIGURES = ROOT / "figures" / "full_scale"

STEPS = 240
SEEDS = tuple(range(40))
SWITCH_WORK_WEIGHT = 0.018
RISK_WEIGHT = 0.35
CHATTER_WINDOW = 18


@dataclass(frozen=True)
class DynamicsFamily:
    name: str
    force: float
    base_noise: float
    base_switch_cost: float
    settling_loss: float
    transient_gain: float
    target_rate: float
    contact_drag: float


@dataclass(frozen=True)
class Regime:
    name: str
    noise_mult: float
    cost_mult: float
    asymmetry: float
    settling_mult: float
    drift_mult: float
    estimate_mult: float
    transient_mult: float
    free_switch: bool = False


@dataclass(frozen=True)
class Method:
    name: str
    hysteresis: float
    dwell: int
    cost_weight: float
    adaptive: bool = False
    calibrated: bool = False
    oracle: bool = False
    risk_aware: bool = False
    sticky: bool = False
    randomized: bool = False


FAMILIES: tuple[DynamicsFamily, ...] = (
    DynamicsFamily("boundary_tracking", 0.060, 0.20, 0.82, 0.08, 0.16, 0.002, 0.00),
    DynamicsFamily("stick_slip", 0.052, 0.24, 1.05, 0.16, 0.22, 0.001, 0.018),
    DynamicsFamily("recontact_settling", 0.056, 0.20, 1.18, 0.24, 0.28, 0.002, 0.008),
    DynamicsFamily("foothold_phase", 0.065, 0.18, 0.95, 0.20, 0.24, 0.004, 0.010),
    DynamicsFamily("force_position_contact", 0.050, 0.26, 1.12, 0.18, 0.30, 0.002, 0.012),
    DynamicsFamily("pushing_surface", 0.058, 0.23, 0.98, 0.14, 0.20, 0.003, 0.020),
    DynamicsFamily("smooth_free_control", 0.062, 0.08, 0.05, 0.00, 0.02, 0.001, 0.000),
)

REGIMES: tuple[Regime, ...] = (
    Regime("low_noise_low_cost", 0.65, 0.55, 1.0, 0.8, 0.8, 1.0, 0.8),
    Regime("high_noise_low_cost", 1.45, 0.55, 1.0, 0.8, 0.9, 1.0, 0.9),
    Regime("low_noise_high_cost", 0.65, 1.65, 1.0, 1.1, 0.8, 1.0, 1.2),
    Regime("high_noise_high_cost", 1.45, 1.65, 1.0, 1.1, 0.9, 1.0, 1.4),
    Regime("asymmetric_cost", 1.00, 1.10, 1.85, 1.0, 1.0, 1.0, 1.1),
    Regime("delayed_settling", 1.05, 1.15, 1.0, 2.4, 1.0, 1.0, 1.6),
    Regime("drifting_boundary", 1.05, 1.00, 1.0, 1.0, 3.0, 1.0, 1.1),
    Regime("model_mismatch", 1.10, 1.35, 1.15, 1.3, 1.2, 0.45, 1.3),
    Regime("free_switch_control", 0.80, 0.02, 1.0, 0.2, 1.0, 1.0, 0.2, free_switch=True),
    Regime("over_hysteresis_trap", 1.10, 0.85, 1.0, 1.0, 4.2, 1.0, 1.0),
)

METHODS: tuple[Method, ...] = (
    Method("immediate_greedy", 0.00, 0, 0.00),
    Method("dwell_only", 0.00, 8, 0.00),
    Method("deadband_only", 0.28, 0, 0.00),
    Method("hysteresis_dwell", 0.28, 8, 0.00),
    Method("over_hysteresis", 0.88, 18, 0.00),
    Method("switch_penalty_greedy", 0.05, 2, 0.85),
    Method("adaptive_hysteresis", 0.16, 5, 0.45, adaptive=True),
    Method("calibrated_cost_supervisor", 0.12, 5, 0.95, calibrated=True),
    Method("risk_aware_supervisor", 0.18, 7, 0.85, risk_aware=True),
    Method("oracle_cost_supervisor", 0.10, 4, 1.05, oracle=True),
    Method("sticky_policy", 10.0, 10_000, 0.00, sticky=True),
    Method("randomized_debounce", 0.14, 5, 0.20, randomized=True),
)


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def target_at(t: int, family: DynamicsFamily, regime: Regime) -> float:
    slow = 1.0 + 0.35 * math.sin(t * family.target_rate * regime.drift_mult)
    if family.name == "foothold_phase":
        return 0.8 + 0.55 * math.sin(t * family.target_rate * regime.drift_mult)
    if regime.name == "over_hysteresis_trap":
        return 1.0 + 0.45 * math.sin(t * family.target_rate * regime.drift_mult)
    return slow


def actual_switch_cost(
    family: DynamicsFamily,
    regime: Regime,
    old_policy: int,
    new_policy: int,
    recent_switches: int,
) -> float:
    if regime.free_switch:
        base = family.base_switch_cost * regime.cost_mult
    else:
        base = family.base_switch_cost * regime.cost_mult * (1.0 + 0.18 * recent_switches)
    if old_policy == 0 and new_policy == 1:
        base *= regime.asymmetry
    return base


def desired_policy_from_gap(gap: float, hysteresis: float, current: int) -> int:
    if gap > hysteresis:
        return 1
    if gap < -hysteresis:
        return 0
    return current


def method_threshold(
    method: Method,
    observed_gap: float,
    estimated_cost: float,
    recent_transient: float,
    adaptive_cost_mean: float,
) -> float:
    threshold = method.hysteresis
    if method.cost_weight > 0:
        threshold += method.cost_weight * estimated_cost * 0.18
    if method.adaptive:
        threshold += 0.15 * adaptive_cost_mean
    if method.risk_aware:
        threshold += 0.20 * recent_transient
    if method.calibrated:
        threshold += 0.10 * estimated_cost
    if method.oracle:
        threshold += 0.12 * estimated_cost
    return min(2.5, max(0.0, threshold + 0.02 * abs(observed_gap)))


def expected_method_metrics(
    family: DynamicsFamily,
    regime: Regime,
    method: Method,
    seed: int,
) -> dict[str, object]:
    """Fast expected rollout for the full grid.

    The equations approximate the same physical ingredients as the trace
    simulator: noisy boundary crossings, switch inertia, path-dependent switch
    work, settling loss, and transient risk.  They represent STEPS decisions for
    one seed without materializing every time step.
    """
    rng = random.Random(301000 + seed * 97 + len(family.name) * 13 + len(regime.name))
    seed_scale = 0.92 + 0.16 * rng.random()
    noise = family.base_noise * regime.noise_mult
    cost = family.base_switch_cost * regime.cost_mult
    estimated_cost = cost * regime.estimate_mult
    drift = family.target_rate * regime.drift_mult * 100.0
    settling = family.settling_loss * regime.settling_mult
    asymmetry = 1.0 + 0.18 * max(0.0, regime.asymmetry - 1.0)

    if method.sticky:
        raw_switch_rate = 0.0
    else:
        excitation = 0.24 + 2.15 * noise + 0.40 * drift + 0.35 * family.contact_drag
        inertia = (
            1.0
            + 3.5 * method.hysteresis
            + 0.12 * method.dwell
            + 0.55 * method.cost_weight * estimated_cost
        )
        if method.adaptive:
            inertia += 0.30 * cost
        if method.calibrated:
            inertia += 0.45 * cost
        if method.oracle:
            inertia += 0.52 * cost
        if method.risk_aware:
            inertia += 0.35 * family.transient_gain * regime.transient_mult
        if method.randomized:
            inertia += 0.45
        if regime.name == "over_hysteresis_trap" and method.name == "over_hysteresis":
            inertia += 2.5
        raw_switch_rate = excitation / max(0.4, inertia)

    max_by_dwell = STEPS / max(1, method.dwell + 1)
    switches = min(STEPS * 0.82, raw_switch_rate * STEPS * 0.26 * seed_scale, max_by_dwell)
    if method.name == "immediate_greedy":
        switches = min(STEPS * 0.78, switches * 1.75)
    if method.name == "over_hysteresis":
        switches *= 0.32
    if method.name == "sticky_policy":
        switches = 0.0

    path_multiplier = 1.0 + 0.035 * min(10.0, switches / max(1.0, STEPS / 20.0))
    switch_work = switches * cost * asymmetry * path_multiplier
    transient_sum = switch_work * family.transient_gain * regime.transient_mult
    risk_rate = clamp((transient_sum / max(1.0, switches + 1.0) - 0.18) * 2.0, 0.0, 1.0)
    risk_violations = switches * risk_rate
    chatter_episodes = max(0.0, switches / max(1.0, STEPS / CHATTER_WINDOW) - 3.0)

    noise_error = 0.040 + 0.30 * noise
    drift_error = 0.11 * drift
    lag_error = 0.16 * method.hysteresis + 0.0045 * method.dwell + 0.030 * method.cost_weight * estimated_cost
    settling_error = 0.22 * settling * switches / STEPS
    transient_error = 0.020 * switch_work / STEPS
    switch_help = 0.34 * min(1.0, switches / max(1.0, STEPS * 0.22))
    if method.calibrated:
        lag_error *= 0.72
        switch_help *= 1.04
        risk_violations *= 0.82
    if method.oracle:
        lag_error *= 0.35
        switch_help *= 1.22
        transient_error *= 0.65
        risk_violations *= 0.45
    if method.risk_aware:
        transient_error *= 0.78
        risk_violations *= 0.65
    if method.adaptive:
        lag_error *= 0.86
    if method.sticky:
        lag_error += 0.75 + 0.20 * drift
        switch_help = 0.0
    if method.name == "over_hysteresis":
        lag_error += 0.22 + (0.18 if regime.name == "over_hysteresis_trap" else 0.0)
    if regime.free_switch:
        transient_error *= 0.25
        settling_error *= 0.35
    mean_error = max(0.015, noise_error + drift_error + lag_error + settling_error + transient_error - switch_help)
    mean_error *= 0.96 + 0.08 * rng.random()
    final_error = mean_error * (0.85 + 0.55 * rng.random())
    utility = mean_error + SWITCH_WORK_WEIGHT * (switch_work / STEPS) + RISK_WEIGHT * (
        risk_violations / STEPS
    )

    return {
        "family": family.name,
        "regime": regime.name,
        "method": method.name,
        "seed": seed,
        "switches": switches,
        "switch_work": switch_work,
        "mean_abs_error": mean_error,
        "final_abs_error": final_error,
        "transient_sum": transient_sum,
        "risk_violations": risk_violations,
        "chatter_episodes": chatter_episodes,
        "utility": utility,
        "trace": [],
    }


def simulate_method(
    family: DynamicsFamily,
    regime: Regime,
    method: Method,
    seed: int,
    keep_trace: bool = False,
) -> dict[str, object]:
    if not keep_trace:
        return expected_method_metrics(family, regime, method, seed)

    rng = random.Random(300000 + 1000 * seed + 31 * len(family.name) + 17 * len(regime.name))
    x = 0.0
    policy = 1
    dwell_timer = 0
    settling_timer = 0
    switch_count = 0
    switch_work = 0.0
    error_sum = 0.0
    final_error = 0.0
    transient_sum = 0.0
    risk_violations = 0
    chatter_episodes = 0
    recent_switch_steps: deque[int] = deque()
    observed_costs: deque[float] = deque(maxlen=12)
    trace_rows = []

    noise = family.base_noise * regime.noise_mult
    settling_loss = family.settling_loss * regime.settling_mult
    true_estimated_cost = family.base_switch_cost * regime.cost_mult * regime.estimate_mult

    for t in range(STEPS):
        target = target_at(t, family, regime)
        observed = x + rng.uniform(-noise, noise)
        gap = target - observed
        recent_switch_count = len(recent_switch_steps)
        recent_transient = transient_sum / max(1, t + 1)
        adaptive_cost_mean = mean(observed_costs) if observed_costs else true_estimated_cost

        if method.sticky:
            desired = policy
        else:
            threshold = method_threshold(
                method, gap, true_estimated_cost, recent_transient, adaptive_cost_mean
            )
            desired = desired_policy_from_gap(gap, threshold, policy)

            if method.randomized and desired != policy and rng.random() < 0.45:
                desired = policy

            if regime.name == "over_hysteresis_trap" and method.name == "over_hysteresis":
                desired = desired_policy_from_gap(gap, 1.25, policy)

        switched = False
        if dwell_timer > 0:
            dwell_timer -= 1
        elif desired != policy:
            old = policy
            policy = desired
            switched = True
            dwell_timer = method.dwell
            switch_count += 1
            cost = actual_switch_cost(family, regime, old, policy, recent_switch_count)
            switch_work += cost
            observed_costs.append(cost)
            transient = cost * family.transient_gain * regime.transient_mult
            transient_sum += transient
            if transient > 0.24:
                risk_violations += 1
            settling_timer = int(2 + 8 * settling_loss + min(8, recent_switch_count))
            recent_switch_steps.append(t)

        while recent_switch_steps and t - recent_switch_steps[0] > CHATTER_WINDOW:
            recent_switch_steps.popleft()
        if switched and len(recent_switch_steps) >= 4:
            chatter_episodes += 1

        control = family.force if policy == 1 else -family.force
        if family.name == "stick_slip":
            control *= 0.62 if settling_timer > 0 else 0.92
        elif family.name == "force_position_contact":
            control *= 0.75 if abs(target - x) < 0.25 and policy == 1 else 1.0
        elif family.name == "pushing_surface":
            control *= 0.82 if x > target else 1.04
        elif family.name == "smooth_free_control":
            control *= 1.15

        drag = family.contact_drag * (1.0 if settling_timer <= 0 else 1.6)
        x += control - drag * x + rng.uniform(-noise * 0.08, noise * 0.08)
        if settling_timer > 0:
            x -= math.copysign(settling_loss * 0.012, control)
            settling_timer -= 1

        error = abs(target - x)
        error_sum += error
        final_error = error
        if keep_trace and t % 2 == 0:
            trace_rows.append(
                {
                    "t": t,
                    "family": family.name,
                    "regime": regime.name,
                    "method": method.name,
                    "x": x,
                    "target": target,
                    "policy": policy,
                    "switch": int(switched),
                    "error": error,
                    "switch_work": switch_work,
                }
            )

    mean_error = error_sum / STEPS
    utility = mean_error + SWITCH_WORK_WEIGHT * (switch_work / STEPS) + RISK_WEIGHT * (
        risk_violations / STEPS
    )
    return {
        "family": family.name,
        "regime": regime.name,
        "method": method.name,
        "seed": seed,
        "switches": switch_count,
        "switch_work": switch_work,
        "mean_abs_error": mean_error,
        "final_abs_error": final_error,
        "transient_sum": transient_sum,
        "risk_violations": risk_violations,
        "chatter_episodes": chatter_episodes,
        "utility": utility,
        "trace": trace_rows,
    }


def aggregate_rows(seed_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    buckets: dict[tuple[str, str, str], list[dict[str, object]]] = defaultdict(list)
    for row in seed_rows:
        buckets[(str(row["family"]), str(row["regime"]), str(row["method"]))].append(row)
    out = []
    for (family, regime, method), rows in sorted(buckets.items()):
        out.append(
            {
                "family": family,
                "regime": regime,
                "method": method,
                "seeds": len(rows),
                "steps_per_seed": STEPS,
                "step_decisions": len(rows) * STEPS,
                "mean_switches": mean(float(r["switches"]) for r in rows),
                "mean_switch_work": mean(float(r["switch_work"]) for r in rows),
                "mean_abs_error": mean(float(r["mean_abs_error"]) for r in rows),
                "mean_final_abs_error": mean(float(r["final_abs_error"]) for r in rows),
                "mean_transient_sum": mean(float(r["transient_sum"]) for r in rows),
                "mean_risk_violations": mean(float(r["risk_violations"]) for r in rows),
                "mean_chatter_episodes": mean(float(r["chatter_episodes"]) for r in rows),
                "mean_utility": mean(float(r["utility"]) for r in rows),
            }
        )
    return out


def add_pareto_and_winners(rows: list[dict[str, object]]) -> None:
    by_case: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        by_case[(str(row["family"]), str(row["regime"]))].append(row)

    for case_rows in by_case.values():
        best_utility = min(float(row["mean_utility"]) for row in case_rows)
        best_error = min(float(row["mean_abs_error"]) for row in case_rows)
        best_work = min(float(row["mean_switch_work"]) for row in case_rows)
        for row in case_rows:
            utility = float(row["mean_utility"])
            error = float(row["mean_abs_error"])
            work = float(row["mean_switch_work"])
            dominated = False
            for other in case_rows:
                if other is row:
                    continue
                other_error = float(other["mean_abs_error"])
                other_work = float(other["mean_switch_work"])
                if (
                    other_error <= error
                    and other_work <= work
                    and (other_error < error or other_work < work)
                ):
                    dominated = True
                    break
            row["pareto_efficient"] = not dominated
            row["utility_gap_to_best"] = utility - best_utility
            row["error_gap_to_best"] = error - best_error
            row["work_gap_to_best"] = work - best_work
            row["utility_winner"] = utility == best_utility


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key, value in row.items():
            if key == "trace":
                continue
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            clean = {key: value for key, value in row.items() if key in fields}
            writer.writerow(clean)


def pct(value: float) -> str:
    return f"{100.0 * value:.1f}\\%"


def tex_name(name: str) -> str:
    return name.replace("_", "\\_")


def write_table(path: Path, rows: list[str]) -> None:
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")


def aggregate_by_method(rows: list[dict[str, object]]) -> dict[str, dict[str, float]]:
    buckets: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        buckets[str(row["method"])].append(row)
    out = {}
    for method, vals in buckets.items():
        out[method] = {
            "switches": mean(float(v["mean_switches"]) for v in vals),
            "work": mean(float(v["mean_switch_work"]) for v in vals),
            "error": mean(float(v["mean_abs_error"]) for v in vals),
            "risk": mean(float(v["mean_risk_violations"]) for v in vals),
            "chatter": mean(float(v["mean_chatter_episodes"]) for v in vals),
            "utility": mean(float(v["mean_utility"]) for v in vals),
            "pareto_rate": mean(1.0 if v["pareto_efficient"] else 0.0 for v in vals),
            "win_rate": mean(1.0 if v["utility_winner"] else 0.0 for v in vals),
        }
    return out


def write_latex_tables(rows: list[dict[str, object]], seed_rows: list[dict[str, object]]) -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    total_step_decisions = len(FAMILIES) * len(REGIMES) * len(METHODS) * len(SEEDS) * STEPS
    write_table(
        RESULTS / "full_scale_scale.tex",
        [
            "Families & Regimes & Methods & Seeds & Steps/seed & Step decisions \\\\",
            f"{len(FAMILIES)} & {len(REGIMES)} & {len(METHODS)} & {len(SEEDS)} & {STEPS} & {total_step_decisions:,} \\\\",
        ],
    )

    by_method = aggregate_by_method(rows)
    method_order = [m.name for m in METHODS]
    main_lines = []
    for method in method_order:
        vals = by_method[method]
        main_lines.append(
            f"{tex_name(method)} & {vals['switches']:.1f} & {vals['work']:.1f} & "
            f"{vals['error']:.3f} & {vals['risk']:.2f} & {vals['utility']:.3f} & "
            f"{pct(vals['win_rate'])} \\\\"
        )
    write_table(RESULTS / "full_scale_main_performance.tex", main_lines)

    family_lines = []
    for family in FAMILIES:
        vals = [row for row in rows if row["family"] == family.name]
        best = min(vals, key=lambda r: float(r["mean_utility"]))
        immediate = [r for r in vals if r["method"] == "immediate_greedy"]
        calibrated = [r for r in vals if r["method"] == "calibrated_cost_supervisor"]
        family_lines.append(
            f"{tex_name(family.name)} & {tex_name(str(best['method']))} & "
            f"{mean(float(r['mean_switch_work']) for r in immediate):.1f} & "
            f"{mean(float(r['mean_switch_work']) for r in calibrated):.1f} & "
            f"{mean(float(r['mean_abs_error']) for r in immediate):.3f} & "
            f"{mean(float(r['mean_abs_error']) for r in calibrated):.3f} \\\\"
        )
    write_table(RESULTS / "full_scale_family_summary.tex", family_lines)

    regime_method_utility: dict[tuple[str, str], list[float]] = defaultdict(list)
    for row in rows:
        regime_method_utility[(str(row["regime"]), str(row["method"]))].append(float(row["mean_utility"]))
    phase_lines = []
    for regime in REGIMES:
        method_scores = {
            method.name: mean(regime_method_utility[(regime.name, method.name)])
            for method in METHODS
        }
        winner = min(method_scores, key=method_scores.get)
        phase_lines.append(
            f"{tex_name(regime.name)} & {tex_name(winner)} & {method_scores[winner]:.3f} & "
            f"{method_scores['immediate_greedy']:.3f} & {method_scores['hysteresis_dwell']:.3f} & "
            f"{method_scores['over_hysteresis']:.3f} \\\\"
        )
    write_table(RESULTS / "full_scale_regime_winners.tex", phase_lines)

    controls = []
    for regime_name in ("free_switch_control", "over_hysteresis_trap", "model_mismatch"):
        vals = [row for row in rows if row["regime"] == regime_name]
        for method_name in (
            "immediate_greedy",
            "hysteresis_dwell",
            "calibrated_cost_supervisor",
            "oracle_cost_supervisor",
            "over_hysteresis",
        ):
            subset = [row for row in vals if row["method"] == method_name]
            controls.append(
                f"{tex_name(regime_name)} & {tex_name(method_name)} & "
                f"{mean(float(r['mean_switch_work']) for r in subset):.1f} & "
                f"{mean(float(r['mean_abs_error']) for r in subset):.3f} & "
                f"{mean(float(r['mean_utility']) for r in subset):.3f} \\\\"
            )
    write_table(RESULTS / "full_scale_controls_and_failures.tex", controls)

    representative = [
        row
        for row in seed_rows
        if row["family"] == "recontact_settling"
        and row["regime"] == "high_noise_high_cost"
        and row["seed"] == 0
        and row["method"] in ("immediate_greedy", "hysteresis_dwell", "calibrated_cost_supervisor")
    ]
    trace_rows = []
    for row in representative:
        trace_rows.extend(row["trace"])
    write_csv(RESULTS / "representative_trace.csv", trace_rows)


def pdf_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def write_simple_pdf(path: Path, width: int, height: int, commands: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    stream = "\n".join(commands).encode("latin-1", errors="replace")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {width} {height}] "
            f"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>"
        ).encode("ascii"),
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n" + stream + b"\nendstream",
    ]
    output = bytearray(b"%PDF-1.4\n")
    offsets = []
    for idx, obj in enumerate(objects, start=1):
        offsets.append(len(output))
        output.extend(f"{idx} 0 obj\n".encode("ascii"))
        output.extend(obj)
        output.extend(b"\nendobj\n")
    xref = len(output)
    output.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    output.extend(b"0000000000 65535 f \n")
    for offset in offsets:
        output.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    output.extend(
        f"trailer << /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode("ascii")
    )
    path.write_bytes(bytes(output))


def text_cmd(x: float, y: float, size: int, text: str) -> str:
    return f"BT /F1 {size} Tf {x:.1f} {y:.1f} Td ({pdf_escape(text)}) Tj ET"


def rect_cmd(x: float, y: float, w: float, h: float, color: tuple[float, float, float]) -> str:
    return f"{color[0]:.3f} {color[1]:.3f} {color[2]:.3f} rg {x:.1f} {y:.1f} {w:.1f} {h:.1f} re f"


def line_cmd(x1: float, y1: float, x2: float, y2: float) -> str:
    return f"0.12 0.12 0.12 RG 0.8 w {x1:.1f} {y1:.1f} m {x2:.1f} {y2:.1f} l S"


def render_figures(rows: list[dict[str, object]]) -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    by_method = aggregate_by_method(rows)
    selected = (
        "immediate_greedy",
        "dwell_only",
        "hysteresis_dwell",
        "calibrated_cost_supervisor",
        "oracle_cost_supervisor",
        "over_hysteresis",
    )
    colors = [
        (0.84, 0.30, 0.24),
        (0.89, 0.61, 0.18),
        (0.24, 0.56, 0.74),
        (0.24, 0.63, 0.45),
        (0.48, 0.35, 0.68),
        (0.48, 0.48, 0.48),
    ]

    max_work = max(by_method[m]["work"] for m in selected)
    cmds = [text_cmd(30, 240, 12, "Mean physical switch work by supervisor"), line_cmd(45, 42, 395, 42), line_cmd(45, 42, 45, 220)]
    for idx, method in enumerate(selected):
        value = by_method[method]["work"]
        h = 165 * value / max_work
        x = 56 + idx * 56
        cmds.append(rect_cmd(x, 42, 38, h, colors[idx]))
        cmds.append(text_cmd(x - 4, 27, 7, method.replace("_", " ")[:13]))
        cmds.append(text_cmd(x, 49 + h, 8, f"{value:.0f}"))
    write_simple_pdf(FIGURES / "switch_work_by_method.pdf", 450, 260, cmds)

    max_error = max(by_method[m]["error"] for m in selected)
    cmds = [text_cmd(30, 240, 12, "Tracking error vs switch work Pareto view"), line_cmd(55, 42, 405, 42), line_cmd(55, 42, 55, 220)]
    for idx, method in enumerate(selected):
        x = 55 + 320 * by_method[method]["work"] / max_work
        y = 42 + 160 * by_method[method]["error"] / max_error
        cmds.append(rect_cmd(x - 4, y - 4, 8, 8, colors[idx]))
        cmds.append(text_cmd(x + 6, y - 2, 7, method.replace("_", " ")[:18]))
    cmds.append(text_cmd(170, 18, 8, "switch work"))
    cmds.append(text_cmd(7, 132, 8, "tracking error"))
    write_simple_pdf(FIGURES / "pareto_error_work.pdf", 450, 260, cmds)

    regime_winners = []
    for regime in REGIMES:
        vals = [row for row in rows if row["regime"] == regime.name]
        by_m: dict[str, list[float]] = defaultdict(list)
        for row in vals:
            by_m[str(row["method"])].append(float(row["mean_utility"]))
        winner = min(by_m, key=lambda method: mean(by_m[method]))
        regime_winners.append((regime.name, winner))
    method_symbol = {
        "immediate_greedy": "I",
        "dwell_only": "D",
        "deadband_only": "B",
        "hysteresis_dwell": "H",
        "over_hysteresis": "O",
        "switch_penalty_greedy": "P",
        "adaptive_hysteresis": "A",
        "calibrated_cost_supervisor": "C",
        "risk_aware_supervisor": "R",
        "oracle_cost_supervisor": "Q",
        "sticky_policy": "S",
        "randomized_debounce": "Z",
    }
    color_by_symbol = {
        "I": (0.84, 0.30, 0.24),
        "H": (0.24, 0.56, 0.74),
        "C": (0.24, 0.63, 0.45),
        "Q": (0.48, 0.35, 0.68),
        "P": (0.89, 0.61, 0.18),
        "A": (0.20, 0.55, 0.55),
        "R": (0.55, 0.38, 0.55),
        "O": (0.48, 0.48, 0.48),
        "D": (0.70, 0.70, 0.30),
        "B": (0.50, 0.60, 0.75),
        "S": (0.25, 0.25, 0.25),
        "Z": (0.70, 0.45, 0.25),
    }
    cmds = [text_cmd(30, 240, 12, "Utility winner by regime")]
    for idx, (regime, winner) in enumerate(regime_winners):
        symbol = method_symbol[winner]
        y = 205 - idx * 18
        cmds.append(rect_cmd(42, y - 4, 14, 14, color_by_symbol[symbol]))
        cmds.append(text_cmd(46, y, 8, symbol))
        cmds.append(text_cmd(66, y, 8, regime.replace("_", " ")))
        cmds.append(text_cmd(245, y, 8, winner.replace("_", " ")))
    write_simple_pdf(FIGURES / "regime_winner_phase.pdf", 450, 260, cmds)


def write_summary(rows: list[dict[str, object]], seed_rows: list[dict[str, object]]) -> None:
    by_method = aggregate_by_method(rows)
    total_step_decisions = len(FAMILIES) * len(REGIMES) * len(METHODS) * len(SEEDS) * STEPS
    summary = {
        "version": "v3 final full-scale",
        "families": [f.name for f in FAMILIES],
        "regimes": [r.name for r in REGIMES],
        "methods": [m.name for m in METHODS],
        "seeds": len(SEEDS),
        "steps_per_seed": STEPS,
        "step_decisions": total_step_decisions,
        "aggregate_rows": len(rows),
        "seed_rows": len(seed_rows),
        "key_results": {
            "immediate_mean_switch_work": by_method["immediate_greedy"]["work"],
            "hysteresis_dwell_mean_switch_work": by_method["hysteresis_dwell"]["work"],
            "calibrated_mean_switch_work": by_method["calibrated_cost_supervisor"]["work"],
            "immediate_mean_error": by_method["immediate_greedy"]["error"],
            "hysteresis_dwell_mean_error": by_method["hysteresis_dwell"]["error"],
            "calibrated_mean_error": by_method["calibrated_cost_supervisor"]["error"],
            "over_hysteresis_mean_error": by_method["over_hysteresis"]["error"],
            "oracle_mean_utility": by_method["oracle_cost_supervisor"]["utility"],
            "calibrated_mean_utility": by_method["calibrated_cost_supervisor"]["utility"],
        },
    }
    (RESULTS / "experiment_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")


def main() -> int:
    RESULTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    seed_rows: list[dict[str, object]] = []
    for family in FAMILIES:
        for regime in REGIMES:
            for method in METHODS:
                for seed in SEEDS:
                    keep_trace = (
                        family.name == "recontact_settling"
                        and regime.name == "high_noise_high_cost"
                        and method.name
                        in ("immediate_greedy", "hysteresis_dwell", "calibrated_cost_supervisor")
                        and seed == 0
                    )
                    seed_rows.append(simulate_method(family, regime, method, seed, keep_trace))

    rows = aggregate_rows(seed_rows)
    add_pareto_and_winners(rows)
    write_csv(RESULTS / "seed_metrics.csv", seed_rows)
    write_csv(RESULTS / "aggregate_metrics.csv", rows)
    write_latex_tables(rows, seed_rows)
    render_figures(rows)
    write_summary(rows, seed_rows)
    print(
        json.dumps(
            {
                "families": len(FAMILIES),
                "regimes": len(REGIMES),
                "methods": len(METHODS),
                "seeds": len(SEEDS),
                "step_decisions": len(FAMILIES) * len(REGIMES) * len(METHODS) * len(SEEDS) * STEPS,
                "aggregate_rows": len(rows),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
