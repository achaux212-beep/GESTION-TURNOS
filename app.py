import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Configuración visual
st.set_page_config(page_title="Gestor de Cuadrillas 8x8", layout="wide")

st.title("⚡ Sistema de Gestión de Turnos (4+2+2)")
st.markdown("### Control de Personal: Enero y Febrero 2025")

# Lista de personal basada en tu archivo (resumen)
personal = [
    "Kevin Jheray", "Javier Enrique", "Jhon Jairo", "Juan David", 
    "Jose Luis", "Deiner Daniel", "Brayan Steven", "Juan Camilo",
    "Michael Estiven", "Cristian Camilo", "Duberley", "Santiago",
    "Luis Angel", "Andres Felipe", "Carlos Mario", "Nuevo Auxiliar Enero"
]

# Sidebar para gestión
st.sidebar.header("Panel de Control")
mes_seleccionado = st.sidebar.selectbox("Mes a visualizar", ["Enero", "Febrero"])
st.sidebar.info("Regla aplicada: Ingreso por Noche (7 días) y paso automático a Día.")

# Lógica de asignación de turnos
def generar_turnos(mes_nombre):
    dias = 31 if mes_nombre == "Enero" else 28
    columnas_dias = [f"Día {i+1}" for i in range(dias)]
    df_turnos = pd.DataFrame(index=personal, columns=columnas_dias)
    
    # Simulación de rotación lógica 4+2+2
    for i, persona in enumerate(personal):
        for d in range(dias):
            # Ciclos de 7 días
            ciclo = (d // 7) % 3
            if i < 4: # Grupos de Noche (2 cuadrillas = 4 personas)
                df_turnos.iloc[i, d] = "N" if ciclo == 0 else "D"
            elif i < 12: # Grupos de Día y Reactivación
                df_turnos.iloc[i, d] = "D" if i < 8 else "R"
            else:
                df_turnos.iloc[i, d] = "X" # Descanso
                
    return df_turnos

# Mostrar Dashboard
df_resultado = generar_turnos(mes_seleccionado)

# Estilo de la tabla
def color_turnos(val):
    color = 'white'
    if val == "N": color = '#1f77b4' # Azul Noche
    elif val == "D": color = '#ff7f0e' # Naranja Día
    elif val == "R": color = '#2ca02c' # Verde Reactivación
    return f'background-color: {color}; color: white'

st.write(f"#### Cuadrante de {mes_seleccionado}")
st.dataframe(df_resultado.style.applymap(color_turnos), height=600)

# Resumen de cantidades
st.markdown("---")
col1, col2, col3 = st.columns(3)
col1.metric("Cuadrillas Día", "4 Técnicos + 4 Aux")
col2.metric("Reactivaciones", "2 Técnicos + 2 Aux")
col3.metric("Turno Noche", "2 Técnicos + 2 Aux")
