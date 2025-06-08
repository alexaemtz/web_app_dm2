"""
detection.py

Este módulo proporciona una interfaz en Streamlit que permite a usuarios con diabetes tipo 2 analizar imágenes de comida
para identificar alimentos y obtener su información nutrimental utilizando inteligencia artificial (Gemini de Google).

Funciones principales:
- Subir una imagen de comida.
- Enviar la imagen a Gemini para detección de alimentos y análisis nutrimental.
- Mostrar los resultados en formato tabular en español.
"""

import streamlit as st
from PIL import Image
import google.generativeai as genai
import re

# Configuración de la API 
my_api_key = st.secrets["GEMINI_API_KEY"]

if not my_api_key:
    st.error("Por favor, configura la clave API de Google en las variables de entorno.")
else:
    genai.configure(api_key=my_api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    def input_image_details(image_upload):
        """
        Procesa la imagen subida por el usuario.

        Parámetros:
            image_upload (UploadedFile): archivo de imagen cargado por el usuario.

        Devuelve:
            list: una lista con la información de la imagen para enviarla al modelo Gemini.
        """
        if image_upload is not None:
            bytes_data = image_upload.getvalue()
            image_parts = [{"mime_type": image_upload.type, "data": bytes_data}]
            return image_parts
        else:
            raise FileNotFoundError("No ha seleccionado una imagen.")

    def get_gemini_response(user_input, image, prompt):
        """
        Envía una imagen y un prompt al modelo Gemini y retorna la respuesta.

        Parámetros:
            user_input (str): texto ingresado por el usuario (puede estar vacío).
            image (list): detalles de la imagen.
            prompt (str): prompt que indica qué debe hacer el modelo.

        Devuelve:
            str: texto generado por Gemini con la información nutrimental.
        """
        try:
            response = model.generate_content([user_input, image[0], prompt])
            return response
        except Exception as e:
            return f"Error al obtener la respuesta de Gemini: {e}"
    
    # Cargar estilos personalizados    
    with open("css/style.css" ) as css:
        st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)
        
    # Interfaz de usuario
    st.title("🌮 Contador de carbohidratos")
    st.write(
        """¡Bienvenido su contador de carbohidratos! Esta app le será de utilidad para calcular el número de carbohidratos contenidos en una comida. 
        Utilice el botón 'Browse files' para seleccionar una imagen. No es necesario que ingrese una descripción de lo deseado, el sistema lo hará por usted.
        El software utilizará inteligencia artificial para determinar el contenido nutrimental de la misma."""
    )

    user_input = st.text_input(
        "Ingrese una descripción de lo deseado:",
        placeholder="Ejemplo: Dime las calorías contenidas en este plato de ensalada.",
        key="user_input",
    )
    image_upload = st.file_uploader("Suba una imagen", type=["png", "jpg", "jpeg"])
    image = ""
    if image_upload is not None:
        image = Image.open(image_upload)
        st.image(image, caption="Imagen cargada", use_container_width=True)
    submit = st.button("Escanear la comida")

    input_prompt = """ You are a helpful dietist. You must identy different types of food in images.
    The system should accurately detect and label varios foods displayed in the image, providing the name of the food.
    Additionally, the system should extract nutritional information and categorize the type of food (e.g., fruits, vegetables, grains, etc.) based on the detected items. 
    Include sugar contents, calories, protein, fat, carbohydrates, and fiber in the output. As well as if it's good for diabetics or not.
    Please provide the output in Spanish and in table format. 
    Also provide the total of sugar contents, calories, protein, fat, carbohydrates, and fiber in the output in a final row of the table. 
    """

    if submit:
        with st.spinner("Escaneando la comida..."):
            try:
                image_data = input_image_details(image_upload)
                response = get_gemini_response(input_prompt, image_data, user_input)

                # Extraer la tabla de la respuesta
                text_response = response.text
                table_match = re.search(r"\| Food Item.*\|", text_response, re.DOTALL)

                if table_match:
                    table_text = table_match.group(0)
                    lines = table_text.strip().split("\n")
                    headers = [h.strip() for h in lines[0].strip("|").split("|")]
                    data = []
                    for line in lines[2:]:
                        row = [r.strip() for r in line.strip("|").split("|")]
                        data.append(dict(zip(headers, row)))

                    st.subheader("Información Nutricional:")
                    st.table(data)
                else:
                    st.subheader("Resultados obtenidos: ")
                    st.write(response.text)

            except Exception as e:
                st.error(f"Ocurrió un error: {e}")