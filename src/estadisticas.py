"""Estadísticas descriptivas del dataset de incendios forestales."""
from pathlib import Path

import pandas as pd

COL_DURACION = "Duración (minutos)"
COLS_CATEGORICAS = ["Región", "Temporada", "Causa", "Escenario", "Alerta"]
TOP_CATEGORIAS = 10  # cuántas categorías mostrar por variable categórica


def columnas_numericas(df):
    """Duración y todas las columnas de superficie quemada."""
    cols = [c for c in df.columns if c.startswith("Superficie quemada")]
    if COL_DURACION in df.columns:
        cols.insert(0, COL_DURACION)
    return cols


def estadisticas_numericas(df):
    filas = []
    for col in columnas_numericas(df):
        s = df[col].dropna()
        medidas = {
            "registros": s.count(),
            "media": s.mean(),
            "mediana": s.median(),
            "minimo": s.min(),
            "maximo": s.max(),
            "rango": s.max() - s.min(),
            "desviacion_estandar": s.std(),
            "cuartil_1 (Q1)": s.quantile(0.25),
            "cuartil_2 (Q2)": s.quantile(0.50),
            "cuartil_3 (Q3)": s.quantile(0.75),
        }
        for medida, valor in medidas.items():
            filas.append({"tipo": "numerica", "variable": col, "medida": medida,
                          "valor": round(float(valor), 4), "porcentaje": ""})
    return pd.DataFrame(filas)


def frecuencias_categoricas(df):
    filas = []
    total = len(df)
    for col in COLS_CATEGORICAS:
        if col not in df.columns:
            continue
        for categoria, n in df[col].value_counts().head(TOP_CATEGORIAS).items():
            filas.append({"tipo": "categorica", "variable": col, "medida": str(categoria),
                          "valor": int(n), "porcentaje": round(100 * n / total, 2)})
    return pd.DataFrame(filas)


def calcular_estadisticas(df):
    return pd.concat([estadisticas_numericas(df), frecuencias_categoricas(df)], ignore_index=True)


def guardar_estadisticas(tabla, ruta):
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    tabla.to_csv(ruta, index=False, encoding="utf-8-sig")
    return ruta
