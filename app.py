
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
import pandas as pd

st.set_page_config(page_title="Buscador de Juegos de Mesa", layout="centered")
st.title("🔍 Buscador de Juegos de Mesa en Tiendas Mexicanas")

juego = st.text_input("Escribe el nombre del juego:")

if st.button("Buscar") and juego.strip():
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
descartes = []
    for nombre, funcion in tiendas:
        try:
            info = funcion(juego, debug=modo_diagnostico)
            if isinstance(info, dict) and info.get("precio") and info.get("url") and not info.get("agotado", False):
                resultados.append({
                    "Tienda": nombre,
                    "Precio": f"${info['precio']}",
                    "Link": f"[Ver producto]({info['url']})",
                    "Imagen": info.get("imagen", "")
                })
        except Exception as e:
            resultados.append({
                "Tienda": nombre,
                "Precio": f"Error: {str(e)}",
                "Link": "-",
                "Imagen": ""
            })

    if resultados:
        df = pd.DataFrame(resultados)
        for _, row in df.iterrows():
            st.markdown(f"### 🛒 {row['Tienda']}")
            col1, col2 = st.columns([1, 3])
            with col1:
                if row["Imagen"]:
                    st.image(row["Imagen"], width=120)
            with col2:
                st.markdown(f"**Precio:** {row['Precio']}")
                st.markdown(f"{row['Link']}")
            st.markdown("---")
    else:
        st.warning("No se encontraron productos disponibles.")
