import pandas as pd

def limpiar_proyeccion(df):
    # Se eliminan 3 filas que son líneas de código pegadas por error
    # al final del CSV: no contienen datos, solo la columna 'region'
    return df.dropna(subset=["zona"]).reset_index(drop=True)

def limpiar_historico(df):
    df = df.copy()
    for col in ["Región", "Provincia", "Comuna", "Nombre", "Alerta", "Causa"]:
        df[col] = df[col].str.strip().str.title()
    df["Fecha"] = pd.to_datetime(df["Fecha"], format="%Y-%m-%d", errors="coerce")
    return df.drop_duplicates()