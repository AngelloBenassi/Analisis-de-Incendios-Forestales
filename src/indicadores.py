"""Indicadores automatizados del proyecto de incendios forestales."""
from pathlib import Path

import pandas as pd

COL_SUP = "Superficie quemada total [ha]"
COL_REGION = "Región"
COL_CAUSA = "Causa"
COL_TEMPORADA = "Temporada"
COL_FECHA = "Fecha"
UMBRAL_GRANDE_HA = 10     # incendio "grande"
UMBRAL_CRITICO_HA = 100   # incendio "crítico"


def calcular_indicadores(df):
    sup = df[COL_SUP].dropna()
    filas = []

    def agregar(indicador, metodo, resultado, interpretacion):
        filas.append({"Indicador": indicador, "Método de cálculo": metodo,
                      "Resultado": resultado, "Interpretación": interpretacion})

    # 1. Total de registros válidos
    agregar("Total de registros válidos",
            f"Conteo de incendios con '{COL_SUP}' no nulo",
            len(sup),
            f"De {len(df)} registros, {len(sup)} tienen superficie quemada registrada y se usan en el análisis.")

    # 2. Promedio de la variable principal
    agregar("Superficie quemada promedio por incendio [ha]",
            f"Media de '{COL_SUP}'",
            round(sup.mean(), 2),
            f"En promedio cada incendio quema {sup.mean():.2f} ha; la mediana es {sup.median():.2f} ha, "
            "por lo que unos pocos incendios muy grandes elevan el promedio." if sup.mean() > sup.median()
            else f"En promedio cada incendio quema {sup.mean():.2f} ha.")

    # 3. Porcentaje de casos que cumplen una condición
    pct_grandes = (sup > UMBRAL_GRANDE_HA).mean() * 100
    agregar(f"Porcentaje de incendios mayores a {UMBRAL_GRANDE_HA} ha",
            f"(incendios con superficie > {UMBRAL_GRANDE_HA} ha / registros válidos) x 100",
            round(pct_grandes, 2),
            f"El {pct_grandes:.2f}% de los incendios supera las {UMBRAL_GRANDE_HA} ha; "
            "el resto son incendios pequeños.")

    # 4. Cantidad de casos críticos
    criticos = int((sup >= UMBRAL_CRITICO_HA).sum())
    agregar(f"Cantidad de incendios críticos (>= {UMBRAL_CRITICO_HA} ha)",
            f"Conteo de incendios con superficie >= {UMBRAL_CRITICO_HA} ha",
            criticos,
            f"Hay {criticos} incendios de gran magnitud, que concentran la mayor parte del daño.")

    # 5. Categoría más frecuente (región)
    reg = df[COL_REGION].value_counts()
    agregar("Región con más incendios",
            f"Categoría más frecuente de '{COL_REGION}'",
            f"{reg.idxmax()} ({reg.max()} incendios)",
            f"{reg.idxmax()} concentra el {reg.max() / len(df) * 100:.1f}% de los incendios registrados.")

    # 6. Categoría más frecuente (causa)
    causa = df[COL_CAUSA].value_counts()
    agregar("Causa más frecuente",
            f"Categoría más frecuente de '{COL_CAUSA}'",
            f"{causa.idxmax()} ({causa.max()} incendios)",
            f"La causa '{causa.idxmax()}' explica el {causa.max() / len(df) * 100:.1f}% de los incendios.")

    # 7. Valor máximo y registro asociado
    fila = df.loc[df[COL_SUP].idxmax()]
    agregar("Mayor incendio registrado",
            f"Valor máximo de '{COL_SUP}' y su registro asociado",
            f"{fila[COL_SUP]:.2f} ha ({fila.get('Comuna', '-')}, {fila.get(COL_REGION, '-')}, "
            f"temporada {fila.get(COL_TEMPORADA, '-')})",
            "Es el evento más extremo del período y sirve de referencia del peor escenario.")

    # 8 y 9. Evolución mensual (el dataset cubre una sola temporada, por eso se compara por mes)
    fechas = pd.to_datetime(df[COL_FECHA], errors="coerce")
    mensual = df.assign(_mes=fechas.dt.to_period("M")).dropna(subset=["_mes"]).groupby("_mes")[COL_SUP].agg(["sum", "count"])
    if len(mensual) >= 2:
        mes_inc = mensual["count"].idxmax()
        agregar("Mes con más incendios",
                f"Mes con mayor conteo de incendios según '{COL_FECHA}'",
                f"{mes_inc} ({int(mensual.loc[mes_inc, 'count'])} incendios)",
                f"En {mes_inc} se concentra el {mensual.loc[mes_inc, 'count'] / mensual['count'].sum() * 100:.1f}% de los incendios.")
        mes_pico = mensual["sum"].idxmax()
        pos = list(mensual.index).index(mes_pico)
        if pos > 0 and mensual["sum"].iloc[pos - 1] != 0:
            ant = mensual["sum"].iloc[pos - 1]
            var = (mensual["sum"].iloc[pos] - ant) / ant * 100
            agregar(f"Variación de superficie quemada: mes pico ({mes_pico}) vs. mes anterior",
                    "((superficie del mes pico - superficie del mes anterior) / mes anterior) x 100",
                    round(var, 2),
                    f"En el mes con más superficie quemada ({mes_pico}) la superficie fue {var:.2f}% "
                    "mayor que en el mes anterior." if var > 0 else
                    f"En {mes_pico} la superficie varió {var:.2f}% respecto del mes anterior.")

    return pd.DataFrame(filas)


def guardar_indicadores(tabla, ruta):
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    tabla.to_csv(ruta, index=False, encoding="utf-8-sig")
    return ruta
