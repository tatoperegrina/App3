import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Configuración de la página y estilo
st.set_page_config(page_title="Simulador y Predicción de ETFs", layout="centered")
st.markdown(
    """
    <style>
    .stApp {background-color: #E8E8E8;}
    h1, h2, h3, h4 {color: #002B4D;}
    .css-1lcbmhc {padding-top: 1.5rem;}
    </style>
    """, unsafe_allow_html=True
)

# Función para obtener datos financieros de un ETF de Yahoo Finance
def obtener_datos_etf(ticker, periodo):
    etf = yf.Ticker(ticker)
    datos = etf.history(period=periodo)
    return datos

# Función para entrenar modelo de predicción
def entrenar_modelo(datos, dias_prediccion):
    datos['Dias'] = np.arange(len(datos))
    X = datos[['Dias']]
    y = datos['Close']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    modelo = LinearRegression()
    modelo.fit(X_train, y_train)
    prediccion = modelo.predict(np.arange(len(datos), len(datos) + dias_prediccion).reshape(-1, 1))
    return prediccion, modelo

# Descripciones breves de los ETFs
descripciones_etfs = {
    "SPY": "SPY: ETF que sigue el índice S&P 500.",
    "QQQ": "QQQ: ETF que sigue el índice Nasdaq-100.",
    "DIA": "DIA: ETF que sigue el índice Dow Jones.",
    "XLF": "XLF: ETF centrado en el sector financiero.",
    "VWO": "VWO: ETF de mercados emergentes.",
    "XLV": "XLV: ETF del sector salud.",
    "ITB": "ITB: ETF del sector de construcción.",
    "SLV": "SLV: ETF que sigue el precio de la plata.",
    "EWU": "EWU: ETF de Reino Unido.",
    "EWT": "EWT: ETF de Taiwán.",
    "EWY": "EWY: ETF de Corea del Sur.",
    "EZU": "EZU: ETF de la eurozona.",
    "EWC": "EWC: ETF de Canadá.",
    "EWJ": "EWJ: ETF de Japón.",
    "EWG": "EWG: ETF de Alemania.",
    "EWA": "EWA: ETF de Australia.",
    "AGG": "AGG: ETF de bonos de EE.UU.",
}

# Configuración de la aplicación
st.title("Simulador y Predicción de ETFs")
st.write("Analiza y proyecta el comportamiento de los ETFs. IMPORTANTE: Ningún resultado está garantizado. Toma tus decisiones con precaución.")

# Selección de ETFs
etf_seleccionado1 = st.selectbox("Selecciona el primer ETF", descripciones_etfs.keys())
st.caption(descripciones_etfs[etf_seleccionado1])
etf_seleccionado2 = st.selectbox("Selecciona el segundo ETF (opcional)", ["Ninguno"] + list(descripciones_etfs.keys()))
if etf_seleccionado2 != "Ninguno":
    st.caption(descripciones_etfs[etf_seleccionado2])

# Selección de periodo
periodo_seleccionado = st.selectbox("Selecciona el periodo de análisis", ["1y", "3y", "5y", "10y"])

# Ingreso de monto y horizonte de predicción
monto_inicial = st.number_input("Ingresa el monto a invertir (USD)", min_value=0.0, value=1000.0, step=100.0, format="%.2f")
horizonte_prediccion = st.number_input("Ingresa el horizonte de predicción (en días)", min_value=30, max_value=365, step=30, value=90)

# Lista para almacenar datos de los ETFs seleccionados
etfs_datos = []

# Función para mostrar resultados y predicciones
def mostrar_resultados(etf_ticker, monto_inicial, color, horizonte_prediccion):
    datos_etf = obtener_datos_etf(etf_ticker, periodo_seleccionado)
    if datos_etf.empty:
        st.write(f"No se encontró información para el ETF {etf_ticker}.")
        return None
    
    # Predicción de Machine Learning
    prediccion, modelo = entrenar_modelo(datos_etf, horizonte_prediccion)
    fechas_prediccion = pd.date_range(datos_etf.index[-1], periods=horizonte_prediccion + 1, freq="D")[1:]
    
    # Almacena datos en lista
    etfs_datos.append((etf_ticker, datos_etf, prediccion, fechas_prediccion))
    
    # Resultados para el ETF actual
    st.markdown(f"### Resultados para {etf_ticker}")
    st.write(f"Predicción del precio de cierre para los próximos {horizonte_prediccion} días.")
    
    # Gráfico de predicción
    fig, ax = plt.subplots()
    ax.plot(datos_etf.index, datos_etf['Close'], label="Precio Histórico", color=color)
    ax.plot(fechas_prediccion, prediccion, label="Predicción", linestyle="--", color="#FF5733")
    ax.set_title(f"Predicción para {etf_ticker}")
    ax.set_xlabel("Fecha")
    ax.set_ylabel("Precio de Cierre (USD)")
    ax.legend()
    st.pyplot(fig)

# Mostrar resultados y predicciones para el primer ETF
mostrar_resultados(etf_seleccionado1, monto_inicial, "#002B4D", horizonte_prediccion)

# Mostrar resultados y predicciones para el segundo ETF si es distinto de "Ninguno"
if etf_seleccionado2 != "Ninguno" and etf_seleccionado2 != etf_seleccionado1:
    mostrar_resultados(etf_seleccionado2, monto_inicial, "#FF5733", horizonte_prediccion)
