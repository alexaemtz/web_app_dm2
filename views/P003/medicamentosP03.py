import streamlit as st
import plotly.express as px
import pandas as pd

st.title("Medicamentos del paciente")

meds = {
    "Sitagliptina" : ["Antidiabético", "Inhibidor DPP-4"],
    "Metformina" : ["Antidiabético", "Hipoglucemiante oral"],
    "Empagliflozina" : ["Antidiabético", "Inhibidor SGLT2"],
    "Telmisartán" : ["Antihipertensivo", "ARA II"],
    "Paracetamol" : ["Analgésico", "No narcótico", "Antipirético"],
    "Nifedipino" : ["Antihipertensivo", "Vasodilatador", "Calcioantagonista"],
    "Complejo B" : ["Suplemento vitamínico", "Vitaminas del grupo B"]
 }

data = []
for med, cats in meds.items():
    for cat in cats:
        data.append({"Medicamento": med, "Categoría" : cat})
        
df = pd.DataFrame(data)
fig = px.histogram(df, x="Categoría", color="Medicamento", barmode="stack", title="Tipos de medicamentos")
st.plotly_chart(fig)

st.subheader("⚠️Interacciones detectadas en medicamentos")

st.markdown("🔸**Nifedipina + Metformina:** Mayor riesgo de desarrollar acidosis láctica.")
st.markdown("🔸**Nifedipina + Empagliflozina:** Pérdida de sales y agua, aumentando el riesgo de deshidratación e hipotensión arterial.")
st.markdown("🔸**Telmisartán + Empagliflozina:** Riesgo de deshidratación y presión baja.")
st.markdown("🔸**Metformina + Empagliflozina:** Mayor riesgo de acidosis láctica y deshidratación, especialmente en pacientes con función renal comprometida.")
st.markdown("🔸**Metformina + Sitagliptina:** Riesgo bajo pero potencial de hipoglucemia, más frecuente si se combinan con otros antidiabéticos.")
st.markdown("🔸**Telmisartán + Nifedipino:** Posible potenciación del efecto hipotensor, riesgo de presión arterial demasiado baja.")
st.markdown("🔸**Nifedipino + Complejo B:** No se espera interacción clínicamente significativa, pero algunos componentes del complejo B pueden alterar la presión en casos sensibles.")
st.markdown("🔸**Empagliflozina + Sitagliptina:** Potencial leve de infecciones urinarias o deshidratación.")
st.markdown("🔸**Paracetamol + Metformina:** En dosis altas o uso crónico, puede aumentar el riesgo de toxicidad hepática y renal.")

st.subheader("🩺 Lista de recomendaciones generales")

st.markdown("🔹**Consulte siempre a su médico antes de iniciar, suspender o combinar medicamentos.**")
st.markdown("🔹**Evite el alcohol** si está tomando **metformina** o **paracetamol**, ya que puede aumentar el riesgo de toxicidad hepática o acidosis láctica.")
st.markdown("🔹**Hidrátese adecuadamente** durante el tratamiento con **empagliflozina, telmisartán o nifedipina** para reducir el riesgo de deshidratación e hipotensión.")
st.markdown("🔹**Monitoree su presión arterial** si está en tratamiento combinado con **telmisartán y nifedipino**.")
st.markdown("🔹**Informe a su médico** si presenta mareo, debilidad o fatiga mientras toma **nifedipino** y **empagliflozina**, ya que podrían indicar presión arterial baja.")
st.markdown("🔹**Evite automedicarse** con analgésicos si ya toma **paracetamol y metformina**, ya que puede afectar la función hepática y renal.")
st.markdown("🔹**Tome metformina con alimentos** para reducir efectos gastrointestinales.")
st.markdown("🔹**Informe a su médico** si experimenta signos de infección urinaria durante el uso de **empagliflozina y/o sitagliptina**.")
st.markdown("🔹**Revise periódicamente su función renal** si está en tratamiento con **empagliflozina**, especialmente si se combina con **metformina** o **telmisartán**.")
st.markdown("🔹**Consulte a su médico** antes de tomar **complejo B** si tiene presión arterial inestable o está en otros tratamientos.")

st.info("ℹ️ Esta guía no reemplaza la consulta médica. Si tiene dudas, consulte a su médico especialista.")