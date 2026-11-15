"""Gráficos con Matplotlib Pyplot. Se guardan como PNG."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # guarda archivos sin abrir ventanas
import matplotlib.pyplot as plt
import numpy as np

COL_SUP = "Superficie quemada total [ha]"
COL_REGION = "Región"
COL_TEMPORADA = "Temporada"


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


def grafico_superficie_por_temporada(df, carpeta):
    serie = df.groupby(COL_TEMPORADA)[COL_SUP].sum().sort_index()
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(serie.index.astype(str), serie.values, marker="o", color="#e67e22",
            label="Superficie quemada total")
    ax.set_title("Evolución de la superficie quemada por temporada")
    ax.set_xlabel("Temporada")
    ax.set_ylabel("Superficie quemada [ha]")
    ax.tick_params(axis="x", rotation=45)
    ax.grid(alpha=0.3)
    ax.legend()
    return _guardar(fig, carpeta, "superficie_por_temporada.png")


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
        grafico_superficie_por_temporada(df, carpeta),
        histograma_superficie(df, carpeta),
    ]
