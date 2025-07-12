import streamlit as st
from scraper import ejecutar_scrapers

st.set_page_config(page_title="Buscador de Juegos de Mesa", layout="wide")

st.title("🔍 Buscador de Juegos de Mesa")
nombre_juego = st.text_input("Ingresa el nombre del juego:", "")

if nombre_juego:
    resultados = ejecutar_scrapers(nombre_juego)
    if not resultados:
        st.warning("No se encontraron resultados.")
    else:
        for row in resultados:
            if not isinstance(row, dict):
                continue
            cols = st.columns([1, 2, 1, 1, 1])
            if row.get("imagen"):
                cols[0].image(row["imagen"], use_container_width=True)
            else:
                cols[0].write("Sin imagen")
            url = row.get("url", "#")
            nombre = row.get("nombre", "Nombre no disponible")
            precio = row.get("precio", "N/A")
            tienda = row.get("tienda", "Tienda")
            disponible = row.get("disponible", True)

            cols[1].markdown(f"**[{nombre}]({url})**")
            cols[2].write(precio)
            cols[3].write(tienda)
            if disponible:
                cols[4].success("✅ Disponible")
            else:
                cols[4].error("❌ No disponible")
