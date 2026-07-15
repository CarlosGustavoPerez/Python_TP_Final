class ServicioLimpieza:

    @staticmethod
    def generar_recomendaciones(
        calidad,
        outliers,
        duplicados
    ):

        recomendaciones = []

        columnas_con_nulos = calidad[
            calidad["nulos"] > 0
        ]

        if not columnas_con_nulos.empty:

            recomendaciones.append(
                f"Se recomienda tratar valores faltantes en {len(columnas_con_nulos)} columnas."
            )

        if duplicados > 0:

            recomendaciones.append(
                f"Se recomienda eliminar {duplicados} registros duplicados."
            )

        total_outliers = (
            outliers["outliers"]
            .sum()
        )

        if total_outliers > 0:

            recomendaciones.append(
                f"Se recomienda revisar {total_outliers} valores atípicos detectados."
            )

        if not recomendaciones:

            recomendaciones.append(
                "No se detectaron acciones de limpieza necesarias."
            )

        return recomendaciones