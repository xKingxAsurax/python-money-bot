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
        self.tag = os.getenv("AMAZON_ID", "")

    def apply_affiliate_link(self, url: str) -> str:
        if not self.tag:
            return url
        if "amazon" in url.lower():
            sep = "&" if "?" in url else "?"
            return f"{url}{sep}tag={self.tag}"
        return url


class AliExpressAffiliateHandler:
    def __init__(self):
        self.tag = os.getenv("ALIEXPRESS_ID", "")

    def apply_affiliate_link(self, url: str) -> str:
        if not self.tag:
            return url
        if "aliexpress" in url.lower():
            sep = "&" if "?" in url else "?"
            return f"{url}{sep}aff_id={self.tag}"
        return url


class MercadoLibreAffiliateHandler:
    def __init__(self):
        self.tag = os.getenv("MELI_ID", "")

    def apply_affiliate_link(self, url: str) -> str:
        if not self.tag:
            return url
        if "mercadolibre" in url.lower() or "mercadolivre" in url.lower():
            sep = "&" if "?" in url else "?"
            return f"{url}{sep}matt_tool={self.tag}"
        return url


class GenericAffiliateHandler:
    def __init__(self):
        self.tag = os.getenv("GENERIC_ID", "")

    def apply_affiliate_link(self, url: str) -> str:
        if not self.tag:
            return url
        sep = "&" if "?" in url else "?"
        return f"{url}{sep}ref={self.tag}"


class AffiliateService:
    def __init__(self):
        self.handlers = {
            "amazon": AmazonAffiliateHandler(),
            "aliexpress": AliExpressAffiliateHandler(),
            "mercadolibre": MercadoLibreAffiliateHandler(),
            "generic": GenericAffiliateHandler(),
        }

    def transform(self, url: str, store_name: str) -> str:
        store_key = store_name.lower().replace(" ", "")
        handler = self.handlers.get(store_key, self.handlers["generic"])
        return handler.apply_affiliate_link(url)