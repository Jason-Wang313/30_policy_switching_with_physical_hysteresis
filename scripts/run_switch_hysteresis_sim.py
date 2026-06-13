from __future__ import annotations

from pathlib import Path
import csv
import math
import random

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figures"
RESULTS = ROOT / "results"
OUT.mkdir(exist_ok=True)
RESULTS.mkdir(exist_ok=True)


def simulate(seed=7, steps=400, noise=0.22, switch_cost=0.8, hysteresis=0.35, dwell=6):
    rng = random.Random(seed)
    x = 0.0
    target = 1.0
    policy = 0  # 0: pull left, 1: pull right
    policy_h = 0
    dwell_timer = 0
    xs_i, xs_h = [], []
    ps_i, ps_h = [], []
    switches_i = switches_h = 0
    work_i = work_h = 0.0
    xi = xh = x
    for t in range(steps):
        obs_i = xi + rng.uniform(-noise, noise)
        obs_h = xh + rng.uniform(-noise, noise)
        # immediate switch baseline
        desired_i = 1 if target - obs_i > 0 else 0
        if desired_i != policy:
            policy = desired_i
            switches_i += 1
            work_i += switch_cost
        force_i = 0.06 if policy == 1 else -0.06
        xi += force_i + rng.uniform(-noise * 0.2, noise * 0.2)
        xs_i.append(xi)
        ps_i.append(policy)

        # hysteresis + dwell supervisor
        desired_h = 1 if target - obs_h > hysteresis else 0 if target - obs_h < -hysteresis else policy_h
        if dwell_timer > 0:
            dwell_timer -= 1
        elif desired_h != policy_h:
            policy_h = desired_h
            dwell_timer = dwell
            switches_h += 1
            work_h += switch_cost
        force_h = 0.06 if policy_h == 1 else -0.06
        xh += force_h + rng.uniform(-noise * 0.2, noise * 0.2)
        xs_h.append(xh)
        ps_h.append(policy_h)
    return xs_i, xs_h, ps_i, ps_h, switches_i, switches_h, work_i, work_h


def simulate_controller(seed=7, steps=400, noise=0.22, switch_cost=0.8, hysteresis=0.35, dwell=6):
    rng = random.Random(seed)
    x = 0.0
    target = 1.0
    policy = 0
    dwell_timer = 0
    switches = 0
    switch_work = 0.0
    error_sum = 0.0
    for _ in range(steps):
        obs = x + rng.uniform(-noise, noise)
        gap = target - obs
        desired = 1 if gap > hysteresis else 0 if gap < -hysteresis else policy
        if dwell_timer > 0:
            dwell_timer -= 1
        elif desired != policy:
            policy = desired
            dwell_timer = dwell
            switches += 1
            switch_work += switch_cost
        force = 0.06 if policy == 1 else -0.06
        x += force + rng.uniform(-noise * 0.2, noise * 0.2)
        error_sum += abs(target - x)
    return {
        "switches": switches,
        "switch_cost": switch_work,
        "mean_abs_error": error_sum / steps,
        "final_abs_error": abs(target - x),
    }


def supervisor_stress(seeds=range(50)):
    configs = [
        ("immediate_switch", 0.0, 0),
        ("dwell_only", 0.0, 6),
        ("deadband_only", 0.35, 0),
        ("hysteresis_dwell", 0.35, 6),
        ("over_hysteresis", 0.90, 18),
    ]
    rows = []
    for name, hysteresis, dwell in configs:
        per_seed = [simulate_controller(seed=s, hysteresis=hysteresis, dwell=dwell) for s in seeds]
        rows.append(
            {
                "controller": name,
                "hysteresis": hysteresis,
                "dwell": dwell,
                "mean_switches": sum(r["switches"] for r in per_seed) / len(per_seed),
                "mean_switch_cost": sum(r["switch_cost"] for r in per_seed) / len(per_seed),
                "mean_abs_error": sum(r["mean_abs_error"] for r in per_seed) / len(per_seed),
                "mean_final_abs_error": sum(r["final_abs_error"] for r in per_seed) / len(per_seed),
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_stress_table(rows: list[dict[str, object]]) -> None:
    lines = [
        "\\begin{tabular}{lrrrr}",
        "\\toprule",
        "Controller & Switches & Switch cost & Mean error & Final error \\\\",
        "\\midrule",
    ]
    for row in rows:
        label = str(row["controller"]).replace("_", " ")
        lines.append(
            f"{label} & {float(row['mean_switches']):.1f} & {float(row['mean_switch_cost']):.1f} & "
            f"{float(row['mean_abs_error']):.3f} & {float(row['mean_final_abs_error']):.3f} \\\\"
        )
    lines.extend(["\\bottomrule", "\\end{tabular}", ""])
    (RESULTS / "supervisor_stress_table.tex").write_text("\n".join(lines), encoding="utf-8")


def main():
    xs_i, xs_h, ps_i, ps_h, sw_i, sw_h, work_i, work_h = simulate()
    fig, axs = plt.subplots(3, 1, figsize=(8.5, 7), sharex=True)
    axs[0].plot(xs_i, label=f"immediate-switch (switches={sw_i})", lw=2)
    axs[0].plot(xs_h, label=f"hysteresis-aware (switches={sw_h})", lw=2)
    axs[0].axhline(1.0, color="k", ls="--", lw=1)
    axs[0].set_ylabel("contact state")
    axs[0].legend(frameon=False, loc="upper left")

    axs[1].step(range(len(ps_i)), ps_i, where="post", label="immediate", lw=2)
    axs[1].step(range(len(ps_h)), ps_h, where="post", label="hysteresis-aware", lw=2)
    axs[1].set_ylabel("policy id")
    axs[1].legend(frameon=False, loc="upper left")

    axs[2].bar([0, 1], [work_i, work_h], color=["#d95f02", "#1b9e77"])
    axs[2].set_xticks([0, 1], ["immediate", "hysteresis"])
    axs[2].set_ylabel("switch cost")
    axs[2].set_title(f"Toy physical hysteresis: work {work_i:.2f} vs {work_h:.2f}")
    axs[2].set_xlabel("time step")
    fig.tight_layout()
    fig.savefig(OUT / "switch_hysteresis_sim.png", dpi=200)
    rows = supervisor_stress()
    write_csv(RESULTS / "supervisor_stress.csv", rows)
    write_stress_table(rows)
    print({"switches_i": sw_i, "switches_h": sw_h, "work_i": work_i, "work_h": work_h, "stress_rows": len(rows)})


if __name__ == "__main__":
    main()
