"""
    Aquí se encuentran las funciones de leer el archivo .csv y tratar los errores de la lectura/archivo

"""

# Importacion de modulos

from pathlib import Path

import sys
import pandas as pd

from src.errorcodes import *

# Funciones

def _chequeo_existencia_archivo(path_a_archivo: Path) -> None:
    """
        Revisa si el path indicado existe
    """
    
    if not path_a_archivo.exists():
        raise FileNotFoundError(f"{path_a_archivo} no existe. Por favor asegure de su existencia.")

def _chequeo_archivo_vacio(df: pd.DataFrame) -> None:
    """
        Esta revisión se hace a nivel de DataFrame, si no contiene ningún dato (len == 0).
    """

    if len(df) == 0:
        raise EmptyFileError("El archivo no contiene registros!")

def _chequeo_valores_nulos(df: pd.DataFrame):
    """ 
        Revisa si hay valores nulos (NA). Y muestra en la pantalla en cual columna contiene tantos nulos.
    """
    
    recuentos_na = [ df[column].isna().sum() for column in list(df.columns)]
    mensaje_error = ""

    for column, recuento_na in zip(df.columns, recuentos_na):
        if recuento_na > 0:
            mensaje_error+= f"\nLa columna {column} tiene {recuento_na} nulos."

    if len(mensaje_error) > 0:
        raise NullValueError(mensaje_error)

def _chequeo_valores_negativos(df: pd.DataFrame, 
                               columna: str) -> None:
    """
        Dada una columna del DataFrame, esta función hace el chequeo de valores negativos (<0).
    """
    
    valores_temporales = df.loc[:, columna].to_list()
    negativos = [ True if temp_valor < 0 else False for temp_valor in valores_temporales ]

    if any(negativos):
        raise NegativeValueError(f"En la columna {columna} existen valores negativos!")

def _chequeo_ceros (df: pd.DataFrame, 
                    columna: str) -> None:
    """
        Dada una columna del DataFrame, esta función hace el chequeo de valores iguales a 0.
        No da un error, sino que da un mensaje de warning, y le da al usuario opción de seguir ejecutando el programa.
        
        Tiene sentido solo cuando el precio sea 0, que puede ser un regalo o descuento para el cliente, pero el stock de la tienda debe actualizarse
        
        Si unidades es igual a 0 es posible que sea un error de sistema.
    """
    
    valores_temporales = df.loc[:, columna].to_list()
    ceros = [True if temp_valor == 0 else False for temp_valor in valores_temporales ]

    if any(ceros):
        while True:
            user_input = input(f"WARNING: En la columna {columna} hay ceros. Desea continuar con la ejecucion? [y/n]")
            match user_input:
                case "y":
                    break
                case "n":
                    print ("El usuario detuvo el programa. Saliendo con error code 1...")
                    sys.exit(1)
                case _:
                    continue

def leer_archivo_csv(path_a_archivo: Path,
                     separador: str = ";",
                     ) -> pd.DataFrame:

    """
        Lee y trata errores de la lectura o el propio archivo .csv.
        Toma 2 argumentos:
            * path_a_archivo: por defecto es directorio_raiz/ventas.csv
            * separador: por defecto es ; (Puede tomar , o incluso ª\t", aunque pasaría a ser un .tsv)
        Devuelve el DataFrame generado al leer el csv de entrada.
    """

    _chequeo_existencia_archivo(path_a_archivo)

    df = pd.DataFrame(pd.read_csv(path_a_archivo, sep=separador, header=0, encoding = "utf-8"))

    _chequeo_archivo_vacio(df) 
    _chequeo_valores_nulos(df) 
    _chequeo_valores_negativos(df, columna = "unidades") 
    _chequeo_valores_negativos(df, columna = "precio_unitario") 
    _chequeo_ceros(df, columna = "unidades")
    _chequeo_ceros(df, columna = "precio_unitario")

    return df


