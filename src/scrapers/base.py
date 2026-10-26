import requests
from bs4 import BeautifulSoup
from typing import List, Optional
from src.core.models import Oferta, StoreConfig
from src.core.logger import logger

class BaseScraper:
    """
    Provides common utilities for all scrapers.
    """
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def get_soup(self, url: str) -> Optional[BeautifulSoup]:
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            logger.error(f"Request failed for {url}: {e}")
            return None

    def clean_price(self, price_text: str) -> float:
        """
        Extracts numeric value from price strings (e.g., '$12.99' -> 12.99).
        """
        cleaned = "".join(c for c in price_text if c.isdigit() or c == '.')
        try:
            return float(cleaned) if cleaned else 0.0
        except ValueError:
            logger.warning(f"Could not parse price text: {price_text}")
            return 0.0
