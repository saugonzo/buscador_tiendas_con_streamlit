
import streamlit as st
import sys
import os
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
import pandas as pd

st.set_page_config(page_title="Buscador de Juegos de Mesa", layout="centered")
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
            productos = funcion(juego)
            if productos:
                for prod in productos:
                    prod["tienda"] = nombre
                    resultados.append(prod)
        except Exception as e:
            resultados.append({
                "tienda": nombre,
                "nombre": "❌ Error",
                "precio": str(e),
                "url": "-",
                "imagen": ""
            })

    for row in resultados:
        cols = st.columns([1, 2, 1, 1, 1])
        if isinstance(row, dict):
            if row.get("imagen"):
                cols[0].image(row["imagen"], use_container_width=True)
            else:
                cols[0].write("Sin imagen")

            cols[1].markdown(f"[{row.get('nombre', 'Sin nombre')}]({row.get('url', '#')})")
            cols[2].write(row.get("precio", "Sin precio"))
            cols[3].write(row.get("tienda", "Sin tienda"))
        else:
            st.warning("Fila inválida, no es un diccionario")
