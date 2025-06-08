"""
mediciones.py

Módulo principal para registrar y visualizar mediciones de glucosa usando Streamlit y Firebase.

Este módulo permite a los pacientes ingresar sus niveles de glucosa, visualizar su historial
en gráficos interactivos y, si el usuario tiene el rol de administrador, visualizar todos los registros.

Requiere autenticación previa del usuario (el UID y el rol deben estar definidos en `st.session_state`).

Dependencias:
- streamlit
- plotly
- pandas
- firebase_utils (módulo personalizado)
- datetime

"""

import streamlit as st
import plotly.express as px
import pandas as pd
from firebase_utils import init_firebase
from datetime import datetime

firebase = init_firebase()
db = firebase["db"]

collection_pacientes = "pacientes"
collection_mediciones = "mediciones"

st.title("Mediciones de glucosa")
st.subheader("Registro y seguimiento de tus niveles de glucosa")

uid = st.session_state['user']['uid']

if uid:
    paciente_ref = db.collection(collection_pacientes).document(uid)
    paciente_doc = paciente_ref.get()

    if paciente_doc.exists:
        st.success(f"¡Hola, paciente con ID: {uid}! Puedes registrar tus mediciones.")

        # Formulario para ingresar la medición
        with st.form("nueva_medicion"):
            valor_glucosa = st.number_input("Valor de glucosa (mg/dL)", min_value=0)
            fecha_medicion = st.date_input("Fecha de la medición", value=datetime.today())
            hora_medicion = st.time_input("Hora de la medición", value=datetime.now().time())
            submitted = st.form_submit_button("Guardar medición")

            if submitted:
                nueva_medicion = {
                    "valor": valor_glucosa,
                    "fecha": fecha_medicion.isoformat(),
                    "hora": hora_medicion.strftime("%H:%M:%S"),
                    "timestamp": datetime.now(),  
                    "uid_paciente": uid
                }
                db.collection(collection_mediciones).document().set(nueva_medicion)
                st.success("Medición guardada exitosamente.")
                
        st.subheader("Gráfico de tus mediciones")
        mediciones_df = None 

        mediciones_ref = db.collection(collection_mediciones).where("uid_paciente", "==", uid).order_by("timestamp")
        mediciones = mediciones_ref.get()

        if mediciones:
            data = []
            for doc in mediciones:
                medicion = doc.to_dict()
                data.append(medicion)
            mediciones_df = pd.DataFrame(data)
            mediciones_df['fecha_hora'] = pd.to_datetime(mediciones_df['fecha'] + ' ' + mediciones_df['hora'])

            if not mediciones_df.empty:
                fig = px.line(mediciones_df, x="fecha_hora", y="valor", title="Historial de glucosa")
                st.plotly_chart(fig)
            else:
                st.info("Aún no has registrado ninguna medición.")

        elif not paciente_doc.exists:
            st.warning("El paciente no existe en la base de datos.")
            
    elif st.session_state['role'] != "Administrador":
        st.warning("No se ha podido obtener la información del usuario. Asegúrate de haber iniciado sesión correctamente.")
else:
    st.warning("No se ha detectado el UID del usuario. Asegúrate de haber iniciado sesión.")

user_role = st.session_state['role']
    
if user_role == "Administrador":
    st.subheader("🔐 Vista de Administrador")
    st.write("Aquí puedes ver todas las mediciones del paciente.")
    
    all_mediciones_ref = db.collection(collection_mediciones).order_by("timestamp")
    all_mediciones = all_mediciones_ref.get()
    
    if all_mediciones:
        data_admin = []
        for doc in all_mediciones:
            medicion_admin = doc.to_dict()
            data_admin.append(medicion_admin)
        mediciones_admin_df = pd.DataFrame(data_admin)
        
        if not mediciones_admin_df.empty:
            st.dataframe(mediciones_admin_df)
        else:
            st.info("No hay mediciones registradas.")
    else:
        st.info("No hay mediciones registradas.")

elif uid and user_role != "Administrador" and user_role is not None:
    st.info("No tienes permisos para ver las mediciones del paciente.")
elif uid is not None and user_role is None:
    st.info("No se ha podido obtener el rol del usuario. Asegúrate de haber iniciado sesión correctamente.")