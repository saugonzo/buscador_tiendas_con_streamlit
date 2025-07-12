import requests
from bs4 import BeautifulSoup

def buscar_yegogames(nombre_juego):
    url = f"https://yegogames.com/search?q={nombre_juego.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    productos = soup.select("li.grid__item")

    for producto in productos:
        nombre = producto.select_one("div.card__content a").text.strip().lower()
        if nombre_juego.lower() in nombre:
            disponibilidad = producto.teimport requests
from bs4 import BeautifulSoup

def buscar_yegogames(juego):
    url_busqueda = f"https://yegogames.com/search?q={juego}&options%5Bprefix%5D=last"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url_busqueda, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        return [f"❌ Error: {str(e)}"]

    soup = BeautifulSoup(response.text, "html.parser")
    productos_html = soup.select(".product-item")

    resultados = []
    for producto in productos_html:
        nombre_tag = producto.select_one(".product-item__title")
        precio_tag = producto.select_one(".price-item.price-item--regular")
        imagen_tag = producto.select_one(".motion-reduce img")
        link_tag = producto.select_one("a.full-unstyled-link")
        boton_agregar = producto.select_one("button[name='add']")

        nombre = nombre_tag.text.strip() if nombre_tag else "Sin nombre"
        precio = precio_tag.text.strip() if precio_tag else "Sin precio"
        imagen = imagen_tag["src"] if imagen_tag and imagen_tag.has_attr("src") else ""
        enlace = "https://yegogames.com" + link_tag["href"] if link_tag and link_tag.has_attr("href") else "#"
        disponible = boton_agregar is not None

        resultados.append({
            "nombre": nombre,
            "precio": precio,
            "url": enlace,
            "imagen": imagen,
            "disponible": disponible
        })

    return resultados
xt.lower()
            if "agotado" not in disponibilidad:
                link = "https://yegogames.com" + producto.select_one("div.card__content a")["href"]
                precio = producto.select_one(".price").text.strip().replace("\n", " ")
                imagen = producto.select_one("img")["src"]
                if imagen.startswith("//"):
                    imagen = "https:" + imagen
                return {
                    "nombre": nombre,
                    "precio": precio,
                    "url": link,
                    "imagen": imagen
                }

    return None
