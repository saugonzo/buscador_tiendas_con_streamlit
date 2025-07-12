import streamlit as st
import pandas as pd
import sys
import os

# Importar scrapers
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
st.title("🎲 Buscador de Juegos de Mesa en Tiendas Mexicanas")

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
                for p in productos:
                    resultados.append({
                        "Tienda": nombre,
                        "Nombre": p.get("nombre", "Sin nombre"),
                        "Precio": p.get("precio", "N/A"),
                        "Disponible": "✅" if p.get("disponible", False) else "❌",
                        "URL": p.get("url", ""),
                        "Imagen": p.get("imagen", ""),
                    })
            else:
                resultados.append({
                    "Tienda": nombre,
                    "Nombre": "Sin resultados",
                    "Precio": "-",
                    "Disponible": "-",
                    "URL": "-",
                    "Imagen": ""
                })
        except Exception as e:
            resultados.append({
                "Tienda": nombre,
                "Nombre": f"❌ Error: {str(e)}",
                "Precio": "-",
                "Disponible": "-",
                "URL": "-",
                "Imagen": ""
            })

    if resultados:
        for row in resultados:
            with st.container():
                cols = st.columns([1, 3, 1, 1, 1])
                if row["Imagen"]:
                    cols[0].image(row["Imagen"], use_container_width=True)
                else:
                    cols[0].write("Sin imagen")
                cols[1].markdown(f"**{row['Nombre']}**\n\n[{row['URL']}]({row['URL']})")
                cols[2].markdown(f"**{row['Precio']}**")
                cols[3].markdown(row["Disponible"])
                cols[4].markdown(f"*{row['Tienda']}*")
    else:
        st.warning("No se encontraron resultados.")
