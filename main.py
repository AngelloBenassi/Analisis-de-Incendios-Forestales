import os
from src.carga import cargar_estadisticas, cargar_comparacion, cargar_proyeccion, cargar_historico
from src.validaciones import reporte_calidad
from src.limpieza import limpiar_proyeccion, limpiar_historico

est = cargar_estadisticas()
comp = cargar_comparacion()
proy = cargar_proyeccion()
hist = cargar_historico()

for nombre, df in [("estadisticas", est), ("comparacion", comp), ("proyeccion", proy), ("historico", hist)]:
    reporte_calidad(df, nombre)

proy = limpiar_proyeccion(proy)
hist = limpiar_historico(hist)

reporte_calidad(proy, "proyeccion (limpio)")
reporte_calidad(hist, "historico (limpio)")

os.makedirs("datos/procesados", exist_ok=True)
hist.to_csv("datos/procesados/dataset_limpio.csv", index=False, encoding="utf-8-sig")
proy.to_csv("datos/procesados/proyeccion_limpio.csv", index=False, encoding="utf-8-sig")