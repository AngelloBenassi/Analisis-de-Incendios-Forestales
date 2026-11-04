def reporte_calidad(df, nombre):
    nulos = df.isna().sum()
    print(f"--- {nombre} ---")
    print("Filas y columnas:", df.shape)
    print("Duplicados:", df.duplicated().sum())
    print("Nulos:\n", nulos[nulos > 0])