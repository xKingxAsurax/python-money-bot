from src.core.models import Oferta
from src.core.storage import StorageManager
from src.affiliates.providers import AffiliateService


def test_oferta_creation():
    o = Oferta(title="Test", price=9.99, url="https://x.com", category="Test", store="T")
    assert o.title == "Test"
    assert o.price == 9.99
    assert o.currency == "USD"


def test_storage_dedup(tmp_path):
    db = tmp_path / "db.json"
    s = StorageManager(db_path=str(db))
    o = Oferta(title="A", price=1.0, url="https://x.com/a", category="C", store="S")
    assert s.is_new(o) is True
    s.mark_as_seen(o)
    assert s.is_new(o) is False


def test_affiliate_amazon(monkeypatch):
    monkeypatch.setenv("AMAZON_ID", "mytag-20")
    svc = AffiliateService()
    url = svc.transform("https://amazon.com/product?x=1", "amazon")
    assert "tag=mytag-20" in url


def test_affiliate_generic():
    svc = AffiliateService()
    url = svc.transform("https://tienda.com/p", "otra")
    assert "ref=" in url