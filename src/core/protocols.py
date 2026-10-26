from typing import Protocol, List
from .models import Oferta, StoreConfig

class Scraper(Protocol):
    """
    Protocol that all store scrapers must implement.
    """
    def scrape(self, config: StoreConfig) -> List[Oferta]:
        """
        Scrape the store and return a list of Oferta objects.
        """
        ...

class AffiliateHandler(Protocol):
    """
    Protocol that all affiliate link providers must implement.
    """
    def apply_affiliate_link(self, url: str) -> str:
        """
        Transform a standard product URL into an affiliate URL.
        """
        ...
