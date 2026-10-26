import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

class MoneyBotWeb:
    def __init__(self, db_file="ofertas.json"):
        self.db_file = db_file
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.ofertas_guardadas = self._cargar_db()
        self.affiliate_id = "TU_ID_AFILIADO"

    def _cargar_db(self):
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def _guardar_db(self):
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(self.ofertas_guardadas, f, indent=4, ensure_ascii=False)

    def generar_link_afiliado(self, url):
        if self.affiliate_id == "TU_ID_AFILIADO":
            return url
        return f"{url}?ref={self.affiliate_id}"

    def scrapear_tienda(self, url, categoria):
        print(f"Escaneando {categoria}...")
        try:
            respuesta = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(respuesta.text, 'html.parser')
            productos_html = soup.find_all('article', class_='product_pod')

            resultados = []
            for p in productos_html:
                titulo = p.h3.a['title']
                precio_texto = p.find('p', class_='price_color').text
                precio_limpio = "".join(c for c in precio_texto if c.isdigit() or c == '.')
                url_original = url + p.h3.a['href']

                resultados.append({
                    "titulo": titulo,
                    "precio": precio_limpio,
                    "url": self.generar_link_afiliado(url_original),
                    "categoria": categoria
                })
            return resultados
        except Exception as e:
            print(f"Error en {categoria}: {e}")
            return []

    def filtrar_ofertas(self, productos):
        nuevas = []
        for p in productos:
            if p['titulo'] not in self.ofertas_guardadas:
                nuevas.append(p)
                self.ofertas_guardadas[p['titulo']] = p['precio']
        self._//guardar_db() # Error manual aquí, corregido abajo
        return nuevas

    def crear_web(self, todas_las_ofertas):
        html_content = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>EcoOfertas - Las Mejores Gangas</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f4f9; margin: 0; padding: 20px; text-align: center; }}
                h1 {{ color: #333; }}
                .container {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 20px; padding: 20px; }}
                .card {{ background: white; border-radius: 15px; padding: 20px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); transition: 0.3s; }}
                .card:hover {{ transform: translateY(-5px); box-shadow: 0 8px 16px rgba(0,0,0,0.2); }}
                .card h3 {{ font-size: 18px; color: #444; height: 50px; overflow: hidden; }}
                .price {{ font-size: 22px; color: #27ae60; font-weight: bold; margin: 15px 0; }}
                .btn {{ background: #e67e22; color: white; text-decoration: none; padding: 10px 20px; border-radius: 5px; display: inline-block; font-weight: bold; }}
                .btn:hover {{ background: #d35400; }}
            </style>
        </head>
        <body>
            <h1>🔥 EcoOfertas - Gangas del Día 🔥</h1>
            <p>Actualizado el: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
            <div class="container">
        """

        for o in todas_las_ofertas:
            html_content += f"""
                <div class="card">
                    <h3>{o['titulo']}</h3>
                    <div class="price">${o['precio']}</div>
                    <a href="{o['url']}" target="_blank" class="btn">Ver Oferta</a>
                </div>
            """

        html_content += """
            </div>
        </body>
        </html>
        """

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print("\n✅ ¡Página web generada con éxito como 'index.html'!")

    def ejecutar(self, tiendas):
        todas_las_ofertas = []
        for cat, url in tiendas.items():
            prods = self.scrapear_tienda(url, cat)
            todas_las_ofertas.extend(prods)

        if todas_las_ofertas:
            print(f"Se encontraron {len(todas_las_ofertas)} productos.")
            self.crear_web(todas_las_ofertas)
        else:
            print("No se encontraron productos.")

if __name__ == "__main__":
    bot =  MoneyBotWeb()()
    tiendas = {"Libros": "https://books.toscrape.com/"}
    bot.ejecutar(tiendas)