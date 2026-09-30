"""
    Contiene las funciones para que el usuario pueda hacer queries de una categoria concreta. En el menu principal, corresponde con la opcion 5.

    En resumen, estas funciones actuan de la siguiente forma, en orden:

        1. Muestra un primer submenu para que el usuario indique si quiere realizar un query por categoria o volver al menu principal.
        2. Si el usuario quiere realizar query por categoria, el programa mostrara en la pantalla las categorias disponibles en el .csv.
        3. El usuario debe introducir una opcion valida de categoria.
        4. Tras ello, aparecera otro menu preguntando al usurio:
            4.1. Si quiere obtener todos los registros de dicha categoria.
            4.2. Si quiere realizar otro query dentro de la categoria indicando la fecha concreta.
            4.3. Si quiere realizar otro query dentro de la categoria indicando un producto concreto.
            4.4. Volver al menu anterior.

            Si usuario selecciona opcion 4.1., el csv resultante se guardara como:
                ./logs/query_por_categoria/{categoria}/{categoria}.csv
            En casos 4.2 o 4.3, para cada query, se guardara el archivo resultante como .csv en un path con el siguiente patrón:
                ./logs/query_por_categoria/{categoria}/{"fecha", "producto"}/{fecha_concreta, producto_concreto}/{categoria}_{fecha_concreta, producto_concreto}.csv
            Ademas de mostrar los 5 primeros registros en la pantalla

    Se ha optado por este diseño de guardar archivos de cada query en vez unicamente mostrarlos por la pantalla se debe a que el resultado de cada query puede tener muchos
    registros que no mostrandolos solo por la pantalla, la informacion que puede aportar es poca.

    Mientras que si se guarda cada .csv de los queries, ese archivo puede ser posteriormente analizados para obtener mas informaciones.

    Nota: todos los .csv creados tienen ";" como separador.
"""

# Importacion de modulos

import os
import time

from pathlib import Path

import pandas as pd

# Definición de variables

COLUMNA_FECHA = "fecha"
COLUMNA_PRODUCTO = "producto"
COLUMNA_CATEGORIA = "categoria"
COLUMNA_UNIDAD = "unidades"

PATH_RAIZ_OUTPUT = Path(os.getcwd(), "logs", "query_por_categoria/")

# Funciones

def _user_submenu():
    """
        Muestra un menu en al pantalla
    """

    print("1. Obtener informacion de ventas de la categoria")
    print("2. Query por fecha")
    print("3. Query por producto")
    print("4. Hacer query por otra categoria")
    print("Introduzca una opcion:\n")


def _guardar_csv(df: pd.DataFrame,
                 categoria: str,
                 seccion_subquery: str | None,
                 user_option: str | None,
                 path_raiz_output: Path = PATH_RAIZ_OUTPUT,
                 ):
    """
        Dada un DataFrame, este se guardara como un .csv con ";" de separador. Los argumentos son:
            * df -> El DataFrame obtenido de algun query por cateroria / categoria y producto/fecha
            * categoria -> El categoria que el usuario ha introducido para hacer query
            * seccion_subquery -> "fecha","producto" o None. No es obligatorio introducir
            * user_option -> Fecha o producto concreto. No es obligatorio introducir, siempre y cuando seccion_subquery sea None
            * path_raiz_output -> Por defecto es ./logs/query_por_categoria/
    """

    # Cuando no se hace query ni por fecha/producto
    if seccion_subquery is None:
        path_a_archivo_final = Path(path_raiz_output, categoria, f"{categoria}.csv")
        os.makedirs(Path(path_raiz_output, categoria), exist_ok=True)
        print(f"Se guardara el archivo en {path_a_archivo_final}...")
        df.to_csv(path_a_archivo_final,
                  sep=";",
                  index=False,
                  )
        print("Se ha guardado correctamente!\n")

    # Cuando se hace query por fecha/producto
    else:
        # Esta condicion existe porque si se hace query por fecha/producto, fecha/producto concreto debe introducirse como argumento
        if user_option is not None:
            path_a_archivo_final = Path(path_raiz_output, categoria, seccion_subquery, user_option, f"{categoria}_{user_option}.csv")
            os.makedirs(Path(path_raiz_output, categoria, seccion_subquery, user_option), exist_ok=True)
            print(f"Se guardara el archivo en {path_a_archivo_final}...")
            df.to_csv(path_a_archivo_final,
                      sep=";",
                      index=False,
                      )
            print("Se ha guardado correctamente!\n")
        else:
            raise TypeError("Falta un argumento por introducir.")


def _query_por_fecha(sub_df,
                     categoria,
                     columna_fecha,
                     columna_categoria):
    """
        Muestra opciones para el usuario pueda hacer query por fecha.
        El resultado se guarda en un .csv
    """
    fechas_unicas = list(sub_df[columna_fecha].unique())
    fechas_unicas_string = "\n".join(list(sub_df[columna_fecha].unique()))             # String que muestra las fechas disponibles

    print(f"Las fechas disponibles son: \n {fechas_unicas_string}")
    user_fecha = input("Introduzca una fecha para realizar el query:")

    # Este bucle valida la opcion introducida.
    while user_fecha not in fechas_unicas:
        print(f"La fecha introducida {user_fecha} no es valida.")
        user_fecha = input("Introduzca una fecha para realizar el query:")

    queried_df = sub_df[sub_df[columna_fecha] == user_fecha]                           # Este es el resultado de query por fecha
    queried_df.drop(columns=[columna_fecha, columna_categoria], inplace=True)          # Eliminamos columnas redundantes
    queried_df.reset_index(drop=True, inplace=True)                                    # Reseteamos las indices

    # Nota: al tener inplace = True, esta operacion se hace directamente sobre el DataFrame

    print(f"Las primeras ventas de la categoria {categoria} en el dia {user_fecha} fueron los siguientes:")
    print(queried_df.head())

    _guardar_csv(queried_df,
                 categoria=categoria,
                 seccion_subquery="fecha",
                 user_option=user_fecha,)

def _query_por_producto(sub_df,
                        categoria,
                        columna_producto,
                        columna_categoria):
    """
        Funciona exactamente igyal que la funcion _query_por_fecha() pero con la columna de productos.
    """
    productos_unicos = list(sub_df[columna_producto].unique())
    productos_unicos_string = "\n".join(list(sub_df[columna_producto].unique()))

    print(f"Los productos disponibles son: \n {productos_unicos_string}")
    user_producto = input("Introduzca un producto para hacer el query:")

    while user_producto not in productos_unicos:
        print("Producto introducido invalido.")
        user_producto = input("Introduzca un producto para hacer el query:")

    queried_df = sub_df[sub_df[columna_producto] == user_producto]
    queried_df.drop(columns=[columna_producto, columna_categoria], inplace=True)
    queried_df.reset_index(drop=True, inplace=True)

    print(f"Las primeras ventas de la categoria {categoria} del producto {user_producto} fueron los siguientes:")
    print(queried_df.head())

    _guardar_csv(queried_df,
                 categoria=categoria,
                 seccion_subquery="producto",
                 user_option=user_producto)

def _user_subquery(sub_df,
                   user_categoria,
                   columna_categoria,
                   columna_fecha,
                   columna_producto):
    """
        Valida las opciones introducida por el usuario del submenu mostrada
    """
    while True:
        _user_submenu()
        user_subcategoria = input("Seleccione el accion que desee realizar:")
        match user_subcategoria:
            case "1":
                _guardar_csv(sub_df,
                             categoria=user_categoria,
                             seccion_subquery=None,
                             user_option=None)
            case "2":
                _query_por_fecha(sub_df,
                                 user_categoria,
                                 columna_fecha,
                                 columna_categoria)

            case "3":
                _query_por_producto(sub_df,
                                    user_categoria,
                                    columna_producto,
                                    columna_categoria)

            case "4":
                print("Volviendo al menu de categorias...")
                time.sleep(0.5)
                break

            case _:
                print("Opcion invalida. Por favor, intente nuevamente.")

def user_query(df,
               columna_categoria=COLUMNA_CATEGORIA,
               columna_fecha=COLUMNA_FECHA,
               columna_producto=COLUMNA_PRODUCTO,
               ):
    """
        Permite que el usuario haga queries para el csv con categoria como la primera condición.
    """

    categorias_unicas = list(df[columna_categoria].unique())
    categorias_unicas_string = "\n".join(list(df[columna_categoria].unique()))

    while True:
        user_choice = input("\n1. Hacer query por categoria\n2. Volver al menu principal\nSeleccione una opcion:")

        match user_choice:
            case "1":
                print(f"Las categorias disponibles son: \n{categorias_unicas_string}\n")

                user_categoria = input("Introduzca una categoria:")

                while user_categoria not in categorias_unicas:
                    print(f"La categoria introducida: {user_categoria} no es valida.")
                    user_categoria = input("\nIntroduzca una categoria:")

                sub_df = df[df[columna_categoria] == user_categoria]
                _user_subquery(sub_df=sub_df,
                               user_categoria=user_categoria,
                               columna_categoria=columna_categoria,
                               columna_fecha=columna_fecha,
                               columna_producto=columna_producto)
            case "2":
                print("\nVolviendo al menu principal...\n")
                time.sleep(0.5)
                break

            case _:
                print("Opcion invalida. Por favor, intente nuevamente.")








