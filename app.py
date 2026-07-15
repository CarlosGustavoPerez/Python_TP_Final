import streamlit as st
import pandas as pd
import plotly.express as px
from analizadores.analizador_dataset import AnalizadorDataset
from servicios.servicio_insights import ServicioInsights
from servicios.servicio_llm import ServicioLLM
from servicios.servicio_pdf import ServicioPDF
from servicios.servicio_limpieza import ServicioLimpieza
from utilidades.validadores import archivo_csv_valido

st.set_page_config(
    page_title="DataPilot AI",
    page_icon="📊",
    layout="wide"
)
st.markdown("""
<style>

/* Tabs */
button[data-baseweb="tab"] {
    font-size: 1.1rem;
    font-weight: 600;
    padding-top: 12px;
    padding-bottom: 12px;
}

/* Tab seleccionada */
button[data-baseweb="tab"][aria-selected="true"] {
    font-size: 1.15rem;
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)
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
st.sidebar.markdown(
    """
    ### Clases Aplicadas

    ✅ Análisis de Datos con Pandas

    ✅ Modelos de Lenguaje (LLM)

    """
)
st.sidebar.markdown("""
### Casos de Prueba

📁 ventas_problematicas.csv

📁 autos.csv

📁 empleados.csv
""")

# Inicialización del historial
if "historial_chat" not in st.session_state:
    st.session_state.historial_chat = []
if "informe_ia" not in st.session_state:
    st.session_state.informe_ia = None
archivo = st.file_uploader(
    "Seleccione un archivo CSV",
    type=["csv"]
)

if archivo is not None:
    try:
        if not archivo_csv_valido(
            archivo.name
        ):
            st.error(
                "Debe seleccionar un archivo CSV válido."
            )
            st.stop()
        
        df = pd.read_csv(archivo)

        analizador = AnalizadorDataset(df)
        metricas = analizador.obtener_resumen()
        celdas_totales = max(
            metricas["filas"] * metricas["columnas"],
            1
        )

        porcentaje_calidad = (
            100
            - (
                metricas["nulos"]
                / celdas_totales
                * 100
            )
        )
        st.success("Archivo cargado correctamente")
        col1, col2, col3, col4 = st.columns(4)
        with col1:st.metric("Variables Numéricas",len(analizador.obtener_columnas_numericas()))
        with col2:st.metric("Variables Categóricas",len(analizador.obtener_columnas_categoricas()))
        with col3:st.metric("Columnas con Nulos",len(analizador.generar_resumen_ejecutivo()["columnas_con_nulos"]))
        with col4:st.metric("Calidad Global",f"{porcentaje_calidad:.2f}%")
        st.progress(porcentaje_calidad / 100)
        if porcentaje_calidad >= 95:
            st.success(f"✅ Dataset de alta calidad ({porcentaje_calidad:.2f}%)")
        elif porcentaje_calidad >= 80:
            st.warning(f"⚠️ Dataset con calidad aceptable ({porcentaje_calidad:.2f}%)")
        else:
            st.error(f"❌ Dataset con problemas de calidad ({porcentaje_calidad:.2f}%)")
        
        st.header("Vista previa")
        cantidad = st.slider(
            "Cantidad de filas a visualizar",
            5,
            min(100, len(df)),
            10
        )

        st.dataframe(df.head(cantidad))

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
        
        
        
        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
            "📊 Visualizaciones",
            "📈 Estadísticas",
            "✅ Calidad de Datos",
            "🔥 Correlaciones",
            "📋 Resumen Ejecutivo",
            "🚨 Outliers",
            "🧹 Limpieza"
        ])

        with tab1:
            st.header("Gráficos")
            columnas_numericas = sorted(analizador.obtener_columnas_numericas(), key=lambda columna: columna.lower())
            if columnas_numericas:
                columna = st.selectbox("Seleccione una columna numérica",columnas_numericas)
                figura = px.histogram(df,x=columna,title=f"Distribución de {columna}")
                st.plotly_chart(figura,width="stretch")
            columnas_categoricas = sorted(analizador.obtener_columnas_categoricas(), key=lambda columna: columna.lower())

            if columnas_categoricas:
                st.subheader("Distribución de Variables Categóricas")
                columna_categoria = st.selectbox(
                    "Seleccione una variable categórica",
                    columnas_categoricas,
                    key="categoria_grafico"
                )
                datos_categoria = (
                    df[columna_categoria]
                    .value_counts()
                    .reset_index()
                )
                datos_categoria.columns = [
                    "Categoria",
                    "Cantidad"
                ]
                fig_categoria = px.bar(
                    datos_categoria,
                    x="Categoria",
                    y="Cantidad",
                    title=f"Distribución de {columna_categoria}"
                )
                st.plotly_chart(
                    fig_categoria,
                    width="stretch"
                )
            
        with tab2:    
            st.header("📊 Estadísticas Descriptivas")
            st.dataframe(analizador.obtener_estadisticas())
            
        with tab3:
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
        
        with tab4:
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
                        if valor > 0.8:
                            st.success(f"✅ Existe una relación positiva fuerte entre '{columna}' y '{otra}'.")
                        if valor < -0.8:
                            st.warning(f"⚠️ Existe una relación negativa fuerte entre '{columna}' y '{otra}'.")
            else:
                st.info("Se necesitan al menos dos columnas numéricas.")    
                
        with tab5:
            st.header("📋 Resumen Ejecutivo")
            resumen_ejecutivo = analizador.generar_resumen_ejecutivo()
            st.write(f"**Cantidad de filas:** {resumen_ejecutivo['filas']}")
            st.write(f"**Cantidad de columnas:** {resumen_ejecutivo['columnas']}")
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
                st.success("No se detectaron valores faltantes.")
        
        with tab6:
            st.header("🚨 Detección de Outliers")
            outliers = analizador.detectar_outliers()
            st.dataframe(outliers)

        with tab7:
            st.header("🧹 Limpieza Automática")
            recomendaciones = (
                ServicioLimpieza
                .generar_recomendaciones(
                    calidad,
                    outliers,
                    metricas["duplicados"]
                )
            )

            st.subheader(" 🧹 Recomendaciones de Limpieza")
            for recomendacion in recomendaciones:
                st.warning(recomendacion)
            if st.button("Limpiar Dataset"):
                resultado_limpieza = (analizador.limpiar_dataset())
                dataset_limpio = (resultado_limpieza["dataset"])
                st.success("Dataset limpiado correctamente")
                col1, col2, col3, col4 = st.columns(4)
                with col1: st.metric("Filas originales",resultado_limpieza["filas_originales"])
                with col2: st.metric("Filas finales",resultado_limpieza["filas_finales"])
                with col3: st.metric("Nulos antes",resultado_limpieza["nulos_antes"])
                with col4: st.metric("Nulos después",resultado_limpieza["nulos_despues"])
                st.subheader("Vista previa del dataset limpio")
                cantidad_limpio = st.slider(
                    "Cantidad de filas del dataset limpio",
                    5,
                    min(100, len(dataset_limpio)),
                    10,
                    key="slider_dataset_limpio"
                )

                st.dataframe(dataset_limpio.head(cantidad_limpio))
                csv_limpio = (dataset_limpio.to_csv(index=False).encode("utf-8"))
                st.download_button(
                    "📥 Descargar Dataset Limpio",
                    csv_limpio,
                    "dataset_limpio.csv",
                    "text/csv"
                )    

        st.header("🤖 Insights Automáticos")
        
        insights = ServicioInsights.generar_insights(
            resumen_ejecutivo,
            calidad,
            outliers
        )
        st.success(
            f"Se generaron {len(insights)} insights automáticos."
        )
        for insight in insights:
            st.info(insight)

        st.header("🧠 Informe Generado por IA")
        
        if st.button("Generar Informe IA"):
            with st.spinner("Analizando dataset..."):
                servicio_llm = ServicioLLM()
                contexto = (analizador.obtener_contexto_llm())
                informe = servicio_llm.generar_informe(contexto)
                st.session_state["informe_ia"] = informe
                
        if st.session_state.informe_ia:
            st.success("✅ Informe generado correctamente")
            st.markdown(
                st.session_state.informe_ia,
                unsafe_allow_html=True
            )
            pdf = ServicioPDF.generar_pdf(
                resumen_ejecutivo,
                insights,
                st.session_state.informe_ia
            )
            st.download_button(
                label="📄 Descargar Informe PDF",
                data=pdf,
                file_name="informe_datapilot.pdf",
                mime="application/pdf"
            )
        
        st.header("💬 Consultar Dataset")
        pregunta = st.text_input("Realice una pregunta sobre el dataset")
        col1, col2 = st.columns([1, 1])
        with col1: consultar = st.button("Consultar")
        with col2:
            limpiar = st.button("Limpiar conversación")
        if limpiar: st.session_state.historial_chat = []
        if consultar:
            if not pregunta.strip():
                st.warning("Ingrese una pregunta.")
            else:
                with st.spinner("Consultando IA..."):
                    servicio_llm = ServicioLLM()
                    contexto = (analizador.obtener_contexto_llm())
                    respuesta = (
                        servicio_llm.responder_pregunta(
                            contexto,
                            st.session_state.historial_chat,
                            pregunta
                        )
                    )
                    st.session_state.historial_chat.append(
                        {
                            "pregunta": pregunta,
                            "respuesta": respuesta
                        }
                    )
        if len(st.session_state.historial_chat) > 0:
            st.subheader("Historial de Conversación")
            for item in reversed(st.session_state.historial_chat):
                st.markdown(f"**🧑 Usuario:** {item['pregunta']}")
                st.markdown(f"**🤖 IA:** {item['respuesta']}",unsafe_allow_html=True)
                st.divider()
        st.divider()
        st.caption(
            """
            DataPilot AI
            
            Trabajo Práctico Final
            
            Programación en Python - UAI
            
            Tecnologías:
            
            Pandas • Streamlit • Hugging Face • Plotly
            
            """
        )
        
    except Exception as error:
        st.error(
            f"Error al procesar el archivo: {error}"
        )