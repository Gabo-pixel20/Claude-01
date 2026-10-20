// Adiós Pan: funciona sin conexión.
// - La app y las recetas (HTML, JS, manifest): primero la red, para que las
//   recetas nuevas de cada mes lleguen solas; sin conexión, la copia guardada.
// - Fotos, íconos y fuentes: primero la copia guardada (no cambian).
const VERSION = "adiospan-v2";
const BASE = ["./", "index.html", "recetas.js", "manifest.webmanifest", "icono-192.png", "icono-512.png",
  "fuentes/poppins-400.woff2", "fuentes/poppins-500.woff2", "fuentes/poppins-700.woff2", "fuentes/cookie-400.woff2"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(VERSION).then(c => c.addAll(BASE)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== VERSION).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});

const guardar = (req, r) => {
  if (r.ok && new URL(req.url).origin === location.origin) { const copia = r.clone(); caches.open(VERSION).then(c => c.put(req, copia)); }
  return r;
};

self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;
  const ruta = new URL(req.url).pathname;
  const cambia = req.mode === "navigate" || /\.(html|js|webmanifest)$/.test(ruta) || ruta.endsWith("/");
  e.respondWith(cambia
    ? fetch(req).then(r => guardar(req, r)).catch(() => caches.match(req).then(h => h || caches.match("index.html")))
    : caches.match(req).then(h => h || fetch(req).then(r => guardar(req, r))));
});
