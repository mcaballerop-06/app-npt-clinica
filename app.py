import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Seguimiento NPT", layout="wide")

st.title("💉 Seguimiento Clínico – Nutrición Parenteral Total")

# -------------------------
# DATOS DEL PACIENTE
# -------------------------

st.header("Datos del Paciente")

nombre = st.text_input("Nombre del paciente")
peso = st.number_input("Peso (kg)", min_value=0.0, step=0.1)
kcal_totales = st.number_input("Kcal totales administradas", min_value=0.0, step=10.0)

if peso > 0:
    kcal_kg = kcal_totales / peso
    st.metric("Kcal/kg/día", round(kcal_kg, 2))
else:
    kcal_kg = 0

st.divider()

# -------------------------
# LABORATORIOS
# -------------------------

st.header("Laboratorios")

col1, col2, col3 = st.columns(3)

with col1:
    glucosa = st.number_input("Glucemia (mg/dL)", min_value=0)
    fosforo = st.number_input("Fósforo (mg/dL)", min_value=0.0, step=0.1)
    magnesio = st.number_input("Magnesio (mg/dL)", min_value=0.0, step=0.1)

with col2:
    trigliceridos = st.number_input("Triglicéridos (mg/dL)", min_value=0)
    ast = st.number_input("AST (U/L)", min_value=0)
    alt = st.number_input("ALT (U/L)", min_value=0)

with col3:
    sodio = st.number_input("Sodio (mEq/L)", min_value=0)
    potasio = st.number_input("Potasio (mEq/L)", min_value=0.0, step=0.1)
    creatinina = st.number_input("Creatinina (mg/dL)", min_value=0.0, step=0.1)

st.divider()

# -------------------------
# SISTEMA DE ALERTAS
# -------------------------

st.header("🚨 Alertas Clínicas Automáticas")

alertas = []

# Glucosa
if glucosa > 180:
    alertas.append("🔴 Hiperglucemia – evaluar insulina o reducir dextrosa")
elif glucosa < 70 and glucosa > 0:
    alertas.append("🔴 Hipoglucemia – riesgo si suspensión brusca")

# Realimentación
if fosforo > 0 and fosforo < 2.5:
    alertas.append("🟠 Hipofosfatemia – sospechar síndrome de realimentación")

if magnesio > 0 and magnesio < 1.5:
    alertas.append("🟠 Hipomagnesemia – vigilar riesgo arrítmico")

# Lípidos
if trigliceridos > 400:
    alertas.append("🟠 Hipertrigliceridemia – considerar suspender lípidos")

# Hepático
if ast > 40 or alt > 40:
    alertas.append("🟡 Alteración hepática – vigilar colestasis / sobrealimentación")

# Sobrealimentación
if kcal_kg > 30:
    alertas.append("🟠 Posible sobrealimentación (>30 kcal/kg)")

if alertas:
    for alerta in alertas:
        st.warning(alerta)
else:
    st.success("✅ Sin alertas metabólicas actuales")

st.divider()

# -------------------------
# REGISTRO HISTÓRICO
# -------------------------

st.header("📊 Registrar Evolución")

if st.button("Guardar Registro"):
    nuevo_dato = {
        "Fecha": datetime.now(),
        "Paciente": nombre,
        "Glucosa": glucosa,
        "Fósforo": fosforo,
        "Triglicéridos": trigliceridos,
        "AST": ast,
        "ALT": alt,
        "Kcal/kg": round(kcal_kg, 2)
    }

    if "historial" not in st.session_state:
        st.session_state.historial = []

    st.session_state.historial.append(nuevo_dato)
    st.success("Registro guardado")

if "historial" in st.session_state:
    df = pd.DataFrame(st.session_state.historial)
    st.dataframe(df)

    st.subheader("📈 Evolución de Glucosa")
    st.line_chart(df.set_index("Fecha")["Glucosa"])

st.caption("App desarrollada para seguimiento clínico de NPT")
