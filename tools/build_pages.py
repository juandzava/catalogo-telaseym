"""Genera blog, Nosotros, Envíos y pagos y Libro de Reclamaciones con el mismo estilo del sitio."""
import re, json, html, urllib.parse
from pathlib import Path
import site_config as C
from content import POSTS

ROOT = Path(__file__).resolve().parent.parent
SITE = 'https://telaseym.com'
e = lambda s: html.escape(str(s), quote=True)
idx = (ROOT / 'index.html').read_text(encoding='utf-8')
CSS = re.search(r'<style>(.*?)</style>', idx, re.S).group(1)
GA = re.search(r'(<script async src="https://www\.googletagmanager.*?</script>\s*<script>.*?</script>)', idx, re.S)
GA = GA.group(1) if GA else ''
FONTS = re.search(r'(<link rel="preconnect" href="https://fonts\.googleapis\.com">.*?display=swap">)', idx, re.S).group(1)
ICONS = re.search(r'(<link rel="icon" href="/favicon\.ico".*?apple-touch-icon[^>]*>)', idx, re.S).group(1)
WA_ICON = re.search(r'<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">.*?</svg>', idx, re.S).group(0)
WA = 'https://wa.me/' + C.WHATSAPP + '?text=' + urllib.parse.quote('Hola, vi la web de Telas E&M y quiero hacer una consulta.')

EXTRA = """
.pg{max-width:760px;margin-inline:auto;padding:28px var(--gut) 56px}
.pg h1{font-family:var(--f-display);font-weight:400;font-size:clamp(38px,7vw,58px);line-height:1;margin:6px 0 10px;text-wrap:balance}
.pg h2{font-family:var(--f-display);font-weight:400;font-size:30px;line-height:1.1;margin:30px 0 8px}
.pg p,.pg li{font-size:17px;line-height:1.6}
.pg ul,.pg ol{padding-left:22px;display:grid;gap:6px}
.pg a{color:var(--green);font-weight:600}
.pg .btn-wa,.pg .cta .btn-wa{color:#fff}.pg .cta .btn-link{color:#C9D1E2;font-weight:600;text-decoration:underline;display:inline-block;margin-left:6px}
.pg .lead{color:var(--muted);font-size:19px}
.pg .meta{color:var(--muted);font-size:14px;font-weight:600}
.pg .nota{font-size:14px;color:var(--muted)}
.pg table{width:100%;border-collapse:collapse;margin:14px 0;background:var(--paper);border-radius:12px;overflow:hidden;border:1px solid var(--line)}
.pg th,.pg td{text-align:left;padding:11px 14px;border-bottom:1px solid var(--line);font-size:16px}
.pg th{background:var(--soft);font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.crumbs{font-size:14px;color:var(--muted);margin-bottom:6px}.crumbs a{color:var(--muted);font-weight:600}
.posts{display:grid;gap:14px;margin-top:20px}
.post{display:block;background:var(--paper);border:1px solid var(--line);border-radius:var(--r);padding:18px 20px;text-decoration:none;transition:transform .15s,box-shadow .15s}
.post:hover{transform:translateY(-2px);box-shadow:0 10px 24px rgba(27,39,66,.12)}
.post h2{margin:0 0 6px;font-size:28px}.post p{margin:0;color:var(--muted);font-size:16px}.post .meta{margin-top:8px}
.cta{background:var(--navy);color:#fff;border-radius:var(--r);padding:22px;margin-top:34px}
.cta h2{margin:0 0 6px;color:#fff;font-size:28px}.cta p{margin:0 0 14px;color:#C9D1E2}.cta .btn-wa{display:inline-flex}
.fm{display:grid;gap:14px;margin-top:18px}
.fm fieldset{border:1px solid var(--line);background:var(--paper);border-radius:var(--r);padding:16px;display:grid;gap:12px;min-width:0}
.fm legend{font-weight:800;font-size:13px;letter-spacing:.1em;text-transform:uppercase;color:var(--green);padding:0 6px}
.fm label{display:grid;gap:4px;font-weight:600;font-size:14px}
.fm input,.fm select,.fm textarea{font:inherit;font-size:16px;border:1px solid var(--line);border-radius:10px;padding:10px 12px;background:#fff;color:var(--navy);width:100%}
.fm textarea{min-height:100px;resize:vertical}
.fm .row2{display:grid;gap:12px}@media(min-width:600px){.fm .row2{grid-template-columns:1fr 1fr}}
.fm .chk{display:flex;gap:10px;align-items:flex-start;font-weight:500}.fm .chk input{width:auto;margin-top:4px}
.fm button[type=submit]{border:0;border-radius:999px;background:var(--navy);color:#fff;font-weight:700;font-size:16px;padding:14px;cursor:pointer}
.okbox{background:var(--soft);border-radius:var(--r);padding:18px;margin-top:18px}
@media print{.bar,footer,.fab,.fm,.cta{display:none!important}}
"""

def header():
    return f'''<header class="bar"><div class="wrap">
<a class="brand" href="/"><img src="/img/logo.png" alt="Logo E&amp;M" width="40" height="40"><span><small>Gamarra · Lima</small><b>Telas E&amp;M</b></span></a>
<nav aria-label="Secciones"><a href="/#telas">Telas</a><a href="/blog/">Blog</a><a href="/nosotros/">Nosotros</a><a href="/envios-y-pagos/">Envíos y pagos</a></nav>
<a class="btn-wa" href="{WA}" target="_blank" rel="noopener">{WA_ICON}Escríbenos</a></div></header>'''

def footer():
    legal = f'{e(C.RAZON_SOCIAL)}' + (f' · RUC {e(C.RUC)}' if C.RUC else '')
    return f'''<footer><div class="wrap"><span>{legal} · Telas importadas</span>
<span><a href="/blog/">Blog</a> · <a href="/nosotros/">Nosotros</a> · <a href="/envios-y-pagos/">Envíos y pagos</a> · <a href="/libro-de-reclamaciones/">Libro de Reclamaciones</a></span></div></footer>'''

def layout(path, title, desc, body, ld=(), og=f'{SITE}/img/og-home.jpg', extra_js=''):
    url = SITE + path
    lds = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in ld)
    return f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{url}">
<meta property="og:type" content="article"><meta property="og:locale" content="es_PE"><meta property="og:site_name" content="Telas E&amp;M">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{og}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{og}">
{lds}{GA}
{ICONS}
{FONTS}
<style>{CSS}{EXTRA}</style></head><body>
{header()}
<main class="pg">{body}</main>
{footer()}
{extra_js}</body></html>'''

def crumbs(*items):
    return '<nav class="crumbs" aria-label="Ruta">' + ' › '.join(f'<a href="{u}">{e(t)}</a>' if u else e(t) for t, u in items) + '</nav>'

def bc_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": t, "item": SITE + u} for i, (t, u) in enumerate(items)]}

def cta(txt='¿Quieres telas para tu próximo proyecto?'):
    return f'<div class="cta"><h2>{e(txt)}</h2><p>Mira el catálogo y pide por WhatsApp desde 1 metro, o por rollo con precio especial.</p><a class="btn-wa" href="{WA}" target="_blank" rel="noopener">{WA_ICON}Escríbenos por WhatsApp</a> <a class="btn-link" style="color:#C9D1E2" href="/#telas">Ver telas</a></div>'

PAGES = []  # (path, html, priority)

# blog
for p in POSTS:
    path = f'/blog/{p["slug"]}/'
    cr = [('Telas E&M', '/'), ('Blog', '/blog/'), (p['titulo'], path)]
    ld = [{"@context": "https://schema.org", "@type": "Article", "headline": p['titulo'], "description": p['desc'],
           "datePublished": p['fecha'], "dateModified": p['fecha'], "inLanguage": "es-PE", "mainEntityOfPage": SITE + path,
           "image": f'{SITE}/img/og-home.jpg', "author": {"@id": f"{SITE}/#negocio"}, "publisher": {"@id": f"{SITE}/#negocio"}}, bc_ld(cr)]
    body = (crumbs(('Telas E&M', '/'), ('Blog', '/blog/')) + f'<h1>{e(p["titulo"])}</h1><p class="meta">{p["min"]} min de lectura</p>' + p['cuerpo'] + cta())
    PAGES.append((path, layout(path, p['titulo'] + ' | Telas E&M', p['desc'], body, ld), 0.7))

lst = ''.join(f'<a class="post" href="/blog/{p["slug"]}/"><h2>{e(p["titulo"])}</h2><p>{e(p["desc"])}</p><div class="meta">{p["min"]} min de lectura</div></a>' for p in POSTS)
PAGES.append(('/blog/', layout('/blog/', 'Blog de telas: guías para confeccionar | Telas E&M', 'Guías prácticas de Telas E&M: cuánta tela comprar, cómo elegir telas para fiesta, comprar por metro o por rollo y cuidado de tus prendas.',
    crumbs(('Telas E&M', '/'), ('Blog', None)) + '<h1>Blog</h1><p class="lead">Guías prácticas para confeccionar mejor, desde Gamarra.</p><div class="posts">' + lst + '</div>' + cta(),
    [bc_ld([('Telas E&M', '/'), ('Blog', '/blog/')])]), 0.7))

# nosotros
nos = f'''{crumbs(('Telas E&M', '/'), ('Nosotros', None))}<h1>Telas importadas, directo desde Gamarra</h1>
<p class="lead">Somos {e(C.RAZON_SOCIAL)}, una tienda de telas en el corazón de Gamarra, Lima.</p>
<h2>Qué hacemos</h2><p>Importamos y vendemos telas para confección: licras, sastrería, linos y fluidas, encajes y bordados, y telas de fiesta. Vendemos <b>desde 1 metro</b> y también por <b>rollo</b> con precio especial para quienes producen.</p>
<h2>Cómo trabajamos</h2><ul><li>Cada tela tiene su ficha con composición, ancho, peso y colores reales.</li><li>Pides por WhatsApp con el código del color, en un solo mensaje.</li><li>Delivery en Lima y provincia, o recoges en tienda.</li></ul>
<h2>Visítanos</h2><p>{e(C.DIRECCION)}.<br>Lunes a viernes, 10 am a 8 pm · Sábados, 10 am a 5 pm.</p>
<p><a href="https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(C.DIRECCION)}" target="_blank" rel="noopener">Ver en Google Maps</a></p>{cta()}'''
PAGES.append(('/nosotros/', layout('/nosotros/', 'Nosotros | Telas E&M en Gamarra', 'Telas E&M: tienda de telas importadas en Gamarra, Lima. Venta desde 1 metro y por rollo, con delivery en Lima y provincia.', nos, [bc_ld([('Telas E&M', '/'), ('Nosotros', '/nosotros/')])]), 0.6))

# envíos y pagos
env = f'''{crumbs(('Telas E&M', '/'), ('Envíos y pagos', None))}<h1>Envíos y pagos</h1><p class="lead">Así recibes tus telas y así puedes pagar.</p>
<h2>Cómo hacer tu pedido</h2><ol><li>Elige la tela y los colores en el catálogo.</li><li>Indica los metros o rollos y envía todo en un solo mensaje por WhatsApp.</li><li>Te confirmamos disponibilidad y el total.</li></ol>
<h2>Entrega</h2><ul><li><b>Recojo en tienda:</b> {e(C.DIRECCION)}.</li><li><b>Delivery en Lima:</b> S/ 20.</li><li><b>Provincia:</b> S/ 20 hasta la courier que elijas.</li></ul>
<h2>Formas de pago</h2><p>Yape, Plin o tu billetera con el QR, transferencia a BCP, Interbank o Caja Piura, y efectivo en tienda. Los datos de las cuentas están en la <a href="/#pagos">sección de pagos</a>. Envíanos tu comprobante por WhatsApp para despachar tu pedido.</p>
<p class="nota">Vendemos desde 1 metro. El precio por rollo aplica comprando el rollo completo. Precios en soles.</p>{cta('¿Tienes dudas con tu pedido?')}'''
PAGES.append(('/envios-y-pagos/', layout('/envios-y-pagos/', 'Envíos y formas de pago | Telas E&M', 'Delivery en Lima y provincia, recojo en tienda en Gamarra y pagos con Yape, Plin, transferencia o efectivo. Así funciona tu pedido en Telas E&M.', env, [bc_ld([('Telas E&M', '/'), ('Envíos y pagos', '/envios-y-pagos/')])]), 0.6))

# libro de reclamaciones
ruc_line = f'<br>RUC: {e(C.RUC)}' if C.RUC else ''
mail_line = f'<br>Correo: {e(C.EMAIL)}' if C.EMAIL else ''
lr_js = f'''<script>
(function(){{
var F=document.getElementById('lr'),OUT=document.getElementById('lrOut'),EP={json.dumps(C.RECLAMOS_ENDPOINT)},WA={json.dumps(C.WHATSAPP)};
F.addEventListener('submit',function(ev){{ev.preventDefault();
 var d=new FormData(F),o={{}};d.forEach(function(v,k){{o[k]=v}});
 var n='RC-'+new Date().toISOString().slice(0,10).replace(/-/g,'')+'-'+Math.random().toString(36).slice(2,6).toUpperCase();o.hoja=n;
 var txt='HOJA DE RECLAMACIÓN '+n+'\\nFecha: '+o.fecha+'\\nTipo: '+o.tipo+'\\nConsumidor: '+o.nombre+' ('+o.doc+')\\nDomicilio: '+o.domicilio+'\\nTeléfono: '+o.telefono+'\\nCorreo: '+o.email+'\\nBien contratado: '+o.bien+' · Monto: S/ '+(o.monto||'-')+'\\nDescripción: '+o.descbien+'\\nDetalle: '+o.detalle+'\\nPedido del consumidor: '+o.pedido;
 function done(extra){{OUT.hidden=false;OUT.innerHTML='<h2>Hoja registrada: '+n+'</h2><p>'+extra+'</p><p>Guarda o imprime esta hoja como tu copia.</p><pre style="white-space:pre-wrap;font:inherit;background:#fff;border:1px solid var(--line);border-radius:12px;padding:14px"></pre><button class="share" onclick="window.print()">Imprimir / guardar PDF</button>';OUT.querySelector('pre').textContent=txt;F.hidden=true;OUT.scrollIntoView();}}
 if(EP){{fetch(EP,{{method:'POST',headers:{{'Content-Type':'application/json','Accept':'application/json'}},body:JSON.stringify(o)}}).then(function(r){{if(!r.ok)throw 0;done('Recibimos tu hoja. Te responderemos en un máximo de 15 días hábiles.')}}).catch(function(){{alert('No se pudo enviar. Inténtalo de nuevo o escríbenos por WhatsApp.')}});}}
 else{{window.open('https://wa.me/'+WA+'?text='+encodeURIComponent(txt),'_blank');done('Se abrió WhatsApp con tu hoja: envía el mensaje para completar el registro. Te responderemos en un máximo de 15 días hábiles.')}}
}});
document.getElementById('fecha').value=new Date().toISOString().slice(0,10);
}})();
</script>'''
lr = f'''{crumbs(('Telas E&M', '/'), ('Libro de Reclamaciones', None))}<h1>Libro de Reclamaciones</h1>
<p class="lead">Si tienes un reclamo o una queja sobre un producto o servicio, regístralo aquí.</p>
<p><b>{e(C.RAZON_SOCIAL)}</b>{ruc_line}<br>{e(C.DIRECCION)}{mail_line}</p>
<form class="fm" id="lr">
<fieldset><legend>1. Identificación del consumidor</legend>
<div class="row2"><label>Nombre completo<input name="nombre" required autocomplete="name"></label><label>DNI / CE<input name="doc" required inputmode="numeric"></label></div>
<label>Domicilio<input name="domicilio" required autocomplete="street-address"></label>
<div class="row2"><label>Teléfono<input name="telefono" required type="tel" autocomplete="tel"></label><label>Correo electrónico<input name="email" required type="email" autocomplete="email"></label></div>
<label>Fecha<input name="fecha" id="fecha" type="date" required></label></fieldset>
<fieldset><legend>2. Identificación del bien contratado</legend>
<div class="row2"><label>Tipo<select name="bien"><option>Producto</option><option>Servicio</option></select></label><label>Monto reclamado (S/)<input name="monto" inputmode="decimal"></label></div>
<label>Descripción (tela, color, fecha de compra)<textarea name="descbien" required></textarea></label></fieldset>
<fieldset><legend>3. Detalle de la reclamación</legend>
<label>Tipo<select name="tipo"><option>Reclamo (disconformidad con el producto o servicio)</option><option>Queja (malestar con la atención, sin relación con el producto)</option></select></label>
<label>Detalle<textarea name="detalle" required></textarea></label>
<label>Pedido del consumidor<textarea name="pedido" required></textarea></label></fieldset>
<label class="chk"><input type="checkbox" required>Declaro que los datos son verdaderos y acepto que se usen para atender mi reclamación.</label>
<button type="submit">Registrar reclamación</button>
<p class="nota">Responderemos en un plazo máximo de 15 días hábiles, según la normativa vigente. El registro no impide acudir a INDECOPI.</p></form>
<div class="okbox" id="lrOut" hidden></div>'''
PAGES.append(('/libro-de-reclamaciones/', layout('/libro-de-reclamaciones/', 'Libro de Reclamaciones | Telas E&M', 'Registra tu reclamo o queja en el Libro de Reclamaciones virtual de Telas E&M.', lr, [bc_ld([('Telas E&M', '/'), ('Libro de Reclamaciones', '/libro-de-reclamaciones/')])], extra_js=lr_js), 0.3))

def write_all():
    for path, h, _ in PAGES:
        d = ROOT / path.strip('/'); d.mkdir(parents=True, exist_ok=True)
        (d / 'index.html').write_text(h, encoding='utf-8')
    return [(p, pr) for p, _, pr in PAGES]
