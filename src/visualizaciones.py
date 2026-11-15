"""Gráficos con Matplotlib Pyplot. Se guardan como PNG."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # guarda archivos sin abrir ventanas
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

COL_SUP = "Superficie quemada total [ha]"
COL_REGION = "Región"
COL_FECHA = "Fecha"


def _guardar(fig, carpeta, nombre):
    carpeta = Path(carpeta)
    carpeta.mkdir(parents=True, exist_ok=True)
    ruta = carpeta / nombre
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)
    return ruta


def grafico_incendios_por_region(df, carpeta):
    conteo = df[COL_REGION].value_counts().sort_values()
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.barh(conteo.index.astype(str), conteo.values, color="#c0392b", label="Cantidad de incendios")
    for i, v in enumerate(conteo.values):
        ax.text(v, i, f" {v}", va="center", fontsize=8)
    ax.set_title("Cantidad de incendios forestales por región")
    ax.set_xlabel("Número de incendios [unidades]")
    ax.set_ylabel("Región")
    ax.grid(axis="x", alpha=0.3)
    ax.legend()
    return _guardar(fig, carpeta, "incendios_por_region.png")


def grafico_evolucion_mensual(df, carpeta):
    fechas = pd.to_datetime(df[COL_FECHA], errors="coerce")
    serie = df.assign(_mes=fechas.dt.to_period("M")).dropna(subset=["_mes"]).groupby("_mes")[COL_SUP].sum()
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(serie.index.astype(str), serie.values, marker="o", color="#e67e22",
            label="Superficie quemada total")
    ax.set_title("Evolución mensual de la superficie quemada (temporada 2005-2006)")
    ax.set_xlabel("Mes")
    ax.set_ylabel("Superficie quemada [ha]")
    ax.tick_params(axis="x", rotation=45)
    ax.grid(alpha=0.3)
    ax.legend()
    return _guardar(fig, carpeta, "superficie_por_mes.png")


def histograma_superficie(df, carpeta):
    datos = df[COL_SUP].dropna()
    datos = datos[datos > 0]
    bins = np.logspace(np.log10(datos.min()), np.log10(datos.max()), 30)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.hist(datos, bins=bins, color="#2980b9", edgecolor="white", label="Incendios")
    ax.axvline(datos.median(), color="black", linestyle="--", label=f"Mediana: {datos.median():.2f} ha")
    ax.set_xscale("log")
    ax.set_title("Distribución de la superficie quemada por incendio")
    ax.set_xlabel("Superficie quemada [ha] (escala logarítmica)")
    ax.set_ylabel("Número de incendios [unidades]")
    ax.grid(alpha=0.3)
    ax.legend()
    return _guardar(fig, carpeta, "histograma_superficie.png")


def generar_graficos(df, carpeta):
    return [
        grafico_incendios_por_region(df, carpeta),
        grafico_evolucion_mensual(df, carpeta),
        histograma_superficie(df, carpeta),
    ]
