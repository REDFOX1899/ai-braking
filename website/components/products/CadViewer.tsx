'use client';
import { useEffect, useRef, useState } from 'react';
import type * as THREE from 'three';
import { RotateCcw, Expand, Download, Box, Eye } from 'lucide-react';
type Part = {
  id: string;
  name: string;
  role: string;
  color: string;
  dimensions?: number[];
};
type Annotation = { label: string; a: number[]; b: number[]; status: string };
type MeshRecord = {
  id: string;
  vertices: number[];
  triangles: number[];
  pos: number[];
  color: string;
  explode: number[];
};
export default function CadViewer({
  slug,
  parts,
  selected,
  onSelect,
  annotations = [],
}: {
  slug: string;
  annotations?: Annotation[];
  parts: Part[];
  selected: string | null;
  onSelect: (id: string | null) => void;
}) {
  const host = useRef<HTMLDivElement>(null);
  const api = useRef<{
    explode: (v: number) => void;
    select: (id: string | null) => void;
    view: (s: string) => void;
    download: () => void;
    options: (
      isolate: boolean,
      section: boolean,
      cut: number,
      dimensions: boolean,
      envelopes: boolean,
    ) => void;
  } | null>(null);
  const selectRef = useRef(onSelect);
  selectRef.current = onSelect;
  const [status, setStatus] = useState('Loading solid model…');
  const [failed, setFailed] = useState(false);
  const [spread, setSpread] = useState(0);
  const [view, setView] = useState('iso');
  const [isolate, setIsolate] = useState(false);
  const [section, setSection] = useState(false);
  const [cut, setCut] = useState(0.5);
  const [dimensions, setDimensions] = useState(false);
  const [envelopes, setEnvelopes] = useState(true);
  const [ready, setReady] = useState(false);
  useEffect(() => {
    let disposed = false;
    let cleanup = () => {};
    setFailed(false);
    setReady(false);
    setSpread(0);
    setView('iso');
    setStatus('Loading solid model…');
    (async () => {
      const T = await import('three');
      const { OrbitControls } =
        await import('three/addons/controls/OrbitControls.js');
      const response = await fetch(`/products/${slug}/mesh.json`);
      if (!response.ok) throw Error('Model unavailable');
      const data: MeshRecord[] = await response.json();
      if (disposed || !host.current) return;
      const el = host.current;
      const renderer = new T.WebGLRenderer({
        antialias: true,
        alpha: true,
        preserveDrawingBuffer: true,
      });
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      renderer.setClearColor(0x07182b, 1);
      renderer.outputColorSpace = T.SRGBColorSpace;
      renderer.localClippingEnabled = true;
      renderer.toneMapping = T.ACESFilmicToneMapping;
      renderer.toneMappingExposure = 1.15;
      el.appendChild(renderer.domElement);
      const scene = new T.Scene();
      const root = new T.Group();
      scene.add(root);
      const camera = new T.PerspectiveCamera(35, 1, 1, 100000);
      camera.up.set(0, 0, 1);
      const controls = new OrbitControls(camera, renderer.domElement);
      controls.enableDamping = true;
      controls.dampingFactor = 0.12;
      scene.add(new T.HemisphereLight(0xe2f4ff, 0x173650, 2.6));
      const key = new T.DirectionalLight(0xffffff, 3);
      key.position.set(600, -700, 1200);
      scene.add(key);
      const fill = new T.DirectionalLight(0x5fbaff, 2);
      fill.position.set(-600, 500, 200);
      scene.add(fill);
      const meshes: THREE.Mesh[] = [];
      const records = new Map(data.map((r) => [r.id, r]));
      data.forEach((r) => {
        const g = new T.BufferGeometry();
        g.setAttribute('position', new T.Float32BufferAttribute(r.vertices, 3));
        g.setIndex(r.triangles);
        g.computeVertexNormals();
        const m = new T.MeshStandardMaterial({
          color: /lining|friction|pad/i.test(
            parts.find((p) => p.id === r.id)?.name || '',
          )
            ? '#536577'
            : /drum|disc|hub|pin|bolt|hardware/i.test(
                  parts.find((p) => p.id === r.id)?.name || '',
                )
              ? '#a4b8c7'
              : r.color,
          metalness: /drum|disc|hub|pin|bolt|hardware/i.test(
            parts.find((p) => p.id === r.id)?.name || '',
          )
            ? 0.72
            : 0.25,
          roughness: 0.38,
          side: T.DoubleSide,
        });
        const mesh = new T.Mesh(g, m);
        mesh.name = r.id;
        mesh.position.set(...(r.pos as [number, number, number]));
        root.add(mesh);
        const edge = new T.LineSegments(
          new T.EdgesGeometry(g, 25),
          new T.LineBasicMaterial({
            color: 0x9bd9f2,
            transparent: true,
            opacity: 0.22,
          }),
        );
        mesh.add(edge);
        meshes.push(mesh);
      });
      const bounds = new T.Box3().setFromObject(root);
      const center = bounds.getCenter(new T.Vector3());
      const size = bounds.getSize(new T.Vector3());
      const radius = Math.max(size.x, size.y, size.z);
      controls.target.copy(center);
      controls.minDistance = radius * 0.2;
      controls.maxDistance = radius * 8;
      const grid = new T.GridHelper(radius * 2.5, 25, 0x1d5575, 0x102f49);
      grid.rotation.x = Math.PI / 2;
      grid.position.set(center.x, center.y, bounds.min.z - 8);
      scene.add(grid);
      function setView(v: string) {
        const dirs: Record<string, number[]> = {
          iso: [1.2, -1.6, 1.05],
          front: [0, -2.3, 0.01],
          top: [0.01, 0, 2.3],
          side: [2.3, 0, 0.01],
        };
        const d = dirs[v] || dirs.iso;
        camera.position.set(
          center.x + d[0] * radius,
          center.y + d[1] * radius,
          center.z + d[2] * radius,
        );
        controls.target.copy(center);
        controls.update();
      }
      setView('iso');
      const ray = new T.Raycaster();
      const pointer = new T.Vector2();
      let start = [0, 0];
      const down = (e: PointerEvent) => {
        start = [e.clientX, e.clientY];
      };
      const up = (e: PointerEvent) => {
        if (Math.hypot(e.clientX - start[0], e.clientY - start[1]) > 5) return;
        const rect = renderer.domElement.getBoundingClientRect();
        pointer.set(
          ((e.clientX - rect.left) / rect.width) * 2 - 1,
          (-(e.clientY - rect.top) / rect.height) * 2 + 1,
        );
        ray.setFromCamera(pointer, camera);
        const hit = ray.intersectObjects(
          meshes.filter(
            (m) =>
              m.visible &&
              parts.find((p) => p.id === m.name)?.role !== 'interface-envelope',
          ),
          false,
        )[0];
        selectRef.current(hit?.object.name ?? null);
      };
      renderer.domElement.addEventListener('pointerdown', down);
      renderer.domElement.addEventListener('pointerup', up);
      renderer.domElement.setAttribute(
        'aria-label',
        'Interactive CAD assembly. Drag to rotate, scroll to zoom. Select parts using the accessible parts list.',
      );
      renderer.domElement.setAttribute('role', 'img');
      const observer = new ResizeObserver(() => {
        const w = el.clientWidth,
          h = el.clientHeight;
        renderer.setSize(w, h);
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
      });
      observer.observe(el);
      let currentSelected: string | null = null,
        solo = false,
        sectionOn = false,
        dimOn = false,
        showEnvelopes = true;
      const clip = new T.Plane(new T.Vector3(0, -1, 0), center.y);
      const annotationGroup = new T.Group();
      scene.add(annotationGroup);
      const textures: THREE.Texture[] = [];
      function clearAnnotations() {
        annotationGroup.traverse((o) => {
          const x = o as THREE.Mesh;
          x.geometry?.dispose();
          if (x.material)
            (Array.isArray(x.material) ? x.material : [x.material]).forEach(
              (m) => m.dispose(),
            );
        });
        annotationGroup.clear();
        textures.forEach((t) => t.dispose());
        textures.length = 0;
      }
      function dimension(
        a: number[],
        b: number[],
        label: string,
        color = 0x78d6f7,
      ) {
        const points = [
          new T.Vector3(...(a as [number, number, number])),
          new T.Vector3(...(b as [number, number, number])),
        ];
        annotationGroup.add(
          new T.Line(
            new T.BufferGeometry().setFromPoints(points),
            new T.LineBasicMaterial({ color, depthTest: false }),
          ),
        );
        points.forEach((p) => {
          const dot = new T.Mesh(
            new T.SphereGeometry(radius * 0.006, 8, 8),
            new T.MeshBasicMaterial({ color, depthTest: false }),
          );
          dot.position.copy(p);
          annotationGroup.add(dot);
        });
        const c = document.createElement('canvas');
        c.width = 768;
        c.height = 80;
        const ctx = c.getContext('2d')!;
        ctx.fillStyle = '#09263dee';
        ctx.fillRect(0, 0, 768, 80);
        ctx.fillStyle = '#b7eaff';
        ctx.font = '26px monospace';
        ctx.textAlign = 'center';
        ctx.fillText(label, 384, 49);
        const texture = new T.CanvasTexture(c);
        textures.push(texture);
        const sprite = new T.Sprite(
          new T.SpriteMaterial({ map: texture, depthTest: false }),
        );
        sprite.position.copy(
          points[0].clone().add(points[1]).multiplyScalar(0.5),
        );
        sprite.position.z += radius * 0.055;
        sprite.scale.set(radius * 0.65, radius * 0.067, 1);
        sprite.renderOrder = 10;
        annotationGroup.add(sprite);
      }
      function refresh() {
        meshes.forEach((m) => {
          const part = parts.find((p) => p.id === m.name)!;
          const envelope = part.role === 'interface-envelope';
          m.visible =
            (!solo || !currentSelected || currentSelected === m.name) &&
            (!envelope || showEnvelopes);
          const mat = m.material as THREE.MeshStandardMaterial;
          mat.emissive.set(currentSelected === m.name ? 0x126da0 : 0);
          mat.emissiveIntensity = 0.3;
          mat.opacity = envelope
            ? 0.08
            : !currentSelected || currentSelected === m.name || solo
              ? 1
              : 0.22;
          mat.transparent = mat.opacity < 1;
          mat.depthWrite = mat.opacity === 1;
          mat.clippingPlanes = sectionOn ? [clip] : [];
          const edge = m.children[0] as THREE.LineSegments;
          (edge.material as THREE.LineBasicMaterial).clippingPlanes = sectionOn
            ? [clip]
            : [];
        });
        clearAnnotations();
        if (!dimOn) return;
        if (!currentSelected && annotations.length) {
          annotations.forEach((x) => dimension(x.a, x.b, x.label));
          return;
        }
        const target = currentSelected
          ? meshes.find((x) => x.name === currentSelected)
          : root;
        if (!target) return;
        const box = new T.Box3().setFromObject(target);
        const a = box.min,
          b = box.max;
        const d = box.getSize(new T.Vector3());
        const nominal = parts.find((p) => p.id === currentSelected)?.dimensions;
        const nums = nominal || [d.x, d.y, d.z];
        dimension(
          [a.x, a.y, a.z],
          [b.x, a.y, a.z],
          `X ${nums[0].toFixed(2)} mm / nominal bounds`,
        );
        dimension(
          [b.x, a.y, a.z],
          [b.x, b.y, a.z],
          `Y ${nums[1].toFixed(2)} mm / nominal bounds`,
        );
        dimension(
          [b.x, b.y, a.z],
          [b.x, b.y, b.z],
          `Z ${nums[2].toFixed(2)} mm / nominal bounds`,
        );
      }
      api.current = {
        explode(v) {
          meshes.forEach((m) => {
            const r = records.get(m.name)!;
            m.position.set(
              ...(r.pos.map((x, i) => x + r.explode[i] * v) as [
                number,
                number,
                number,
              ]),
            );
          });
          refresh();
        },
        select(id) {
          currentSelected = id;
          refresh();
        },
        options(i, s, c, d, e) {
          solo = i;
          sectionOn = s;
          dimOn = d;
          showEnvelopes = e;
          clip.constant = bounds.min.y + (bounds.max.y - bounds.min.y) * c;
          refresh();
        },
        view: setView,
        download() {
          renderer.render(scene, camera);
          const a = document.createElement('a');
          a.href = renderer.domElement.toDataURL('image/png');
          a.download = `${slug}-C0-concept.png`;
          a.click();
        },
      };
      let frame = 0;
      const draw = () => {
        frame = requestAnimationFrame(draw);
        controls.update();
        renderer.render(scene, camera);
      };
      refresh();
      draw();
      setReady(true);
      setStatus(`${parts.length} components · mm · C0`);
      cleanup = () => {
        cancelAnimationFrame(frame);
        clearAnnotations();
        observer.disconnect();
        controls.dispose();
        scene.traverse((o) => {
          const m = o as THREE.Mesh;
          if (m.geometry) m.geometry.dispose();
          if (m.material) {
            (Array.isArray(m.material) ? m.material : [m.material]).forEach(
              (x) => x.dispose(),
            );
          }
        });
        renderer.dispose();
        renderer.domElement.remove();
        api.current = null;
      };
      if (disposed) cleanup();
    })().catch(() => {
      if (!disposed) {
        setFailed(true);
        setStatus('3D unavailable · CAD preview below');
      }
    });
    return () => {
      disposed = true;
      cleanup();
    };
  }, [slug, parts.length]);
  useEffect(() => {
    api.current?.select(selected);
  }, [selected, ready]);
  useEffect(() => {
    api.current?.options(isolate, section, cut, dimensions, envelopes);
  }, [isolate, section, cut, dimensions, envelopes, ready]);
  return (
    <div className="cad-shell">
      <div className="cad-top">
        <span>
          <i />
          {status}
        </span>
        <span>ENGINEER REVIEW</span>
      </div>
      <div className="cad-stage" ref={host}>
        {failed && (
          <img
            src={`/products/${slug}/preview.svg`}
            alt="CAD-derived assembly preview"
          />
        )}
        <span className="cad-coordinate">
          Z ↑<br />X → Y ↗
        </span>
        <span className="cad-watermark">C0 / NOT FOR MANUFACTURE</span>
      </div>
      <div className="cad-controls">
        <div className="view-buttons">
          {['iso', 'front', 'top', 'side'].map((v) => (
            <button
              key={v}
              aria-pressed={view === v}
              onClick={() => {
                setView(v);
                api.current?.view(v);
              }}
            >
              {v}
            </button>
          ))}
        </div>
        <label className="explode-control">
          <Expand size={14} /> Explode{' '}
          <input
            aria-label="Exploded assembly amount"
            type="range"
            min="0"
            max="1.5"
            step="0.05"
            value={spread}
            onChange={(e) => {
              const x = Number(e.target.value);
              setSpread(x);
              api.current?.explode(x);
            }}
          />
        </label>
        <button
          title="Reset model"
          aria-label="Reset model"
          onClick={() => {
            setSpread(0);
            setSection(false);
            setDimensions(false);
            setIsolate(false);
            setEnvelopes(true);
            setView('iso');
            api.current?.explode(0);
            api.current?.view('iso');
            onSelect(null);
          }}
        >
          <RotateCcw size={16} />
        </button>
        <button
          title="Download current CAD view"
          aria-label="Download current CAD view"
          onClick={() => api.current?.download()}
        >
          <Download size={16} />
        </button>
      </div>
      <div className="cad-inspection-tools">
        <button
          aria-pressed={dimensions}
          onClick={() => setDimensions((v) => !v)}
        >
          Dimensions
        </button>
        <button
          aria-pressed={isolate}
          disabled={!selected}
          onClick={() => setIsolate((v) => !v)}
        >
          Isolate part
        </button>
        <button aria-pressed={section} onClick={() => setSection((v) => !v)}>
          Section cut
        </button>
        {section && (
          <input
            aria-label="Section plane position"
            type="range"
            min="0"
            max="1"
            step=".01"
            value={cut}
            onChange={(e) => setCut(Number(e.target.value))}
          />
        )}
        <button
          aria-pressed={envelopes}
          onClick={() => setEnvelopes((v) => !v)}
        >
          Envelopes
        </button>
        <button
          onClick={() => host.current?.parentElement?.requestFullscreen?.()}
        >
          Full screen
        </button>
      </div>
      {(section || dimensions) && (
        <p className="cad-explanation">
          {section ? 'Open clipping view; cut faces are not capped. ' : ''}
          {dimensions
            ? annotations.length && !selected
              ? 'Cyan: published reference dimensions; current supplier confirmation pending.'
              : 'Nominal CAD bounds, not toleranced acceptance dimensions.'
            : ''}
        </p>
      )}
      <div className="cad-help">
        <span>
          <Box size={13} /> Drag to orbit · scroll to zoom · click a part
        </span>
        <span>
          <Eye size={13} /> Actual tessellated CAD geometry
        </span>
      </div>
    </div>
  );
}
