import io
import pandas as pd

RUTA = "datos/originales/"

def cargar_estadisticas():
    return pd.read_csv(RUTA + "estadisticas_incendios_por_region.csv")

def cargar_comparacion():
    return pd.read_csv(RUTA + "comparacion_historica_y_proyecciones_incendios.csv")

def cargar_proyeccion():
    return pd.read_csv(RUTA + "proyeccion_superficie_y_frecuencia_incendios.csv")

def cargar_historico():
    # El archivo mezcla ',' y ';' como separador
    with open(RUTA + "Analisis de incendios forestales.CSV", encoding="utf-8") as f:
        texto = f.read().replace(";", ",")
    return pd.read_csv(io.StringIO(texto))