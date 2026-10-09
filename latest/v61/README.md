# v61 — Overlapping two-pair cube extensions

The main result is a written analytic proof candidate for four-dimensional bodies

```
conv([-1,1]^4, ±(a,u,p3,p4), ±(v,b,q3,q4)),
a,b > 1; all six other coordinates in [-1,1].
```

Cap overlaps are allowed. This is **not** a proof for arbitrary four-dimensional
centrally symmetric convex bodies. General-n exact volume formulas are included;
the full lower-bound argument in this snapshot is four-dimensional.

## Rebuild

Python 3.10+ (tested with the environment recorded in `provenance.json`):

```bash
python -m pip install -r requirements.txt
python replay.py --rebuild
```

The replay copies the manifest payload into a clean temporary directory, deletes
the two certificates there, reruns both verifiers, and compares output bytes with
the archived certificates. It does not rerun any earlier v1–v60 mathematics.

## Contents

- `report_zh.md`: hypotheses, complete reduction, geometric volume formulas,
  twelve parameter-domain certificates, scope and source information.
- `analytic_verifier.py`: generates the twelve complete-domain polynomial
  certificates and checks the cap coordinate change and calibration identities.
- `geometry_verifier.py`: 31 independent rational primal/polar reconstructions,
  27 local overlaps and 27 bridge hulls, plus the six-step example.
- `descent.py`: derivative-directed one-coordinate reduction of the displayed
  rational example; provides full-segment denominator and derivative certificates.
- `overlap_formula.py`: exact general-dimensional two-pair volume formulas.
- `exact_geometry.py`: inherited rational geometry utility; source hash recorded.

No floating-point convex hull or random sampling is used in the certificates.
The external Meyer–Reisner theorem, geometric decomposition, and universal
endpoint argument are written mathematics, **not** a Lean/Coq formal proof.
The work has not had independent peer review and makes no literature-priority claim.
