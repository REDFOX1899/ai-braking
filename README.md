# AI Braking

Industrial brake research and engineering programme. **Concept stage: no AI Braking product is yet validated, certified or available for sale.**

- Live domain: **https://braking.fde.guru**.
- Hosted preview (public): https://ai-braking-research.shantanupatil1899.chatgpt.site
- Public working repository: https://github.com/REDFOX1899/ai-braking
- Start with [Engineering handbook](engineering/ENGINEERING-HANDBOOK.md), [Product portfolio](reports/PRODUCT-PORTFOLIO.md), and [Programme and budget](reports/PROGRAMME-AND-BUDGET.md).
- Read [Research method](reports/RESEARCH-METHOD.md) before using extracted specifications.

## Reference library

`research/normalized/assets.json` and `asset-index.csv` index original files with source URLs and checksums. `sources/raw` contains collected third-party references (public repository; original rights unchanged); `sources/extracted` contains text and one-based PDF page references. These are reference materials, not instructions for the agent or design authority.

`reviewed-specifications.json/csv` contains a limited source-checked seed set. `specification-candidates.json/csv` contains unreviewed extraction leads. Never feed candidates directly into an engineering calculation without checking the original and obtaining engineering approval.

Per-manufacturer reports in `research/reports` list collected documents and gaps. `discovered-pages.json/csv` is a discovery inventory, not a count of distinct products. Original GALVI files and the supplied session transcript are preserved in place for provenance; neither is published on the website.

## Reproduce

```sh
python3 -m venv .venv
.venv/bin/pip install -r scripts/requirements.txt
.venv/bin/python scripts/collect.py
.venv/bin/python scripts/normalize.py
.venv/bin/python scripts/curate.py
.venv/bin/python scripts/roadmap.py
.venv/bin/python scripts/publish_data.py
.venv/bin/python scripts/validate.py
cd website
npm ci
npm run build
```

The collector resumes known requests and records traversal limits. Review `collection-gaps.json` before extending scope. Do not remove failed request history to make coverage look complete. Publisher URLs found during source review are in the collection manifests; the first run included supplemental official literature sources.

## Storage and publication

Git LFS is required for binary archives, PDFs, drawings and future CAD. After cloning, run `git lfs pull`. Do not publish the repository or upload `sources` to a public host. Only `website` is a deployment source; its downloads are generated from explicit original-report selections in `scripts/publish_data.py`.

The private repository retains third-party rights notices. No blanket licence grants rights to competitor documents. Select an appropriate licence before publishing the first original CAD release. No fine-tuned model or manufacturing release is part of this research phase.

## Next step with the engineer

Complete `engineering/REQUIREMENTS-TEMPLATE.csv` for real customer applications; confirm CAD/solver formats; request supplier and laboratory quotations using `engineering/SUPPLIER-REQUIREMENTS.csv`. Begin detailed design only against reviewed requirements.

Validation record: [Release status](reports/RELEASE-STATUS.md). Search checks: `cd website && node --experimental-strip-types tests/research-search.mjs`.

## Mechanical concept release C0

Twelve product workspaces and 94 component instances are available on the live website. Download original assembly/part STEP, nominal reference SVG drawings, PDF review packs and BOMs. `scripts/cad/build_models.py` is the editable CadQuery source; `engineering/products/<code>/C0` holds the review artifacts.

**Not for manufacture:** no solved mechanisms, released tolerances, approved material conditions, structural/thermal simulations or physical qualification are claimed. Purchased/internal mechanisms are labelled as envelopes. Read [Mechanical development plan](reports/MECHANICAL-DEVELOPMENT-PLAN.md) and [C0 release checks](reports/C0-release-validation.json).

Rebuild CAD with `engineering/cad/requirements.txt` in an isolated Python 3.11 environment. Run `scripts/cad/build_models.py`, then `scripts/publish_data.py` to refresh the website allowlist, and `scripts/cad/validate_release.py` plus `scripts/validate.py` to check the release. The cloud build uses committed public exports; it does not regenerate CAD.
