# AI Braking: mechanical development programme

Revision C0 | 7 September 2026 | Original engineering concepts for review

## What this release actually contains

Twelve independently addressable product workspaces, one representative static CAD concept for each existing portfolio family, named solid STEP parts and assemblies, nominal orthographic SVG/PDF review sheets, a make/buy BOM, candidate material/process choices, assembly intent, study targets and open risks. Source models use CadQuery 2.6.1 / OpenCascade and millimetres. These are original models, not copied competitor drawings.

This is an initial concept design review. It is not a complete detailed design, a functional prototype, an offer to supply rated brakes, or a manufacturing release. Geometry-valid solids can still represent an incomplete mechanism. No FEA, thermal simulation, solved kinematics, hydraulic simulation, electrical circuit, fatigue qualification or physical brake test has been performed. Every sheet and package carries C0 status.

## Product scope and sequence

1. **AB-ROT rotating components:** first shared disc and hub nominal interface. Review shaft attachment, bolted joint and friction material selection first. The drum reference is included in AB-DR, not substituted for the disc.
2. **AB-DR drum platform:** first candidate brake architecture. The spring/equalizer and thruster linkage are reserved layouts. Finish force path and motion before detailed stresses.
3. **AB-DC spring-applied disc platform:** parallel requirements only unless a second mechanical lead is available. Bought release cartridge; bridge/pad geometry is a concept.
4. **AB-SP service kits:** controlled parts for our own assemblies only. Compound and retention depend on a friction specialist.
5. **AB-MON inspection fixture:** non-safety metrology fixture concept. Calibrated equipment accepts dimensions; AI assists reporting and anomaly review.
6. **AB-HPU:** integrate purchased qualified hydraulics after a schematic and safety-state review. Reservoir/deck are packaging concepts.
7. **AB-ACT:** integrate a bought electrohydraulic thruster; custom internals deferred.
8. **AB-AIST:** separate mill/export interface review. The 304.8 mm layout is not verified against an AISE/AIST interface standard.
9. **AB-COUP:** buy complete coupling or flexible element first; no gear tooth or elastomer torque-transmission design in C0.
10. **AB-POS:** positive actuation for an application that accepts loss of force on loss of supply. Not a spring-applied holding brake.
11. **AB-BUF:** specialist absorber programme. Energy divided by stroke gives average force, never peak force.
12. **AB-SPEC:** rail-clamp packaging only. Wind load, actual rail profile, normal-force mechanism and wet/contaminated holding tests are separate engineering work.

These twelve families do not represent every size, option or variant we might eventually sell. This release offers one representative review concept per family. It makes no 80% market-coverage assertion.

## Phase 1 — review C0 and lock one customer duty (2–4 weeks)

Owner: lead mechanical engineer with founder and customer application engineer.

- Collect torque versus time, inertia, speed, stopping distance/time, gravitational loads, external drive torque, duty cycle, thermal surroundings, contamination, machine interfaces, available energy supplies and failure-state requirements.
- Select one first product and one actual duty. A 500 N·m or 1,000 N·m study value in this release is a discussion input, not a customer requirement.
- Replace bought envelopes with vendor STEP and dimensioned interface drawings. Ask for force/stroke/time/temperature curves, rated operating conditions, material/certification records and installation constraints.
- Solve mechanism motion and load paths; establish release clearance at cold/hot/worn extremes. Check actual bolt access and maintenance motion, not just assembled appearance.
- Create requirements, hazard and verification matrices. Engineer signs assumptions or replaces them; unresolved values stay explicitly open.

Exit: approved requirements and mechanism architecture, reviewed make/buy plan, selected CAD source of truth and analysis boundary conditions. No production purchase orders from C0.

## Phase 2 — detailed mechanical design and simulation (6–10 weeks for one platform)

Owner: mechanical lead, stress/thermal specialist and manufacturing engineer.

- Approve friction pair using supplier data; bound coefficient over speed, pressure, temperature and wear. Reconcile static holding and dynamic stopping requirements.
- Calculate spring force and transmission ratio, pins in shear/bearing/bending, lever and bracket strength, weld fatigue, rotor/hub stresses, bolted-joint preload/slip and shaft attachment.
- Perform mechanism motion sweeps and tolerance stacks. A static no-intersection result is not a motion/clearance result.
- Use mesh-converged structural and transient thermal analysis with recorded material properties, loads, contacts and boundary conditions. Correlate heat partition and contact assumptions with testing. Free candidates: FreeCAD for CAD inspection/editing; CalculiX/PrePoMax-compatible solver workflows for appropriate structural studies; Gmsh for meshes. Select versions/platform workflow with the analyst, rather than assume tool access creates trustworthy results.
- Issue C1 prototype drawings: datum scheme, GD&T, fits, surface finish, material condition, heat treatment, weld symbols, critical characteristics, revision, marking, deburring, coating masks, BOM and assembly torque/preload procedure.
- Complete the electrical/hydraulic requirements review; separate subsequent controls design from the mechanical release.

Exit: independent checker approval, closed calculation comments, complete prototype package and a written test plan. No self-certification from simulation plots.

## Phase 3 — supplier and prototype validation (8–16 weeks, lead-time dependent)

Owner: manufacturing/quality engineer, mechanical lead and test laboratory.

- Obtain at least two comparable quotes for major metalwork. Compare setup/tooling, material condition, inspection capability, heat treatment subcontractors, minimum quantity and delivery. No cost reduction is assumed without these quotes.
- Approve cast/forged/machined material certificates, traceable friction lots, weld procedures, calibrated measurement and first-article inspection reports.
- Build on a guarded test fixture with controlled stored-energy and rotating-part hazards. Define proof/limit loads with the responsible engineer, not from the website sliders.
- Measure static/dynamic torque, release/application response, thermal fade/recovery, wear, cycle endurance and the actual application’s fault conditions.
- Close the loop: test discrepancy -> revised assumptions -> revised model -> checked drawing -> repeat test.

Exit: test evidence meeting approved requirements and a signed deviation/closure record. Failed tests extend the schedule.

## Phase 4 — manufacturing release and variants

Owner: engineering authority and quality lead.

Release R1 only after all critical characteristics, supplier processes, inspection criteria, functional tests and applicable certification/compliance obligations are satisfied. Qualification is application and jurisdiction specific. Archive the signed design baseline and full evidence; do not silently overwrite C0. Extend sizes by engineering calculations and tests, not uniform scaling of a mesh.

## Staffing, budget and efficient tools

For the first platform: one accountable mechanical lead; part-time experienced brake/stress/thermal reviewer; manufacturing/quality engineer; specialist friction, hydraulics and test support. Add a second design lead before treating disc and drum development as simultaneous full programmes.

Keep the existing programme budget scenarios as estimates; this CAD release does not establish vendor prices or a new validated budget. The planning envelope above ₹75 lakh is an assumption, not proof that it funds all 12 product qualifications. Gate expenditure after requirement approval and supplier/lab quotations. Do not buy custom actuator tooling before the bought component integration proves demand.

Installed free tooling for this release: CadQuery 2.6.1 and its OpenCascade kernel in an isolated `.cad-venv`; ReportLab for review PDFs; Three.js for browser inspection. Native editable source is Python, and neutral solid exchange is STEP. The web mesh is an inspection aid, never the manufacturing master.

## Required from the founder and reviewing engineer

Provide the first customer duty, first product/size choice, installation drawings, engineer’s preferred native CAD platform, candidate supplier interface drawings, friction/actuator contacts and laboratory access. These inputs are required for the next approval gate; the current first-pass models proceed using visibly labelled assumptions.

## Evidence and sources

- CadQuery official documentation: https://cadquery.readthedocs.io/en/stable/ — STEP/assembly interchange and modelling workflow.
- Twiflex industrial catalogue: https://www.twiflex.com/-/media/project/altramotion/shared/files/literature/brand/twiflex-limited/catalogs/p-1648-tf.pdf — brake selection context. Competitor friction values are not assigned to our lining.
- SSAB S355J2+N product data: https://www.ssab.com/en/brands-and-products/ssab-zero/s355j2-plus-n-zero — candidate structural material context; local material condition must be certified.
- Ovako 42CrMo4 data: https://steelnavigator.ovako.com/steel-grades/42crmo4/pdf?variantIDs=280 — candidate alloy steel context; use section/condition-specific properties.

Sources consulted 7 September 2026. The original competitor library retains document hashes and reviewed specification provenance. No numeric improvement over a competitor is substantiated by this C0 release.
