# Análisis de incendios forestales

Proyecto de [nombre del curso] sobre datos de incendios forestales en Chile.
Autores: Angello y Martina.

## Descripción

Este avance prepara los datos para su análisis posterior mediante un proceso
reproducible en Python y Pandas: detección de problemas de calidad, limpieza,
tratamiento de nulos y transformaciones.

## Estructura

- `datos/originales/`: los 4 archivos CSV originales (no se modifican).
- `datos/procesados/`: archivos limpios generados por el código.
- `reportes/`: informes de avance (`avance_1.pdf`, `avance_2.pdf`).
- `src/carga.py`: lectura de los archivos.
- `src/validaciones.py`: reporte de calidad (nulos, duplicados, tamaño).
- `src/limpieza.py`: eliminación de filas inválidas y duplicados.
- `src/transformaciones.py`: normalización de textos y conversión de fechas.
- `main.py`: ejecuta todo el proceso.

## Cómo ejecutarlo

1. Instalar pandas: `pip install pandas`
2. Ejecutar desde la carpeta del proyecto: `python main.py`

Se generan `dataset_limpio.csv` y `proyeccion_limpio.csv` en `datos/procesados/`.

## Decisiones de limpieza

- En `proyeccion_superficie_y_frecuencia_incendios.csv` se eliminaron 3 filas
  sin datos (líneas de código pegadas por error al final del archivo).
- El archivo histórico mezclaba `,` y `;` como separador, por lo que se
  unificaron antes de leerlo.
- La columna `Fecha` se convirtió a tipo fecha y se normalizaron los textos.