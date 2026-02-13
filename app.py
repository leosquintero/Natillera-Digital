import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configuración visual de la página
st.set_page_config(page_title="Natillera Digital MVP", page_icon="💰", layout="wide")

# Estilo CSS para mejorar la estética "Fintech"
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1f2937; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("💰 Natillera Digital")
st.markdown("### Simulador de Interés Compuesto para Inversionistas")

# --- BARRA LATERAL (Inputs para que el inversionista juegue) ---
with st.sidebar:
    st.header("🎮 Parámetros del Fondo")
    cuota_mensual = st.number_input("Cuota por persona (COP)", value=200000, step=50000)
    tasa_mensual = st.slider("Tasa de Interés Mensual (%)", 0.1, 5.0, 1.2)
    meses = st.select_slider("Plazo del Ciclo (Meses)", options=[6, 12, 18, 24], value=12)
    penalidad = st.slider("Penalidad por retiro anticipado (%)", 0, 100, 50)

# --- MOTOR FINANCIERO ---
def calcular_datos(cuota, tasa_pct, tiempo):
    n_miembros = 10
    tasa = tasa_pct / 100
    datos = []
    saldo_fondo = 0
    ahorro_lineal = 0
    
    for m in range(1, tiempo + 1):
        aporte_grupo = cuota * n_miembros
        # Fórmula: Saldo_Nuevo = (Saldo_Anterior + Aportes_Nuevos) * (1 + Tasa)
        saldo_fondo = (saldo_fondo + aporte_grupo) * (1 + tasa)
        
        ahorro_lineal += cuota
        saldo_miembro = saldo_fondo / n_miembros
        ganancia = saldo_miembro - ahorro_lineal
        
        # Valor de rescate (Ahorro + Ganancia tras penalidad)
        rescate = ahorro_lineal + (ganancia * (1 - (penalidad/100)))
        
        datos.append({
            "Mes": m,
            "Mi Saldo": saldo_miembro,
            "Mi Ahorro": ahorro_lineal,
            "Ganancia": ganancia,
            "Rescate": rescate
        })
    return pd.DataFrame(datos)

df = calcular_datos(cuota_mensual, tasa_mensual, meses)
resultado_final = df.iloc[-1]

# --- DASHBOARD PRINCIPAL ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Aportado", f"${resultado_final['Mi Ahorro']:,.0f}")
with col2:
    st.metric("Saldo Proyectado", f"${resultado_final['Mi Saldo']:,.0f}", 
              delta=f"{(tasa_mensual):.1f}% interés")
with col3:
    st.metric("Ganancia Total", f"${resultado_final['Ganancia']:,.0f}", delta="Inversión Progresiva")

# --- GRÁFICA INTERACTIVA ---
fig = go.Figure()
fig.add_trace(go.Scatter(x=df["Mes"], y=df["Mi Saldo"], name="Natillera Digital", 
                         line=dict(color='#00ff88', width=4)))
fig.add_trace(go.Scatter(x=df["Mes"], y=df["Mi Ahorro"], name="Ahorro Lineal", 
                         line=dict(color='white', dash='dash')))
fig.add_trace(go.Scatter(x=df["Mes"], y=df["Rescate"], name="Valor de Retiro", 
                         fill='tonexty', line=dict(color='orange')))

fig.update_layout(template="plotly_dark", hovermode="x unified", height=500,
                  yaxis_title="Pesos Colombianos (COP)", xaxis_title="Meses")
st.plotly_chart(fig, use_container_width=True)

st.info(f"💡 En el mes {meses}, habrás ganado ${resultado_final['Ganancia']:,.0f} más que ahorrando solo.")