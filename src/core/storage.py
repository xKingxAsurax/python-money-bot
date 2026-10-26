import json
import os
from typing import List, Dict, Any
from src.core.models import Oferta
from src.core.logger import logger

class StorageManager:
    """
    Handles persistence of seen offers to prevent duplicates.
    """
    def __init__(self, db_path: str = "data/ofertas.json"):
        self.db_path = db_path
        self._ensure_db_exists()

    def _ensure_db_exists(self):
        if not os.path.exists(self.db_path):
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            self.save_db({})

    def load_db(self) -> Dict[str, Any]:
        try:
            with open(self.db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Error loading database {self.db_path}: {e}")
            return {}

    def save_db(self, data: Dict[str, Any]):
        try:
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except IOError as e:
            logger.error(f"Error saving database {self.db_path}: {e}")

    def is_new(self, oferta: Oferta) -> bool:
        db = self.load_db()
        return oferta.title not in db

    def mark_as_seen(self, oferta: Oferta):
        db = self.load_db()
        db[oferta.title] = {
            "price": oferta.price,
            "last_seen": None # Could be extended with timestamps
        }
        self.save_db(db)
