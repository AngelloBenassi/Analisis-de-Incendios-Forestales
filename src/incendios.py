#Analisis de incendios forestales
#Por Angello Benassi
import pandas as pd

IncendiosForestales = ["estadisticas_incendios_por_region.csv", "proyeccion_superficie_y_frecuencia_incendios.csv", "Analisis de incendios forestales.CSV", "comparacion_historica_y_proyecciones_incendios.csv"]

DataDF = pd.concat((pd.read_csv(dataset, sep=',') for dataset in IncendiosForestales), ignore_index=True)

print(DataDF.head())