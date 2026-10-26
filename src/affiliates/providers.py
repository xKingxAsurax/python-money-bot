import os
from typing import Protocol
from dotenv import load_dotenv
from src.core.logger import logger

load_dotenv()

class AffiliateHandler(Protocol):
    def apply_affiliate_link(self, url: str) -> str:
        ...

class AmazonAffiliateHandler:
    def __init__(self):
        self.tag = os.getenv("AMAZON_ID", "default_tag")

    def apply_affiliate_link(self, url: str) -> str:
        if "amazon" in url.lower():
            separator = "&" if "?" in url else "?"
            return f"{url}{separator}tag={self.tag}"
        return url

class AliExpressAffiliateHandler:
    def __init__(self):
        self.tag = os.getenv("ALIEXPRESS_ID", "default_tag")

    def apply_affiliate_link(self, url: str) -> str:
        if "aliexpress" in url.lower():
            separator = "&" if "?" in url else "?"
            return f"{url}{separator}aff_id={self.tag}"
        return url

class GenericAffiliateHandler:
    def __init__(self):
        self.tag = os.getenv("GENERIC_ID", "default_tag")

    def apply_affiliate_link(self, url: str) -> str:
        separator = "&" if "?" in url else "?"
        return f"{url}{separator}ref={self.tag}"

class AffiliateService:
    """
    Orchestrates affiliate link transformation based on the store.
    """
    def __init__(self):
        self.handlers = {
            "amazon": AmazonAffiliateHandler(),
            "aliexpress": AliExpressAffiliateHandler(),
            "generic": GenericAffiliateHandler()
        }

    def transform(self, url: str, store_name: str) -> str:
        store_key = store_name.lower()
        handler = self.handlers.get(store_key, self.handlers["generic"])
        return handler.apply_affiliate_link(url)
