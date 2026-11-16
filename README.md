# Catálogo web · Telas E&M

Sitio: https://telaseym.com

- `index.html`: la página (catálogo, pedido por WhatsApp, pagos).
- `catalogo.json`: telas, precios, colores y agotados. **Para cambiar precios o marcar un color como agotado, se edita aquí** (`"agotado": true`).
- `img/<tela>/`: fotos de cada tela (`portada.jpg` y `NN.jpg` por código de color).

## Páginas por tela (SEO y vista previa)
Cada tela tiene su enlace: `https://telaseym.com/telas/<slug>/`. Esas páginas se **generan**; no se editan a mano.
Después de cambiar `catalogo.json` o `index.html`, ejecutar: `python3 tools/build.py` (regenera `telas/`, `sitemap.xml` y `404.html`).
Para una tela nueva o con portada nueva, generar su imagen de vista previa: `python3 tools/og.py <slug>` (crea `img/<slug>/og.jpg`).
