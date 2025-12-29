import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Configuración de la Web
st.set_page_config(page_title="Gestión de Cuadrillas Operativas", layout="wide")

st.title("📊 Control de Turnos: 8 Cuadrillas (4+2+2)")

# --- BASE DE DATOS DE PERSONAL (Separados por Cargo) ---
tecnicos = ["Kevin Jheray", "Jhon Jairo", "Jose Luis", "Brayan Steven", "Michael Estiven", "Duberley", "Luis Angel", "Andres Felipe"]
auxiliares = ["Javier Enrique", "Juan David", "Deiner Daniel", "Juan Camilo", "Cristian Camilo", "Santiago", "Carlos Mario", "Nuevo Auxiliar"]

def obtener_turno(fecha, es_tecnico, indice):
    dia_semana = fecha.weekday() # 2=Miércoles, 4=Viernes
    
    # Lógica de rotación Noche (N) en Miércoles y Viernes
    if (dia_semana == 2 or dia_semana == 4) and indice < 2:
        return "N"
    
    # Distribución de las 8 cuadrillas
    if indice < 4: return "D"  # 4 Cuadrillas Día
    if indice < 6: return "R"  # 2 Cuadrillas Reactivación
    if indice < 8: return "N"  # 2 Cuadrillas Noche
    return "X" # Descanso

# --- INTERFAZ WEB ---
st.sidebar.header("Opciones de Visualización")
mes = st.sidebar.radio("Seleccione Mes", ["Enero", "Febrero"])

st.subheader(f"Programación Detallada - {mes} 2025")

# Generar Tabla
dias = 31 if mes == "Enero" else 28
columnas = [f"{(datetime(2025, 1 if mes=='Enero' else 2, d+1)).strftime('%a %d')}" for d in range(dias)]

# Crear filas para Técnicos y Auxiliares por separado
data = []
for i in range(len(tecnicos)):
    fila_t = [obtener_turno(datetime(2025, 1 if mes=='Enero' else 2, d+1), True, i) for d in range(dias)]
    data.append([tecnicos[i], "Técnico"] + fila_t)
    
    fila_a = [obtener_turno(datetime(2025, 1 if mes=='Enero' else 2, d+1), False, i) for d in range(dias)]
    data.append([auxiliares[i], "Auxiliar"] + fila_a)

df = pd.DataFrame(data, columns=["Nombre", "Cargo"] + columnas)

# Aplicar Colores
def style_turnos(val):
    if val == "N": return 'background-color: #002b36; color: white' # Noche
    if val == "R": return 'background-color: #2aa198; color: white' # Reactivación
    if val == "D": return 'background-color: #b58900; color: white' # Día
    return ''

st.dataframe(df.style.applymap(style_turnos), height=500)

st.info("✅ El sistema detecta automáticamente los Miércoles y Viernes para el ingreso de nuevas cuadrillas a Noche.")
