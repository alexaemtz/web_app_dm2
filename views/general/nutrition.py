import streamlit as st
import google.generativeai as genai
from firebase_utils import init_firebase
from login import get_user_uid

my_api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=my_api_key)

model = genai.GenerativeModel("gemini-2.0-flash")

firebase = init_firebase()
db = firebase["db"]

st.title("Asistente virtual para nutrición")
st.subheader("Este asistente virtual le ayudará a obtener sugerencias de alimentos y nutrición para su dieta, de acuerdo a sus necesides y preferencias.")

restricciones_dieteticas = st.multiselect("Restricciones dietéticas", ["Sin gluten", "Sin lácteos", "Vegetariano", "Vegano", "Paleo", "Otras (especificar)"], placeholder="Seleccione una opción")
otras_restricciones = st.text_input("Otras restricciones dietéticas (si aplica)")
alergias = st.text_input("¿Tiene alguna alergia o alergias? Si no, deje este campo en blanco.")
tipo_comida = st.multiselect("Tipo de comida preferida", ["Italiana", "Mexicana", "Americana", "Asiática", "Mediterránea", "Otras (especificar)"], placeholder="Seleccione una opción")
otro_tipo_comida = st.text_input("Otro tipo de comida preferida (si aplica)")
historial_glucosa = st.number_input("¿Cuál fue su última lectura de glucosa (en mg/dL)? Este dato puede ayudar a personalizar mejor su sugerencia.", value=100)
nivel_actividad = st.selectbox("¿Cuál es su nivel de actividad física?", ["Sedentario", "Ligero", "Moderado", "Intenso"])
comidas_dia = st.number_input("¿Cuántas comidas diarias le gustaría que le diera este asistente virtual?", value=1)
objetivos_glucosa = st.text_input("Opcional: ¿Hasta que valor le gustaría controlar su glucosa?", placeholder="Ejemplo: 80 mg/dL")

sugerencias = st.button("Generar sugerencias")

if sugerencias:
    prompt = f"""Eres un asistente virtual para nutrición. Genera un plan de comidas personalizado para el paciente con diabetes. Considera la siguiente información:
    Restricciones dietéticas: {', '.join(restricciones_dieteticas) + (f', {otras_restricciones}' if otras_restricciones else '')}
    Alergias: {alergias if alergias else 'Ninguna'}
    Tipo de comida: {', '.join(tipo_comida) + (f', {otro_tipo_comida}' if otro_tipo_comida else '')}
    Historial reciente de glucosa: {historial_glucosa if historial_glucosa else 'No proporcionado'}
    Nivel de actividad física: {nivel_actividad}
    Número de comidas al día: {comidas_dia}
    Objetivos de rango de glucosa: {objetivos_glucosa if objetivos_glucosa else 'No especificado'}
    
    El plan de comidas debe ser saludable, equilibrado y adaptado a las restricciones dietéticas, preferencias alimentarias, nivel de actividad física, 
    historial de glucosa y objetivos de rango de glucosa. El plan debe incluir una variedad de alimentos.
    Además, debe ser adecuado para controlar los niveles de glucosa en un paciente diabético.
    Incluye ideas de recetas específicas y considera las porciones adecuadas.
    
    Formato de salida sugerido:
    **Día [Número]:**
    
    * **Desayuno:** [Nombre del plato] - [Descripción breve]
    * **Media Mañana:** [Nombre del snack] - [Descripción breve]
    * **Almuerzo:** [Nombre del plato] - [Descripción breve]
    * **Media Tarde:** [Nombre del snack] - [Descripción breve]
    * **Cena:** [Nombre del plato] - [Descripción breve]
    """
    
    try:
        response = model.generate_content(prompt)
        st.subheader("Plan de comidas sugerido:")
        st.markdown(response.text)
        st.subheader("Recomendaciones Nutricionales Adicionales:")
        prompt_recomendaciones = f"""
        Considerando las restricciones y preferencias del paciente diabético con la siguiente información:
        Restricciones dietéticas: {', '.join(restricciones_dieteticas) + (f', {otras_restricciones}' if otras_restricciones else '')}
        Preferencias alimentarias: {', '.join(tipo_comida) + (f', {otro_tipo_comida}' if otro_tipo_comida else '')}
        Proporciona algunas recomendaciones nutricionales generales para ayudar a controlar sus niveles de glucosa.
        """
        response_recomendaciones = model.generate_content(prompt_recomendaciones)
        st.markdown(response_recomendaciones.text)
    except Exception as e:
        st.error(f"Ocurrió un error al generar la sugerencia: {e}")