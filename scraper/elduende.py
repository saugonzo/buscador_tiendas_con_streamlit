import requests
from bs4 import BeautifulSoup

def buscar_elduende(nombre_juego):
    resultados = []
    url = f"https://www.elduende.com.mx/?s={nombre_juego}&post_type=product&dgwt_wcas=1"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.select("ul.products li.product")

        for item in items:
            nombre_tag = item.select_one("h2.woocommerce-loop-product__title")
            enlace_tag = item.select_one("a.woocommerce-LoopProduct-link")
            precio_tag = item.select_one("span.woocommerce-Price-amount")
            img_tag = item.select_one("img")

            if not nombre_tag or not enlace_tag:
                continue

            nombre = nombre_tag.get_text(strip=True)
            enlace = enlace_tag["href"]
            precio = precio_tag.get_text(strip=True) if precio_tag else "N/A"
            imagen = img_tag["src"] if img_tag else None

            # Verificamos disponibilidad accediendo a la página del producto
            disponible = False
            try:
                producto_response = requests.get(enlace, headers=headers, timeout=10)
                producto_response.raise_for_status()
                producto_soup = BeautifulSoup(producto_response.text, "html.parser")
                add_to_cart = producto_soup.select_one("button.single_add_to_cart_button")
                disponible = add_to_cart is not None
            except:
                pass

            resultados.append({
                "nombre": nombre,
                "precio": precio,
                "url": enlace,
                "imagen": imagen,
                "disponible": disponible
            })

        return resultados

    except Exception as e:
        return [{
            "nombre": f"❌ Error: {str(e)}",
            "precio": "",
            "url": "",
            "imagen": None,
            "disponible": False
        }]
