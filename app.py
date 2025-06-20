import streamlit as st
import pandas as pd
import plotly.express as px
from funciones import cargar_datos, modelo_regresion, modelo_clasificacion
from fpdf import FPDF
import tempfile
import os

st.set_page_config(page_title="Empleo y Desempleo", layout="wide")

# Título y estilos
st.markdown("""
    <style>
    .title { text-align: center; color: #800020; font-size: 3em; }
    </style>
    <h1 class='title'>🇲🇽 Empleo y Desempleo Estado de México</h1>
""", unsafe_allow_html=True)

# Navegación
nav_items = ["Inicio", "2020", "2021", "2022", "2023", "2024", "Predicción", "Descargas"]
nav = st.query_params.get("page")
if nav in nav_items:
    seccion = nav
else:
    seccion = "Inicio"

nav_html = "".join([f"<a href='?page={i}' style='margin:10px;'>{i}</a>" for i in nav_items])
st.markdown(f"<div style='text-align:center'>{nav_html}</div>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# Cargar datos
df = cargar_datos("data/empleodesempleo.csv")

# Inicio
if seccion == "Inicio":
    st.write("## Introducción")
    st.write("""
    El Estado de México es uno de los centros económicos más importantes...
    (Aquí puedes extender tu texto a ~400 palabras sobre características, empleo formal e informal,
    estado con más empleo, niveles de desempleo, recuperación post-pandemia, retos, etc.)
    """)
    st.dataframe(df)

# Por año
elif seccion in ["2020", "2021", "2022", "2023", "2024"]:
    año = int(seccion)
    df_año = df[df['Año'] == año]

    st.write(f"## Análisis {año}")
    fig1 = px.histogram(df_año, x='Sexo', color='Sexo', title=f"Distribución por Sexo {año}")
    st.plotly_chart(fig1)

    fig2 = px.box(df_año, x='Sexo', y='Nivel_Ingresos', color='Sexo', title=f"Ingreso por Sexo {año}")
    st.plotly_chart(fig2)

# Predicción
elif seccion == "Predicción":
    edad = st.slider("Edad", 18, 100, 30)
    sexo = st.selectbox("Sexo", df['Sexo'].unique())
    if st.button("Predecir Ingreso"):
        st.write(modelo_regresion(df, edad, sexo))
    if st.button("Predecir Categoría"):
        st.write(modelo_clasificacion(df, edad, sexo))

# Descargas
elif seccion == "Descargas":
    st.write("## 📄 Descargar PDF con Gráficas")
    if st.button("Generar PDF"):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)

        for año in range(2020, 2025):
            df_año = df[df['Año'] == año]
            fig1 = px.histogram(df_año, x='Sexo', color='Sexo', title=f"Distribución por Sexo {año}")
            fig2 = px.box(df_año, x='Sexo', y='Nivel_Ingresos', color='Sexo', title=f"Ingreso por Sexo {año}")

            # Guardar imágenes temporalmente usando kaleido
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp1:
                fig1.write_image(tmp1.name)
                img1_path = tmp1.name
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp2:
                fig2.write_image(tmp2.name)
                img2_path = tmp2.name

            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, f"Reporte {año}", ln=True)
            pdf.image(img1_path, x=10, y=30, w=180)
            pdf.ln(105)
            pdf.image(img2_path, x=10, y=150, w=180)

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_pdf:
            pdf.output(tmp_pdf.name)
            pdf_path = tmp_pdf.name

        with open(pdf_path, "rb") as f:
            st.download_button("📄 Descargar PDF", f, file_name="reporte.pdf", mime="application/pdf")
