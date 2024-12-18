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

# Obtención de datos
monto_inicial = st.number_input("Ingresa el monto a invertir (USD)", min_value=0.0, value=1000.0, step=100.0, format="%.2f")
etfs_datos = []

# Función para obtener datos financieros de un ETF o índice de Yahoo Finance
def obtener_datos_etf(ticker, periodo):
    etf = yf.Ticker(ticker)
    datos = etf.history(period=periodo)
    return datos

# Cálculo de rendimiento y riesgo
def calcular_rendimiento_riesgo(datos):
    rendimiento = datos['Close'].pct_change().mean() * 252
    riesgo = datos['Close'].pct_change().std() * (252 ** 0.5)
    rendimiento_periodo = (datos['Close'].iloc[-1] - datos['Close'].iloc[0]) / datos['Close'].iloc[0]
    return rendimiento, riesgo, rendimiento_periodo

# Función para mostrar resultados de un ETF específico
def mostrar_resultados(etf_ticker, monto_inicial, color):
    datos_etf = obtener_datos_etf(etf_ticker, periodo_seleccionado)
    if datos_etf.empty:
        st.write(f"No se encontró información para el ETF {etf_ticker}.")
        return None

    # Calcula el rendimiento y el riesgo
    rendimiento, riesgo, rendimiento_periodo = calcular_rendimiento_riesgo(datos_etf)
    monto_final = monto_inicial * (1 + rendimiento_periodo)
    ganancia_perdida = monto_final - monto_inicial

    # Almacena datos en lista
    etfs_datos.append((etf_ticker, datos_etf))

    # Resultados para el ETF actual
    st.markdown(f"### Resultados para {etf_ticker}")
    st.markdown(f"""
        <div class="metrics-container">
            <h4 style="color: {color};">Monto Final Estimado (USD)</h4>
            <div style="font-size: 1.2em; font-weight: bold;">${monto_final:,.2f}</div>
            <p><span style="color: {'#28a745' if ganancia_perdida >= 0 else '#dc3545'};">{'Ganancia ESTIMADA' if ganancia_perdida >= 0 else 'Pérdida ESTIMADA'}: ${abs(ganancia_perdida):,.2f}</span></p>
        </div>
        <div class="metrics-container">
            <h4 style="color: {color};">Detalles de la Inversión</h4>
            <table style="width: 100%; font-size: 1em;">
                <tr>
                    <td><strong>Monto Inicial:</strong></td>
                    <td style="text-align: right;">${monto_inicial:,.2f}</td>
                </tr>
                <tr>
                    <td><strong>Rendimiento del Período:</strong></td>
                    <td style="text-align: right;">{rendimiento_periodo:.2%}</td>
                </tr>
                <tr>
                    <td><strong>Ganancia/Pérdida:</strong></td>
                    <td style="text-align: right; color: {'#28a745' if ganancia_perdida >= 0 else '#dc3545'};">${abs(ganancia_perdida):,.2f}</td>
                </tr>
                <tr>
                    <td><strong>Monto Final:</strong></td>
                    <td style="text-align: right;">${monto_final:,.2f}</td>
                </tr>
            </table>
        </div>
    """, unsafe_allow_html=True)

# Mostrar resultados para el primer ETF
mostrar_resultados(etf_seleccionado1, monto_inicial, "#002B4D")

# Mostrar resultados para el segundo ETF si es distinto de "Ninguno"
if etf_seleccionado2 != "Ninguno" and etf_seleccionado2 != etf_seleccionado1:
    mostrar_resultados(etf_seleccionado2, monto_inicial, "#FF5733")

# Gráfica de proyección de inversión para uno o dos ETFs
st.write("### Gráfico del Precio Histórico")

fig, ax = plt.subplots()

# Crear gráfica para cada ETF seleccionado con colores distintos
for idx, (etf_ticker, datos_etf) in enumerate(etfs_datos):
    color = "#002B4D" if idx == 0 else "#FF5733"  # Color distinto para el segundo ETF
    datos_etf["Investment Value"] = monto_inicial * (datos_etf["Close"] / datos_etf["Close"].iloc[0])
    sns.lineplot(data=datos_etf, x=datos_etf.index, y="Investment Value", ax=ax, label=etf_ticker, color=color)

ax.set_title("Crecimiento del Monto Invertido", fontsize=14)
ax.set_ylabel("Monto (USD)", fontsize=12)
ax.set_xlabel("Fecha", fontsize=12)
ax.legend()
st.pyplot(fig)

# Predicción con regresión lineal
st.write("### Predicción del Precio Futuro")
dias_a_predecir = st.slider("Selecciona el número de días para predecir. ¡Recuerda que NO es garantizado!", 30, 360, step=30)

fig_prediccion, ax_pred = plt.subplots()
for etf_ticker, datos_etf in etfs_datos:
    datos_entrenamiento = datos_etf.reset_index()
    datos_entrenamiento["Tiempo"] = np.arange(len(datos_entrenamiento))
    modelo = LinearRegression()
    X = datos_entrenamiento[["Tiempo"]]
    y = datos_entrenamiento["Close"]
    modelo.fit(X, y)

    # Predicción para cada día hasta el futuro seleccionado
    tiempo_futuro = np.arange(len(X), len(X) + dias_a_predecir).reshape(-1, 1)
    predicciones = modelo.predict(tiempo_futuro)

    # Mostrar predicción final
    st.write(f"El precio estimado para {etf_ticker} en {dias_a_predecir} días es **${predicciones[-1]:.2f}**.")

    # Graficar datos históricos y predicción
    sns.lineplot(x=datos_entrenamiento["Tiempo"], y=y, label=f"Histórico {etf_ticker}", ax=ax_pred)
    sns.lineplot(x=np.arange(len(X), len(X) + dias_a_predecir), y=predicciones, label=f"Predicción {etf_ticker}", linestyle="--", ax=ax_pred)

ax_pred.set_title("Precio Histórico y Proyección")
ax_pred.set_xlabel("Días")
ax_pred.set_ylabel("Precio (USD)")
ax_pred.legend()
st.pyplot(fig_prediccion)

# Sección de Información de Contacto
st.markdown("""
    <div class="contact-info">
        <h4>Información de Contacto del Asesor</h4>
        <p><strong>Nombre:</strong> Santiago Peregrina Flores</p>
        <p><strong>Celular:</strong> 3312706143</p>
        <p><strong>Correo Electrónico:</strong> 0242856@up.edu.mx</p>
    </div>
""", unsafe_allow_html=True)
