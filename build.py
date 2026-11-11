#!/usr/bin/env python3
"""Build the installable EA Excerpts web app.

Usage:  python3 build.py      (uses the newest app/ea_excerpts_vNN.html)

Writes site/: index.html, sw.js (offline cache), manifest.webmanifest, icons/ (drawn here). Needs Pillow.
"""
import glob, os, re, hashlib, datetime, math

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, 'site')

SW = """/* EA Excerpts offline cache, build __BUILD__ */
const CACHE = 'ea-excerpts-__BUILD__';
const SHELL = ['./', 'index.html', 'manifest.webmanifest', 'icons/icon-180.png', 'icons/icon-192.png', 'icons/icon-512.png'];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith('ea-excerpts-') && k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
// Use what's on the iPad straight away; fetch a fresh copy in the background when online.
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;
  const key = req.mode === 'navigate' ? 'index.html' : req;
  e.respondWith(caches.open(CACHE).then(async c => {
    const hit = await c.match(key, { ignoreSearch: true });
    const net = fetch(req).then(r => { if (r && r.ok) c.put(key, r.clone()); return r; }).catch(() => null);
    if (hit) { e.waitUntil(net); return hit; }
    return (await net) || new Response('Offline and not yet saved on this iPad. Open the app once while online.', { status: 503, headers: { 'Content-Type': 'text/plain' } });
  }));
});
"""

MANIFEST = """{
  "name": "EA Excerpts",
  "short_name": "EA Excerpts",
  "start_url": "./",
  "scope": "./",
  "display": "standalone",
  "orientation": "any",
  "background_color": "#f2ede2",
  "theme_color": "#f2ede2",
  "icons": [
    { "src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png" },
    { "src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable" }
  ]
}
"""

def make_icons(out):
    # Parchment square: a sonogram-like band of partials over a strip of piano keys.
    from PIL import Image, ImageDraw
    N = 1024
    im = Image.new('RGB', (N, N), (242, 237, 226)); d = ImageDraw.Draw(im)
    for k in range(7):  # partial lines, rising and fading
        y0 = 560 - k * 62; w = max(4, 22 - k * 3); c = tuple(int(30 + (201 - 30) * k / 7) for _ in range(1))[0]
        col = (30 + k * 24, 29 + k * 18, 27 + k * 12)
        pts = [(140 + i * 8, y0 - 40 * math.sin(i * 0.035 + k * 0.4) - i * 0.12) for i in range(94)]
        d.line(pts, fill=col, width=w, joint='curve')
    d.rectangle([140, 700, 884, 900], fill=(255, 255, 255), outline=(30, 29, 27), width=6)
    ww = 744 / 10
    for i in range(1, 10): d.line([140 + i * ww, 700, 140 + i * ww, 900], fill=(30, 29, 27), width=4)
    for i in (1, 2, 4, 5, 6, 8, 9):
        x = 140 + i * ww; d.rectangle([x - 20, 700, x + 20, 810], fill=(30, 29, 27))
    os.makedirs(os.path.join(out, 'icons'), exist_ok=True)
    for n in (180, 192, 512):
        im.resize((n, n), Image.LANCZOS).save(os.path.join(out, 'icons', f'icon-{n}.png'))

def main():
    files = glob.glob(os.path.join(HERE, 'app', 'ea_excerpts_v*.html'))
    def ver(p):
        m = re.search(r'_v(\d+)\.html$', p)
        return int(m.group(1)) if m else -1
    assert files, 'no app/ea_excerpts_vNN.html found'
    src = max(files, key=ver)
    html = open(src, encoding='utf-8').read()
    build = f'v{ver(src)}-' + datetime.datetime.now().strftime('%Y%m%d-%H%M') + '-' + hashlib.sha1(html.encode()).hexdigest()[:6]
    os.makedirs(SITE, exist_ok=True)
    open(os.path.join(SITE, 'index.html'), 'w', encoding='utf-8').write(html)
    open(os.path.join(SITE, 'sw.js'), 'w', encoding='utf-8').write(SW.replace('__BUILD__', build))
    open(os.path.join(SITE, 'manifest.webmanifest'), 'w', encoding='utf-8').write(MANIFEST)
    open(os.path.join(SITE, '.nojekyll'), 'w').write('')
    make_icons(SITE)
    print('built', build, 'from', os.path.basename(src))

if __name__ == '__main__':
    main()
