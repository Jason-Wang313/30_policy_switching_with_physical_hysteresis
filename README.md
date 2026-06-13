# Policy Switching With Physical Hysteresis

Recovered paper package for robotics batch paper 30.

The project contains a Crossref-derived literature sweep, novelty/audit notes,
a small hysteresis-switching simulation, and an anonymous ICLR-style paper.

## Hardening Status

This is the v2 submission-hardened version. The added supervisor stress shows
the tradeoff: hysteresis+dwell reduces mean switch cost from 171.0 to 29.5
across 50 seeds, but mean tracking error rises from 0.090 to 0.186; an
over-hysteresis setting reduces switch cost to 11.4 but raises mean error to
0.439.

Build from the project root:

```powershell
python scripts\run_switch_hysteresis_sim.py
powershell -ExecutionPolicy Bypass -File scripts\build_pdf.ps1
```

The batch output PDF is copied to `C:/Users/wangz/Downloads/30.pdf`.
