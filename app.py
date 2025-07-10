import streamlit as st
import sys
import os
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), "scraper"))

from scraper.alfaydelta import buscar_alfaydelta
from scraper.tdetlacuache import buscar_tdetlacuache

st.set_page_config(page_title="Buscador de Juegos de Mesa", layout="wide")
st.title("🔍 Buscador de Juegos de Mesa en Tiendas Mexicanas")

juego = st.text_input("Escribe el nombre del juego:", "")

if st.button("Buscar"):
    st.info(f"Buscando '{juego}' en tiendas disponibles...")

    tiendas = [
        ("Alfa y Delta", buscar_alfaydelta),
        ("T de Tlacuache", buscar_tdetlacuache),
    ]

    resultados = []
    for nombre, funcion in tiendas:
        try:
            info = funcion(juego)
            if info:
                resultados.append({
                    "Tienda": nombre,
                    "Precio": info["precio"],
                    "Link": info["url"],
                    "Imagen": info["imagen"]
                })
            else:
                resultados.append({
                    "Tienda": nombre,
                    "Precio": "No disponible",
                    "Link": "-",
                    "Imagen": None
                })
        except Exception as e:
            resultados.append({
                "Tienda": nombre,
                "Precio": f"❌ Error: {e}",
                "Link": "-",
                "Imagen": None
            })

    for row in resultados:
        cols = st.columns([1, 2, 2])
        cols[0].image(row["Imagen"], use_column_width=True) if row["Imagen"] else cols[0].write("Sin imagen")
        cols[1].markdown(f"**{row['Tienda']}**")
        if row["Link"] != "-" and "http" in row["Link"]:
            cols[2].markdown(f"[{row['Precio']}]({row['Link']})")
        else:
            cols[2].write(row["Precio"])