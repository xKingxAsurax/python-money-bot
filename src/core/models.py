from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Oferta:
    """
    Represents a product offer found by the scraper.
    """
    title: str
    price: float
    url: str
    category: str
    store: str
    image_url: Optional[str] = None
    currency: str = "USD"

@dataclass(frozen=True)
class StoreConfig:
    """
    Configuration for a specific store scraper.
    """
    name: str
    base_url: str
    product_selector: str
    title_selector: str
    price_selector: str
    image_selector: Optional[str] = None
