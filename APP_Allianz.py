import streamlit as st
import yfinance as yf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

# Configuración de la página
st.set_page_config(page_title="Simulador de ETFs", layout="centered")

# Función para obtener datos de ETF con manejo de errores
def obtener_datos_etf(ticker, periodo):
    try:
        etf = yf.Ticker(ticker)
        datos = etf.history(period=periodo)
        if datos.empty:
            st.warning(f"No se encontraron datos para el ETF {ticker}.")
            return None
        return datos
    except Exception as e:
        st.error(f"Error al obtener datos de {ticker}: {e}")
        return None

# Función para calcular rendimiento y riesgo
def calcular_metrica(datos):
    if datos is None:
        return None, None, None
    rendimiento = datos['Close'].pct_change().mean() * 252
    riesgo = datos['Close'].pct_change().std() * (252 ** 0.5)
    rendimiento_periodo = (datos['Close'].iloc[-1] - datos['Close'].iloc[0]) / datos['Close'].iloc[0]
    return rendimiento, riesgo, rendimiento_periodo

# Función para graficar resultados históricos
def graficar_resultados(etfs_datos, monto_inicial):
    fig, ax = plt.subplots()
    for idx, (ticker, datos) in enumerate(etfs_datos):
        color = sns.color_palette("husl", len(etfs_datos))[idx]
        datos['Investment Value'] = monto_inicial * (datos['Close'] / datos['Close'].iloc[0])
        sns.lineplot(data=datos, x=datos.index, y="Investment Value", ax=ax, label=ticker, color=color)
    ax.set_title("Crecimiento de la Inversión")
    ax.set_ylabel("Monto (USD)")
    ax.set_xlabel("Fecha")
    ax.legend(title="ETF")
    st.pyplot(fig)

# Función para predecir con regresión lineal
def predecir_precio(datos, dias_prediccion):
    datos['Tiempo'] = np.arange(len(datos))
    modelo = LinearRegression()
    modelo.fit(datos[['Tiempo']], datos['Close'])
    tiempo_futuro = np.arange(len(datos), len(datos) + dias_prediccion).reshape(-1, 1)
    predicciones = modelo.predict(tiempo_futuro)
    return predicciones

# Título e instrucciones
st.title("Simulador y Predicción de ETFs")
st.write("Seleccione ETFs y analice su comportamiento histórico, riesgos, rendimientos y predicciones futuras.")

# Selección de ETFs
etfs_seleccionados = st.multiselect("Seleccione ETFs", ["SPY", "QQQ", "DIA", "XLF", "VWO", "XLV", "ITB", "SLV"], default=["SPY"])
periodo_seleccionado = st.selectbox("Seleccione el periodo", ["1mo", "3mo", "6mo", "1y", "3y", "5y"])
monto_inicial = st.number_input("Monto inicial (USD)", min_value=100.0, value=1000.0, step=100.0)
dias_a_predecir = st.slider("Días para predecir", 30, 360, step=30)

# Procesar datos y mostrar resultados
etfs_datos = []
for ticker in etfs_seleccionados:
    datos = obtener_datos_etf(ticker, periodo_seleccionado)
    if datos is not None:
        rendimiento, riesgo, rendimiento_periodo = calcular_metrica(datos)
        st.subheader(f"Resultados para {ticker}")
        st.write(f"**Rendimiento anualizado:** {rendimiento:.2%}")
        st.write(f"**Riesgo anualizado:** {riesgo:.2%}")
        st.write(f"**Rendimiento del período:** {rendimiento_periodo:.2%}")
        etfs_datos.append((ticker, datos))
        # Predicción
        predicciones = predecir_precio(datos, dias_a_predecir)
        st.write(f"Precio estimado en {dias_a_predecir} días: ${predicciones[-1]:.2f}")

# Graficar resultados históricos
if etfs_datos:
    graficar_resultados(etfs_datos, monto_inicial)
