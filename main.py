
from scraper.alfaydelta import buscar_alfaydelta
from scraper.canteraludica import buscar_canteraludica
from scraper.yegogames import buscar_yegogames
from scraper.geekystuff import buscar_geekystuff
from scraper.elduende import buscar_elduende
from scraper.tdetlacuache import buscar_tdetlacuache
from scraper.eurojuegos import buscar_eurojuegos
from scraper.lacasadelaeducadora import buscar_lacasadelaeducadora
from scraper.juegodebelugas import buscar_juegodebelugas
from tabulate import tabulate

def main():
    juego = input("🔍 Escribe el nombre del juego de mesa: ").strip()
    print(f'Buscando "{juego}" en todas las tiendas...\n')

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
            info = funcion(juego)
            if info:
                resultados.append([nombre, f"${info['precio']}", info['url']])
            else:
                resultados.append([nombre, "No disponible", "-"])
        except Exception as e:
            resultados.append([nombre, f"Error: {str(e)}", "-"])

    print("\n✅ Resultados obtenidos:")
    print(tabulate(resultados, headers=["Tienda", "Precio", "URL"], tablefmt="fancy_grid"))

if __name__ == "__main__":
    main()