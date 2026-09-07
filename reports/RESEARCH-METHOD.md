# Research method and limitations

Collection date: 7 September 2026 (UTC). This is a first research release with explicit gaps, not a complete global product census.

## What the library contains

The original GALVI files remain unchanged. Imported archive members have CRC validation and SHA-256 identities. Their original retrieval timestamps and individual download URLs were not supplied; these are recorded as unknown rather than invented.

The collector visits official manufacturer product sites and publisher literature sites linked by those manufacturers. It uses bounded breadth-first traversal, respects robots exclusions, does not log in, does not submit forms and records HTTP failures. PDFs directly linked by an official page may reside on a CDN. Collection limits and unfetched URLs are retained in each manifest. Documents accessible by a public link are not treated as freely redistributable.

Content hashes deduplicate storage. Different URLs can legitimately refer to the same bytes, so reference counts exceed unique files. Product-page counts are not SKU counts. Category pages, translations and related links can appear in the discovery inventory. Some corporate or peripheral documents are retained as context, not counted as brake models.

## Evidence levels

1. **Archive / discovery:** a file or page was retrieved; no technical claim is approved.
2. **Unreviewed extraction:** numeric text was detected automatically. Tables, rotated text and merged layers can corrupt extraction. These rows must not enter calculations automatically.
3. **Source-checked:** a limited seed set was checked against the original PDF rendering or archived official page. These remain manufacturer specifications or claims, not independently tested results.
4. **Engineering-approved:** reserved for a named engineer's review against a defined application. No record currently has this status.
5. **Measured validation:** reserved for controlled physical test results. No AI Braking product currently has this status.

The 24 source-checked seed facts demonstrate the schema and comparison method; they do not mean all extracted values were checked. PDF page numbers are one-based file page indices, with printed page numbers recorded separately where known. Document revisions are null unless identified; automatic revision matches are only candidates.

## Known interpretation issues

- The Twiflex MU catalogue page (P-1648-TF, printed page 6 / PDF page 8) gives an 8 mm thickness with a parenthetical inch value that is inconsistent. That conversion is not promoted into the reviewed dataset. Confirm the requirement with the manufacturer.
- The SIBRE SHI 75 PDF includes overlapping text layers. The reviewed values were taken from the visible table, not assumed from extraction order.
- Torque, clamping force and tangential braking force are different quantities. Compare only after accounting for geometry, friction, units and conditions.
- Nominal friction coefficients are design assumptions for specified friction pairs. They are not universal material constants.
- Ambient operating temperature is not a disc/drum friction-surface temperature limit.
- Old catalogue dates are preserved. Public availability today does not establish that an old configuration remains orderable.
- Missing files and access restrictions are unresolved gaps, not evidence that a manufacturer lacks a capability.

## Using the archive with AI

Retrieve a relevant document/page, cite it, keep the raw unit and condition, and require review before turning it into a design input. Do not instruct a model to imitate a competitor's entire design. Published catalogue drawings rarely contain all tolerances, process controls or material evidence. The programme develops original designs from customer requirements and physical principles.

No fine-tuning dataset or model weights are created. The private archive is a searchable reference corpus. The public site contains original summaries and selected metadata, not raw third-party page text or PDF copies.
