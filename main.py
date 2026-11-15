"""Ejecuta todo el proceso del avance 3: python main.py (desde la raíz)."""
from pathlib import Path

import pandas as pd

from src import estadisticas, indicadores, visualizaciones

RAIZ = Path(__file__).resolve().parent
DATASET = RAIZ / "datos" / "procesados" / "dataset_limpio.csv"
SALIDA = RAIZ / "resultados"

COLUMNAS_REQUERIDAS = ["Región", "Fecha", "Causa", "Superficie quemada total [ha]"]


def cargar_datos():
    try:
        return pd.read_csv(DATASET)
    except UnicodeDecodeError:
        return pd.read_csv(DATASET, encoding="latin-1")


def main():
    df = cargar_datos()
    faltan = [c for c in COLUMNAS_REQUERIDAS if c not in df.columns]
    if faltan:
        raise SystemExit(f"Faltan columnas en el dataset: {faltan}\nColumnas disponibles: {list(df.columns)}")
    print(f"Dataset cargado: {df.shape[0]} filas, {df.shape[1]} columnas")

    tabla = estadisticas.calcular_estadisticas(df)
    print("Estadísticas guardadas en", estadisticas.guardar_estadisticas(tabla, SALIDA / "estadisticas.csv"))

    tabla_ind = indicadores.calcular_indicadores(df)
    print("Indicadores guardados en", indicadores.guardar_indicadores(tabla_ind, SALIDA / "indicadores.csv"))
    print(tabla_ind[["Indicador", "Resultado"]].to_string(index=False))

    for ruta in visualizaciones.generar_graficos(df, SALIDA / "graficos"):
        print("Gráfico guardado en", ruta)


if __name__ == "__main__":
    main()
