from src.core.logger import logger
from src.core.models import Oferta
from src.core.storage import StorageManager
from src.scrapers.generic import GenericScraper
from src.affiliates.providers import AffiliateService
from src.web.generator import WebGenerator
from src.config import STORES, SITE_URL


def main():
    logger.info("Starting EcoOfertasBot...")

    storage = StorageManager()
    scraper = GenericScraper()
    affiliate_service = AffiliateService()
    web_gen = WebGenerator(site_url=SITE_URL)

    new_count = 0

    for config in STORES:
        try:
            raw_offers = scraper.scrape(config)
            for offer in raw_offers:
                if storage.is_new(offer):
                    affiliate_url = affiliate_service.transform(offer.url, config.name)
                    final_offer = Oferta(
                        title=offer.title,
                        price=offer.price,
                        url=affiliate_url,
                        category=offer.category,
                        store=config.name,
                        image_url=offer.image_url,
                        currency=offer.currency,
                    )
                    storage.mark_as_seen(final_offer)
                    new_count += 1
        except Exception as e:
            logger.error(f"Error processing {config.name}: {e}")

    all_offers = storage.get_all_offers()
    logger.info(f"Total in DB: {len(all_offers)} | New this run: {new_count}")

    if all_offers:
        web_gen.generate(all_offers)
    else:
        logger.warning("No offers in DB, skipping web generation.")


if __name__ == "__main__":
    main()