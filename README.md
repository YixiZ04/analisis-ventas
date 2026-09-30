# Analisis-venta

## 1. Datos crudos (ventas.csv)

Los datos crudos tienden a simular la venta de un supermercado pequeño (Carrefour Express, por ejemplo) de una semana. Tiene en total 5068 registros. Estos datos se han generado con IA generativa.

## 2. Estructura del proyecto
La estructura adaptada en este proyecto es la más común para un proyecto de Python, lo que permite un debugging y una revisión más sencilla.

### 2.1. main.py
Este es el archivo principal que debe ejecutarse para ver el programa, para ello ejecute en un terminal:

```
python main.py
```

### 2.2 ./data/

En este directorio contiene varios archivos .csv y el archivo ventas_procesadas.parquet:

```
    na_ventas.csv
    negative_ventas.csv
    vacio.csv
    ventas.csv
    ventas_procesadas.parquet
    zero_precio_ventas.csv
```
Para obtener el archivo ventas_procesado.parquet, debe usar ventas.csv. 

El resto de archivos csv se usa unicamente si el usuario desea comprobar el tratamiento de errores en la lectura de archivo. Esta misma información está comentado en main.py (line 152-156)

### 2.3. ./src/

Contiene los scripts con funciones reutilizadas en main.py:

```
    category_query.py
    errorcodes.py
    file_reading.py
    process_data.py
    user_query.py
    __init__.py
```

Cada archivo contiene funciones con la misma logica:
* file_reading.py -> Lee ventas.csv y procesa los errores producidos en la lectura o de los propios datos
* process_data.py -> Procesado de datos.
* category_quering.py -> Visualizacion de datos agrupados por "categoria"
* user_query.py -> Contiene las funciones para que usuria pueda hacer consultas de una categoria espeficadas por el.
* errorcodes.py -> Contiene clases de errores creadas para file_reading.py

Nota: En todos los scripts, al comienzo hay una breve explicacion de su contenido. Además de que en cada funcion hay una explicacion de los argumentos y su utilidad. Razón por la que en esta documentacion no hay ninguna explicacino de funciones construidas.

### 2.4. ./logs/

Este directorio se crea para guardar resultados obtenidos al ejecutar el programa. Por ejemplo, si el usuario quiere hacer consultas agrupadas por categoria, se guardará un resumen en este directorio.

## 3. requirements.txt

Este archivo contiene las librerias necesarias para poder ejecutar sin problema este programa. Para ello, introduzca en la terminal:

```
pip install -r requirements.txt
```
Sin embargo, las librerías basicas son los siguientes:
* pandas 3.0.6
* numpy 2.5.3
* matplotlib 3.11.2
* pyarrow 25.0.1

## 4. Algunas detalles

En muchos casos en los print() o bien hay un salto de línea (\n) al principio del string, al final o ambos . El único propósito de esto es por la estética.

En algunos casos, tras ciertas opciones de menu se encuentra time.sleep(0.5), hace una pequeña pausa en saltos de menu, es totalmente eliminable, pero personalmente me gusta que entre acciones haya una peqeuña pausa para que no todo sea tan "inmediato". (Si hay muchos datos y/o procesado es muy complejo, se eliminarán, pero no es el caso).

En todos los menus, he utilizado bucle infinito (while True) y match/case, en vez de varios if/elif. En este caso es totalmente intercambiable, pero personalmente me gusta más match/case para construir estos menus.

Para calcular la nueva columna de "importe_venta", lo que he hecho ha sido multiplicar dos columnas directamente, que es la forma más eficiente, no solo por la simplicidad del sintaxis sino que también por ser una operación vectorizada. Se ha comentado otra función cuyo cálculo se hace con un bucle for.

## 5. Uso de IA

Solo se ha usado para la generación de ventas.csv