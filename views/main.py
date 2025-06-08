import streamlit as st
import pandas as pd
from firebase_utils import init_firebase

firebase = init_firebase()
db = firebase["db"]

st.title(":blue[¡Bienvenido!]")
st.header("Base de datos de pacientes", divider="rainbow")
st.write("Esta dashboard será de ayuda para el monitereo y control de los pacientes que así lo requieran, clientes de Consultas Servicios Contables 2025®.")
st.write("En la tabla puede observar todos los pacientes registrados en la base de datos, con su nombre y apellidos, y su diagnóstico principal y complementarios.")
st.write("Si desea mayor información sobre un paciente, puede seleccionarlo en la barra lateral.")


def obtener_pacientes():
    pacientes_ref = db.collection("pacientes").stream()
    pacientes = []

    for paciente in pacientes_ref:
        data = paciente.to_dict()
        pacientes.append(data)
        nombre = data.get("nombre", '')
        apellidos = data.get("apellidos", '')

    return pacientes

def obtener_diagnosticos(paciente):
    return paciente.get("diagnosticos", {})

# Obtener pacientes
pacientes = obtener_pacientes()

# Crear listas para la tabla
nombres = []
diagnosticos_list = []

for paciente in pacientes:
    nombre_completo = f"{paciente.get('nombre', '')} {paciente.get('apellidos', '')}"
    diagnosticos = obtener_diagnosticos(paciente)

    # Concatenar diagnósticos secundarios en una sola cadena
    secundarios = diagnosticos.get("secundarios", [])
    secundarios_texto = ", ".join(secundarios)

    # Diagnóstico principal (si existe)
    principal = diagnosticos.get("principal", "")
    
    texto_diagnostico = principal
    if secundarios_texto:
        texto_diagnostico += f" (Complementario: {secundarios_texto})"

    nombres.append(nombre_completo)
    diagnosticos_list.append(texto_diagnostico)

# Crear DataFrame
df = pd.DataFrame({
    "Nombre": nombres,
    "Diagnóstico": diagnosticos_list
})

st.table(df)
