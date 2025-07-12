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

            url_elem = producto.select_one('a.woocommerce-LoopProduct-link')
            precio_elem = producto.select_one('span.price')
            imagen_elem = producto.select_one('img')

            if not url_elem or not precio_elem:
                continue

            # Verificar stock dentro de la página del producto
            producto_url = url_elem['href']
            detalle = requests.get(producto_url, headers=headers, timeout=10)
            detalle_soup = BeautifulSoup(detalle.text, "html.parser")
            agotado = detalle_soup.select_one('.stock.out-of-stock')  # Clase típica en WooCommerce

            if agotado:
                continue  # Producto agotado, lo ignoramos

            return {
                "titulo": titulo_elem.text.strip(),
                "precio": precio_elem.text.strip(),
                "url": producto_url,
                "imagen": imagen_elem['src'] if imagen_elem else None,
            }

    except Exception as e:
        print("Error en el scraper de El Duende:", e)
        return None
