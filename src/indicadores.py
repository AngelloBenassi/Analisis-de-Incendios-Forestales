"""Indicadores automatizados del proyecto de incendios forestales."""
from pathlib import Path

import pandas as pd

COL_SUP = "Superficie quemada total [ha]"
COL_REGION = "Región"
COL_CAUSA = "Causa"
COL_TEMPORADA = "Temporada"
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

    # 8. Variación entre períodos (última temporada vs anterior)
    por_temp = df.groupby(COL_TEMPORADA)[COL_SUP].sum().sort_index()
    if len(por_temp) >= 2 and por_temp.iloc[-2] != 0:
        ult, ant = por_temp.iloc[-1], por_temp.iloc[-2]
        var = (ult - ant) / ant * 100
        agregar(f"Variación de superficie quemada entre temporadas ({por_temp.index[-2]} a {por_temp.index[-1]})",
                "((superficie última temporada - superficie temporada anterior) / temporada anterior) x 100",
                round(var, 2),
                f"La superficie quemada {'aumentó' if var > 0 else 'disminuyó'} {abs(var):.2f}% "
                "respecto de la temporada anterior (revisa si la última temporada está completa).")

    return pd.DataFrame(filas)


def guardar_indicadores(tabla, ruta):
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    tabla.to_csv(ruta, index=False, encoding="utf-8-sig")
    return ruta
