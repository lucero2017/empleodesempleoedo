import streamlit as st
import pandas as pd
import plotly.express as px
from funciones import cargar_datos, modelo_regresion, modelo_clasificacion
from fpdf import FPDF
import tempfile

# --- Configuración de página ---
st.set_page_config(page_title="Empleo y Desempleo en el Estado de México", layout="wide")

# --- CSS ---
st.markdown("""
    <style>
    body { background-color: #ffffff; }
    .main { font-family: Arial, sans-serif; color: #333333; }
    .title-box {
        background: #800020;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        margin-bottom: 20px;
        border: 5px solid #FFD700;
    }
    .title-box h1 {
        color: white;
        font-size: 3em;
        margin: 0;
    }
    hr {
        border: none;
        border-top: 3px solid #FFD700;
        margin: 20px 0;
    }
    .intro-text {
        font-size: 1.3em;
        margin-bottom: 20px;
    }
    .nav-button {
        display: inline-block;
        background-color: #800020;
        color: #fff;
        border: 2px solid #FFD700;
        border-radius: 50px;
        padding: 10px 25px;
        margin: 5px;
        text-decoration: none;
        font-size: 1em;
        transition: all 0.3s ease;
    }
    .nav-button:hover {
        background-color: #990033;
        transform: scale(1.05);
        color: #fff;
    }
    </style>
""", unsafe_allow_html=True)

# --- Título ---
st.markdown("""
    <div class='title-box'>
        <h1>🇲🇽 EMPLEO Y DESEMPLEO EN EL ESTADO DE MÉXICO</h1>
    </div>
""", unsafe_allow_html=True)

# --- Navegación ---
nav_items = ["Inicio", "2020", "2021", "2022", "2023", "2024", "Realizar Predicción", "Descargas"]
nav_query = st.query_params.get("page")

if nav_query in nav_items:
    seccion = nav_query
else:
    seccion = "Inicio"

nav_html = "".join(
    [f"<a class='nav-button' href='?page={item}'>{item}</a>" for item in nav_items]
)
st.markdown(f"<div style='text-align: center;'>{nav_html}</div>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# --- Cargar datos ---
df = cargar_datos("data/empleodesempleo.csv")

# --- Intro general ---
def mostrar_intro_general():
    st.markdown("""
    <div class="intro-text">
    El Estado de México, uno de los motores económicos de la nación, refleja una dinámica laboral compleja y en constante evolución.
    Este territorio concentra una gran parte de la fuerza laboral del país, destacándose tanto en industrias manufactureras como en el sector servicios.
    Durante los últimos cinco años, factores como la pandemia, la recuperación económica, la digitalización y las reformas laborales han moldeado el panorama de empleo y desempleo.
    <br><br>
    Entre las principales características destacan:
    <ul>
        <li>Alta concentración de empleo formal en zonas industriales y corredores urbanos.</li>
        <li>Una significativa proporción de empleo informal en áreas periurbanas y rurales.</li>
        <li>Fluctuaciones en los ingresos promedio, estrechamente vinculadas a la estabilidad económica nacional.</li>
        <li>Distribución equitativa del empleo entre sexos, aunque persisten brechas salariales y de horas trabajadas.</li>
    </ul>
    Además, municipios como Toluca, Ecatepec y Naucalpan figuran entre los de mayor actividad económica y empleo.
    No obstante, el desempleo afecta con mayor dureza a jóvenes y mujeres, especialmente en épocas de desaceleración económica.
    <br><br>
    Esta plataforma permite analizar datos de 2020 a 2024, visualizar gráficas de distribución por sexo, ingresos, tipos de empleo y posición ocupacional, además de realizar predicciones personalizadas. 
    Es una herramienta valiosa para académicos, estudiantes, tomadores de decisiones y ciudadanía interesada en comprender la evolución del mercado laboral mexiquense.
    </div>
    """, unsafe_allow_html=True)

def mostrar_intro_anual(año):
    st.markdown(f"""
    <div class="intro-text">
    Durante el año {año}, se observaron tendencias particulares en el mercado laboral del Estado de México, afectando variables como ingresos promedio, distribución por sexo y la prevalencia del empleo formal e informal.
    Las gráficas presentadas permiten visualizar de forma clara la situación de ese año específico.
    </div>
    """, unsafe_allow_html=True)

# --- Inicio ---
if seccion == "Inicio":
    st.header("Introducción General")
    mostrar_intro_general()

    img_path = "empleo.jpg"
    if os.path.exists(img_path):
        st.image(img_path, caption="Empleo en el Estado de México", use_container_width=True)
    else:
        st.warning(f"No se encontró la imagen '{img_path}'.")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("Base de datos de empleo y desempleo (2020 - 2024)")
    st.dataframe(df, use_container_width=True)

# --- Por año ---
elif seccion in ["2020", "2021", "2022", "2023", "2024"]:
    año = int(seccion)
    st.header(f"Empleo y Desempleo en {año}")
    mostrar_intro_anual(año)
    df_año = df[df['Año'] == año]
    st.dataframe(df_año, use_container_width=True)

    fig1 = px.histogram(df_año, x='Sexo', color='Sexo',
                        color_discrete_sequence=['#800020', '#FFD700'],
                        title=f"Distribución por Sexo en {año}")
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.box(df_año, x='Sexo', y='Nivel_Ingresos',
                  color='Sexo',
                  color_discrete_sequence=['#800020', '#FFD700'],
                  title=f"Ingreso Promedio por Sexo en {año}")
    st.plotly_chart(fig2, use_container_width=True)

# --- Predicción ---
elif seccion == "Realizar Predicción":
    st.header("Realizar Predicción")
    edad_input = st.slider("Edad", min_value=18, max_value=100, value=30)
    sexo_input = st.selectbox("Sexo", options=df['Sexo'].unique())

    if st.button("Predecir Ingreso (Regresión)"):
        pred_r = modelo_regresion(df, edad_input, sexo_input)
        st.success(f"Ingreso estimado: ${pred_r:,.2f}")

    if st.button("Predecir Categoría (Clasificación)"):
        pred_c = modelo_clasificacion(df, edad_input, sexo_input)
        st.info(f"Categoría estimada: {pred_c}")

# --- Descargas ---
elif seccion == "Descargas":
    st.header("Descargar Datos y Reportes")

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Descargar Base de Datos CSV", csv, "empleodesempleo.csv", "text/csv")

    st.markdown("### Generar Reporte PDF (SOLO TEXTO)")
    if st.button("Generar y Descargar Reporte PDF (Texto)"):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Reporte General de Empleo y Desempleo", ln=True)

        pdf.set_font("Arial", size=12)
        texto = """
Este es un reporte de texto resumen del análisis de empleo y desempleo en el Estado de México.
Incluye:
- Descripción general de la base de datos.
- Resumen por año de los datos cargados.
- Para ver gráficas interactivas, consulta la plataforma o descarga las tablas.

Este PDF no incluye imágenes, para garantizar compatibilidad en la nube.
"""
        pdf.multi_cell(0, 10, texto)

        for año in range(2020, 2025):
            pdf.add_page()
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, f"Año {año}", ln=True)
            pdf.set_font("Arial", size=12)
            texto_año = f"Resumen de datos para el año {año}. Para detalles visuales, consulte la plataforma."
            pdf.multi_cell(0, 10, texto_año)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            pdf.output(tmp_pdf.name)
            pdf_path = tmp_pdf.name

        with open(pdf_path, "rb") as f:
            st.download_button(
                label="Descargar Reporte PDF",
                data=f,
                file_name="reporte_empleo_mexico.pdf",
                mime="application/pdf"
            )
