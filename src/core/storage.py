import json
import os
from datetime import datetime
from typing import List, Dict, Any
from src.core.models import Oferta
from src.core.logger import logger


class StorageManager:
    """Persistencia de ofertas con deduplicacion por URL."""

    def __init__(self, db_path: str = "data/ofertas.json"):
        self.db_path = db_path
        self._ensure_db_exists()

    def _ensure_db_exists(self):
        if not os.path.exists(self.db_path):
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            self.save_db({})

    def load_db(self) -> Dict[str, Any]:
        try:
            with open(self.db_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Error loading DB: {e}")
            return {}

    def save_db(self, data: Dict[str, Any]):
        try:
            with open(self.db_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            logger.error(f"Error saving DB: {e}")

    def is_new(self, oferta: Oferta) -> bool:
        return oferta.url not in self.load_db()

    def mark_as_seen(self, oferta: Oferta):
        db = self.load_db()
        existing = db.get(oferta.url, {})
        db[oferta.url] = {
            "title": oferta.title,
            "price": oferta.price,
            "url": oferta.url,
            "category": oferta.category,
            "store": oferta.store,
            "image_url": oferta.image_url,
            "currency": oferta.currency,
            "first_seen": existing.get("first_seen", datetime.now().isoformat()),
            "last_seen": datetime.now().isoformat(),
            "prev_price": existing.get("price"),
        }
        self.save_db(db)

    def get_all_offers(self) -> List[Oferta]:
        return [
            Oferta(
                title=v["title"],
                price=float(v["price"]),
                url=v["url"],
                category=v.get("category", "General"),
                store=v.get("store", "Various"),
                image_url=v.get("image_url"),
                currency=v.get("currency", "USD"),
            )
            for v in self.load_db().values()
        ]