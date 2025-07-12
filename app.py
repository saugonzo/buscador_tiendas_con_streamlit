
import streamlit as st
import pandas as pd
from scraper import geekystuff, yegogames, elduende

st.title("Buscador de Juegos de Mesa")

nombre_juego = st.text_input("Escribe el nombre del juego que deseas buscar:")

if nombre_juego:
    resultados = []

    with st.spinner("Buscando en Geeky Stuff..."):
        try:
            data = geekystuff.buscar_geekystuff(nombre_juego)
            if data:
                resultados.extend(data)
        except Exception as e:
            resultados.append({"tienda": "Geeky Stuff", "nombre": f"Error: {str(e)}", "precio": "", "url": "", "imagen": None, "disponible": False})

    with st.spinner("Buscando en Yego Games..."):
        try:
            data = yegogames.buscar_yegogames(nombre_juego)
            if data:
                resultados.extend(data)
        except Exception as e:
            resultados.append({"tienda": "Yego Games", "nombre": f"Error: {str(e)}", "precio": "", "url": "", "imagen": None, "disponible": False})

    with st.spinner("Buscando en El Duende..."):
        try:
            data = elduende.buscar_elduende(nombre_juego)
            if data:
                resultados.extend(data)
        except Exception as e:
            resultados.append({"tienda": "El Duende", "nombre": f"Error: {str(e)}", "precio": "", "url": "", "imagen": None, "disponible": False})

    if resultados:
        st.write(f"Se encontraron {len(resultados)} resultado(s):")

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
    else:
        st.warning("No se encontraron resultados.")
