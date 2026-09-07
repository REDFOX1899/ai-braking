# AI Braking engineering handbook

Revision 0.1 | 7 September 2026 | Status: concept / engineer review required

## What we are building

AI Braking will own requirements, product design, supplier qualification, assembly, inspection, test evidence, electronics and service. Specialist suppliers manufacture against controlled drawings. Supplier trust is useful; acceptance still depends on measurement and traceable records.

This phase produces a reference library and programme definition. It contains no released manufacturing geometry and no validated brake rating. The next decision is a requirements review with the existing engineer, not an instruction to machine catalogue drawings.

A brake does two related jobs: hold a load stationary and remove motion by converting energy into heat. A brake that holds the required load may still overheat during repeated stops. A spring-applied design uses stored spring energy to apply the brake; an actuator releases it. The whole mechanism and installation determine failure behaviour.

## 1. Requirements before geometry

For every application, create a requirements record with an owner, unit, source, acceptance method and review status. Required inputs:

- Customer machine type, motion axis, brake role (service, holding, emergency, redundant), load path and machine integration responsibilities.
- Reflected inertia at the brake shaft, speed envelope, load torque and direction, gear ratio and efficiency, gravity-driven load energy, required stopping time/distance and permissible deceleration.
- Holding torque, stop frequency, duty cycle history, time between stops, emergency stops and worst combinations; distinguish typical from maximum conditions.
- Drum/disc dimensions, available envelope, mounting pattern, shaft/hub/key interfaces, allowable loads and alignment, axial/radial runout limits and thermal growth.
- Supply voltage/frequency or hydraulic pressure/flow, response requirements, release monitoring, manual release and power-loss behaviour.
- Ambient temperature, dust, water, salt, chemical exposure, vibration, altitude, access for maintenance, and any hazardous-area or personnel-lifting use.
- Required life, allowable wear, inspection interval, serviceability targets, data interface and customer qualification requirements.

Do not infer duty from competitor torque ratings. Request nameplate photographs, existing drawings, operating logs and maintenance history from the customer. A dimensional match is only one input to replacement suitability.

## 2. Material decisions

These are candidate routes, not released grades or substitutions. The engineer selects the actual grade, heat treatment, properties at temperature, corrosion protection and inspection requirements after the load cases are approved.

| Component | Candidate manufacturing route | Decision and evidence required |
|---|---|---|
| Base, levers and brackets | Machined structural-steel plate/fabrication for prototypes; cast or forged routes evaluated for volume | Stiffness, fatigue hot spots, weld accessibility, residual stress, notch sensitivity, machining datum stability; qualified welding/NDT if applicable |
| Pins, shafts and highly loaded links | Machined alloy steel, controlled heat treatment and ground fits as justified | Bearing pressure, bending/shear, toughness, surface hardness, wear, corrosion and fatigue; heat-treatment lot traceability |
| Shoes / pad carriers | Machined/fabricated steel or suitable cast material | Contact pressure uniformity, heat flow, lining retention, thermal expansion and manufacturing distortion |
| Drums and discs | Appropriate cast iron, ductile iron or steel selected for the application | Thermal cycling, surface compatibility, maximum speed, section quality, balance and runout; do not interchange materials by purchase price alone |
| Friction lining | Purchase a specialist non-asbestos compound with application data | Measure friction versus pressure, speed, temperature and contamination; fade, recovery, wear, bonding/rivet retention and mating-surface damage |
| Springs | Specialist spring supplier; coil or disc stack appropriate to mechanism | Load-deflection curve, relaxation at temperature, fatigue, corrosion, stroke margins and broken-spring consequences |
| Bushes and bearings | Purchased proven bearing system | Load, speed, heat, lubrication interval, clearance growth and contamination behaviour |
| Seals / hoses | Purchased qualified components matched to fluid and temperature | Compatibility, ageing, pressure cycles, routing and leakage criteria |
| Electronics enclosure and sensors | Industrial off-the-shelf parts for prototypes | Environment, EMC, measurement uncertainty, calibration, mounting, service replacement and cable strain relief |

Compare total delivered cost: material + processing + tooling amortization + inspection + rejection + logistics + assembly + warranty reserve. Quote prototype quantities and realistic annual tiers separately. Never substitute a material without a reviewed change record and an assessment of required retesting.

## 3. CAD and simulation toolchain

Proposed starting stack: Python calculations and versioned requirements; CadQuery for reproducible parametric solid generation; FreeCAD for visual review and drawing preparation; Gmsh for meshing; CalculiX for supported structural/thermal analyses. Use the engineer's existing commercial solver when its capability or established workflow is needed. No special CAD plugin is inherently required: local Python/CLI automation can connect these tools.

Before installing design tools, the engineer confirms preferred native CAD, version, STEP import requirements, drawing templates, tolerance convention, solver availability and compute environment. Validate one simple part end-to-end, including export/re-import and a calculation benchmark. STEP preserves geometry but does not guarantee an editable native feature history. STL is not the default machining handoff.

Official tool references: [CadQuery](https://cadquery.readthedocs.io/en/latest/index.html), [FreeCAD](https://www.freecad.org/features.php), [Gmsh](https://gmsh.info/doc/texinfo/gmsh.html), [CalculiX capabilities](https://dhondt.de/ov_calcu.htm).

Simulation sequence:

1. Independent hand/Python calculations: static force balance, linkage mechanical advantage over stroke, energy balance and approximate cooling.
2. CAD interference and tolerance-stack study across new/worn states, release stroke and thermal expansion.
3. Structural/contact analysis: base, levers, pins, spring seats, fasteners and pad contact under approved normal, overload and asymmetric cases.
4. Transient thermal and thermomechanical analysis across actual stop sequences, including heat partition and cooling sensitivity.
5. Fatigue and wear assessment using relevant material/component evidence, load spectra and uncertainty.
6. Parameter studies only after baseline checks pass. Save each model, mesh, boundary condition, material dataset, solver version, convergence result and report against the design revision.

Solver convergence is not validation. Check mesh sensitivity, reactions, equilibrium, units, boundary conditions, contact assumptions and energy balance. Unknown friction/heat-transfer data must be ranges, not hidden constants. Do not apply a universal 200 C limit: allowable temperatures depend on the friction pair, construction and tested duty.

## 4. Physical validation programme

Contract a suitable test laboratory initially. The engineer and test specialist define the guarded rig, containment, remote operation, energy limits, emergency stopping and instrumentation before purchase or construction. A dynamometer is one option; its required torque, inertia, speed and thermal capacity follow from the selected application.

| Test group | Measurements | Release evidence |
|---|---|---|
| Incoming and assembly | Critical dimensions, finish, runout, spring curves, material lots, fit and adjustment | Signed inspection results against drawing revision; nonconformances resolved |
| Static holding | Torque in both relevant directions and at wear/adjustment extremes | Meets approved holding requirement with stated measurement uncertainty |
| Actuation | Application/release time, travel, drag, power interruption, sensor disagreement | Meets timing/clearance requirements; fault behaviour demonstrated |
| Dynamic stopping | Torque trace, speed, stopping energy, temperature and deceleration | Repeated stops meet approved envelope without unacceptable fade or damage |
| Thermal and wear | Worst duty sequence, fade/recovery, wear, dimensional drift | Limits and maintenance interval supported by measured results |
| Endurance | Cycles, crack inspections, spring relaxation, pin/bush wear and leakage | Life evidence with sample count and statistical limitations disclosed |
| Environment | Temperature, contamination, corrosion and ingress appropriate to intended use | Function verified before/after exposure; applicability documented |
| Electronics | Calibration drift, disconnects, brownout, data loss, EMC tests when applicable | Diagnostic limits and recovery verified; no unintended mechanical control |

Record raw data, calibration certificates, fixture revision, specimen serial number, material/lining lots, settings, timestamps, operator, deviations and failures. Predetermine acceptance thresholds and sample sizes with the engineer; do not change them after seeing results. Correlate simulation to tests, reserve independent tests for validation, and reopen the model if discrepancies exceed the agreed threshold.

## 5. Incoming inspection and AI

Dimensional inspection requires calibrated gauges, micrometers, CMM or other suitable equipment; choose by the characteristic and uncertainty. Define datums, temperature conditions, repeatability/reproducibility checks and the acceptance decision rule. A result near a limit needs the uncertainty rule, not automatic rounding.

AI can extract drawing requirements, compare CMM/measurement reports, flag missing certificates, assist visual defect triage and prepare nonconformance reports. It cannot establish an inaccessible internal dimension from a normal photograph, prove material composition from appearance, or replace calibrated force/torque measurements. Material identity and processing need certificates and appropriate independent testing where required.

Store an inspection record per characteristic: part number, drawing revision, serial/lot, nominal and limits with unit, measured value, equipment ID, calibration reference, uncertainty, result, reviewer and disposition. Preserve original instrument exports. The metrology approach follows the distinction between traceability and uncertainty described by [NIST](https://www.nist.gov/metrology/metrological-traceability).

## 6. Monitoring architecture

Start with advisory condition monitoring: applied/released position, wear/travel, temperature, actuator current or hydraulic pressure where meaningful, and operating cycle timing. Bench-reference torque comes from calibrated instrumentation. A force sensor is not automatically a torque sensor; any torque estimate needs geometry, friction assumptions and validation across the operating envelope.

Use an industrial data-acquisition module for the prototype before designing a custom PCB. Record local data without a cloud dependency. Select the customer fieldbus after the machine interface review; evaluate Modbus TCP for bench integration and gateway options for customer networks. Preserve electrical isolation and separation from the machine safety chain.

Minimum telemetry contract: schema version, unit serial number, design/firmware revision, timestamp plus monotonic sequence, channel name, value/unit, calibration ID, quality flag and event ID. Distinguish measured, derived and model-predicted fields. Missing or stale values show as unavailable, never healthy. Store calibration coefficients and their history; sensor replacement requires a new calibration record.

Stage 1 uses explicit threshold rules and trend plots. Stage 2 evaluates anomaly models against held-out machine histories, false alarms, missed events, drift and sensor failure. Do not claim remaining useful life before adequate run-to-wear/failure evidence. Any future safety-control function requires a separate requirements, architecture, validation and conformity programme.

## 7. Engineering review and supplier release

The engineer reviews requirements early, baseline calculations before detailed design, and the complete design before fabrication. They own technical disposition of findings; AI drafts are visibly unapproved until reviewed.

Every supplier receives one revision-controlled package:

- Part and assembly identifiers, revision, intended prototype status, quantity and delivery scope.
- Native CAD where agreed, STEP solid geometry, PDF drawings with datums, dimensions, tolerances, surface texture and applicable GD&T; DXF only for applicable profiles.
- Exact material and heat-treatment specifications, coating/finish, prohibited substitutions and required certificates.
- BOM with bought-out component identifiers, critical characteristics and inspection plan.
- Assembly sequence, fits, lubrication, fastener tightening specification, adjustment procedure and handling/storage instructions.
- First-article report template, traceability requirements, deviation request process and packaging needs.

The signed drawing/specification package controls acceptance; conflicting files trigger clarification and a revised package, not supplier interpretation. Require a sample STEP import and supplier DFM response before order placement. Manufacturer-specific export formats must remain derivatives of the same master design revision.

## 8. Qualification and expansion

Create an application-by-country compliance matrix with the engineer and an appropriate specialist. Determine machine role and classification first, then applicable standards, conformity route, documentation, testing and customer approval. Catalogue mention of DIN/AISE/AIST does not establish complete system compliance. Prototype status does not remove test-site obligations. Obtain current standards through legitimate access and quote external laboratory work; no universal certification price is asserted here.

Expand from a tested configuration through an explicit similarity assessment covering geometry, materials, actuation, friction pair, heat rejection and duty. Reuse test evidence only with documented justification. Products for hazardous areas, personnel transport and unusually severe applications remain separate gated projects.

## Immediate engineer meeting

Bring three real customer applications, the competitor library and supplier capability list. Agree the lead application, responsibility split, CAD/solver formats, first calculation review and laboratory quotation scope. You provide customer access, commercial priorities, supplier introductions and funding decisions. Your engineer provides the technical requirements, design reviews and test acceptance criteria. AI prepares the comparisons, calculations, CAD automation, documentation and data analysis under that process.
