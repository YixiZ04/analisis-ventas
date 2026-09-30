"""
    Es el menu principal con 7 opciones que se muestra al usuario:
        1. Leer archivo
        2. Calcular importe de cada venta
        3. Calcular la venta total
        4. Obtener informacion de cada categoria
        5. Consulta sobre una categoria concreta
        6. Guardar archivo .parquet procesado
        7. Salir del programa
"""

# Importacion de modulos

import os
import sys
import time
from pathlib import Path

from src.file_reading import *
from src.category_query import *
from src.user_query import *
from src.process_data import *

# Crear el menu

def mostrar_menu_principal():
    """
        Muestra el menu principal
    """
    print("Seleccione una opcion:")
    print("1. Leer archivo")
    print("2. Calcular importe de cada venta")
    print("3. Calcular la venta total")
    print("4. Obtener informacion de cada categoria")
    print("5. Consulta sobre una categoria concreta")
    print("6. Guardar archivo .parquet procesado")
    print("7. Salir del programa")

def opcion_uno(path_a_datos_crudos):
    """
        Lectura del archivo y mensaje informativo.
        No hay statements try-except porque los errores se incluyen dentro de la funcion leer_archivo_csv()
    """

    df = leer_archivo_csv(path_a_datos_crudos)
    print("\nLa lectura del archivo se ha realizado correctamente!\n")
    time.sleep(0.5)

    return df

def opcion_dos(path_a_datos_crudos,
               df: pd.DataFrame | None,):
    """
        Procesa los datos. Una peculiaridad es que puede aceptar el df de datos crudos como argumento.
        Esto evita se lea mas de una vez el mismo archivo.

        (Es este caso, el archivo es pequeño, puede puede tener impacto cuando sea muy grande).
        Devuelve ambos df: crudo y procesado, esto es util en otras funciones para evitar trabajo doble.
    """

    if df is None:
        df = opcion_uno(path_a_datos_crudos)

    try:
        # df.rename(columns={"precio_unitario":"precio_unitari"}, inplace=True) # Test case
        print("\nCalculando el importe de cada venta...")
        df_importe = calcular_importe_ventas(df)
        print("\nSe han calculado correctamente!")
        print(f"\nLos primeros registros son:\n{df_importe.head()}\n")
        time.sleep(0.5)

        return df, df_importe

    except Exception as e:  # Lo principal que captaria seria error en nombre de columnas
        raise e

def opcion_tres(path_a_datos_crudos,
                df_crudos: pd.DataFrame | None,
                df_procesado: pd.DataFrame | None,):
    """
        Calcula y muestra el importe total de las ventas en la pantalla.
        Acepta tanto df con datos crudos y procesados como argumento, con la misma idea de evitar hacer doble lectura/procesamiento

        (Igual que en la funcion opcion_dos(), no hay mucho efecto en cuanto al tiempo de ejecucion dado que es un archivo pequeño,
         ademas de que el procesamiento es muy sencilla, pero si hay mas datos/procesamiento complicado, esto ahorra tiempo de ejecucion).
    """
    if df_procesado is None:
        df_crudos, df_procesado = opcion_dos(path_a_datos_crudos,
                                             df_crudos,)

    importe_total = df_procesado["importe_venta"].sum()

    print(f"El importe total de las ventas es: {importe_total:.2f} €\n")

    return df_crudos, df_procesado

def opcion_cuatro(path_a_datos_crudos,
                  df_crudos: pd.DataFrame | None,
                  df_procesado: pd.DataFrame | None,):

    """
        Muestra y guarda datos agrupados por categoria.
    """
    if df_procesado is None:
        df_crudos, df_procesado = opcion_dos(path_a_datos_crudos, df_crudos)

    muestreo_datos_por_categoria(df_procesado)

    return df_crudos, df_procesado

def opcion_cinco(path_a_datos_crudos,
                 df_crudos,
                 df_procesado):
    """
        Abre el menu para que el usuario pueda hacer query por categoria que desea
    """
    if df_procesado is None:
        df_crudos, df_procesado = opcion_dos(path_a_datos_crudos,
                                             df_crudos, )
    user_query(df_procesado)

    return df_crudos, df_procesado

def guardar_parquet(path_a_datos_crudos,
                    path_a_datos_procesados,
                    nombre_archivo: str,
                    df_crudos: pd.DataFrame | None,
                    df_procesado: pd.DataFrame | None,):

    """
        Guarda el df procesado como un archivo .parquet en el path indicado (path_a_datos_procesados)
    """
    if df_procesado is None:
        df_crudos, df_procesado = opcion_dos(path_a_datos_crudos,
                                             df_crudos,)
    print(f"Guardando los datos procesados como {Path(path_a_datos_procesados, nombre_archivo)}\n...")
    df_procesado.to_parquet(Path(path_a_datos_procesados, nombre_archivo), index=False)
    print("Se ha guardado correctamente!\n")

    try:
        pd.read_parquet(Path(path_a_datos_procesados, nombre_archivo))
        print("El archivo se puede recuperar de forma correcta!\n")
    except Exception as e:
        print(e)

    return df_crudos, df_procesado

def main():

    directorio_raiz = os.getcwd()

    # Descomenta las siguientes lineas para probar los errorcodes
    # path_a_datos_crudos = Path(directorio_raiz, "data", "na_ventas.csv")
    # path_a_datos_crudos = Path(directorio_raiz, "data", "negative_ventas.csv")
    # path_a_datos_crudos = Path(directorio_raiz, "data", "vacio.csv")
    # path_a_datos_crudos = Path(directorio_raiz, "data", "zero_precio_ventas.csv")

    path_a_datos_crudos = Path(directorio_raiz, "data", "ventas.csv")

    path_a_datos_procesados = Path(directorio_raiz, "data/")
    nombre_archivo_datos_procesados = "ventas_procesadas.parquet"

    print("Bienvenido al programa!\n")

    df,df_procesado = None, None                                    # Iniciamos estos variables nulos

    while True:
        mostrar_menu_principal()
        opcion_usuario = input()

        # Nota: aqui en cada caso se asigna valor a df y df_procesado porque el usuario puede intentar hacer cualquier opcion al entrar al programa.
        # Asi para asegurar que dada cualquier opcion, podemos asignar el valor a los variables para evitar trabajo doble.
        match opcion_usuario:
            case "1":
                df = opcion_uno(path_a_datos_crudos)
            case "2":
                df, df_procesado = opcion_dos(path_a_datos_crudos,
                                         df)
            case "3":
                df, df_procesado = opcion_tres(path_a_datos_crudos,
                                               df_crudos=df,
                                               df_procesado=df_procesado)
            case "4":
                df, df_procesado = opcion_cuatro(path_a_datos_crudos,
                                                 df_crudos=df,
                                                 df_procesado=df_procesado)
            case "5":
                df, df_procesado = opcion_cinco(path_a_datos_crudos,
                                                df_crudos=df,
                                                df_procesado=df_procesado)
            case "6":
                df, df_procesado = guardar_parquet(path_a_datos_crudos,
                                                   path_a_datos_procesados,
                                                   nombre_archivo=nombre_archivo_datos_procesados,
                                                   df_crudos=df,
                                                   df_procesado=df_procesado)

            case "7":
                print("Saliendo del programa con code 0...")
                sys.exit(0)

            case _:
                print("Por favor, seleccione una opcion valida:\n")
                time.sleep(0.5)

if __name__ == "__main__":
    main()