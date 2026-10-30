from src.core.logger import logger
from src.core.models import Oferta
from src.core.storage import StorageManager
from src.scrapers.generic import GenericScraper
from src.scrapers.mercadolibre import MercadoLibreScraper
from src.affiliates.providers import AffiliateService
from src.web.generator import WebGenerator
from src.config import STORES, SITE_URL, MERCADOLIBRE_QUERIES

def main():
    logger.info("Starting EcoOfertasBot...")

    storage = StorageManager()
    affiliate_service = AffiliateService()
    web_gen = WebGenerator(site_url=SITE_URL)

    new_count = 0

    # === 1. Scraping HTML (BooksToScrape) ===
    if STORES:
        scraper = GenericScraper()
        for config in STORES:
            try:
                raw = scraper.scrape(config)
                for offer in raw:
                    if storage.is_new(offer):
                        affiliate_url = affiliate_service.transform(offer.url, config.name)
                        final = Oferta(title=offer.title, price=offer.price, url=affiliate_url, category=offer.category, store=offer.store, image_url=offer.image_url, currency=offer.currency)
                        storage.mark_as_seen(final)
                        new_count += 1
            except Exception as e:
                logger.error(f"Error processing {config.name}: {e}")

    # === 2. MercadoLibre (Desactivado temporalmente) ===
    # if MERCADOLIBRE_QUERIES:
    #     ml = MercadoLibreScraper(country="co")
    #     for query in MERCADOLIBRE_QUERIES:
    #         try:
    #             raw = ml.search(query, limit=20)
    #             for offer in raw:
    #                 if storage.is_new(offer):
    #                     affiliate_url = affiliate_service.transform(offer.url, "MercadoLibre")
    #                     final = Oferta(title=offer.title, price=offer.price, url=affiliate_url, category=offer.category, store=offer.store, image_url=offer.image_url, currency=offer.currency)
    #                     storage.mark_as_seen(final)
    #                     new_count += 1
    #         except Exception as e:
    #             logger.error(f"Error ML '{query}': {e}")

    # === 3. INYECCIÓN MANUAL DE HOTMART ===
    # Aquí metemos tu producto de Hotmart directamente en la base de datos
    hotmart_offer = Oferta(
        title="Curso Completo: Trading de Forex y Análisis Técnico",
        price=126000.0, 
        url="https://go.hotmart.com/P108258779B", # Tu enlace de afiliado real
        category="Finanzas",
        store="Hotmart",
        image_url="https://i.ytimg.com/vi/8Xy2Gj4Gq6E/maxresdefault.jpg", # Una imagen genérica de trading
        currency="COP"
    )
    
    # Lo guardamos en la base de datos si no existe
    if storage.is_new(hotmart_offer):
        storage.mark_as_seen(hotmart_offer)
        new_count += 1
        logger.info("Hotmart offer injected successfully!")

    all_offers = storage.get_all_offers()
    logger.info(f"Total en DB: {len(all_offers)} | Nuevas este run: {new_count}")

    if all_offers:
        web_gen.generate(all_offers)
    else:
        logger.warning("No hay ofertas en DB, no se genera web.")

if __name__ == "__main__":
    main()