import streamlit as st
import yfinance as yf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

# Configuración de la página y estilo
st.set_page_config(page_title="Simulador y Consulta de Rendimientos de los ETFs", layout="centered")
st.markdown(
    """
    <style>
    .stApp {background-color: #E8E8E8;}
    h1, h2, h3, h4 {color: #002B4D;}
    .css-1lcbmhc {padding-top: 1.5rem;}
    .metric-value {
        font-size: 1.2em;
        font-weight: bold;
        color: #002B4D;
    }
    .metrics-container {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .contact-info {
        margin-top: 50px;
        text-align: center;
        font-family: Arial, sans-serif;
        color: #002B4D;
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .contact-info h4 {
        font-size: 1.2em;
    }
    .contact-info p {
        font-size: 1em;
        margin: 5px 0;
    }
    </style>
    """, unsafe_allow_html=True
)

# Descripciones de ETFs
descripciones_etfs = {
    "SPY": "SPY: Sigue el índice S&P 500, compuesto por 500 empresas de gran capitalización en EE.UU.",
    "QQQ": "QQQ: Sigue el índice Nasdaq-100, enfocado en empresas tecnológicas de alta innovación.",
    "DIA": "DIA: Replica el índice Dow Jones Industrial Average, que incluye 30 grandes empresas de EE.UU.",
    "XLF": "XLF: ETF que invierte en empresas del sector financiero como bancos y aseguradoras.",
    "VWO": "VWO: ETF de mercados emergentes, enfocado en países en desarrollo.",
    "XLV": "XLV: ETF del sector salud, que incluye farmacéuticas y biotecnológicas.",
    "ITB": "ITB: ETF del sector de construcción e inmobiliario en EE.UU.",
    "SLV": "SLV: Sigue el precio de la plata física como inversión.",
    "EWU": "EWU: ETF que invierte en empresas del Reino Unido.",
    "EWT": "EWT: ETF centrado en el mercado de Taiwán.",
    "EWY": "EWY: ETF que invierte en empresas de Corea del Sur.",
    "EZU": "EZU: ETF que representa la zona euro.",
    "EWC": "EWC: ETF que invierte en empresas canadienses.",
    "EWJ": "EWJ: ETF centrado en el mercado japonés.",
    "EWG": "EWG: ETF que representa a las principales empresas de Alemania.",
    "EWA": "EWA: ETF que invierte en el mercado australiano.",
    "AGG": "AGG: ETF que replica el mercado de bonos en EE.UU.",
}

# Configuración de la aplicación
st.title("Simulador y Consulta de Rendimientos de los ETFs")
st.write("Este simulador te ayudará a ver los rendimientos de algunos ETFs y a consultar el riesgo. IMPORTANTE, ningún rendimiento o resultado está garantizado. Tome sus decisiones con precaución.")

# Selección de ETFs con descripciones
etf_seleccionado1 = st.selectbox("Selecciona el primer ETF", descripciones_etfs.keys())
st.caption(descripciones_etfs[etf_seleccionado1])  # Mostrar descripción del primer ETF

etf_seleccionado2 = st.selectbox("Selecciona el segundo ETF (opcional)", ["Ninguno"] + list(descripciones_etfs.keys()))
if etf_seleccionado2 != "Ninguno":
    st.caption(descripciones_etfs[etf_seleccionado2])  # Mostrar descripción del segundo ETF

# Selección del periodo
periodo_seleccionado = st.selectbox("Selecciona el periodo", ("1mo", "3mo", "6mo", "1y", "3y", "5y", "10y"))

# Obtención de datos y lógica de análisis (sin cambios)
monto_inicial = st.number_input("Ingresa el monto a invertir (USD)", min_value=0.0, value=1000.0, step=100.0, format="%.2f")
etfs_datos = []

# Resto del código permanece igual, incluyendo las funciones de cálculo, resultados y gráficas
# Función para mostrar resultados y gráficas...
# ...
