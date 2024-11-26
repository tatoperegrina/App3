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
