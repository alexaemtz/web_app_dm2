import streamlit as st
import plotly.express as px
import pandas as pd

st.title("Medicamentos del paciente")

meds = {
    "Ácido acetilsalicílico" : ["Analgésico", "No narcótico", "AINE", "Antiagregante plaquetario"],
    "Atorvastatina" : ["Antihiperlipidemiante", "Cardiovascular"],
    "Sulindaco" : ["Analgésico", "No narcótico", "AINE"],
    "Sitagliptina" : ["Antidiabético", "Inhibidor DPP-4"],
    "Metformina" : ["Antidiabético", "Hipoglucemiante oral"],
    "Empagliflozina" : ["Antidiabético", "Inhibidor SGLT2"],
    "Telmisartán" : ["Antihipertensivo", "ARA II"],
    "Paracetamol" : ["Analgésico", "No narcótico", "Antipirético"],
    "Tramadol" : ["Analgésico", "Narcótico", "Opioide"]
}

data = []
for med, cats in meds.items():
    for cat in cats:
        data.append({"Medicamento": med, "Categoría" : cat})
        
df = pd.DataFrame(data)
fig = px.histogram(df, x="Categoría", color="Medicamento", barmode="stack", title="Tipos de medicamentos")
st.plotly_chart(fig)

st.subheader("⚠️Interacciones detectadas en medicamentos")

st.markdown("🔸**Ácido acetilsalicílico + Sulindaco:** Mayor riesgo de úlceras gastrointestinales o sangrado.")
st.markdown("🔸**Sulindaco + Metformina** Mayor riesgo de desarrollar acidosis láctica.")
st.markdown("🔸**Sulindaco + Telmisartán:** Puede reducir los efectos del telmisartán y afectar la función renal.")
st.markdown("🔸**Telmisartán + Ácido acetilsalicílico:** Disminución del efecto antihipertensivo y daño a la función renal.")
st.markdown("🔸**Telmisartán + Empagliflozina:** Riesgo de deshidratación y presión baja.")

st.subheader("🩺 Lista de recomendaciones generales")

st.markdown("🔹**Consulte a su médico** antes de modificar cualquier tratamiento.")
st.markdown("🔹**Evite el alcohol** al ingerir **aspirina, sulindac, metformina o tramadol**, ya que puede aumentar el riesgo de efectos adversos.")
st.markdown("🔹**Limite el consumo de jugo de toronja** si toma **atorvastatina**, ya que puede elevar sus niveles en sangre y aumentar efectos secundarios.")
st.markdown("🔹**Hidrátese bien** si está en tratamiento con **empagliflozina y telmisartán** para evitar deshidratación e hipotensión.")

st.info("ℹ️ Esta guía no reemplaza la consulta médica. Si tiene dudas, consulte a su médico especialista.")