import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from scraper.alfaydelta import buscar_alfaydelta
from scraper.canteraludica import buscar_canteraludica
import pandas as pd

st.set_page_config(page_title="Buscador de Juegos de Mesa", layout="centered")
st.title("🔍 Buscador de Juegos de Mesa en Tiendas Mexicanas")

juego = st.text_input("Escribe el nombre del juego:", "")

if st.button("Buscar"):
    st.info(f"Buscando '{juego}' en tiendas disponibles...")

    tiendas = [
        ("Alfa y Delta", buscar_alfaydelta),
        ("Cantera Lúdica", buscar_canteraludica),
    ]

    resultados = []
    for nombre, funcion in tiendas:
        try:
            info = funcion(juego)
            if info:
                resultados.append({
                    "Tienda": nombre,
                    "Precio": f"${info['precio']}",
                    "Link": info['url']
                })
            else:
                resultados.append({
                    "Tienda": nombre,
                    "Precio": "No disponible",
                    "Link": "-"
                })
        except Exception as e:
            resultados.append({
                "Tienda": nombre,
                "Precio": f"Error: {str(e)}",
                "Link": "-"
            })

    df = pd.DataFrame(resultados)
    st.dataframe(df, use_container_width=True)