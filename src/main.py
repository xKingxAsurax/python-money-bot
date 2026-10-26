import os
from typing import List
from src.core.logger import logger
from src.core.models import Oferta, StoreConfig
from src.core.storage import StorageManager
from src.scrapers.generic import GenericScraper
from src.affiliates.providers import AffiliateService
from src.web.generator import WebGenerator

def main():
    logger.info("🚀 Starting EcoOfertasBot Orchestrator...")

    # 1. Configuration
    # In a real scenario, this could be loaded from a config.json file
    stores_to_scan = [
        StoreConfig(
            name="BooksToScrape",
            base_url="https://books.toscrape.com/",
            product_selector="article.product_pod",
            title_selector="h3 a",
            price_selector=".price_color",
            image_selector="img"
        ),
        # Add more stores here as needed
    ]

    # 2. Initialize Components
    storage = StorageManager()
    scraper = GenericScraper()
    affiliate_service = AffiliateService()
    web_gen = WebGenerator()

    all_new_offers: List[Oferta] = []

    # 3. Execution Loop
    for config in stores_to_scan:
        try:
            # Step A: Scrape products
            raw_offers = scraper.scrape(config)

            # Step B: Filter new ones and apply affiliate links
            for offer in raw_offers:
                if storage.is_new(offer):
                    # Transform URL to affiliate link
                    affiliate_url = affiliate_service.transform(offer.url, config.name)

                    # Create a new Oferta object with the affiliate link
                    final_offer = Oferta(
                        title=offer.title,
                        price=offer.price,
                        url=affiliate_url,
                        category="General", # Can be customized per store
                        store=config.name,
                        image_url=offer.image_url
                    )

                    all_new_offers.append(final_offer)
                    storage.mark_as_seen(final_offer)

        except Exception as e:
            logger.error(f"Critical error processing {config.name}: {e}")

    # 4. Finalization
    if all_new_offers:
        logger.info(f"Found {len(all_new_offers)} new offers! Updating website...")
        # We pass all offers from the DB to the web generator to keep the site full
        # For this version, we'll just use the new ones or reload all from DB
        db_data = storage.load_db()
        all_offers_for_web = [
            Oferta(
                title=title,
                price=val["price"],
                url="#", # In a full version, we'd store the affiliate URL in the DB too
                category="General",
                store="Various"
            )
            for title, val in db_data.items()
        ]
        # Add the newly found ones
        all_offers_for_web.extend(all_new_offers)

        web_gen.generate(all_offers_for_web)
        logger.info("✨ Cycle completed successfully.")
    else:
        logger.info("No new offers found in this cycle.")

if __name__ == "__main__":
    main()
