'use client';
import { useState } from 'react';
import Link from 'next/link';
import {
  ArrowLeft,
  ArrowRight,
  Download,
  ExternalLink,
  CheckCircle2,
  Clock3,
  Layers3,
  FileCheck2,
} from 'lucide-react';
import data from '@/app/galvi-study.json';
import CadViewer from './CadViewer';
const stages = [
  'Opportunity',
  'Interface model',
  'Source evidence',
  'Manufacturing gates',
  'Partnership ask',
];
const gates = [
  [
    'Reference selection',
    'Prepared',
    'N.315.HYD.030/05 + PD.315; archived catalogue identified.',
  ],
  [
    'Interface geometry',
    'Prepared for review',
    'Published dimensions transcribed; original nominal adapter and drum model.',
  ],
  [
    'Current supplier data',
    'Awaiting supplier',
    'Current controlled drawing, options, STEP and tolerances.',
  ],
  [
    'Duty & load case',
    'Not approved',
    'Machine torque, speed, inertia, stop duty, environment and failure states.',
  ],
  [
    'Detailed mechanical design',
    'Not complete',
    'Shaft connection, joints, material condition, tolerances, retention and full brake mechanism.',
  ],
  [
    'Simulation & prototype tests',
    'Not performed',
    'Structural/thermal calculations and correlated physical results.',
  ],
  [
    'Manufacturing release',
    'Not released',
    'Signed drawings, inspection criteria and qualification evidence.',
  ],
];
export default function DirectorReview() {
  const [stage, setStage] = useState(0);
  const [selected, setSelected] = useState<string | null>(null);
  const [step, setStep] = useState(0);
  const p = data;
  const base = '/products/galvi-315-reference';
  return (
    <main className="director-review">
      <header className="product-header">
        <Link href="/" className="brand">
          AI<span> / </span>BRAKING
        </Link>
        <nav>
          <Link href="/">Product library</Link>
          <Link href="/products/drum-brake">Original drum concept</Link>
        </nav>
        <span className="engineering-badge">TECHNICAL PARTNERSHIP REVIEW</span>
      </header>
      <div className="review-heading">
        <p className="eyebrow">
          DIRECTOR BRIEFING / GALVI-REFERENCED DEVELOPMENT
        </p>
        <h1>
          A precise starting point.
          <br />
          <em>A credible path to production.</em>
        </h1>
        <p>
          Build the first platform around an established supplier interface.
          Bring original integration work, measurable acceptance criteria and a
          focused engineering request to the table.
        </p>
        <div className="review-facts">
          <span>
            <strong>315 mm</strong> reference drum diameter
          </span>
          <span>
            <strong>440 × 80 mm</strong> derived mounting pitch
          </span>
          <span>
            <strong>20</strong> published dimensional entries
          </span>
          <span>
            <strong>Concept</strong> current release status
          </span>
        </div>
      </div>
      <nav className="review-nav" aria-label="Presentation sections">
        {stages.map((s, i) => (
          <button
            key={s}
            aria-current={i === stage ? 'step' : undefined}
            onClick={() => setStage(i)}
          >
            <span>0{i + 1}</span>
            {s}
          </button>
        ))}
      </nav>
      {stage === 0 && (
        <section className="review-content">
          <div className="design-columns">
            <div>
              <p className="eyebrow">THE PROPOSAL</p>
              <h2>
                Integrate first.
                <br />
                Qualify together.
              </h2>
              <p className="body-row">
                Use the GALVI N.315.HYD.030/05 brake and PD.315 drum as the
                initial reference. Explore a supply or technical partnership for
                proven brake mechanisms while AI Braking develops traceable
                integration, inspection and service documentation.
              </p>
              <p className="body-row">
                GALVI is a reference and potential partner. No partnership,
                licensing, compatibility or supplier endorsement is currently
                established.
              </p>
              <button className="download-primary" onClick={() => setStage(1)}>
                Explore the interface model <ArrowRight size={17} />
              </button>
            </div>
            <div className="technical-panel">
              <p className="eyebrow">WHAT WE BRING TO THIS MEETING</p>
              <h3>Work you can inspect.</h3>
              {[
                'Twelve original concept families with downloadable CAD.',
                'A selected supplier interface with source-linked dimensions.',
                'A part-level adapter and drum integration study.',
                'An explicit engineering gate and supplier information list.',
              ].map((x) => (
                <p className="body-row" key={x}>
                  <CheckCircle2 size={15} /> {x}
                </p>
              ))}
              <a
                href={`${base}/${p.downloads.pdf}`}
                download
                className="text-link"
              >
                Download this study’s review pack <Download size={15} />
              </a>
            </div>
          </div>
          <div className="blue-note">
            <FileCheck2 size={22} />
            <p>
              <strong>The honest meeting statement:</strong> “We have a
              traceable concept and integration package ready for your technical
              review. We want to agree the supplier interfaces, detailed
              engineering responsibilities and qualification route before
              manufacturing release.”
            </p>
          </div>
        </section>
      )}
      {stage === 1 && (
        <section className="review-content">
          <div className="blue-section-title">
            <div>
              <p className="eyebrow">
                NOMINAL INTEGRATION / NOT A GALVI MANUFACTURING MODEL
              </p>
              <h2>Inspect the reference assembly.</h2>
              <p>
                Turn on Dimensions, hide the reserved envelope or cut through
                the drum. Cyan dimensions reference the catalogue; selected-part
                bounds describe our CAD.
              </p>
            </div>
            <a
              href={`${base}/${p.downloads.zip}`}
              download
              className="download-primary"
            >
              Review package <Download size={16} />
            </a>
          </div>
          <div className="product-cad-layout">
            <CadViewer
              slug={p.slug}
              parts={p.parts}
              selected={selected}
              onSelect={setSelected}
              annotations={p.annotations}
            />
            <aside className="assembly-tree">
              <div className="assembly-tree-head">
                <h2>Component layers</h2>
                <button onClick={() => setSelected(null)}>All</button>
              </div>
              <div className="part-scroll">
                {p.parts.map((x) => (
                  <button
                    key={x.id}
                    aria-pressed={selected === x.id}
                    onClick={() => setSelected(x.id)}
                    className={selected === x.id ? 'selected' : ''}
                  >
                    <span className="part-index">{x.item}</span>
                    <span>
                      <strong>{x.name}</strong>
                      <small>{x.role}</small>
                    </span>
                  </button>
                ))}
              </div>
              <div className="part-inspector">
                <p className="eyebrow">{selected || 'GEOMETRY BOUNDARY'}</p>
                <p>
                  {p.parts.find((x) => x.id === selected)?.notes.join(' ') ||
                    'The transparent volume is reserved installation space, not a brake mechanism. Envelope overlaps are expected and do not establish fit.'}
                </p>
                {selected && (
                  <>
                    <a
                      href={`${base}/parts/${selected}/${selected}.step`}
                      download
                    >
                      Part STEP ↓
                    </a>
                    <a
                      href={`${base}/parts/${selected}/${selected}.svg`}
                      target="_blank"
                      rel="noreferrer"
                    >
                      Drawing ↗
                    </a>
                  </>
                )}
              </div>
            </aside>
          </div>
          <div className="assembly-walk">
            <p className="eyebrow">
              ASSEMBLY REVIEW WALKTHROUGH / NO SOLVED MOTION
            </p>
            <h3>
              {String(step + 1).padStart(2, '0')} / {p.steps[step]}
            </h3>
            <div>
              <button
                disabled={step === 0}
                onClick={() => setStep((x) => x - 1)}
              >
                Previous step
              </button>
              <span>
                {step + 1} / {p.steps.length}
              </span>
              <button
                disabled={step === p.steps.length - 1}
                onClick={() => {
                  setStep((x) => x + 1);
                  setSelected(
                    p.parts[Math.min(step + 1, p.parts.length - 1)].id,
                  );
                }}
              >
                Next step <ArrowRight size={14} />
              </button>
            </div>
          </div>
          <div className="blue-note">
            <Layers3 size={22} />
            <p>
              The mounting pitch is <strong>2 × H = 440 mm</strong>; H is a
              half-pitch on the source drawing. The transverse pitch is I = 80
              mm. A proposed M16 bolt is not a GALVI hardware specification.
              Drum internal wall/web thickness and shaft bore selection are our
              assumptions, not source dimensions.
            </p>
          </div>
        </section>
      )}
      {stage === 2 && (
        <section className="review-content">
          <div className="blue-section-title">
            <div>
              <p className="eyebrow">SOURCE → DIMENSION → MODEL</p>
              <h2>Every reference has an address.</h2>
              <p>
                GALVI Shoe Brakes catalogue, February 2016. PDF page 4 / printed
                4–5: brake. PDF page 15 / printed 26–27: drum. Current supplier
                confirmation remains open.
              </p>
            </div>
            <a
              href={p.source.url}
              target="_blank"
              rel="noreferrer"
              className="download-primary"
            >
              Original catalogue <ExternalLink size={16} />
            </a>
          </div>
          <div className="parts-table-wrap">
            <table className="parts-table">
              <thead>
                <tr>
                  <th>Symbol</th>
                  <th>Published dimension</th>
                  <th>Value</th>
                  <th>Source</th>
                </tr>
              </thead>
              <tbody>
                {p.dimensions.map((d) => (
                  <tr key={d.symbol}>
                    <td>{d.symbol}</td>
                    <td>{d.label}</td>
                    <td>
                      <strong>
                        {d.value} {d.unit}
                      </strong>
                    </td>
                    <td>
                      <a
                        href={`${p.source.url}#page=${d.page}`}
                        target="_blank"
                        rel="noreferrer"
                      >
                        PDF page {d.page} ↗
                      </a>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="design-columns">
            <article className="technical-panel">
              <p className="eyebrow">OUR CHOICES / NOT GALVI DIMENSIONS</p>
              <h3>Explicit design assumptions</h3>
              <p className="body-row">
                Adapter 762 × 220 × 20 mm; shaft bore 50 mm within a published
                maximum of 80 mm; simplified 20 mm radial rim and 15 mm flat
                web; proposed M16 hardware; installation display width 200 mm.
              </p>
              <p className="body-row">
                No supplier speed, torque or material rating is inherited by our
                simplified drum model. No fit tolerance or production drawing is
                released.
              </p>
            </article>
            <article className="technical-panel">
              <p className="eyebrow">FILE INTEGRITY</p>
              <h3>Check the evidence.</h3>
              <p className="body-row">Archived catalogue SHA-256:</p>
              <code className="source-hash">{p.source.sha256}</code>
              <p className="body-row">
                Read from the original table and drawing, including the repeated
                H dimension. Exact numeric references do not establish current
                validity.
              </p>
              <a
                href={`${base}/dimension-register.json`}
                download
                className="text-link"
              >
                Download dimension register <Download size={14} />
              </a>
            </article>
          </div>
        </section>
      )}
      {stage === 3 && (
        <section className="review-content">
          <div className="blue-section-title">
            <div>
              <p className="eyebrow">A RELEASE DECISION NEEDS EVIDENCE</p>
              <h2>What is ready—and what is not.</h2>
              <p>
                Prepared for a technical meeting. Not released for
                manufacturing.
              </p>
            </div>
          </div>
          <div className="readiness-list">
            {gates.map(([name, status, evidence], i) => (
              <article key={name}>
                <span className={i < 2 ? 'gate-done' : 'gate-open'}>
                  {i < 2 ? <CheckCircle2 size={19} /> : <Clock3 size={19} />}
                </span>
                <div>
                  <h3>{name}</h3>
                  <p>{evidence}</p>
                </div>
                <strong>{status}</strong>
              </article>
            ))}
          </div>
          <div className="blue-note">
            <FileCheck2 size={22} />
            <p>
              Geometry checks establish valid solids and repeatable exports.
              They do not prove mechanism operation, material adequacy, fatigue
              life, thermal capacity, tolerance compliance or safety
              performance. Manufacturing release requires a responsible
              engineering authority’s approval.
            </p>
          </div>
        </section>
      )}
      {stage === 4 && (
        <section className="review-content">
          <div className="blue-section-title">
            <div>
              <p className="eyebrow">LEAVE WITH AN AGREED NEXT STEP</p>
              <h2>The partnership discussion.</h2>
            </div>
            <a
              href="/downloads/director-brief.md"
              download
              className="download-primary"
            >
              Download meeting brief <Download size={16} />
            </a>
          </div>
          <div className="meeting-asks">
            {[
              [
                '01',
                'Confirm the reference',
                'Is this brake/drum combination current and suitable for our first target duty? Which model, options and material variant should we use?',
              ],
              [
                '02',
                'Define the technical handoff',
                'Can you provide controlled interface drawings, supplier STEP, tolerances, mounting hardware, installation limits and force/stroke/time data?',
              ],
              [
                '03',
                'Allocate responsibilities',
                'Who owns brake selection, integration design, independent checking, supplier qualification, testing and release approval?',
              ],
              [
                '04',
                'Agree a pilot programme',
                'Choose one customer duty and one prototype, agree the review gates and obtain supplier/laboratory quotes before tooling commitments.',
              ],
            ].map(([n, title, body]) => (
              <article className="technical-panel" key={n}>
                <p className="eyebrow">{n} / DISCUSSION</p>
                <h3>{title}</h3>
                <p className="body-row">{body}</p>
              </article>
            ))}
          </div>
          <div className="technical-panel">
            <h3>Evidence to request from the director’s team</h3>
            <p className="body-row">
              Current drawings and revisions; approved material and friction
              pair; bore/shaft connection; mounting and retention instructions;
              torque/duty limits; actuator data; failure modes; test reports;
              applicable compliance scope; document-use permissions and service
              support.
            </p>
            <p className="body-row">
              Success for this meeting is an agreed technical review and pilot
              scope—not an unsupported declaration that the current concepts can
              go straight to production.
            </p>
          </div>
        </section>
      )}
      <div className="presentation-footer">
        <button
          disabled={stage === 0}
          onClick={() => {
            setStage((i) => i - 1);
            window.scrollTo({ top: 250, behavior: 'smooth' });
          }}
        >
          <ArrowLeft size={16} /> Previous
        </button>
        <span>
          {stage + 1} / {stages.length}
        </span>
        <button
          disabled={stage === stages.length - 1}
          onClick={() => {
            setStage((i) => i + 1);
            window.scrollTo({ top: 250, behavior: 'smooth' });
          }}
        >
          Next <ArrowRight size={16} />
        </button>
      </div>
      <footer>
        <p>
          AI Braking / Original integration study · GALVI referenced, not
          endorsed
        </p>
        <Link href="/">
          Return to all product workspaces <ArrowRight size={15} />
        </Link>
      </footer>
    </main>
  );
}
