from typing import List
from bs4 import BeautifulSoup
from src.core.models import Oferta, StoreConfig
from src.scrapers.base import BaseScraper
from src.core.logger import logger

class GenericScraper(BaseScraper):
    """
    A configuration-driven scraper that can work with any store
    that follows a simple HTML structure.
    """
    def scrape(self, config: StoreConfig) -> List[Oferta]:
        logger.info(f"Scanning store: {config.name} at {config.base_url}")
        soup = self.get_soup(config.base_url)

        if not soup:
            return []

        offers = []
        # Find all product containers based on the selector
        products = soup.select(config.product_selector)

        for p in products:
            try:
                # Extract title
                title_el = p.select_one(config.title_selector)
                title = title_el.get_text(strip=True) if title_el else "Unknown Product"

                # Extract price
                price_el = p.select_one(config.price_selector)
                price_text = price_el.get_text(strip=True) if price_el else "0"
                price = self.clean_price(price_text)

                # Extract URL (handle relative paths)
                link_el = p.select_one(config.title_selector if not config.image_selector else config.title_selector)
                # Default to title selector for URL if not specified
                url = link_el['href'] if link_el and link_el.has_attr('href') else ""
                if url and not url.startswith('http'):
                    # Simple relative URL resolution
                    url = config.base_url + url if config.base_url.endswith('/') else config.base_url + '/' + url

                # Extract Image
                image_url = None
                if config.image_selector:
                    img_el = p.select_one(config.image_selector)
                    if img_el and img_el.has_attr('src'):
                        image_url = img_el['src']
                        if image_url and not image_url.startswith('http'):
                            image_url = config.base_url + image_url if config.base_url.endswith('/') else config.base_url + '/' + image_url

                offers.append(Oferta(
                    title=title,
                    price=price,
                    url=url,
                    category="General", # Default, can be expanded
                    store=config.name,
                    image_url=image_url
                ))
            except Exception as e:
                logger.warning(f"Failed to parse a product in {config.name}: {e}")
                continue

        logger.info(f"Successfully extracted {len(offers)} offers from {config.name}")
        return offers
