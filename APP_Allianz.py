import streamlit as st
import yfinance as yf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from etfs_data import ETFs_Data

# Configuración de la página y estilo
st.set_page_config(page_title="Allianz Patrimonial - Simulador y Consulta de Rendimientos de los ETFs", layout="centered")
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
    </style>
    """, unsafe_allow_html=True
)

# Función para obtener datos financieros de un ETF de Yahoo Finance
def obtener_datos_etf(ticker, periodo):
    etf = yf.Ticker(ticker)
    datos = etf.history(period=periodo)
    return datos

# Cálculo de rendimiento y riesgo
def calcular_rendimiento_riesgo(datos):
    rendimiento = datos['Close'].pct_change().mean() * 252
    riesgo = datos['Close'].pct_change().std() * (252 ** 0.5)
    return rendimiento, riesgo

# Configuración de la aplicación
st.title("Allianz Patrimonial - Simulador y Consulta de Rendimientos de los ETFs")
st.write("Este simulador te ayudará a ver los rendimientos de algunos ETfs y a consultar el riesgo.")

# Selección de ETF y periodo de análisis
etf_seleccionado = st.selectbox("Selecciona el ETF", ("SPY", "QQQ", "DIA", "XLF", "VWO", "XLV", "ITB", "SLV", "EWU", "EWT", "EWY", "EZU", "EWC", "EWJ", "EWG", "EWA", "AGG"))   
periodo_seleccionado = st.selectbox("Selecciona el periodo", ("1mo", "3mo", "6mo", "1y", "3y", "5y", "10y"))

# Obtención de datos
st.write(f"Mostrando datos para el ETF {etf_seleccionado} en el periodo {periodo_seleccionado}.")
datos_etf = obtener_datos_etf(etf_seleccionado, periodo_seleccionado)

# Verificación de que los datos fueron obtenidos
if not datos_etf.empty:
    st.write("### Datos Históricos del ETF")
    st.write(datos_etf.tail())

    # Calcula rendimiento y riesgo
    rendimiento, riesgo = calcular_rendimiento_riesgo(datos_etf)
    
    # Contenedor con fondo blanco para las métricas
    st.markdown("""
        <div class="metrics-container">
            <div style="display: flex; justify-content: space-around;">
                <div style="text-align: center;">
                    <h3 style="color: #002B4D;">Rendimiento Anualizado</h3>
                    <div class="metric-value">{}</div>
                </div>
                <div style="text-align: center;">
                    <h3 style="color: #002B4D;">Riesgo Anualizado</h3>
                    <div class="metric-value">{}</div>
                </div>
            </div>
        </div>
    """.format(f"{rendimiento:.2%}", f"{riesgo:.2%}"), unsafe_allow_html=True)

    # Visualización con Seaborn y Pyplot
    st.write("### Gráfico de Precio de Cierre")
    fig, ax = plt.subplots()
    sns.lineplot(data=datos_etf, x=datos_etf.index, y="Close", ax=ax, color="#002B4D")
    ax.set_title(f"Precio de Cierre de {etf_seleccionado} en {periodo_seleccionado}")
    ax.set_xlabel("Fecha")
    ax.set_ylabel("Precio de Cierre (USD)")
    st.pyplot(fig)
else:
    st.write("No se encontró información del ETF seleccionado.")
   