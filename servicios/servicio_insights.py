class ServicioInsights:

    @staticmethod
    def generar_insights(
        resumen,
        calidad,
        outliers
    ):

        insights = []

        if resumen["filas"] < 100:
            insights.append(
                "El dataset tiene una cantidad reducida de registros."
            )

        columnas_con_nulos = len(
            resumen["columnas_con_nulos"]
        )

        if columnas_con_nulos > 0:
            insights.append(
                f"Se detectaron {columnas_con_nulos} columnas con valores faltantes."
            )

        total_outliers = outliers["outliers"].sum()

        if total_outliers > 0:
            insights.append(
                f"Se detectaron {total_outliers} valores atípicos."
            )

        if not insights:
            insights.append(
                "No se detectaron problemas relevantes."
            )

        return insights