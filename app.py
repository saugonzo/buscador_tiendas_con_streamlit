import streamlit as st
import sys
import os
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), "scraper"))
from alfaydelta import buscar_alfaydelta
from canteraludica import buscar_canteraludica
from yegogames import buscar_yegogames
from geekystuff import buscar_geekystuff
from elduende import buscar_elduende
from tdetlacuache import buscar_tdetlacuache
from eurojuegos import buscar_eurojuegos
from lacasadelaeducadora import buscar_lacasadelaeducadora
from juegodebelugas import buscar_juegodebelugas

st.set_page_config(page_title="Buscador de Juegos de Mesa", layout="wide")
st.title("🎲 Buscador de Juegos de Mesa en Tiendas Mexicanas")

juego = st.text_input("Escribe el nombre del juego:", "")

if st.button("Buscar"):
    st.info(f"Buscando '{juego}' en tiendas...")

    tiendas = [
        ("Alfaydelta", buscar_alfaydelta),
        ("Canteraludica", buscar_canteraludica),
        ("Yegogames", buscar_yegogames),
        ("Geekystuff", buscar_geekystuff),
        ("Elduende", buscar_elduende),
        ("Tdetlacuache", buscar_tdetlacuache),
        ("Eurojuegos", buscar_eurojuegos),
        ("Lacasadelaeducadora", buscar_lacasadelaeducadora),
        ("Juegodebelugas", buscar_juegodebelugas)
    ]

    resultados = []

    for nombre, funcion in tiendas:
        try:
            info = funcion(juego)
            if info:
                resultados.append({
                    "Tienda": nombre,
                    "Precio": info['precio'],
                    "Link": f"[Abrir tienda]({info['url']})",
                    "Imagen": f"![]({info['imagen']})"
                })
            else:
                resultados.append({
                    "Tienda": nombre,
                    "Precio": "No disponible",
                    "Link": "-",
                    "Imagen": "-"
                })
        except Exception as e:
            resultados.append({
                "Tienda": nombre,
                "Precio": f"Error: {str(e)}",
                "Link": "-",
                "Imagen": "-"
            })

<<<<<<< HEAD
    df = pd.DataFrame(resultados)
    st.write("### Resultados de búsqueda")
    st.write(df.to_html(escape=False), unsafe_allow_html=True)
=======
    st.markdown("### Resultados")
for r in resultados:
    if r["Link"] != "-":
        st.markdown(f"- **{r['Tienda']}**: {r['Precio']} – [Ver juego]({r['Link']})", unsafe_allow_html=True)
    else:
        st.markdown(f"- **{r['Tienda']}**: {r['Precio']}")

>>>>>>> 18a451ebe720c484ddcb3bc9ff54b853133278cd
