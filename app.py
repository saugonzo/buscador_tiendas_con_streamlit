
import streamlit as st
import sys
import os
import pandas as pd

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from scraper.alfaydelta import buscar_alfaydelta
from scraper.canteraludica import buscar_canteraludica
from scraper.yegogames import buscar_yegogames
from scraper.geekystuff import buscar_geekystuff
from scraper.elduende import buscar_elduende
from scraper.tdetlacuache import buscar_tdetlacuache
from scraper.eurojuegos import buscar_eurojuegos
from scraper.lacasadelaeducadora import buscar_lacasadelaeducadora
from scraper.juegodebelugas import buscar_juegodebelugas
from scraper.infiniteskill import buscar_infiniteskill

st.set_page_config(page_title="Buscador de Juegos de Mesa", layout="wide")
st.title("🔍 Buscador de Juegos de Mesa en Tiendas Mexicanas")

juego = st.text_input("Escribe el nombre del juego:", "")

if st.button("Buscar"):
    st.info(f"Buscando '{juego}' en tiendas disponibles...")

    tiendas = [
        ("Alfa y Delta", buscar_alfaydelta),
        ("Cantera Lúdica", buscar_canteraludica),
        ("Yego Games", buscar_yegogames),
        ("Geeky Stuff", buscar_geekystuff),
        ("El Duende", buscar_elduende),
        ("T de Tlacuache", buscar_tdetlacuache),
        ("Eurojuegos", buscar_eurojuegos),
        ("La Casa de la Educadora", buscar_lacasadelaeducadora),
        ("Juegos de Belugas", buscar_juegodebelugas),
        ("Infinite Skill", buscar_infiniteskill),
    ]

    resultados = []
    for nombre, funcion in tiendas:
        try:
            juegos = funcion(juego)
            if juegos:
                for info in juegos:
                    resultados.append({
                        "Tienda": nombre,
                        "Nombre": info.get("nombre", "Sin nombre"),
                        "Precio": info.get("precio", "Sin precio"),
                        "Link": info.get("url", "-"),
                        "Imagen": info.get("imagen", None),
                        "Disponible": "✅" if info.get("disponible", False) else "❌"
                    })
            else:
                resultados.append({
                    "Tienda": nombre,
                    "Nombre": "Sin resultados",
                    "Precio": "-",
                    "Link": "-",
                    "Imagen": None,
                    "Disponible": "-"
                })
        except Exception as e:
            resultados.append({
                "Tienda": nombre,
                "Nombre": f"Error: {str(e)}",
                "Precio": "-",
                "Link": "-",
                "Imagen": None,
                "Disponible": "-"
            })

    for row in resultados:
    cols = st.columns([1, 2, 1, 1, 1])

    if row["imagen"]:
        cols[0].image(row["imagen"], use_container_width=True)
    else:
        cols[0].write("Sin imagen")

    cols[1].markdown(f"**{row['nombre']}**")

    disponible = row.get("disponible", False)
    icono = "✅" if disponible else "❌"
    precio = row.get("precio", "N/A")
    cols[2].markdown(f"{precio} {icono}")

    if row.get("url"):
        cols[3].markdown(f"[Ir al producto]({row['url']})")
    else:
        cols[3].write("Sin enlace")

    cols[4].markdown(f"*{row.get('tienda', '')}*")
