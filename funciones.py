import pandas as pd
import re
from sklearn.linear_model import LinearRegression, LogisticRegression

def cargar_datos(ruta):
    """Carga el archivo CSV como DataFrame"""
    return pd.read_csv(ruta)

def convertir_rango_ingreso(valor):
    """
    Convierte un rango de ingreso tipo '$5,001 - $10,000' a promedio numérico.
    Soporta valores sin coma o con espacios. Devuelve float o None.
    """
    try:
        if isinstance(valor, str):
            # Eliminar símbolos $, comas y espacios
            partes = valor.replace("$", "").replace(",", "").split("-")
            numeros = [float(p.strip()) for p in partes if p.strip().replace('.', '', 1).isdigit()]
            if len(numeros) == 2:
                return sum(numeros) / 2
            elif len(numeros) == 1:
                return numeros[0]
            else:
                return None
        else:
            return float(valor)
    except:
        return None  # Si algo falla, devuelve None

def modelo_regresion(df, edad, sexo):
    """
    Modelo de regresión lineal para predecir ingreso.
    Usa Edad + Sexo codificado como dummy.
    """
    data = df[['Edad', 'Sexo', 'Nivel_Ingresos']].dropna()

    data['Edad'] = pd.to_numeric(data['Edad'], errors='coerce')
    data['Nivel_Ingresos'] = data['Nivel_Ingresos'].apply(convertir_rango_ingreso)

    data = data.dropna()

    X = pd.get_dummies(data[['Edad', 'Sexo']], drop_first=True)
    y = data['Nivel_Ingresos']

    model = LinearRegression()
    model.fit(X, y)

    input_data = pd.DataFrame({'Edad': [edad]})
    for col in X.columns:
        if col.startswith("Sexo_"):
            input_data[col] = 1 if col.split("_")[1] == sexo else 0
    for col in X.columns:
        if col not in input_data:
            input_data[col] = 0

    return model.predict(input_data)[0]

def modelo_clasificacion(df, edad, sexo):
    """
    Modelo de clasificación para predecir tipo de empleo: Formal o Informal.
    Usa Edad y Sexo.
    """
    data = df[['Edad', 'Sexo', 'Tipo_Empleo']].dropna()
    data['Edad'] = pd.to_numeric(data['Edad'], errors='coerce')
    data = data.dropna()

    X = pd.get_dummies(data[['Edad', 'Sexo']], drop_first=True)
    y = data['Tipo_Empleo']

    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)

    input_data = pd.DataFrame({'Edad': [edad]})
    for col in X.columns:
        if col.startswith("Sexo_"):
            input_data[col] = 1 if col.split("_")[1] == sexo else 0
    for col in X.columns:
        if col not in input_data:
            input_data[col] = 0

    return model.predict(input_data)[0]
