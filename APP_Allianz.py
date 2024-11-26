import streamlit as st
import yfinance as yf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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
st.write("Este simulador te ayudará a ver los rendimientos de algunos ETFs y a consultar el riesgo. IMPORTANTE, ningún rendimiento o resultado está garantizado. Tome sus decisiones con precaución.")

# Selección de uno o dos ETFs y periodo de análisis
etf_seleccionado1 = st.selectbox("Selecciona el primer ETF", ("SPY", "QQQ", "DIA", "XLF", "VWO", "XLV", "ITB", "SLV", "EWU", "EWT", "EWY", "EZU", "EWC", "EWJ", "EWG", "EWA", "AGG"))   
etf_seleccionado2 = st.selectbox("Selecciona el segundo ETF (opcional)", ("Ninguno", "SPY", "QQQ", "DIA", "XLF", "VWO", "XLV", "ITB", "SLV", "EWU", "EWT", "EWY", "EZU", "EWC", "EWJ", "EWG", "EWA", "AGG"))
periodo_seleccionado = st.selectbox("Selecciona el periodo", ("1mo", "3mo", "6mo", "1y", "3y", "5y", "10y"))

# Obtención de datos
monto_inicial = st.number_input("Ingresa el monto a invertir (USD)", min_value=0.0, value=1000.0, step=100.0, format="%.2f")

# Lista para almacenar datos de los ETFs seleccionados
etfs_datos = []

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
            <p><span style="color: {'#28a745' if ganancia_perdida >= 0 else '#dc3545'};">{'Ganancia' if ganancia_perdida >= 0 else 'Pérdida'}: ${abs(ganancia_perdida):,.2f}</span></p>
        </div>
        <div class="metrics-container">
            <h4 style="color: {color};">Detalles de la Inversión</h4>
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
                    <h4 style="color: {color};">Rendimiento Anualizado</h4>
                    <div>{rendimiento:.2%}</div>
                </div>
                <div style="text-align: center;">
                    <h4 style="color: {color};">Riesgo Anualizado</h4>
                    <div>{riesgo:.2%}</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Interpretación del Rendimiento y Riesgo
    st.write("#### Interpretación de las Métricas:")
    st.write(f"**Rendimiento Anualizado:** Representa el promedio del crecimiento esperado por año basado en los datos históricos del ETF **{etf_ticker}**. Este valor no garantiza rendimientos futuros, pero es útil para estimar el comportamiento potencial.")
    st.write(f"**Riesgo Anualizado:** Indica la volatilidad del ETF **{etf_ticker}**, es decir, qué tan fluctuante es su rendimiento anual. Un valor más alto implica mayor incertidumbre en los resultados.")

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

ax.set_title("Histórico")
ax.set_xlabel("Fecha")
ax.set_ylabel("Monto de Inversión (USD)")
ax.legend(title="ETF")

st.pyplot(fig)

benchmark = st.selectbox("Selecciona un índice de referencia", ("^GSPC", "^IXIC", "^DJI"))
datos_benchmark = obtener_datos_etf(benchmark, periodo_seleccionado)
rendimiento_benchmark = calcular_rendimiento_riesgo(datos_benchmark)[0]
st.write(f"Rendimiento anualizado del índice {benchmark}: {rendimiento_benchmark:.2%}")

from sklearn.linear_model import LinearRegression
modelo = LinearRegression()
datos_etf['Tiempo'] = range(len(datos_etf))
modelo.fit(datos_etf[['Tiempo']], datos_etf['Close'])
prediccion = modelo.predict([[len(datos_etf) + 30]])  # Precio en 30 días
st.write(f"Predicción del precio del ETF en 30 días: ${prediccion[0]:.2f}")



# Sección de Información de Contacto
st.markdown("""
    <div class="contact-info">
        <h4>Información de Contacto del Asesor</h4>
        <p><strong>Nombre:</strong> Santiago Peregrina Flores</p>
        <p><strong>Celular:</strong> 3312706143</p>
        <p><strong>Correo Electrónico:</strong> 0242856@up.edu.mx</p>
    </div>
""", unsafe_allow_html=True)
