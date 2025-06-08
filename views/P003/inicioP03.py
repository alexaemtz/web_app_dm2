import streamlit as st
import firebase_utils
from firebase_utils import init_firebase

firebase = init_firebase()
db = firebase["db"]

st.title(":blue[Página principal]")

doc_ref = db.collection("pacientes").document("P003")
doc = doc_ref.get()

def obtener_nombre():
    if doc.exists:
        data = doc.to_dict()
        nombre = data.get("nombre", '')
        apellidos = data.get("apellidos", '')
        nombre_completo = f"{nombre} {apellidos}"
        st.markdown(f"### :orange-background[Nombre del paciente:] {nombre_completo}")
    else:
        st.error("No se encontró el documento del paciente")
        
obtener_nombre()

st.markdown("---")

def obtener_diagnosticos():
    if doc.exists:
        data = doc.to_dict()
        principal = data.get("diagnosticos", {}).get("principal", None)
        secundarios = data.get("diagnosticos", {}).get("secundarios", [])
        st.markdown(f'Su diagnóstico principal es :blue-background[{principal}]')
        st.write("Sus diagnósticos complementarios son:")
        for diagnostico in secundarios:
            st.markdown(f':blue-background[{diagnostico}]')
    else:
        st.error("No se encontró el documento del paciente.")
        principal = None
        secundarios = None

obtener_diagnosticos()

def obtener_medicamentos():
    if doc.exists:
        data = doc.to_dict()
        medicamentos = data.get("medicamentos", [])
        return medicamentos
    else:
        st.error("No se encontró el documento del paciente.")
        return []
    
medicamentos = obtener_medicamentos()

st.subheader("Medicamentos")
if medicamentos:
    num_columns = 2
    cols = st.columns(num_columns)
    
    for i, medicamento in enumerate(medicamentos):
        nombre = medicamento.get("nombre", 'Nombre no encontrado')
        dosis = medicamento.get("dosis", 'Dosis no encontrada')
        frecuencia = medicamento.get("frecuencia", 'Frecuencia no encontrada')
        
        col = cols[i % num_columns]  # ✅ Esto asegura que el índice nunca se salga de rango
        with col:
            st.markdown(f"### 💊 {nombre}")
            st.write(f"##### Dosis: {dosis}")
            st.write(f"##### Frecuencia: {frecuencia}")
            st.markdown("--------")
else:
    st.write("No se encontraron medicamentos.")
