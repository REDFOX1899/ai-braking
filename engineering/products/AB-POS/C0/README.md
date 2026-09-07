# AB-POS / C0 / engineer review

A direct-applied cartridge variant of the disc concept for controlled process braking. Loss of actuation releases braking force; it does not inherit spring-applied holding behaviour.

NOT FOR MANUFACTURE. All dimensions are nominal mm. Drawings are orthographic reference projections, not complete production drawings. Hardware, fits, tolerances, GD&T, welds, material condition, shaft attachment, retention and performance remain to be approved. Envelope parts are not manufacturable internals.

Open `geometry-checks.json` before reviewing assembly. Intersections are recorded, not silently accepted. Models are static; no solved motion, FEA, CFD, thermal or physical qualification is included.

STEP: solid geometry. SVG: viewable nominal reference drawing. PDF: review drawing pack. BOM: part identity and make/buy status. These are original models, not copied competitor CAD.

Rebuild from repository: `uv venv --python 3.11 .cad-venv`, `uv pip install --python .cad-venv/bin/python -r engineering/cad/requirements.txt`, `.cad-venv/bin/python scripts/cad/build_models.py AB-POS`. Packaged scripts are source references; run them in the documented repository layout.
