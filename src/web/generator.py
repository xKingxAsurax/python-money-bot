import json
from datetime import datetime
from html import escape
from typing import List
from src.core.models import Oferta
from src.core.logger import logger


class WebGenerator:
    """Genera index.html con SEO, sitemap.xml y robots.txt."""

    def __init__(self, output_file: str = "index.html", site_url: str = "https://example.com"):
        self.output_file = output_file
        self.site_url = site_url.rstrip("/")

    def generate(self, offers: List[Oferta]):
        logger.info(f"Generating web with {len(offers)} offers...")

        categories = sorted(set(o.category for o in offers))
        cards_html = "\n".join(self._generate_card(o) for o in offers)
        filters_html = "\n".join(
            f'<button onclick="filterCategory(\'{escape(c)}\')" class="px-4 py-2 rounded-full bg-white text-gray-700 font-medium border hover:bg-gray-50 transition">{escape(c)}</button>'
            for c in categories
        )

        items = [
            {
                "@type": "ListItem",
                "position": i,
                "item": {
                    "@type": "Product",
                    "name": o.title,
                    "image": o.image_url or f"{self.site_url}/placeholder.png",
                    "offers": {
                        "@type": "Offer",
                        "price": f"{o.price:.2f}",
                        "priceCurrency": o.currency,
                        "url": o.url,
                        "availability": "https://schema.org/InStock",
                    },
                },
            }
            for i, o in enumerate(offers, 1)
        ]
        jsonld = json.dumps(
            {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": items},
            ensure_ascii=False,
        )

        updated = datetime.now().strftime("%Y-%m-%d %H:%M")
        html_out = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EcoOfertas - Gangas y ofertas actualizadas</title>
    <meta name="description" content="Ofertas reales actualizadas cada 6 horas. Descubre las mejores gangas en libros, tecnologia y mas.">
    <meta property="og:title" content="EcoOfertas - Gangas del dia">
    <meta property="og:description" content="Ofertas reales actualizadas automaticamente cada 6 horas.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{self.site_url}/">
    <link rel="canonical" href="{self.site_url}/">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">{jsonld}</script>
    <style>
        .product-card:hover {{ transform: translateY(-5px); transition: all 0.3s ease; }}
    </style>
</head>
<body class="bg-gray-100 min-h-screen font-sans">
    <header class="bg-white shadow-sm py-8 mb-8 text-center">
        <h1 class="text-4xl font-extrabold text-gray-800 mb-2">EcoOfertas</h1>
        <p class="text-gray-500">Actualizado: {updated}</p>
    </header>
    <main class="container mx-auto px-4">
        <div class="flex flex-wrap justify-center gap-2 mb-8">
            <button onclick="filterCategory('all')" class="px-4 py-2 rounded-full bg-orange-500 text-white font-bold hover:bg-orange-600 transition">Todas</button>
            {filters_html}
        </div>
        <div id="offers-grid" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {cards_html}
        </div>
    </main>
    <footer class="text-center text-gray-400 text-sm py-8">
        <p>Contiene enlaces de afiliado. Podemos recibir una comision por tus compras.</p>
    </footer>
    <script>
        function filterCategory(cat) {{
            document.querySelectorAll('.product-card').forEach(card => {{
                card.style.display = (cat === 'all' || card.dataset.category === cat) ? 'block' : 'none';
            }});
        }}
    </script>
</body>
</html>
"""
        try:
            with open(self.output_file, "w", encoding="utf-8") as f:
                f.write(html_out)
            logger.info(f"Web generated: {self.output_file}")
        except IOError as e:
            logger.error(f"Failed to write HTML: {e}")
            return

        self._write_sitemap()
        self._write_robots()

    def _generate_card(self, o: Oferta) -> str:
        image = o.image_url or "https://via.placeholder.com/300x300?text=No+Image"
        return f"""
        <div class="product-card bg-white rounded-2xl shadow-md overflow-hidden border border-gray-200" data-category="{escape(o.category)}">
            <div class="h-48 overflow-hidden">
                <img src="{escape(image)}" alt="{escape(o.title)}" loading="lazy" class="w-full h-full object-cover">
            </div>
            <div class="p-4 flex flex-col">
                <span class="text-xs font-bold text-orange-600 uppercase mb-1">{escape(o.store)} | {escape(o.category)}</span>
                <h3 class="text-lg font-semibold text-gray-800 line-clamp-2 mb-4 h-14">{escape(o.title)}</h3>
                <div class="mt-auto flex items-center justify-between">
                    <span class="text-2xl font-bold text-green-600">${o.price:.2f}</span>
                    <a href="{escape(o.url)}" rel="nofollow sponsored noopener" target="_blank" class="bg-orange-500 text-white px-4 py-2 rounded-lg font-bold hover:bg-orange-600 transition shadow-sm">Ver Oferta</a>
                </div>
            </div>
        </div>
        """

    def _write_sitemap(self):
        now = datetime.now().strftime("%Y-%m-%d")
        sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>{self.site_url}/</loc>
        <lastmod>{now}</lastmod>
        <changefreq>hourly</changefreq>
        <priority>1.0</priority>
    </url>
</urlset>
"""
        with open("sitemap.xml", "w", encoding="utf-8") as f:
            f.write(sitemap)

    def _write_robots(self):
        robots = f"""User-agent: *
Allow: /
Sitemap: {self.site_url}/sitemap.xml
"""
        with open("robots.txt", "w", encoding="utf-8") as f:
            f.write(robots)