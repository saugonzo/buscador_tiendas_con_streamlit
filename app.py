
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
        ("Infinite Skill", buscar_infiniteskill)
    ]

    for nombre, funcion in tiendas:
        st.subheader(f"Tienda: {nombre}")
        try:
            resultados = funcion(juego)
            disponibles = [r for r in resultados if r["disponible"]]
            if not disponibles:
                st.warning("❌ No disponible.")
            else:
                for r in disponibles:
                    cols = st.columns([1, 3, 3])
                    if r["imagen"]:
                        cols[0].image(r["imagen"], use_container_width=True)
                    else:
                        cols[0].write("Sin imagen")
                    cols[1].markdown(f"**{r['nombre']}**")
                    cols[2].markdown(f"[{r['precio']}]({r['url']})")
        except Exception as e:
            st.error(f"⚠️ Error en {nombre}: {e}")
