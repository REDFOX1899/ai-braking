'use client';
import { useEffect, useRef, useState } from 'react';
import type * as THREE from 'three';
import { RotateCcw, Expand, Download, Box, Eye } from 'lucide-react';
type Part = { id: string; name: string; role: string; color: string };
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
}: {
  slug: string;
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
  } | null>(null);
  const selectRef = useRef(onSelect);
  selectRef.current = onSelect;
  const [status, setStatus] = useState('Loading solid model…');
  const [failed, setFailed] = useState(false);
  const [spread, setSpread] = useState(0);
  const [view, setView] = useState('iso');
  useEffect(() => {
    let disposed = false;
    let cleanup = () => {};
    setFailed(false);
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
          color: r.color,
          metalness: 0.32,
          roughness: 0.5,
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
        const hit = ray.intersectObjects(meshes, false)[0];
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
        },
        select(id) {
          meshes.forEach((m) => {
            const mat = m.material as THREE.MeshStandardMaterial;
            mat.emissive.set(id === m.name ? 0x157db1 : 0x000000);
            mat.emissiveIntensity = id === m.name ? 0.55 : 0;
            mat.opacity = !id || id === m.name ? 1 : 0.25;
            mat.transparent = !!id && id !== m.name;
            mat.depthWrite = !id || id === m.name;
          });
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
      draw();
      setStatus(`${parts.length} components · mm · C0`);
      cleanup = () => {
        cancelAnimationFrame(frame);
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
  }, [selected]);
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
