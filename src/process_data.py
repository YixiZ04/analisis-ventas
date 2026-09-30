"""
    Contiene una unica funcion de procesar los datos.

"""

# Importacion de pandas

import pandas as pd

# Definicion de parametros

COLUMNA_UNIDAD = "unidades"
COLUMNA_PRECIO_UNITARIO = "precio_unitario"

# Funciones

# def calcular_importe_ventas(df: pd.DataFrame,
#                            columna_unidad: str = COLUMNA_UNIDAD,
#                            columna_precio: str = COLUMNA_PRECIO_UNITARIO) -> pd.DataFrame:
#     """
#         Hace lo mismo que la otra funcion, pero la operacion central se hace con un bucle for.
#     """
#     temp_df = df.copy()
#     lista_unidades = temp_df.loc[:, columna_unidad].tolist()
#     lista_precios = temp_df.loc[:, columna_precio].tolist()
#
#     lista_importe_ventas = []
#     for i in range(len(lista_unidades)):
#         importe_venta = lista_unidades[i] * lista_precios[i]
#         lista_importe_ventas.append(importe_venta)
#
#     temp_df["importe_venta"] = lista_importe_ventas
#     return temp_df

def calcular_importe_ventas(df: pd.DataFrame,
                           columna_unidad: str = COLUMNA_UNIDAD,
                           columna_precio: str = COLUMNA_PRECIO_UNITARIO) -> pd.DataFrame:
    """
        Dada un DataFrame con las columnas de unidades vendidas y precio unitario, esta función calcula el precio total de cada venta.
        Esta información es almacenada en una nueva columna llamada "importe_venta".
    """
    temp_df = df.copy() # Haciendo una copia, esta funcion deja de modificar el df original, que puede causar problemas
    temp_df ["importe_venta"] = temp_df[columna_unidad] * temp_df[columna_precio]

    return temp_df
