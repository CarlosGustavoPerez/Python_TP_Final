import pandas as pd


class AnalizadorDataset:

    def __init__(self, dataframe):
        self.df = dataframe

    def obtener_resumen(self):
        return {
            "filas": self.df.shape[0],
            "columnas": self.df.shape[1],
            "nulos": int(self.df.isnull().sum().sum()),
            "duplicados": int(self.df.duplicated().sum())
        }

    def obtener_tipos(self):
        return pd.DataFrame({
            "Columna": self.df.columns,
            "Tipo": self.df.dtypes.astype(str)
        })

    def obtener_estadisticas(self):
        return self.df.describe()

    def obtener_columnas_numericas(self):
        return self.df.select_dtypes(
            include=["number"]
        ).columns.tolist()

    def obtener_columnas_categoricas(self):
        return self.df.select_dtypes(
            exclude=["number"]
        ).columns.tolist()
        
    def analizar_calidad_datos(self):
        resultado = []

        for columna in self.df.columns:

            nulos = self.df[columna].isnull().sum()

            porcentaje_nulos = (
                nulos / len(self.df)
            ) * 100

            valores_unicos = (
                self.df[columna]
                .nunique(dropna=True)
            )

            resultado.append({
                "columna": columna,
                "nulos": nulos,
                "porcentaje_nulos": round(
                    porcentaje_nulos,
                    2
                ),
                "valores_unicos": valores_unicos,
                "es_constante": valores_unicos <= 1
            })

        return pd.DataFrame(resultado)
    
    def obtener_correlaciones(self):
        return self.df.corr(numeric_only=True)
    
    def generar_resumen_ejecutivo(self):
        resumen = self.obtener_resumen()
        calidad = self.analizar_calidad_datos()
        columnas_numericas = self.obtener_columnas_numericas()
        columnas_categoricas = self.obtener_columnas_categoricas()
        columnas_con_nulos = calidad[
            calidad["nulos"] > 0
        ]["columna"].tolist()
        return {
            "filas": resumen["filas"],
            "columnas": resumen["columnas"],
            "numericas": columnas_numericas,
            "categoricas": columnas_categoricas,
            "columnas_con_nulos": columnas_con_nulos
        }
        
    def detectar_outliers(self):
        resultado = []
        columnas = self.obtener_columnas_numericas()
        for columna in columnas:
            q1 = self.df[columna].quantile(0.25)
            q3 = self.df[columna].quantile(0.75)
            iqr = q3 - q1
            limite_inferior = q1 - 1.5 * iqr
            limite_superior = q3 + 1.5 * iqr
            cantidad = self.df[
                (self.df[columna] < limite_inferior)
                | (self.df[columna] > limite_superior)
            ].shape[0]
            resultado.append({
                "columna": columna,
                "outliers": cantidad
            })

        return pd.DataFrame(resultado)
    
    def obtener_contexto_llm(self):
        resumen = self.generar_resumen_ejecutivo()
        calidad = self.analizar_calidad_datos()
        outliers = self.detectar_outliers()
        correlaciones = self.obtener_correlaciones()
        primeras_filas = []
        for indice, fila in enumerate(
            self.iterar_filas()
        ):
            if indice >= 10:
                break
            primeras_filas.append(
                str(fila.to_dict())
            )
        muestra = "\n".join(
            primeras_filas
        )
        return f"""
        FILAS:
        {resumen['filas']}
        COLUMNAS:
        {resumen['columnas']}
        VARIABLES NUMERICAS:
        {', '.join(resumen['numericas'])}
        VARIABLES CATEGORICAS:
        {', '.join(resumen['categoricas'])}
        COLUMNAS CON NULOS:
        {', '.join(resumen['columnas_con_nulos'])}
        CALIDAD DE DATOS:
        {calidad.to_string()}
        OUTLIERS:
        {outliers.to_string()}
        CORRELACIONES:
        {correlaciones.to_string()}
        MUESTRA DE DATOS:
        {muestra}
        """
    
    def limpiar_dataset(self):
        df_limpio = self.df.copy()
        filas_originales = len(df_limpio)
        duplicados = df_limpio.duplicated().sum()
        df_limpio = df_limpio.drop_duplicates()
        nulos_antes = self.df.isnull().sum().sum()
        
        for columna in df_limpio.columns:
            if df_limpio[columna].dtype in [
                "int64",
                "float64"
            ]:
                mediana = df_limpio[columna].median()
                df_limpio[columna] = (
                    df_limpio[columna]
                    .fillna(mediana)
                )
            else:
                if not df_limpio[columna].mode().empty:
                    moda = (
                        df_limpio[columna]
                        .mode()[0]
                    )
                    df_limpio[columna] = (
                        df_limpio[columna]
                        .fillna(moda)
                    )
        nulos_despues = (df_limpio.isnull().sum().sum())
        filas_finales = len(df_limpio)
        
        return {
            "dataset": df_limpio,
            "duplicados_eliminados": int(duplicados),
            "filas_originales": filas_originales,
            "filas_finales": filas_finales,
            "nulos_antes": int(nulos_antes),
            "nulos_despues": int(nulos_despues)
        }
    def obtener_columnas_ordenadas(self):
        return sorted(
            self.df.columns,
            key=lambda columna: columna.lower()
        )
    
    def iterar_filas(self):
        for _, fila in self.df.iterrows():
            yield fila
