from __future__ import annotations

from pathlib import Path
import math
import random

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figures"
OUT.mkdir(exist_ok=True)


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
    print({"switches_i": sw_i, "switches_h": sw_h, "work_i": work_i, "work_h": work_h})


if __name__ == "__main__":
    main()
