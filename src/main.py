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
    # Aquí agregaremos los nuevos cursos que elijas
    hotmart_products = [
        {
            "title": "Curso Completo: Trading de Forex y Análisis Técnico",
            "price": 126000.0,
            "url": "https://go.hotmart.com/P108258779B",
            "category": "Finanzas",
            "store": "Hotmart",
            "image_url": "https://i.ytimg.com/vi/8Xy2Gj4Gq6E/maxresdefault.jpg"
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