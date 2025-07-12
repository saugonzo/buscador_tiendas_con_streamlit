from bs4 import BeautifulSoup
import requests

def buscar_elduende(query):
    url_busqueda = f"https://www.elduende.com.mx/?s={query}&post_type=product"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url_busqueda, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    resultados = []
    productos = soup.select("li.product")

    for producto in productos:
        nombre_elem = producto.select_one("h2.woocommerce-loop-product__title")
        precio_elem = producto.select_one("span.woocommerce-Price-amount")
        link_elem = producto.select_one("a.woocommerce-LoopProduct-link")
        imagen_elem = producto.select_one("img")

        if not nombre_elem or not precio_elem or not link_elem:
            continue

        nombre = nombre_elem.text.strip()
        precio = precio_elem.text.strip()
        url = link_elem["href"]
        imagen = imagen_elem["src"] if imagen_elem else ""

        # Verificar si está agotado
        detalle_html = requests.get(url, headers=headers).text
        detalle_soup = BeautifulSoup(detalle_html, "html.parser")
        agotado = detalle_soup.select_one(".single_add_to_cart_button.button.alt.disabled") or "Avísame" in detalle_html

        resultados.append({
            "nombre": nombre,
            "precio": precio,
            "url": url,
            "imagen": imagen,
            "disponible": not agotado
        })

    return resultados
