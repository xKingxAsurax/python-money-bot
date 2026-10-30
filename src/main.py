from src.core.logger import logger
from src.core.models import Oferta
from src.core.storage import StorageManager
from src.web.generator import WebGenerator
from src.config import SITE_URL

def main():
    logger.info("Starting EcoOfertasBot...")
    storage = StorageManager()
    web_gen = WebGenerator(site_url=SITE_URL)

    # === LISTA DE PRODUCTOS DE HOTMART ===
    hotmart_products = [
        {
            "title": "Curso Completo: Trading de Forex y Análisis Técnico",
            "price": 126000.0,
            "url": "https://go.hotmart.com/P108258779B",
            "category": "Finanzas",
            "store": "Hotmart",
            "image_url": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&w=500&q=80"
        },
        {
            "title": "MME VIP 2026 - Money Mastery Event",
            "price": 1197000.0,
            "url": "https://go.hotmart.com/H108258991W",
            "category": "Finanzas",
            "store": "Hotmart",
            "image_url": "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?auto=format&fit=crop&w=500&q=80"
        },
        {
            "title": "Criptomonedas: Domina el Futuro del Dinero",
            "price": 840000.0,
            "url": "https://go.hotmart.com/F108259033U",
            "category": "Finanzas",
            "store": "Hotmart",
            "image_url": "https://images.unsplash.com/photo-1621761191319-c6fb62004040?auto=format&fit=crop&w=500&q=80"
        },
        {
            "title": "Curso Intensivo: Invirtiendo Desde Cero",
            "price": 599000.0,
            "url": "https://go.hotmart.com/W108259053J",
            "category": "Finanzas",
            "store": "Hotmart",
            "image_url": "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?auto=format&fit=crop&w=500&q=80"
        },
        {
            "title": "Libertad Financiera con PNL - Nivel Avanzado",
            "price": 425000.0,
            "url": "https://go.hotmart.com/B108259067M",
            "category": "Finanzas",
            "store": "Hotmart",
            "image_url": "https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?auto=format&fit=crop&w=500&q=80"
        }
    ]

    new_count = 0
    for p in hotmart_products:
        offer = Oferta(
            title=p["title"],
            price=p["price"],
            url=p["url"],
            category=p["category"],
            store=p["store"],
            image_url=p["image_url"],
            currency="COP"
        )
        if storage.is_new(offer):
            storage.mark_as_seen(offer)
            new_count += 1
            logger.info(f"Hotmart offer injected: {offer.title}")

    all_offers = storage.get_all_offers()
    logger.info(f"Total en DB: {len(all_offers)} | Nuevas este run: {new_count}")

    if all_offers:
        web_gen.generate(all_offers)
    else:
        logger.warning("No hay ofertas en DB.")

if __name__ == "__main__":
    main()