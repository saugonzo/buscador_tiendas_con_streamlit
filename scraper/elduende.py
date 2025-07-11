import requests
from bs4 import BeautifulSoup

def buscar_elduende(nombre_juego):
    try:
        url = f"https://www.elduende.com.mx/?s={nombre_juego}&post_type=product"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        for producto in soup.select('li.product'):
            titulo_elem = producto.select_one('h2.woocommerce-loop-product__title')
            if not titulo_elem or nombre_juego.lower() not in titulo_elem.text.lower():
                continue

            # Verifica si está agotado
            stock_elem = producto.select_one('.out-of-stock')
            if stock_elem:
                continue  # Saltar si está agotado

            url_elem = producto.select_one('a.woocommerce-LoopProduct-link')
            precio_elem = producto.select_one('span.price')
            imagen_elem = producto.select_one('img')

            if not url_elem or not precio_elem:
                continue

            return {
                "titulo": titulo_elem.text.strip(),
                "precio": precio_elem.text.strip(),
                "url": url_elem['href'],
                "imagen": imagen_elem['src'] if imagen_elem else None,
            }

    except Exception as e:
        print("Error en el scraper de El Duende:", e)
        return None
