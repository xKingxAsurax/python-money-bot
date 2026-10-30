import os
import time
import requests
from typing import List, Optional
from src.core.models import Oferta
from src.core.logger import logger
from dotenv import load_dotenv

load_dotenv()


class MercadoLibreScraper:
    """Scraper de MercadoLibre via API oficial con autenticacion OAuth."""

    SITE_IDS = {
        "co": "MCO",
        "ar": "MLA",
        "mx": "MLM",
        "cl": "MLC",
        "pe": "MPE",
        "uy": "MLU",
    }

    def __init__(self, country: str = "co"):
        self.site_id = self.SITE_IDS.get(country.lower(), "MCO")
        self.base_url = "https://api.mercadolibre.com"
        self.client_id = os.getenv("MELI_CLIENT_ID", "")
        self.client_secret = os.getenv("MELI_CLIENT_SECRET", "")
        self.access_token: Optional[str] = None
        self.token_expires_at: float = 0

    def _get_token(self) -> Optional[str]:
        """Obtiene un token OAuth usando client_credentials."""
        if self.access_token and time.time() < self.token_expires_at - 60:
            return self.access_token

        if not self.client_id or not self.client_secret:
            logger.error("Faltan MELI_CLIENT_ID o MELI_CLIENT_SECRET en .env")
            return None

        url = f"{self.base_url}/oauth/token"
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        headers = {"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}

        try:
            r = requests.post(url, data=payload, headers=headers, timeout=20)
            r.raise_for_status()
            data = r.json()
            self.access_token = data["access_token"]
            self.token_expires_at = time.time() + data.get("expires_in", 21600)
            logger.info("Token OAuth obtenido correctamente.")
            return self.access_token
        except requests.RequestException as e:
            logger.error(f"Error obteniendo token OAuth: {e}")
            if hasattr(e, "response") and e.response is not None:
                logger.error(f"Respuesta: {e.response.text}")
            return None

    def search(self, query: str, limit: int = 20) -> List[Oferta]:
        token = self._get_token()
        if not token:
            return []

        url = f"{self.base_url}/sites/{self.site_id}/search"
        params = {"q": query, "limit": limit}
        headers = {"Authorization": f"Bearer {token}"}

        try:
            response = requests.get(url, params=params, headers=headers, timeout=20)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            logger.error(f"MercadoLibre search failed for '{query}': {e}")
            if hasattr(e, "response") and e.response is not None:
                logger.error(f"Respuesta: {e.response.text}")
            return []

        results = data.get("results", [])
        offers = []

        for item in results:
            try:
                price = float(item.get("price", 0))
                if price <= 0:
                    continue

                image = item.get("secure_thumbnail") or item.get("thumbnail", "")
                if image.startswith("http://"):
                    image = image.replace("http://", "https://", 1)

                offers.append(Oferta(
                    title=item.get("title", "Sin titulo"),
                    price=price,
                    url=item.get("permalink", ""),
                    category=query.title(),
                    store="MercadoLibre",
                    image_url=image,
                    currency="COP",
                ))
            except (KeyError, ValueError, TypeError) as e:
                logger.warning(f"Error parsing ML item: {e}")
                continue

        logger.info(f"MercadoLibre '{query}': {len(offers)} ofertas")
        return offers