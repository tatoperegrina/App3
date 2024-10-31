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

# Función para obtener datos financieros de un ETF de Yahoo Finance
def obtener_datos_etf(ticker, periodo):
    etf = yf.Ticker(ticker)
    datos = etf.history(period=periodo)
    return datos

# Cálculo de rendimiento y riesgo
def calcular_rendimiento_riesgo(datos):
    rendimiento = datos['Close'].pct_change().mean() * 252
    riesgo = datos['Close'].pct_change().std() * (252 ** 0.5)
    rendimiento_periodo = (datos['Close'][-1] - datos['Close'][0]) / datos['Close'][0]
    return rendimiento, riesgo, rendimiento_periodo

# Configuración de la aplicación
st.title("Allianz Patrimonial - Simulador y Consulta de Rendimientos de los ETFs")
st.write("Este simulador te ayudará a ver los rendimientos de algunos ETFs y a consultar el riesgo.")

# Selección de uno o dos ETFs y periodo de análisis
etf_seleccionado1 = st.selectbox("Selecciona el primer ETF", ("SPY", "QQQ", "DIA", "XLF", "VWO", "XLV", "ITB", "SLV", "EWU", "EWT", "EWY", "EZU", "EWC", "EWJ", "EWG", "EWA", "AGG"))   
etf_seleccionado2 = st.selectbox("Selecciona el segundo ETF (opcional)", ("Ninguno", "SPY", "QQQ", "DIA", "XLF", "VWO", "XLV", "ITB", "SLV", "EWU", "EWT", "EWY", "EZU", "EWC", "EWJ", "EWG", "EWA", "AGG"))
periodo_seleccionado = st.selectbox("Selecciona el periodo para la proyección", ("1 Año", "3 Años", "5 Años", "10 Años"))

# Conversión del periodo en años
periodos_anos = {"1 Año": 1, "3 Años": 3, "5 Años": 5, "10 Años": 10}
anos = periodos_anos[periodo_seleccionado]

# Obtención del monto inicial
monto_inicial = st.number_input("Ingresa el monto a invertir (USD)", min_value=0.0, value=1000.0, step=100.0, format="%.2f")

# Lista para almacenar datos de los ETFs seleccionados
etfs_info = []

# Función para mostrar resultados de un ETF específico
def mostrar_resultados(etf_ticker, monto_inicial, color):
    datos_etf = obtener_datos_etf(etf_ticker, "5y")  # Se usa un periodo de 5 años para calcular el rendimiento histórico
    if datos_etf.empty:
        st.write(f"No se encontró información para el ETF {etf_ticker}.")
        return None
    
    # Calcula el rendimiento y el riesgo
    rendimiento, riesgo, rendimiento_periodo = calcular_rendimiento_riesgo(datos_etf)
    monto_final = monto_inicial * (1 + rendimiento_periodo)
    ganancia_perdida = monto_final - monto_inicial
    
    # Almacena información del ETF para proyección futura
    etfs_info.append((etf_ticker, rendimiento, color))

    # Resultados para el ETF actual
    st.markdown(f"### Resultados para {etf_ticker}")
    st.markdown(f"""
        <div class="metrics-container">
            <h4 style="color: #002B4D;">Monto Final Estimado</h4>
            <div style="font-size: 1.2em; font-weight: bold;">${monto_final:,.2f}</div>
            <p><span style="color: {'#28a745' if ganancia_perdida >= 0 else '#dc3545'};">{'Ganancia' if ganancia_perdida >= 0 else 'Pérdida'}: ${abs(ganancia_perdida):,.2f}</span></p>
        </div>
        <div class="metrics-container">
            <h4 style="color: #002B4D;">Detalles de la Inversión</h4>
            <table style="width: 100%;">
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
        <div class="metrics-container">
            <div style="display: flex; justify-content: space-around;">
                <div style="text-align: center;">
                    <h4 style="color: #002B4D;">Rendimiento Anualizado</h4>
                    <div>{rendimiento:.2%}</div>
                </div>
                <div style="text-align: center;">
                    <h4 style="color: #002B4D;">Riesgo Anualizado</h4>
                    <div>{riesgo:.2%}</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Mostrar resultados para el primer ETF
mostrar_resultados(etf_seleccionado1, monto_inicial, "#002B4D")

# Mostrar resultados para el segundo ETF si es distinto de "Ninguno"
if etf_seleccionado2 != "Ninguno" and etf_seleccionado2 != etf_seleccionado1:
    mostrar_resultados(etf_seleccionado2, monto_inicial, "#002B4D")

# Gráfica de proyección de inversión para el futuro
st.write(f"### Proyección de Inversión en el Futuro ({periodo_seleccionado})")

fig, ax = plt.subplots()

# Crear proyección futura para cada ETF seleccionado
for etf_ticker, rendimiento_anual, color in etfs_info:
    # Generar fechas futuras para la proyección
    fechas = pd.date_range(start=pd.Timestamp.today(), periods=anos + 1, freq='Y')
    proyeccion_montos = [monto_inicial * (1 + rendimiento_anual)**i for i in range(anos + 1)]
    
    # Graficar proyección
    ax.plot(fechas, proyeccion_montos, marker="o", linestyle="--", color=color, label=etf_ticker)

ax.set_title("Proyección de Inversión Futura")
ax.set_xlabel("Fecha")
ax.set_ylabel("Monto de Inversión (USD)")
ax.legend(title="ETF")

st.pyplot(fig)

# Sección de Información de Contacto
st.markdown("""
    <div class="contact-info">
        <h4>Información de Contacto del Asesor</h4>
        <p><strong>Nombre:</strong> Santiago Peregrina Flores</p>
        <p><strong>Celular:</strong> 3312706143</p>
        <p><strong>Correo Electrónico:</strong> 0242856@up.edu.mx</p>
    </div>
""", unsafe_allow_html=True)
