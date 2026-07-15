# DataPilot AI

## Descripción

DataPilot AI es una aplicación web desarrollada en Python que permite realizar análisis inteligentes sobre datasets en formato CSV.

La aplicación integra técnicas de análisis de datos con Pandas y Modelos de Lenguaje (LLM) mediante Hugging Face para generar informes automáticos, detectar problemas en los datos y responder consultas realizadas por el usuario.

---

## Funcionalidades

### Análisis de Datos

- Carga de archivos CSV.
- Vista previa del dataset.
- Estadísticas descriptivas.
- Identificación de tipos de datos.
- Detección de valores nulos.
- Detección de registros duplicados.
- Matriz de correlación.
- Identificación de columnas problemáticas.
- Detección de outliers.
- Gráficos interactivos.

### Inteligencia Artificial

- Generación automática de informes mediante LLM.
- Generación de insights sobre los datos.
- Recomendaciones de mejora de calidad de datos.
- Chat interactivo sobre el dataset cargado.
- Historial de consultas.
- Exportación de informes en PDF.

---

## Tecnologías Utilizadas

- Python
- Streamlit
- Pandas
- Plotly
- Hugging Face
- ReportLab
- Python Dotenv

---

## Arquitectura del Proyecto

```text
Python_TP_Final/

├── app.py
├── config.py
├── requirements.txt
├── README.md
├── .env.example
│
├── analizadores/
│   └── analizador_dataset.py
│
├── servicios/
│   ├── servicio_insights.py
│   ├── servicio_llm.py
│   └── servicio_pdf.py
│
├── componentes/
├── modelos/
└── utilidades/
```

---

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/CarlosGustavoPerez/Python_TP_Final.git

cd Python_TP_Final
```

Crear entorno virtual:

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

### Linux / Mac

```bash
python -m venv .venv

source .venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

---

## Configuración

Crear un archivo `.env` en la raíz del proyecto.

Ejemplo:

```env
HF_TOKEN=su_token_de_huggingface
```

---

## Ejecución

Iniciar la aplicación:

```bash
streamlit run app.py
```

La aplicación quedará disponible en:

```text
http://localhost:8501
```

---

## Clases del Curso Aplicadas

### Análisis de Datos con Pandas

- Limpieza de datos.
- Análisis exploratorio.
- Estadísticas descriptivas.
- Calidad de datos.
- Correlaciones.
- Detección de anomalías.

### Uso de Modelos de Lenguaje (LLM)

- Generación de informes automáticos.
- Generación de insights.
- Interpretación de datasets.
- Respuesta a consultas realizadas por el usuario.

---

## Flujo de Funcionamiento

```text
Usuario
   │
   ▼

Carga CSV

   │
   ▼

Análisis con Pandas

   ├── Estadísticas
   ├── Calidad de datos
   ├── Correlaciones
   ├── Outliers
   └── Gráficos

   │
   ▼

Generación de contexto

   │
   ▼

Modelo de Lenguaje (LLM)

   ├── Informe IA
   ├── Insights
   └── Chat

   │
   ▼

Exportación PDF
```

---

## Aplicación desplegada

https://iatpfinal.streamlit.app/

---

## Casos de Prueba Incluidos

El repositorio incluye datasets de demostración para validar distintas funcionalidades de la aplicación:

- ventas_problematicas.csv
  - Valores nulos
  - Registros duplicados
  - Outliers
  - Correlaciones fuertes

- autos.csv
  - Correlaciones débiles
  - Variables numéricas y categóricas

- empleados.csv
  - Dataset de Recursos Humanos
  - Consultas mediante IA

---

## Autor

Carlos Gustavo Pérez

Trabajo Práctico Final

Programación en Python - UAI