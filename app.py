import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Schedule Operativo 2025", layout="wide")

# Estilo para imitar el formato de celdas pequeñas del Excel adjunto
st.markdown("""
    <style>
    .reportview-container .main .block-container{ max-width: 100%; }
    th { background-color: #f0f2f6 !important; font-size: 10px; padding: 2px !important; }
    td { font-size: 10px; text-align: center !important; padding: 1px !important; width: 30px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📅 SCHEDULE TÉCNICO - GESTIÓN DE TURNOS")

# --- BASE DE DATOS ESTRUCTURADA ---
# Basado en tu tabla, organizamos por parejas (Técnico + Auxiliar)
personal = [
    {"T": "Kevin Jheray", "A": "Javier Enrique", "id": 1},
    {"T": "Jhon Jairo", "A": "Juan David", "id": 2},
    {"T": "Jose Luis", "A": "Deiner Daniel", "id": 3},
    {"T": "Brayan Steven", "A": "Juan Camilo", "id": 4},
    {"T": "Michael Estiven", "A": "Cristian Camilo", "id": 5},
    {"T": "Duberley", "A": "Santiago", "id": 6},
    {"T": "Luis Angel", "A": "Andres Felipe", "id": 7},
    {"T": "Carlos Mario", "A": "Auxiliar Nuevo", "id": 8},
    # Agrega aquí las demás parejas de tu tabla...
]

def calcular_turno(fecha, id_cuadrilla):
    # Lógica de rotación 7 días (Miércoles o Viernes)
    semana = fecha.isocalendar()[1]
    dia_sem = fecha.weekday() # 2=Miércoles, 4=Viernes
    
    # Cuadrilla que cambia los Miércoles
    if id_cuadrilla % 2 != 0:
        es_noche = (semana % 2 == 0 and dia_sem >= 2) or (semana % 2 != 0 and dia_sem < 2)
        if es_noche and id_cuadrilla <= 2: return "N"
    # Cuadrilla que cambia los Viernes
    else:
        es_noche = (semana % 2 != 0 and dia_sem >= 4) or (semana % 2 == 0 and dia_sem < 4)
        if es_noche and id_cuadrilla <= 2: return "N"

    if id_cuadrilla <= 4: return "D"
    if id_cuadrilla <= 6: return "R"
    return "X"

# --- GENERACIÓN DE DATOS ---
mes = st.sidebar.selectbox("Mes", ["Enero", "Febrero"])
m_num = 1 if mes == "Enero" else 2
dias = 31 if mes == "Enero" else 28

columnas = ["Nombre", "Cargo"] + [str(d) for d in range(1, dias + 1)]
filas = []

for p in personal:
    f_t = [p["T"], "Técnico"]
    f_a = [p["A"], "Auxiliar"]
    for d in range(1, dias + 1):
        t = calcular_turno(datetime(2025, m_num, d), p["id"])
        f_t.append(t)
        f_a.append(t)
    filas.append(f_t)
    filas.append(f_a)

df = pd.DataFrame(filas, columns=columnas)

# --- PANEL DE CONTEO (Lo que pediste: cuántos de cada uno) ---
dia_ver = st.slider("Ver resumen del día:", 1, dias, 1)
col_dia = str(dia_ver)
t_n = len(df[(df['Cargo'] == 'Técnico') & (df[col_dia] == 'N')])
a_n = len(df[(df['Cargo'] == 'Auxiliar') & (df[col_dia] == 'N')])
t_d = len(df[(df['Cargo'] == 'Técnico') & (df[col_dia] == 'D')])
a_d = len(df[(df['Cargo'] == 'Auxiliar') & (df[col_dia] == 'D')])

c1, c2 = st.columns(2)
c1.metric("Personal en Noche", f"{t_n} Técnicos / {a_n} Aux")
c2.metric("Personal en Día", f"{t_d} Técnicos / {a_d} Aux")

# --- APLICAR COLORES AL ESTILO EXCEL ---
def color_excel(val):
    if val == "N": return 'background-color: #31859c; color: white'
    if val == "D": return 'background-color: #ffc000; color: black'
    if val == "R": return 'background-color: #92d050; color: black'
    return 'background-color: #ffffff; color: #ccc'

st.dataframe(df.style.applymap(color_excel), height=600)
