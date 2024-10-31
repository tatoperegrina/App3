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
st.write("Este simulador te ayudará a ver los rendimientos de algunos ETfs y a consultar el riesgo.")

# Selección de ETF y periodo de análisis
etf_seleccionado = st.selectbox("Selecciona el ETF", ("SPY", "QQQ", "DIA", "XLF", "VWO", "XLV", "ITB", "SLV", "EWU", "EWT", "EWY", "EZU", "EWC", "EWJ", "EWG", "EWA", "AGG"))   
periodo_seleccionado = st.selectbox("Selecciona el periodo", ("1mo", "3mo", "6mo", "1y", "3y", "5y", "10y"))

# Obtención de datos
st.write(f"Mostrando datos para el ETF {etf_seleccionado} en el periodo {periodo_seleccionado}.")
datos_etf = obtener_datos_etf(etf_seleccionado, periodo_seleccionado)

# Añadimos la calculadora de inversión
st.write("### Calculadora de Inversión")
col1, col2 = st.columns(2)

with col1:
    monto_inicial = st.number_input("Ingresa el monto a invertir (USD)", 
                                   min_value=0.0, 
                                   value=1000.0, 
                                   step=100.0,
                                   format="%.2f")

# Verificación de que los datos fueron obtenidos
if not datos_etf.empty:
    rendimiento, riesgo, rendimiento_periodo = calcular_rendimiento_riesgo(datos_etf)
    
    monto_final = monto_inicial * (1 + rendimiento_periodo)
    ganancia_perdida = monto_final - monto_inicial
    
    with col2:
        st.markdown("""
            <div class="metrics-container">
                <div style="text-align: center;">
                    <h4 style="color: #002B4D;">Monto Final Estimado</h4>
                    <div class="metric-value">${:,.2f}</div>
                    <div style="margin-top: 10px; font-size: 0.9em;">
                        {}: ${:,.2f}
                    </div>
                </div>
            </div>
        """.format(
            monto_final,
            "Ganancia" if ganancia_perdida >= 0 else "Pérdida",
            abs(ganancia_perdida)
        ), unsafe_allow_html=True)

    st.markdown("""
        <div class="metrics-container">
            <h4 style="color: #002B4D;">Detalles de la Inversión</h4>
            <table style="width: 100%;">
                <tr>
                    <td style="padding: 5px;"><strong>Monto Inicial:</strong></td>
                    <td style="text-align: right;">${:,.2f}</td>
                </tr>
                <tr>
                    <td style="padding: 5px;"><strong>Rendimiento del Período:</strong></td>
                    <td style="text-align: right;">{:.2%}</td>
                </tr>
                <tr>
                    <td style="padding: 5px;"><strong>Ganancia/Pérdida:</strong></td>
                    <td style="text-align: right; color: {};">${:,.2f}</td>
                </tr>
                <tr>
                    <td style="padding: 5px;"><strong>Monto Final:</strong></td>
                    <td style="text-align: right;">${:,.2f}</td>
                </tr>
            </table>
        </div>
    """.format(
        monto_inicial,
        rendimiento_periodo,
        "#28a745" if ganancia_perdida >= 0 else "#dc3545",
        abs(ganancia_perdida),
        monto_final
    ), unsafe_allow_html=True)
    
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
    
    # Gráfico de proyección de inversión
    st.write("### Proyección de Inversión en el Tiempo")
    datos_etf["Investment Value"] = monto_inicial * (datos_etf["Close"] / datos_etf["Close"].iloc[0])
    
    fig, ax = plt.subplots()
    sns.lineplot(data=datos_etf, x=datos_etf.index, y="Investment Value", ax=ax, color="#002B4D")
    ax.set_title(f"Proyección de Inversión para {etf_seleccionado}")
    ax.set_xlabel("Fecha")
    ax.set_ylabel("Monto de Inversión (USD)")
    st.pyplot(fig)
else:
    st.write("No se encontró información del ETF seleccionado.")

# Sección de Información de Contacto
st.markdown("""
    <div class="contact-info">
        <h4>Información de Contacto del Asesor</h4>
        <p><strong>Nombre:</strong> Santiago Peregrina Flores</p>
        <p><strong>Celular:</strong> 3312706143</p>
        <p><strong>Correo Electrónico:</strong> 0242856@up.edu.mx</p>
    </div>
""", unsafe_allow_html=True)
