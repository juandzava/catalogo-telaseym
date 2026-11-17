#!/usr/bin/env python3
"""Genera telas/<slug>/index.html (SEO + vista previa), sitemap.xml y 404.html a partir de index.html y catalogo.json.
Ejecutar después de cambiar catalogo.json o index.html:  python3 tools/build.py"""
import json, re, html, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = 'https://telaseym.com'
tpl = (ROOT / 'index.html').read_text(encoding='utf-8')
data = json.loads((ROOT / 'catalogo.json').read_text(encoding='utf-8'))
today = datetime.date.today().isoformat()
e = lambda s: html.escape(str(s), quote=True)

# home: imagen de vista previa grande
home = tpl.replace(f'{SITE}/favicon-512.png"><meta', f'{SITE}/img/og-home.jpg"><meta')  # (no-op si no coincide)
home = re.sub(r'<meta property="og:image" content="[^"]*">\n<meta property="og:image:width" content="512">\n<meta property="og:image:height" content="512">',
              f'<meta property="og:image" content="{SITE}/img/og-home.jpg">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">', home)
home = home.replace('<meta name="twitter:card" content="summary">', '<meta name="twitter:card" content="summary_large_image">')
home = home.replace(f'<meta name="twitter:image" content="{SITE}/favicon-512.png">', f'<meta name="twitter:image" content="{SITE}/img/og-home.jpg">')
(ROOT / 'index.html').write_text(home, encoding='utf-8')

def page(f):
    url = f"{SITE}/telas/{f['slug']}/"
    title = f"{f['name']} por metro y por rollo en Gamarra | Telas E&M"
    desc = f"{f['name']} ({f['comp']}): {len(f['colors'])} colores, S/ {f['pm']} el metro y S/ {f['pr']} por rollo. Pide por WhatsApp en Telas E&M, Gamarra."
    og = f"{SITE}/img/{f['slug']}/og.jpg"
    s = home
    s = re.sub(r'<title>.*?</title>', f'<title>{e(title)}</title>', s, 1)
    s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{e(desc)}">', s, 1)
    s = s.replace(f'<link rel="canonical" href="{SITE}/">', f'<link rel="canonical" href="{url}">')
    s = s.replace(f'<meta property="og:url" content="{SITE}/">', f'<meta property="og:url" content="{url}">')
    for p in ('og:title', 'twitter:title'):
        s = re.sub(rf'<meta (property|name)="{p}" content="[^"]*">', rf'<meta \1="{p}" content="{e(title)}">', s, 1)
    for p in ('og:description', 'twitter:description'):
        s = re.sub(rf'<meta (property|name)="{p}" content="[^"]*">', rf'<meta \1="{p}" content="{e(desc)}">', s, 1)
    s = s.replace(f'{SITE}/img/og-home.jpg', og)
    ld = [{
        "@context": "https://schema.org", "@type": "Product", "name": f['name'], "description": desc,
        "image": [f"{SITE}/{f['hero']}"] + [f"{SITE}/{c['img']}" for c in f['colors'] if c.get('img')][:5],
        "brand": {"@type": "Brand", "name": "Telas E&M"}, "material": f['comp'], "category": "Telas",
        "offers": {"@type": "Offer", "url": url, "priceCurrency": "PEN", "price": str(f['pm']),
                   "availability": "https://schema.org/InStock", "seller": {"@id": f"{SITE}/#negocio"}}
    }, {
        "@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Telas E&M", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": f['name'], "item": url}]
    }]
    s = s.replace('</head>', ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in ld) + '</head>', 1)
    colors = ''.join(f"<li>{e(c['code'] + ' ' if c.get('code') else '')}{e(c['name'])}</li>" for c in f['colors'])
    seo = (f'<div class="wrap"><a class="back" href="/#telas" data-home>← Todas las telas</a><div class="dh" style="display:block">'
           f'<div class="eyebrow">{e(f["sub"])}</div><h1>{e(f["name"])}</h1>'
           f'<p>S/ {f["pm"]} el metro · S/ {f["pr"]} por rollo · {e(f["comp"])} · Ancho {e(f["ancho"])}</p><p>Ideal para: {e(f["usos"])}</p>'
           f'<h2>{len(f["colors"])} colores</h2><ul>{colors}</ul></div></div>')
    s = s.replace('<section id="home">', '<section id="home" hidden>', 1)
    s = s.replace('<section class="detail" id="detail" hidden></section>', f'<section class="detail" id="detail">{seo}</section>', 1)
    return s

for f in data:
    d = ROOT / 'telas' / f['slug']; d.mkdir(parents=True, exist_ok=True)
    (d / 'index.html').write_text(page(f), encoding='utf-8')

import sys; sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_pages
extra = build_pages.write_all()
urls = [f'  <url><loc>{SITE}/</loc><lastmod>{today}</lastmod><priority>1.0</priority></url>']
for f in data:
    urls.append(f"  <url><loc>{SITE}/telas/{f['slug']}/</loc><lastmod>{today}</lastmod><priority>0.8</priority></url>")
urls += [f'  <url><loc>{SITE}{p}</loc><lastmod>{today}</lastmod><priority>{pr}</priority></url>' for p, pr in extra]
(ROOT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(urls) + '\n</urlset>\n', encoding='utf-8')

(ROOT / '404.html').write_text('''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Página no encontrada | Telas E&amp;M</title><meta name="robots" content="noindex"><meta http-equiv="refresh" content="3;url=/">
<link rel="icon" href="/favicon.ico"><style>body{margin:0;min-height:100vh;display:grid;place-items:center;background:#F5F6F2;color:#29395C;font-family:system-ui,sans-serif;text-align:center;padding:24px}
h1{font-family:Georgia,serif;font-weight:400;font-size:44px;margin:0 0 8px}a{display:inline-block;margin-top:16px;background:#29395C;color:#fff;text-decoration:none;font-weight:700;border-radius:999px;padding:12px 22px}</style></head>
<body><div><h1>No encontramos esa página</h1><p>Te llevamos al catálogo de telas.</p><a href="/">Ver telas</a></div></body></html>''', encoding='utf-8')
print(len(data), 'páginas generadas')
