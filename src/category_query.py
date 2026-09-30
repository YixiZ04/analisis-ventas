"""
    Contiene una unica funcion exportable: muestreo_datos_por_categoria().
    Esta funcion realiza 2 acciones:
        1. Mostrar un resumen de cada categoria en la pantalla y guardar esa informacion en un archivo resumen.csv
        2. Mostrar una grafica de barras en la pantalla y guardarla como .png.

    Todos los parametros para sacar la grafica se ha ajustado a los datos actuales. Si hubiera mas categorias, es posible que haya que rehacer la funcion por completo.

    Aqui, las funciones cumple el objetivo de visualizacion de datos en vez su procesamiento
"""
# Importar modulos

import os
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

import pandas as pd

# Definición de algunas variables

COLUMNA_CATEGORIA = "categoria"
COLUMNA_UNIDAD = "unidades"
COLUMNA_PRECIO_UNITARIO = "precio_unitario"
COLUMNA_IMPORTE_VENTA = "importe_venta"
PATH_GUARDAR_ARCHIVOS = Path(os.getcwd(), "logs", "todas_las_categorias/")

# Funciones

def _barplot_ventas_categoria(array_categorias: np.ndarray,
                              array_importe_ventas: np.ndarray,
                              array_unidades: np.ndarray,
                              path_guardar_archivos: Path = PATH_GUARDAR_ARCHIVOS) -> None:
    """
        Genera y guarda una grafica de barras con importe de las ventas y unidades de cada categoria.

        Los parametros para generar la grafica se ha ajustado a los datos actuales.
    """

    valores_x = np.arange(len(array_categorias))
    fig, ax = plt.subplots(1,1,figsize = [12,5])
    barra_unidades = ax.bar(valores_x, array_unidades,  width=0.4, label="Unidades")
    barra_importes = ax.bar(valores_x+0.4, array_importe_ventas, width=0.4, label="Venta categoria (€)")

    ax.bar_label (barra_unidades, array_unidades)
    ax.bar_label (barra_importes, array_importe_ventas)

    ax.legend()
    ax.set_xticks(valores_x+0.2)
    ax.set_xticklabels(array_categorias, rotation=10)
    ax.set_title("Unidades e importes por categoria")

    os.makedirs(path_guardar_archivos, exist_ok=True)
    nombre_figura = Path(path_guardar_archivos, "ventas_por_categoria.png")
    print(f"La figura se guardara como {nombre_figura}...")
    fig.savefig(nombre_figura, format="png", dpi=150)
    print("La figura se ha guardado correctamente!\n")
    plt.show()

def _guardar_resumen_csv (array_categorias: np.ndarray,
                          array_importe_ventas: np.ndarray,
                          array_unidades: np.ndarray,
                          array_minimo: np.ndarray,
                          array_maximo: np.ndarray,
                          path_guardar_archivos: Path = PATH_GUARDAR_ARCHIVOS) -> None:

    """
        Dadas las siguientes np.ndarrays:
            * array_categorias -> Contiene las categorias unicas
            * array_importe_ventas -> Contiene el importe de ventas totales de cada categoria
            * array_unidades -> Contiene las unidades vendidas de cada categoria
            * array_minimo -> Contiene los precios unitarios mínimos de cada categoria
        Esta funcion genera un resumen.csv que contiene para categoria las siguientes informaciones:
            * Unidades vendidas
            * Importe total de cada categoria
            * El precio medio de los productos vendidos
            * Precio unitario maximo y minimo de cada categoria
        Este .csv (con ; de separador) con nombre resumen.csv será guardado en el Path indicado, que por defecto será:
        ./logs/category_query/
    """

    precio_medio = array_importe_ventas / array_unidades
    venta_total = array_importe_ventas.sum()
    porcentaje_ventas = np.round(array_importe_ventas * 100 / venta_total, 2)

    df_resumen = pd.DataFrame({"categoria":array_categorias,
                               "importe_ventas": array_importe_ventas,
                               "unidades_vendidas": array_unidades,
                               "precio_medio_unidad": precio_medio,
                               "precio_unitario_minimo":array_minimo,
                               "precio_unitario_maximo": array_maximo,
                               "porcentaje_venta_total": porcentaje_ventas
                                })

    nombre_archivo = "resumen.csv"
    print(f"El resumen se guardara como {Path(path_guardar_archivos,nombre_archivo)}...")
    df_resumen.to_csv(Path(path_guardar_archivos,nombre_archivo), sep=";",  index=False)
    print("El resumen se ha guardado correctamente!\n")

def muestreo_datos_por_categoria(df: pd.DataFrame,
                                 columna_categoria: str = COLUMNA_CATEGORIA,
                                 columna_unidad: str= COLUMNA_UNIDAD,
                                 columna_importe_venta: str =COLUMNA_IMPORTE_VENTA,
                                 columna_precio_unitario: str=COLUMNA_PRECIO_UNITARIO,
                                 ) -> None:

    """
        Función principal y exportado para procesar datos agrupados por categorias:
            * Mustra en la terminal infomracion de cada categoria (unidades vendidas, importe total de venta y precio medio)
            * Muestra y guarda una gráfica de barras con importe total y unidades vendidas de cada categoria
            * Por último, guarda un resumen.csv de los resultados obtenidos
    """

    datos_agrupados = df.groupby(by=columna_categoria)

    categorias, importe_ventas, unidades, precio_minimo, precio_maximo = [],[],[],[],[]

    for categoria,df_agrupado in datos_agrupados:

        temp_unidades_total = df_agrupado[columna_unidad].sum()
        temp_importe_total = df_agrupado[columna_importe_venta].sum()

        categorias.append(categoria)
        importe_ventas.append(temp_importe_total)
        unidades.append(temp_unidades_total)
        precio_minimo.append(df_agrupado[columna_precio_unitario].min())
        precio_maximo.append(df_agrupado[columna_precio_unitario].max())

        print(f"En la categoria {categoria} se vendieron {temp_unidades_total} unidades a {temp_importe_total:.2f} €. Precio medio producto = {temp_importe_total/temp_unidades_total:.2f} €")

    categorias = np.array(categorias)
    importe_ventas = np.array(importe_ventas)
    unidades = np.array(unidades)
    precio_minimo = np.array(precio_minimo)
    precio_maximo = np.array(precio_maximo)

    _barplot_ventas_categoria(categorias,
                              importe_ventas,
                              unidades)

    _guardar_resumen_csv(categorias,
                         importe_ventas,
                         unidades,
                         precio_minimo,
                         precio_maximo)