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

st.set_page_config(page_title="Buscador de Juegos de Mesa", layout="wide")
st.title("🎲 Buscador de Juegos de Mesa en Tiendas Mexicanas")

juego = st.text_input("🔍 Escribe el nombre del juego:")
modo_diagnostico = st.checkbox("Mostrar todos los productos encontrados (modo diagnóstico)", value=False)

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
    ]

    resultados = []

    for nombre, funcion in tiendas:
        try:
            productos = funcion(juego)
            if not productos:
                resultados.append({
                    "Tienda": nombre,
                    "Precio": "No disponible",
                    "Imagen": "",
                    "Link": "-"
                })
                continue

            for prod in productos:
                if not modo_diagnostico and prod.get("agotado", False):
                    continue
                resultados.append({
                    "Tienda": nombre,
                    "Precio": f"${prod['precio']}",
                    "Imagen": prod.get("imagen", ""),
                    "Link": f"[Abrir página]({prod['url']})"
                })

        except Exception as e:
            resultados.append({
                "Tienda": nombre,
                "Precio": f"❌ Error: {str(e)}",
                "Imagen": "",
                "Link": "-"
            })

    if resultados:
        df = pd.DataFrame(resultados)
        for idx, row in df.iterrows():
            cols = st.columns([1, 2, 4])
            if row["Imagen"]:
                cols[0].image(row["Imagen"], width=100)
            cols[1].markdown(f"**{row['Tienda']}**")
            cols[2].markdown(f"[{row['Precio']}]({row['Link']})")
    else:
        st.warning("No se encontraron resultados.")
