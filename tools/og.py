#!/usr/bin/env python3
"""Genera las imágenes de vista previa (1200x630) para WhatsApp/Facebook: img/<slug>/og.jpg e img/og-home.jpg.
Requiere: playwright (chromium) y `npm i @fontsource/instrument-serif @fontsource/figtree` en FONTS_DIR."""
import json, os, sys, html
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
FONTS = Path(os.environ.get('FONTS_DIR', '/tmp/ogb/node_modules/@fontsource'))
data = json.load(open(ROOT / 'catalogo.json', encoding='utf-8'))
only = set(sys.argv[1:])

def ff():
    s = FONTS / 'instrument-serif/files/instrument-serif-latin-400-normal.woff2'
    f7 = FONTS / 'figtree/files/figtree-latin-700-normal.woff2'
    f5 = FONTS / 'figtree/files/figtree-latin-500-normal.woff2'
    return (f"@font-face{{font-family:'IS';src:url('file://{s}')}}"
            f"@font-face{{font-family:'FG';font-weight:700;src:url('file://{f7}')}}"
            f"@font-face{{font-family:'FG';font-weight:500;src:url('file://{f5}')}}")

BASE = ("*{box-sizing:border-box;margin:0}body{width:1200px;height:630px;background:#29395C;color:#fff;font-family:'FG';display:flex;overflow:hidden}"
        ".p{flex:none;width:504px;height:630px;overflow:hidden;background:#E9ECE4}.p img{width:100%;height:100%;object-fit:cover}"
        ".r{flex:1;padding:54px 56px;display:flex;flex-direction:column;justify-content:space-between}"
        ".k{font-size:20px;letter-spacing:.2em;text-transform:uppercase;color:#8CCB7E;font-weight:700}"
        "h1{font-family:'IS';font-weight:400;font-size:92px;line-height:.95;margin-top:18px}"
        ".s{font-size:22px;color:#C9D1E2;margin-top:14px;font-weight:500}"
        ".pr{display:flex;gap:14px;margin-top:26px}.pr div{background:#fff;color:#29395C;border-radius:16px;padding:12px 20px}"
        ".pr div.r2{background:#3F8A3A;color:#fff}.pr b{display:block;font-size:40px;line-height:1}.pr span{font-size:15px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;opacity:.75}"
        ".f{display:flex;justify-content:space-between;align-items:center;font-size:24px;font-weight:700}.f i{font-style:normal;color:#8CCB7E}")

def fabric_html(f):
    img = (ROOT / f['hero']).as_uri()
    return (f"<style>{ff()}{BASE}</style><div class=p><img src='{img}'></div><div class=r><div>"
            f"<div class=k>Telas E&amp;M · Gamarra</div><h1>{html.escape(f['name'])}</h1>"
            f"<div class=s>{len(f['colors'])} colores · {html.escape(f['comp'])}</div>"
            f"<div class=pr><div><b>S/ {f['pm']}</b><span>el metro</span></div><div class=r2><b>S/ {f['pr']}</b><span>por rollo</span></div></div></div>"
            f"<div class=f><span>telaseym.com</span><i>Pide por WhatsApp</i></div></div>")

def home_html():
    imgs = ''.join(f"<img src='{(ROOT / f['hero']).as_uri()}'>" for f in data[:6])
    return (f"<style>{ff()}{BASE}.g{{flex:none;width:540px;display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(2,1fr)}}.g img{{width:100%;height:100%;object-fit:cover}}"
            f"h1{{font-size:84px}}</style><div class=g>{imgs}</div><div class=r><div><div class=k>Gamarra · Lima</div>"
            f"<h1>Telas E&amp;M</h1><div class=s>Telas importadas desde 1 metro y por rollo. Delivery en Lima y provincia.</div></div>"
            f"<div class=f><span>telaseym.com</span><i>Pide por WhatsApp</i></div></div>")

with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1200, 'height': 630})
    jobs = [(ROOT / 'img/og-home.jpg', home_html())] if not only or 'home' in only else []
    jobs += [(ROOT / 'img' / f['slug'] / 'og.jpg', fabric_html(f)) for f in data if not only or f['slug'] in only]
    for out, h in jobs:
        tmp = ROOT / '_og.html'; tmp.write_text(h, encoding='utf-8')
        pg.goto(tmp.as_uri()); pg.wait_for_timeout(250)
        pg.screenshot(path=str(out), type='jpeg', quality=88); print(out.relative_to(ROOT))
    tmp.unlink(); b.close()
