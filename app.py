from analizadores.analizador_dataset import AnalizadorDataset
from servicios.servicio_insights import ServicioInsights
from servicios.servicio_llm import ServicioLLM
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="DataPilot AI",
    page_icon="📊",
    layout="wide"
)

st.title("📊 DataPilot AI")
st.subheader("Analizador Inteligente de Datasets")
st.markdown(
    """
    Esta herramienta permite analizar datasets,
    detectar problemas de calidad,
    encontrar correlaciones,
    identificar outliers y generar insights automáticos.
    """
)
st.sidebar.title("DataPilot AI")

st.sidebar.markdown(
    """
    ### Funcionalidades
    
    - Vista previa
    - Calidad de datos
    - Correlaciones
    - Outliers
    - Insights automáticos
    """
)

archivo = st.file_uploader(
    "Seleccione un archivo CSV",
    type=["csv"]
)

if archivo is not None:
    try:
        df = pd.read_csv(archivo)

        analizador = AnalizadorDataset(df)
        metricas = analizador.obtener_resumen()
        st.success("Archivo cargado correctamente")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Variables Numéricas",
                len(
                    analizador.obtener_columnas_numericas()
                )
            )
        with col2:
            st.metric(
                "Variables Categóricas",
                len(
                    analizador.obtener_columnas_categoricas()
                )
            )
        with col3:
            st.metric(
                "Columnas con Nulos",
                len(
                    analizador
                    .generar_resumen_ejecutivo()["columnas_con_nulos"]
                )
            )

        st.header("Vista previa")
        st.dataframe(df.head())

        st.header("Información general")
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("Filas", metricas["filas"])
        with col2: st.metric("Columnas", metricas["columnas"])
        with col3: st.metric("Valores nulos", metricas["nulos"])
        with col4: st.metric("Duplicados", metricas["duplicados"])

        st.header("Tipos de datos")
        tipos = pd.DataFrame({
            "Columna": df.columns,
            "Tipo": df.dtypes.astype(str)
        })
        st.dataframe(analizador.obtener_tipos())

        st.header("Estadísticas descriptivas")
        st.dataframe(analizador.obtener_estadisticas())

        st.header("Gráficos")
        columnas_numericas = (analizador.obtener_columnas_numericas())
        if columnas_numericas:
            columna = st.selectbox("Seleccione una columna numérica",columnas_numericas)
            figura = px.histogram(df,x=columna,title=f"Distribución de {columna}")
            st.plotly_chart(figura,width="stretch")

        st.header("Calidad de Datos")
        calidad = (analizador.analizar_calidad_datos())
        st.dataframe(calidad)
        columnas_problematicas = calidad[calidad["porcentaje_nulos"] > 20]
        if not columnas_problematicas.empty:
            st.warning("Se detectaron columnas con más del 20% de valores nulos.")
            st.dataframe(columnas_problematicas)
        else:
            st.success("No se detectaron problemas importantes de calidad.")

        st.header("Valores Nulos por Columna")
        fig_nulos = px.bar(
            calidad,
            x="columna",
            y="nulos",
            title="Cantidad de valores nulos"
        )
        st.plotly_chart(fig_nulos,width="stretch")
        
        st.header("Matriz de Correlación")
        correlaciones = analizador.obtener_correlaciones()
        if len(correlaciones.columns) > 1:
            fig_corr = px.imshow(
                correlaciones,
                text_auto=".2f",
                color_continuous_scale="RdBu_r",
                aspect="auto"
            )
            st.plotly_chart(
                fig_corr,
                width="stretch"
            )

            st.subheader("Relaciones detectadas")
            relaciones_mostradas = set()
            for columna in correlaciones.columns:
                for otra in correlaciones.columns:
                    if columna == otra:
                        continue
                    clave = tuple(sorted([columna, otra]))
                    if clave in relaciones_mostradas:
                        continue
                    relaciones_mostradas.add(clave)
                    valor = correlaciones.loc[columna, otra]
                    if abs(valor) > 0.8:
                        st.success(
                            f"Correlación fuerte entre '{columna}' y '{otra}': {valor:.2f}"
                        )
        else:
            st.info(
                "Se necesitan al menos dos columnas numéricas."
            )
        
        st.header("📋 Resumen Ejecutivo")
        resumen_ejecutivo = analizador.generar_resumen_ejecutivo()
        st.write(
            f"**Cantidad de filas:** {resumen_ejecutivo['filas']}"
        )
        st.write(
            f"**Cantidad de columnas:** {resumen_ejecutivo['columnas']}"
        )

        st.subheader("Variables Numéricas")
        for columna in resumen_ejecutivo["numericas"]:
            st.write(f"• {columna}")
            
        st.subheader("Variables Categóricas")
        for columna in resumen_ejecutivo["categoricas"]:
            st.write(f"• {columna}")

        st.subheader("Columnas con Valores Faltantes")
        if resumen_ejecutivo["columnas_con_nulos"]:
            for columna in resumen_ejecutivo["columnas_con_nulos"]:
                st.warning(columna)
        else:
            st.success(
                "No se detectaron valores faltantes."
            )
        
        st.header("🚨 Detección de Outliers")
        outliers = analizador.detectar_outliers()
        st.dataframe(outliers)

        st.header("🤖 Análisis Inteligente")
        insights = ServicioInsights.generar_insights(
            resumen_ejecutivo,
            calidad,
            outliers
        )
        for insight in insights:
            st.info(insight)

        st.header("🧠 Informe Generado por IA")
        if st.button("Generar Informe IA"):
            with st.spinner(
                "Analizando dataset..."
            ):
                servicio_llm = ServicioLLM()
                
                contexto = (
                    analizador.obtener_contexto_llm()
                )
                                
                informe = servicio_llm.generar_informe(
                    contexto
                )

                st.markdown(
                    informe,
                    unsafe_allow_html=True
                )
        
        st.header("💬 Consultar Dataset")
        pregunta = st.text_input(
            "Realice una pregunta sobre el dataset"
        )
        if st.button("Consultar"):
            if not pregunta.strip():
                st.warning(
                    "Ingrese una pregunta."
                )
            else:
                with st.spinner(
                    "Consultando IA..."
                ):
                    servicio_llm = ServicioLLM()
                    contexto = (
                        analizador.obtener_contexto_llm()
                    )
                    respuesta = (
                        servicio_llm.responder_pregunta(
                            contexto,
                            pregunta
                        )
                    )

                    st.markdown(respuesta)
                    
    except Exception as error:
        st.error(
            f"Error al procesar el archivo: {error}"
        )