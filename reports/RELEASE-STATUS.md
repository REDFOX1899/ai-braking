# Release 01 status

Date: 7 September 2026 UTC

## Delivered

- Private repository: https://github.com/REDFOX1899/ai-braking
- Hosted owner-only preview: https://ai-braking-research.shantanupatil1899.chatgpt.site
- Intended later domain: braking.fde.guru; founder-managed Cloudflare connection not performed.
- Eight manufacturer collections; 291 distinct valid PDF files in the combined corpus, including historical and corporate context.
- 24 source-checked seed facts and 985 separately marked unreviewed numeric leads.
- 12 proposed product workstreams, engineering handbook (Markdown and PDF), supplier requirements, customer requirements template and funding scenarios.

## Verification

Archive SHA-256 checks, original per-product ZIP CRC checks, PDF signature checks, reviewed-fact page/provenance checks and publication allowlist checks passed. The production build and TypeScript check passed. Search checks cover case/whitespace, combined manufacturer filtering, empty query and no-match results. npm audit reported zero vulnerabilities after compatible dependency updates.

The deployment archive was inspected: only the original engineering handbook PDF is packaged; raw competitor archives and the session transcript are absent. Published file hashes match the selected export manifest. Sites reported deployment success for version 1 on 7 September 2026.

The handbook was rendered and visually checked. Browser visual/interaction testing was not requested and was not performed. The optional WebMCP search integration is feature-detected; no supported WebMCP runtime validation context was available, so it is not claimed verified.

## Collection limits

698 URLs were failed or deferred by the scoped collector. Most are deferred traversal links, not HTTP failures; the detailed register distinguishes them. The corpus is a useful first collection rather than a claim of exhaustive current SKU coverage. Stromag and Twiflex are represented primarily by their large official catalogues; some direct pages restrict collection. Some EMG brochure URLs are unavailable.

One supplied GALVI PDF is empty. It is retained as invalid provenance and excluded from valid PDF counts. Source documents contain historical revisions, overlapping text layers and at least one inconsistent unit conversion; automated extraction is not engineering approval.

## Not performed

No original manufacturing CAD, brake simulation, prototype construction, physical test, certification or customer qualification. The next technical step is the existing engineer's requirements review, including customer duty data, tool formats and test scope.
