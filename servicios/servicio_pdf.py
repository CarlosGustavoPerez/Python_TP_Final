from io import BytesIO

from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet


class ServicioPDF:

    @staticmethod
    def generar_pdf(
        resumen_ejecutivo,
        insights,
        informe_ia
    ):

        buffer = BytesIO()

        documento = SimpleDocTemplate(
            buffer,
            pagesize=letter
        )

        estilos = getSampleStyleSheet()

        contenido = []

        contenido.append(
            Paragraph(
                "DataPilot AI - Informe de Dataset",
                estilos["Title"]
            )
        )

        contenido.append(Spacer(1, 12))

        contenido.append(
            Paragraph(
                "Resumen Ejecutivo",
                estilos["Heading2"]
            )
        )

        contenido.append(
            Paragraph(
                f"Filas: {resumen_ejecutivo['filas']}",
                estilos["BodyText"]
            )
        )

        contenido.append(
            Paragraph(
                f"Columnas: {resumen_ejecutivo['columnas']}",
                estilos["BodyText"]
            )
        )

        contenido.append(Spacer(1, 12))

        contenido.append(
            Paragraph(
                "Variables Numéricas",
                estilos["Heading3"]
            )
        )

        for columna in resumen_ejecutivo["numericas"]:
            contenido.append(
                Paragraph(
                    f"• {columna}",
                    estilos["BodyText"]
                )
            )

        contenido.append(Spacer(1, 12))

        contenido.append(
            Paragraph(
                "Variables Categóricas",
                estilos["Heading3"]
            )
        )

        for columna in resumen_ejecutivo["categoricas"]:
            contenido.append(
                Paragraph(
                    f"• {columna}",
                    estilos["BodyText"]
                )
            )

        contenido.append(Spacer(1, 12))

        contenido.append(
            Paragraph(
                "Insights Automáticos",
                estilos["Heading2"]
            )
        )

        for insight in insights:
            contenido.append(
                Paragraph(
                    f"• {insight}",
                    estilos["BodyText"]
                )
            )

        contenido.append(Spacer(1, 12))

        contenido.append(
            Paragraph(
                "Informe Generado por IA",
                estilos["Heading2"]
            )
        )

        contenido.append(
            Paragraph(
                informe_ia.replace("\n", "<br/>"),
                estilos["BodyText"]
            )
        )

        documento.build(contenido)

        buffer.seek(0)

        return buffer