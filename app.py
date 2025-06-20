import streamlit as st
import pandas as pd
import plotly.express as px
from funciones import cargar_datos, modelo_regresion, modelo_clasificacion
from fpdf import FPDF
import os
import tempfile

# --- Configuración de página ---
st.set_page_config(page_title="Empleo y Desempleo en el Estado de México", layout="wide")

# --- CSS para diseño ---
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

# --- Línea dorada decorativa ---
st.markdown("<hr>", unsafe_allow_html=True)

# --- Cargar datos ---
df = cargar_datos("data/empleodesempleo.csv")

# --- Funciones de introducción ---
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

# --- Sección Inicio ---
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
    st.write("Esta base de datos muestra información clave para analizar las tendencias del empleo y desempleo en el Estado de México.")
    st.dataframe(df, use_container_width=True)

# --- Apartados por año ---
elif seccion in ["2020", "2021", "2022", "2023", "2024"]:
    año = int(seccion)
    st.header(f"Empleo y Desempleo en {año}")
    mostrar_intro_anual(año)

    df_año = df[df['Año'] == año]

    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader(f"Tabla de datos para {año}")
    st.dataframe(df_año, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    fig1 = px.histogram(df_año, x='Sexo', color='Sexo',
                        color_discrete_sequence=['#800020', '#FFD700'],
                        title=f"Distribución por Sexo en {año}")
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.box(df_año, x='Sexo', y='Nivel_Ingresos',
                  color='Sexo',
                  color_discrete_sequence=['#800020', '#FFD700'],
                  title=f"Ingreso Promedio por Sexo en {año}")
    st.plotly_chart(fig2, use_container_width=True)

    if 'Horas_Trabajo' in df_año.columns:
        fig3 = px.bar(df_año.groupby('Sexo')['Horas_Trabajo'].mean().reset_index(),
                      x='Sexo', y='Horas_Trabajo', color='Sexo',
                      color_discrete_sequence=['#800020', '#FFD700'],
                      title=f"Promedio de Horas Trabajadas por Sexo en {año}")
        st.plotly_chart(fig3, use_container_width=True)

    if 'Tipo_Empleo' in df_año.columns:
        empleo_counts = df_año['Tipo_Empleo'].value_counts().reset_index()
        empleo_counts.columns = ['Tipo_Empleo', 'Count']
        fig4 = px.pie(empleo_counts, names='Tipo_Empleo', values='Count',
                      title=f"Proporción de Empleos Formales e Informales en {año}",
                      color_discrete_sequence=['#800020', '#FFD700'])
        st.plotly_chart(fig4, use_container_width=True)

    if 'Posicion_Ocupacion' in df_año.columns and 'Total_Poblacion' in df_año.columns:
        ocupacion_sum = df_año.groupby('Posicion_Ocupacion')['Total_Poblacion'].sum().reset_index()
        fig5 = px.pie(ocupacion_sum, names='Posicion_Ocupacion', values='Total_Poblacion',
                      title=f"Posición/Ocupación vs Población Total en {año}",
                      color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig5, use_container_width=True)

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

    if st.button("Generar y Descargar Reporte PDF"):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)

        for año in range(2020, 2025):
            df_año = df[df['Año'] == año]

            fig1 = px.histogram(df_año, x='Sexo', color='Sexo',
                                color_discrete_sequence=['#800020', '#FFD700'],
                                title=f"Distribución por Sexo en {año}")

            fig2 = px.box(df_año, x='Sexo', y='Nivel_Ingresos',
                          color='Sexo',
                          color_discrete_sequence=['#800020', '#FFD700'],
                          title=f"Ingreso Promedio por Sexo en {año}")

            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp1:
                fig1.write_image(tmp1.name)
                img1_path = tmp1.name

            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp2:
                fig2.write_image(tmp2.name)
                img2_path = tmp2.name

            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, f"Reporte {año}", ln=True)
            pdf.image(img1_path, x=10, y=30, w=180)
            pdf.ln(105)
            pdf.image(img2_path, x=10, y=150, w=180)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            pdf.output(tmp_pdf.name)
            pdf_path = tmp_pdf.name

        with open(pdf_path, "rb") as f:
            st.download_button(
                label="Descargar Reporte PDF",
                data=f,
                file_name="reporte_graficas.pdf",
                mime="application/pdf"
            )
