from datetime import datetime
from typing import List
from src.core.models import Oferta
from src.core.logger import logger

class WebGenerator:
    """
    Generates a modern, responsive HTML gallery of offers.
    """
    def __init__(self, output_file: str = "index.html"):
        self.output_file = output_file

    def generate(self, offers: List[Oferta]):
        logger.info(f"Generating web page with {len(offers)} offers...")

        # Extract unique categories for the filter bar
        categories = sorted(list(set(o.category for o in offers)))

        html_content = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>EcoOfertas - Gangas del Día</title>
            <script src="https://cdn.tailwindcss.com"></script>
            <style>
                .product-card:hover {{ transform: translateY(-5px); transition: all 0.3s ease; }}
            </style>
        </head>
        <body class="bg-gray-100 min-h-screen font-sans">
            <header class="bg-white shadow-sm py-8 mb-8 text-center">
                <h1 class="text-4xl font-extrabold text-gray-800 mb-2">🔥 EcoOfertas 🔥</h1>
                <p class="text-gray-500">Actualizado el: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
            </header>

            <main class="container mx-auto px-4">
                <!-- Category Filter -->
                <div class="flex flex-wrap justify-center gap-2 mb-8">
                    <button onclick="filterCategory('all')" class="px-4 py-2 rounded-full bg-orange-500 text-white font-bold hover:bg-orange-600 transition">Todas</button>
                    {"".join([f'<button onclick="filterCategory(\'{cat}\')" class="px-4 py-2 rounded-full bg-white text-gray-700 font-medium border hover:bg-gray-50 transition">{cat}</button>' for cat in categories])}
                </div>

                <!-- Offers Grid -->
                <div id="offers-grid" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                    {"".join([self._generate_card(o) for o in offers])}
                </div>
            </main>

            <script>
                function filterCategory(cat) {{
                    const cards = document.querySelectorAll('.product-card');
                    cards.forEach(card => {{
                        if (cat === 'all' || card.dataset.category === cat) {{
                            card.style.display = 'block';
                        }} else {{
                            card.style.display = 'none';
                        }}
                    }});
                }}
            </script>
        </body>
        </html>
        """

        try:
            with open(self.output_file, "w", encoding="utf-8") as f:
                f.write(html_content)
            logger.info(f"✅ Web page generated successfully: {self.output_file}")
        except IOError as e:
            logger.error(f"Failed to write HTML file: {e}")

    def _generate_card(self, o: Oferta) -> str:
        # Fallback image if none found
        image = o.image_url if o.image_url else "https://via.placeholder.com/300x300?text=No+Image"

        return f"""
        <div class="product-card bg-white rounded-2xl shadow-md overflow-hidden border border-gray-200" data-category="{o.category}">
            <div class="h-48 overflow-hidden">
                <img src="{image}" alt="{o.title}" class="w-full h-full object-cover">
            </div>
            <div class="p-4 flex flex-col">
                <span class="text-xs font-bold text-orange-600 uppercase mb-1">{o.store} | {o.category}</span>
                <h3 class="text-lg font-semibold text-gray-800 line-clamp-2 mb-4 h-14">{o.title}</h3>
                <div class="mt-auto flex items-center justify-between">
                    <span class="text-2xl font-bold text-green-600">${o.price:.2f}</span>
                    <a href="{o.url}" target="_blank" class="bg-orange-500 text-white px-4 py-2 rounded-lg font-bold hover:bg-orange-600 transition shadow-sm">Ver Oferta</a>
                </div>
            </div>
        </div>
        """
