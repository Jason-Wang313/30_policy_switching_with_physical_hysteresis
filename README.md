# Policy Switching With Physical Hysteresis

Recovered and v3 submission-hardened package for robotics batch paper 30.

The project contains a Crossref-derived literature sweep, novelty/audit notes,
the original toy hysteresis-switching simulation, a RAM-light full-scale
synthetic experiment suite, and a 25-page anonymous ICLR-style manuscript.

## Hardening Status

This is the v3 final full-scale version. The new suite covers 7 dynamics
families, 10 regimes, 12 supervisors, 40 seeds, and 8,064,000 represented step
decisions. Immediate greedy switching keeps low mean tracking error (0.015) but
accumulates high mean switch work (108.0) and transient risk (32.81). The
calibrated cost supervisor cuts mean switch work to 16.2 with mean error 0.067;
the oracle cost-aware supervisor gives the best utility, 0.034.

Build from the project root:

```powershell
python scripts\run_full_scale_hysteresis_suite.py
powershell -ExecutionPolicy Bypass -File scripts\build_pdf.ps1
```

The canonical final PDF is `C:/Users/wangz/Downloads/30.pdf`.
The final build removes the transient local `main.pdf`.
