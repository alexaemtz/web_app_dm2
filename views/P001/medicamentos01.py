import streamlit as st
import pandas as pd
import plotly.express as px

meds = {
    "Ácido acetilsalicílico" : ["Analgésico", "No narcótico", "AINE"], 
    "Atorvastatina" : ["Antihiperlipidemiante","Cardiovascular"], 
    "Linagliptina" : ["Antidiabético", "Inhibidor DPP-4"],
    "Metformina" : ["Antidiabético", "Hipoglucemiante oral"], 
    "Empagliflozina" : ["Antidiabético", "Inhibidor SGLT2"], 
    "Telmisartán" : ["Antihipertensivo", "ARA II"],
    "Isosorbida" : ["Cardiovascular", "Vasodilatador"], 
    "Pantoprazol" : ["Protector gástrico", "Inhibidor de bomba de protones"], 
    "Amlodipino" : ["Antihipertensivo", "Calcioantagonista"], 
    "Complejo B" : ["Multivitamínico"], 
    "Clopidogrel" : ["Antiagregante plaquetario"], 
}

data = []
for med, cats in meds.items():
    for cat in cats:
        data.append({"Medicamento" : med, "Categoría" : cat})
        
df = pd.DataFrame(data)
fig = px.histogram(df, x="Categoría", color="Medicamento", barmode="stack", title="Tipos de medicamentos")
st.plotly_chart(fig)

st.subheader("⚠️Interacciones detectadas en medicamentos")

st.markdown("🔸 **Ácido acetilsalicílico + Clopidogrel:** Mayor riesgo de sangrado gastrointestinal o hemorragia.")
st.markdown("🔸**Ácido acetilsalicílico + Telmisartán:** Disminución del efecto antihipertensivo y posible daño renal.")
st.markdown("🔸**Telmisartán + Empagliflozina:** Riesgo aumentado de hipotensión y deterioro de la función renal.")
st.markdown("🔸**Metformina + Empagliflozina:** Riesgo aumentado de acidosis láctica y deshidratación.")
st.markdown("🔸**Metformina + Linagliptina:** Riesgo de hipoglucemia, aunque bajo si se usa sin sulfonilureas.")
st.markdown("🔸**Empagliflozina + Linagliptina:** Riesgo leve de infecciones urinarias y genitales.")
st.markdown("🔸**Pantoprazol + Clopidogrel:** Posible disminución del efecto antiagregante de clopidogrel.")
st.markdown("🔸**Isosorbida + Amlodipino:** Riesgo de hipotensión significativa por efecto vasodilatador combinado.")
st.markdown("🔸**Amlodipino + Telmisartán:** Riesgo de hipotensión, especialmente al inicio del tratamiento.")
st.markdown("🔸**Atorvastatina + Complejo B:** No hay interacción significativa, pero algunos componentes del complejo B pueden interferir con metabolismo hepático.")
st.markdown("🔸**Atorvastatina + Empagliflozina:** Riesgo bajo pero potencial de mialgia o rabdomiólisis aumentado en pacientes con deterioro renal.")

st.subheader("🩺 Lista de recomendaciones generales")

st.markdown("🔹**Consulte a su médico** antes de modificar cualquier tratamiento.")
st.markdown("🔹**Evite el alcohol** al tomar **ácido acetilsalicílico, metformina o isosorbida**, ya que puede aumentar los riesgos de efectos adversos.")
st.markdown("🔹**Evite automedicarse con AINEs adicionales** si ya usa **ácido acetilsalicílico**, para no aumentar el riesgo de sangrado gastrointestinal.")
st.markdown("🔹**Limite el consumo de jugo de toronja** si está tomando **atorvastatina o amlodipino**, ya que puede alterar su metabolismo.")
st.markdown("🔹**Hidrátese adecuadamente** si toma **empagliflozina y/o telmisartán** para prevenir hipotensión y problemas renales.")
st.markdown("🔹**Monitoree su presión arterial regularmente** si usa **amlodipino y telmisartán**.")
st.markdown("🔹**No suspenda bruscamente** **clopidogrel o ácido acetilsalicílico** sin indicación médica, ya que puede aumentar el riesgo cardiovascular.")
st.markdown("🔹**Informe a su médico** si nota síntomas como fatiga, debilidad muscular o calambres al tomar **atorvastatina**.")
st.markdown("🔹**Informe cualquier signo de infección urinaria** si está usando **empagliflozina**.")
st.markdown("🔹**Tome metformina con alimentos** para reducir molestias gastrointestinales.")
st.markdown("🔹**Evite usar pantoprazol por periodos prolongados** sin seguimiento médico, debido al riesgo de deficiencias nutricionales o efectos renales.")

st.info("ℹ️ Esta guía no reemplaza la consulta médica. Si tiene dudas, consulte a su médico especialista.")