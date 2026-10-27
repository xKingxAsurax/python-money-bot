"""Configuracion central del bot. Edita aqui las tiendas y la URL del sitio."""
from src.core.models import StoreConfig

# URL publica del sitio (GitHub Pages). Cambiala cuando sepas la tuya.
SITE_URL = "https://TU-USUARIO.github.io/python-money-bot"

# Sitio de practica. Reemplazar por tiendas reales con afiliados.
STORES = [
    StoreConfig(
        name="BooksToScrape",
        base_url="https://books.toscrape.com/",
        product_selector="article.product_pod",
        title_selector="h3 a",
        price_selector=".price_color",
        image_selector="img",
    ),
    # Ejemplo AliExpress (descomenta cuando tengas tu ID aprobado):
    # StoreConfig(
    #     name="AliExpress",
    #     base_url="https://es.aliexpress.com/category/...",
    #     product_selector=".multi--product-card--...",
    #     title_selector=".multi--title--...",
    #     price_selector=".multi--price--...",
    #     image_selector="img",
    # ),
]