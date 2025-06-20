import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import tempfile

# --- Configuración de página ---
st.set_page_config(page_title="Empleo y Desempleo - Streamlit Cloud", layout="wide")

# --- Datos de ejemplo ---
df = pd.DataFrame({
    "Año": [2020, 2020, 2021, 2021, 2022, 2022, 2023, 2023],
    "Sexo": ["Hombre", "Mujer"] * 4,
    "Nivel_Ingresos": [5000, 7000, 6000, 8000, 6500, 8500, 7000, 9000]
})

# --- Título ---
st.title("Empleo y Desempleo — Streamlit Cloud")

# --- Selección de año ---
año = st.selectbox("Selecciona un año", sorted(df["Año"].unique()))
df_año = df[df["Año"] == año]

# --- Gráficas ---
fig1 = px.histogram(df_año, x="Sexo", color="Sexo",
                    color_discrete_sequence=['#800020', '#FFD700'],
                    title=f"Distribución por Sexo - {año}")

fig2 = px.box(df_año, x="Sexo", y="Nivel_Ingresos", color="Sexo",
              color_discrete_sequence=['#800020', '#FFD700'],
              title=f"Ingreso Promedio por Sexo - {año}")

st.plotly_chart(fig1, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)

# --- Botones para descargar cada gráfica como HTML (seguro en Cloud) ---
html1 = fig1.to_html(full_html=True).encode()
html2 = fig2.to_html(full_html=True).encode()

st.download_button(
    "Descargar Distribución por Sexo (HTML)",
    html1,
    file_name=f"Distribucion_Sexo_{año}.html",
    mime="text/html"
)

st.download_button(
    "Descargar Ingreso Promedio por Sexo (HTML)",
    html2,
    file_name=f"Ingreso_Sexo_{año}.html",
    mime="text/html"
)

# --- Generar PDF SOLO con TEXTO (sin imágenes para evitar kaleido) ---
if st.button("Generar PDF de Reporte (Texto)"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"Reporte Empleo y Desempleo - {año}", ln=True)

    pdf.set_font("Arial", size=12)
    texto = f"""
Reporte de Análisis de Empleo y Desempleo para el Estado de México - Año {año}

Este documento es un resumen generado en la nube.
Incluye:
- Distribución por sexo del empleo.
- Rango de ingresos promedio por sexo.
- Para ver las gráficas interactivas, descárgalas desde la app como archivos HTML.

Características Clave:
- Año: {año}
- Variables: Sexo, Nivel de Ingresos
- Información generada desde plataforma Streamlit Cloud.

Gracias por usar esta plataforma.
    """
    pdf.multi_cell(0, 10, texto)

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_pdf:
        pdf.output(tmp_pdf.name)
        pdf_path = tmp_pdf.name

    with open(pdf_path, "rb") as f:
        st.download_button(
            "Descargar PDF de Reporte (Texto)",
            f,
            file_name=f"reporte_texto_{año}.pdf",
            mime="application/pdf"
        )
