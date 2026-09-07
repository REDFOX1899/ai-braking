'use client';
import { useState } from 'react';
import Link from 'next/link';
import {
  ArrowUpRight,
  ArrowLeft,
  ArrowRight,
  Download,
  Box,
  Layers3,
  FileText,
  Check,
  ChevronRight,
  ExternalLink,
  Activity,
  Target,
  AlertCircle,
  Cpu,
  Wrench,
} from 'lucide-react';
import all from '@/app/products-data.json';
import CadViewer from './CadViewer';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs';
import { Button } from '@/components/ui/button';
type Product = Omit<(typeof all)[number], 'intersections'> & {
  intersections: { a: string; b: string; volume_mm3: number; status: string }[];
};
const phases = [
  [
    '01',
    'Concept geometry',
    'NOW',
    'C0 solids, nominal reference drawings, make/buy decisions and review questions.',
  ],
  [
    '02',
    'Engineering definition',
    '2–4 weeks*',
    'Choose one real customer duty; approve interfaces, calculations, material condition, fits and full mechanisms.',
  ],
  [
    '03',
    'Detailed design',
    '6–10 weeks*',
    'Solve motion, joints, fatigue and thermal behaviour; run simulation; issue checked C1 drawings.',
  ],
  [
    '04',
    'Prototype & validation',
    '8–16 weeks*',
    'Obtain supplier quotes, manufacture approved parts and test on calibrated guarded equipment.',
  ],
  [
    '05',
    'Manufacturing release',
    'After evidence',
    'Close failures, qualify suppliers and process controls; sign drawings and inspection criteria.',
  ],
];
export function ProductIndex() {
  const [q, setQ] = useState('');
  const ps = all.filter((p) =>
    (p.short + ' ' + p.code + ' ' + p.level)
      .toLowerCase()
      .includes(q.toLowerCase()),
  );
  return (
    <div className="product-index">
      <div className="blue-section-title">
        <div>
          <p className="eyebrow">DESIGN LIBRARY / REVISION C0</p>
          <h2>From an idea to an assembly.</h2>
          <p>
            Explore the geometry, inspect each part and download the complete
            review package.
          </p>
        </div>
        <span className="engineering-badge">12 CONCEPT PACKAGES</span>
      </div>
      <div className="product-search">
        <input
          aria-label="Search product concepts"
          placeholder="Find a product, part family or maturity…"
          value={q}
          onChange={(e) => setQ(e.target.value)}
        />
        <span>{ps.length} families</span>
      </div>
      <div className="product-cards">
        {ps.map((p) => (
          <Link
            href={`/products/${p.slug}`}
            className="product-card"
            key={p.code}
          >
            <div className="product-card-top">
              <span>{p.code} / C0</span>
              <span>{String(p.priority).padStart(2, '0')}</span>
            </div>
            <div className="product-render">
              <img
                src={`/products/${p.slug}/preview.svg`}
                alt={`Original CAD concept of ${p.short}`}
                loading="lazy"
              />
              <span className="render-axis">Z ↑ / mm</span>
            </div>
            <div className="product-card-copy">
              <p className="eyebrow">{p.level}</p>
              <h3>
                {p.short}
                <ArrowUpRight size={21} />
              </h3>
              <p>{p.subtitle}</p>
              <div className="product-card-foot">
                <span>{p.part_count} model components</span>
                <span>
                  Open workspace <ArrowRight size={14} />
                </span>
              </div>
            </div>
          </Link>
        ))}
      </div>
      {!ps.length && (
        <p>No matching concepts. Try “disc”, “hub” or “envelope”.</p>
      )}
      <div className="blue-note">
        <AlertCircle size={20} />
        <p>
          <strong>
            A first engineering review, not a manufacturing release.
          </strong>{' '}
          The packages contain original nominal geometry. Purchased and
          unresolved mechanisms are marked as envelopes. Dimensions, material
          choices and target performance require engineering approval.
        </p>
      </div>
      <PhasePlan />
    </div>
  );
}
function PhasePlan() {
  return (
    <section className="phase-plan" id="phases">
      <p className="eyebrow">A CONTROLLED PATH TO PRODUCTION</p>
      <h2>Build one platform well. Then expand.</h2>
      <div className="phase-list">
        {phases.map(([n, title, time, body]) => (
          <article key={n}>
            <span className="phase-num">{n}</span>
            <div>
              <small>{time}</small>
              <h3>{title}</h3>
              <p>{body}</p>
            </div>
          </article>
        ))}
      </div>
      <p className="smallnote">
        *Planning estimates for one lead mechanical engineer with specialist
        support on one core platform, after requirements are available. Supplier
        lead times, test failures and certification can extend the programme.
        These are not delivery commitments for all 12 families.
      </p>
      <a
        href="/downloads/mechanical-development-plan.md"
        download
        className="text-link"
      >
        Download the detailed phase plan <Download size={15} />
      </a>
    </section>
  );
}
function TorqueStudy({ code }: { code: string }) {
  const [mu, setMu] = useState(0.3);
  const torque = code === 'AB-DC' ? 1000 : 500;
  const drum = code === 'AB-DR' || code === 'AB-AIST';
  const radius = code === 'AB-AIST' ? 0.1524 : drum ? 0.1575 : 0.155;
  const force = torque / (mu * radius * (drum ? 1 : 2)) / 1000;
  if (!['AB-DR', 'AB-AIST', 'AB-DC', 'AB-POS'].includes(code)) return null;
  return (
    <div className="torque-study">
      <div>
        <p className="eyebrow">FIRST-ORDER SENSITIVITY / NOT A RATING</p>
        <h3>What happens when friction falls?</h3>
        <p>
          At a study torque of {torque.toLocaleString()} N·m and effective
          radius {radius * 1000} mm, lower friction requires more normal force.
          This excludes thermal fade, dynamics, safety factors and{' '}
          {drum ? 'shoe self-energization' : 'pressure imbalance'}.
        </p>
      </div>
      <div>
        <label>
          Assumed coefficient μ <strong>{mu.toFixed(2)}</strong>
          <input
            type="range"
            min="0.15"
            max="0.45"
            step="0.01"
            value={mu}
            aria-label="Assumed friction coefficient"
            onChange={(e) => setMu(Number(e.target.value))}
          />
        </label>
        <strong className="force-result">
          {force.toFixed(2)} <small>kN</small>
        </strong>
        <p>{drum ? 'Total shoe normal force' : 'Normal force per disc face'}</p>
        <code>{drum ? 'Ntotal = T / (μ × r)' : 'Nface = T / (2 × μ × r)'}</code>
      </div>
    </div>
  );
}
export default function ProductWorkspace({ product: p }: { product: Product }) {
  const [selected, setSelected] = useState<string | null>(null);
  const [tab, setTab] = useState('design');
  const part = p.parts.find((x) => x.id === selected);
  const base = `/products/${p.slug}`;
  const index = all.findIndex((x) => x.code === p.code);
  const next = all[(index + 1) % all.length];
  return (
    <main className="product-workspace">
      <header className="product-header">
        <Link href="/" className="brand">
          AI<span> / </span>BRAKING
        </Link>
        <nav>
          <Link href="/?tab=portfolio">
            <ArrowLeft size={14} /> All products
          </Link>
          <Link href="/?tab=library">Reference library</Link>
        </nav>
        <span className="engineering-badge">C0 · CONCEPT</span>
      </header>
      <div className="product-breadcrumb">
        <Link href="/?tab=portfolio">Products</Link>
        <ChevronRight size={12} />
        <span>{p.code}</span>
        <span className="breadcrumb-end">ORIGINAL CAD / {p.date}</span>
      </div>
      <section className="product-heading">
        <div>
          <p className="eyebrow">
            {p.code} / {p.subtitle}
          </p>
          <h1>
            {p.short}
            <span>.</span>
          </h1>
          <p>{p.description}</p>
        </div>
        <div className="package-action">
          <a
            className="download-primary"
            href={`${base}/${p.downloads.zip}`}
            download
          >
            <Download size={17} /> Download review package
          </a>
          <small>
            STEP · part drawings · PDF · BOM · source
            <br />
            {p.level} / not for manufacture
          </small>
        </div>
      </section>
      <section className="product-cad-layout">
        <div>
          <CadViewer
            slug={p.slug}
            parts={p.parts}
            selected={selected}
            onSelect={setSelected}
          />
          <div className="model-readout">
            <span>
              <Box size={14} />
              {p.part_count} components
            </span>
            <span>
              <Layers3 size={14} />
              {p.parts.filter((x) => x.role.includes('envelope')).length}{' '}
              envelopes
            </span>
            <span>
              <Activity size={14} />
              {p.intersections.length} overlaps to review
            </span>
            <span>Units: mm</span>
          </div>
        </div>
        <aside className="assembly-tree">
          <div className="assembly-tree-head">
            <h2>Assembly navigator</h2>
            <button onClick={() => setSelected(null)}>Show all</button>
          </div>
          <p>Select a part to highlight its geometry.</p>
          <div className="part-scroll">
            {p.parts.map((x) => (
              <button
                key={x.id}
                className={selected === x.id ? 'selected' : ''}
                aria-pressed={selected === x.id}
                onClick={() => setSelected(selected === x.id ? null : x.id)}
              >
                <span className="part-index">
                  {String(x.item).padStart(2, '0')}
                </span>
                <span>
                  <strong>{x.name}</strong>
                  <small>
                    {x.id} ·{' '}
                    {x.role.includes('envelope') ? 'envelope' : 'concept part'}
                  </small>
                </span>
                <ChevronRight size={14} />
              </button>
            ))}
          </div>
          <div className="part-inspector">
            {part ? (
              <>
                <p className="eyebrow">{part.id}</p>
                <h3>{part.name}</h3>
                <p>{part.material}</p>
                <dl>
                  <dt>Bounding size</dt>
                  <dd>
                    {part.dimensions.map((x) => x.toFixed(1)).join(' × ')} mm
                  </dd>
                  <dt>Manufacturing intent</dt>
                  <dd>{part.process}</dd>
                </dl>
                <a href={`${base}/parts/${part.id}/${part.id}.step`} download>
                  Part STEP <Download size={13} />
                </a>
                <a
                  href={`${base}/parts/${part.id}/${part.id}.svg`}
                  target="_blank"
                  rel="noreferrer"
                >
                  Drawing <ArrowUpRight size={13} />
                </a>
              </>
            ) : (
              <>
                <p className="eyebrow">PART-LEVEL TRACEABILITY</p>
                <p>
                  Every model component has a matching part number, STEP file
                  and nominal reference drawing.
                </p>
              </>
            )}
          </div>
        </aside>
      </section>
      <Tabs value={tab} onValueChange={(v) => setTab(String(v))}>
        <TabsList variant="line" className="section-tabs product-section-tabs">
          <TabsTrigger value="design">
            <Box />
            Design intent
          </TabsTrigger>
          <TabsTrigger value="manufacture">
            <Wrench />
            Parts & assembly
          </TabsTrigger>
          <TabsTrigger value="targets">
            <Target />
            Targets & evidence
          </TabsTrigger>
          <TabsTrigger value="release">
            <FileText />
            Review & downloads
          </TabsTrigger>
        </TabsList>
        <TabsContent value="design">
          <div className="design-columns">
            <section>
              <p className="eyebrow">WHY THIS ARCHITECTURE</p>
              <h2>Decisions you can inspect.</h2>
              {p.decisions.map((d, i) => (
                <article className="decision-row" key={d}>
                  <span>0{i + 1}</span>
                  <p>{d}</p>
                </article>
              ))}
            </section>
            <section className="technical-panel">
              <p className="eyebrow">GEOMETRY + STUDY INPUTS</p>
              <h3>Proposed specification</h3>
              {p.targets.map(([a, b, c]) => (
                <div className="spec-line" key={a}>
                  <span>{a}</span>
                  <strong>{b}</strong>
                  <small>{c}</small>
                </div>
              ))}
            </section>
          </div>
          <TorqueStudy code={p.code} />
          <div className="design-columns">
            <section>
              <p className="eyebrow">MATERIALS / CANDIDATES ONLY</p>
              <h2>Choose for the load and the process.</h2>
              {p.materials.map((x) => (
                <p className="body-row" key={x}>
                  {x}
                </p>
              ))}
              <p className="smallnote">
                No cost or strength advantage is assumed from a grade name.
                Obtain section-specific properties, material certificates, local
                quotes and process capability evidence.
              </p>
            </section>
            <section className="technical-panel">
              <p className="eyebrow">CONTROL SYSTEMS / REQUIREMENTS ONLY</p>
              <h3>Electrical & sensing boundary</h3>
              {p.sensors.map((x) => (
                <p className="body-row" key={x}>
                  {x}
                </p>
              ))}
              <span className="subtle-tag">
                <Cpu size={13} /> Electronics design deferred
              </span>
            </section>
          </div>
        </TabsContent>
        <TabsContent value="manufacture">
          <div className="blue-section-title">
            <div>
              <p className="eyebrow">MAKE / BUY / VERIFY</p>
              <h2>Every part has a place.</h2>
            </div>
            <a href={`${base}/bom.csv`} download className="text-link">
              Download BOM <Download size={15} />
            </a>
          </div>
          <div className="parts-table-wrap">
            <table className="parts-table">
              <thead>
                <tr>
                  <th>Mark / component</th>
                  <th>Status</th>
                  <th>Material & process</th>
                  <th>Files</th>
                </tr>
              </thead>
              <tbody>
                {p.parts.map((x) => (
                  <tr key={x.id}>
                    <td>
                      <button
                        onClick={() => {
                          setSelected(x.id);
                          window.scrollTo({ top: 200, behavior: 'smooth' });
                        }}
                      >
                        <small>{x.id}</small>
                        <strong>{x.name}</strong>
                      </button>
                      <span>Qty {x.quantity} · nominal mm</span>
                    </td>
                    <td>
                      <span className="subtle-tag">{x.role}</span>
                    </td>
                    <td>
                      {x.material}
                      <small>{x.process}</small>
                    </td>
                    <td>
                      <a href={`${base}/parts/${x.id}/${x.id}.step`} download>
                        STEP ↓
                      </a>
                      <a
                        href={`${base}/parts/${x.id}/${x.id}.svg`}
                        target="_blank"
                        rel="noreferrer"
                      >
                        Drawing ↗
                      </a>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="design-columns">
            <section>
              <p className="eyebrow">ASSEMBLY INTENT</p>
              <h2>How the concept comes together.</h2>
              {p.steps.map((s, i) => (
                <article className="decision-row" key={s}>
                  <span>{String(i + 1).padStart(2, '0')}</span>
                  <p>{s}</p>
                </article>
              ))}
            </section>
            <section className="technical-panel">
              <p className="eyebrow">BEFORE A MANUFACTURER CUTS METAL</p>
              <h3>Release details still required</h3>
              <p className="body-row">
                Signed duty requirements; complete force paths and motion;
                fastening and retention; approved material condition; datums and
                GD&T; fit and tolerance stacks; welds, heat treatment and
                finish; inspection and test criteria.
              </p>
              <p className="body-row">
                The C0 drawings show nominal shape and selected features. They
                are not complete production drawings. No manufacturing quotation
                should interpret missing tolerances as permission to choose
                them.
              </p>
              <p className="body-row">
                Suggested marking: part ID, revision and lot on a non-friction,
                non-fit surface. Exact marking location and method remain to be
                released.
              </p>
            </section>
          </div>
        </TabsContent>
        <TabsContent value="targets">
          <div className="blue-section-title">
            <div>
              <p className="eyebrow">IMPROVEMENT NEEDS A BASELINE</p>
              <h2>Ambitious targets. Explicit evidence.</h2>
              <p>No competitor performance multiple has been established.</p>
            </div>
          </div>
          <div className="hypothesis-grid">
            {p.hypotheses.map(([a, b, c]) => (
              <article className="technical-panel" key={a}>
                <p className="eyebrow">{a}</p>
                <h3>{b}</h3>
                <span className="subtle-tag">Untested hypothesis</span>
                <p className="body-row">{c}</p>
              </article>
            ))}
          </div>
          <div className="design-columns">
            <section>
              <p className="eyebrow">SIMULATION + PHYSICAL TESTS</p>
              <h2>The evidence to earn a rating.</h2>
              {p.validation.map((x, i) => (
                <article className="decision-row" key={x}>
                  <span>0{i + 1}</span>
                  <p>{x}</p>
                </article>
              ))}
            </section>
            <section className="technical-panel">
              <p className="eyebrow">OPEN ENGINEERING RISKS</p>
              <h3>What this model does not prove</h3>
              {p.risks.map((x) => (
                <p className="body-row" key={x}>
                  {x}
                </p>
              ))}
            </section>
          </div>
          <div className="blue-note">
            <AlertCircle size={21} />
            <p>
              <strong>Compare like for like.</strong> Fix duty, torque, speed,
              temperature, environment, access and service procedure before
              testing a competitor benchmark. Percentage targets here are
              proposed experiments, not predicted or measured superiority.
            </p>
          </div>
        </TabsContent>
        <TabsContent value="release">
          <div className="blue-section-title">
            <div>
              <p className="eyebrow">C0 / ENGINEER HANDOFF</p>
              <h2>Open, inspect, annotate.</h2>
            </div>
            <span className="engineering-badge">NOT FOR MANUFACTURE</span>
          </div>
          <div className="release-downloads">
            {[
              [
                p.downloads.zip,
                'Complete review package',
                'All part STEP/SVG files, PDF, BOM, source references and checksums',
              ],
              [
                p.downloads.step,
                'Assembly STEP',
                'Named solid components · open in FreeCAD or another STEP CAD tool',
              ],
              [
                p.downloads.pdf,
                'Engineering review PDF',
                'Design brief, assembly intent and nominal part drawing sheets',
              ],
              [
                'bom.csv',
                'Bill of materials',
                'Part marks, make/buy classification and candidate processes',
              ],
              [
                'geometry-checks.json',
                'Geometry check report',
                'Solid validity, STEP volume round-trip and detected intersections',
              ],
            ].map(([file, title, desc]) => (
              <a href={`${base}/${file}`} download key={file}>
                <FileText size={25} />
                <div>
                  <h3>{title}</h3>
                  <p>{desc}</p>
                </div>
                <Download size={18} />
              </a>
            ))}
          </div>
          <section className="technical-panel">
            <p className="eyebrow">
              GEOMETRY CHECKS / NOT ENGINEERING APPROVAL
            </p>
            <h3>
              {p.intersections.length
                ? `${p.intersections.length} geometric overlaps need review`
                : 'No positive-volume intersections detected'}
            </h3>
            <p className="body-row">
              Every exported part passed CAD solid validity and STEP volume
              round-trip checks. This does not establish strength, clearance
              through motion, contact behaviour or manufacturability. Contacting
              faces can exist without positive overlap.
            </p>
            {p.intersections.length > 0 && (
              <details>
                <summary>Inspect detected overlaps</summary>
                {p.intersections.map((x) => (
                  <p className="body-row" key={x.a + x.b}>
                    {x.a} ↔ {x.b}: {x.volume_mm3.toLocaleString()} mm³. Review
                    whether this is an envelope overlap or a geometric defect
                    before progressing.
                  </p>
                ))}
              </details>
            )}
          </section>
          <PhasePlan />
        </TabsContent>
      </Tabs>
      <footer>
        <div>
          <strong>AI BRAKING / ENGINEERING IN THE OPEN</strong>
          <p>
            Original concept models · manufactured-in-India ambition ·
            performance pending validation
          </p>
        </div>
        <Link href={`/products/${next.slug}`}>
          Next: {next.short} <ArrowRight size={16} />
        </Link>
      </footer>
    </main>
  );
}
