# AB-G315 / C0 / engineer review

Original integration geometry referencing GALVI N.315.HYD.030/05 and PD.315 catalogue dimensions. This is not a GALVI manufacturing model or verified replacement. Purchased brake internals, load paths and shaft locking are not released.

NOT FOR MANUFACTURE. All dimensions are nominal mm. Drawings are orthographic reference projections, not complete production drawings. Hardware, fits, tolerances, GD&T, welds, material condition, shaft attachment, retention and performance remain to be approved. Envelope parts are not manufacturable internals.

Open `geometry-checks.json` before reviewing assembly. Intersections are recorded, not silently accepted. Models are static; no solved motion, FEA, CFD, thermal or physical qualification is included.

STEP: solid geometry. SVG: viewable nominal reference drawing. PDF: review drawing pack. BOM: part identity and make/buy status. These are original models, not copied competitor CAD.

Rebuild from repository: `uv venv --python 3.11 .cad-venv`, `uv pip install --python .cad-venv/bin/python -r engineering/cad/requirements.txt`, `.cad-venv/bin/python scripts/cad/build_models.py AB-G315`. Packaged scripts are source references; run them in the documented repository layout.
