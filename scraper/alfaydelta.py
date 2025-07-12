import requests
from bs4 import BeautifulSoup

def buscar_alfaydelta(juego):
    url_busqueda = f"https://www.alfaydelta.com.mx/search?q={juego}"
    response = requests.get(url_busqueda, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
import requests
from bs4 import BeautifulSoup

def buscar_alfaydelta(juego: str) -> list:
    url = f"https://alfaydelta.com/search?q={juego.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    productos = soup.select("li.grid__item")
    resultados = []

    for producto in productos:
        nombre_elem = producto.select_one(".card__heading a")
        precio_elem = producto.select_one(".price")
        imagen_elem = producto.select_one(".media.media--transparent img")
        disponibilidad_elem = producto.select_one(".badge--sold-out")

        if not nombre_elem or not precio_elem:
            continue

        nombre = nombre_elem.get_text(strip=True)
        link = "https://alfaydelta.com" + nombre_elem["href"]
        precio = precio_elem.get_text(strip=True)
        imagen = (
            "https:" + imagen_elem["src"]
            if imagen_elem and imagen_elem.get("src", "").startswith("//")
            else imagen_elem["src"] if imagen_elem else ""
        )
        disponible = disponibilidad_elem is None

        resultados.append({
            "nombre": nombre,
            "precio": precio,
            "url": link,
            "imagen": imagen,
            "disponible": disponible
        })

    return resultados

    resultados = []
    productos = soup.select(".productgrid--item")

    for producto in productos:
        nombre = producto.select_one(".productitem--title")
        precio = producto.select_one(".money")
        link_tag = producto.select_one("a")
        imagen_tag = producto.select_one("img")

        if not (nombre and precio and link_tag and imagen_tag):
            continue  # Saltar si falta algún dato importante

        url = "https://www.alfaydelta.com.mx" + link_tag["href"]
        nombre = nombre.text.strip()
        precio = precio.text.strip().replace("\n", "")
        imagen = "https:" + imagen_tag.get("src", "")

        # Determinar si está disponible (no dice "Agotado")
        agotado = producto.select_one(".productitem--badge")
        disponible = not (agotado and "agotado" in agotado.text.lower())

        resultados.append({
            "nombre": nombre,
            "precio": precio,
            "url": url,
            "imagen": imagen,
            "disponible": disponible
        })

    return resultados
