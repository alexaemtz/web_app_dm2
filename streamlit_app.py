"""
streamlit_app.py

Aplicación principal desarrollada con Streamlit para pacientes con diabetes tipo 2. 
Permite iniciar sesión mediante Firebase, visualizar módulos específicos según el rol 
(Administrador o paciente P001, P002, P003) e interactuar con asistentes y módulos médicos.

Autores: Alexa Escalante Martínez
Fecha de creación: 21-05-2025
Dependencias:

    - streamlit
    - firebase_admin
    - módulos locales: firebase_utils.py, login.py, register.py
"""

# Importar librerías necesarias
import streamlit as st
from firebase_admin import auth
from firebase_utils import init_firebase
from login import login, logout, get_user_role
from register import register

# Inicializa Firebase y obtiene instancia de base de datos
firebase = init_firebase()
db = firebase["db"]

# Carga estilos CSS personalizados 
with open("css/style.css") as css:
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

def display_header():
    """
    Muestra la cabecera superior de la app, incluyendo:
    - Logo institucional.
    - Email y rol del usuario logueado (si existe).
    - Botón de logout.
    """
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.image("assets/logo.png", width=80)  
    with col2:
        if 'user' in st.session_state and st.session_state['user']:
            st.markdown(f"**Logueado como:** {st.session_state['user']['email']}")
            if 'role' in st.session_state:
                st.markdown(f"**Rol:** {st.session_state['role']}")
    with col3:
        logout()
    st.divider()

def display_content():
    """
    Configura las páginas visibles dependiendo del rol del usuario autenticado.
    Las secciones disponibles incluyen módulos médicos, chatbot, historial de glucosa,
    nutrición y filtrado glomerular.
    
    Roles disponibles:
    - Administrador: Acceso total.
    - P001, P002, P003: Acceso a su propio perfil y módulos relevantes.
    """
    
    # --- Configuración de las páginas ---
    main_page = st.Page("views/main.py", title="Inicio", icon="🏠")
    p01_main_page = st.Page("views/P001/inicioP01.py", title="Principal", icon="🏚️")
    p01_medicamentos_page = st.Page("views/P001/medicamentos01.py", title="Medicamentos", icon="💉")
    p02_main_page = st.Page("views/P002/inicioP02.py", title="Principal", icon="🏚️")
    p02_laboratoriales_page = st.Page("views/P002/laboratorialesP02.py", title="Laboratoriales del paciente", icon="🥼")
    p02_medicamentos_page = st.Page("views/P002/medicamentosP02.py", title="Medicamentos", icon="💉")
    p02_info_page = st.Page("views/P002/infoP02.py", title="Información del paciente", icon="ℹ️")
    p03_main_page = st.Page("views/P003/inicioP03.py", title="Principal", icon="🏚️")
    p03_medicamentos_page = st.Page("views/P003/medicamentosP03.py", title="Medicamentos", icon="💉")
    detection_page = st.Page("views/general/detection.py", title="Contador de carbohidratos", icon="🥘")
    chatbot_page = st.Page("views/general/chatbot.py", title="Chatbot", icon="🤖")
    nutrition_page = st.Page("views/general/nutrition.py", title="Asistente virtual para nutrición", icon="🥘")
    mediciones_page = st.Page("views/general/mediciones.py", title="Mediciones de glucosa", icon="📊")
    filtrado_page = st.Page("views/general/filtrado.py", title="Filtrado glomerular", icon="🧠")

# --- Navegación según el rol ----

    if st.session_state['role'] == "Administrador":
        # Menu completo para administradores
        admin_nav = st.navigation({
            "Inicio": [main_page],
            "P001": [p01_main_page,
                     p01_medicamentos_page],
            "P002": [p02_main_page,
                     p02_laboratoriales_page,
                     p02_medicamentos_page],
            "P003": [p03_main_page,
                     p03_medicamentos_page],
            "Detección de carbohidratos": [detection_page],
            "Chatbot" : [chatbot_page],
            "Asistente virtual para nutrición": [nutrition_page],
            "Historial de glucosa" : [mediciones_page],
            "Filtrado glomerular" : [filtrado_page],
        })
        admin_nav.run()

    elif st.session_state['user']['uid'] == "P001":
        # Menu de páginas para paciente P001
        p001_nav = st.navigation({
            "Inicio" : [main_page],
            "P001" : [p01_main_page,
                      p01_medicamentos_page],
            "Detección de carbohidratos": [detection_page],
            "Chatbot" : [chatbot_page],
            "Asistente virtual para nutrición": [nutrition_page],
            "Historial de glucosa" : [mediciones_page],
        })
        p001_nav.run()

    elif st.session_state['user']['uid'] == "P002":
        # Menu de páginas para paciente P002
        p002_nav = st.navigation({
            "Inicio" : [main_page],
            "P002" : [p02_main_page,
                      p02_laboratoriales_page,
                      p02_medicamentos_page],
            "Detección de carbohidratos": [detection_page],
            "Chatbot" : [chatbot_page],
            "Asistente virtual para nutrición": [nutrition_page],
            "Historial de glucosa" : [mediciones_page],
        })
        p002_nav.run()

    elif st.session_state['user']['uid'] == "P003":
        # Menu de páginas para paciente P003
        p003_nav = st.navigation({
            "Inicio" : [main_page],
            "P003" : [p03_main_page, 
                      p03_medicamentos_page],
            "Detección de carbohidratos": [detection_page],
            "Chatbot" : [chatbot_page],
            "Asistente virtual para nutrición": [nutrition_page],
            "Historial de glucosa" : [mediciones_page],
        })
        p003_nav.run()

if __name__ == "__main__":
    """
    Punto de entrada principal de la aplicación.
    Gestiona el estado de sesión, muestra el formulario de login o registro y,
    una vez autenticado el usuario, redirige al contenido correspondiente.
    """
    # Inicialización de estados de sesión
    if 'user' not in st.session_state:
        st.session_state['user'] = None
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'show_register_form' not in st.session_state:
        st.session_state['show_register_form'] = False
    # Mostrar login o formulario de registro
    if not st.session_state['logged_in']:
        if st.session_state['show_register_form']:
            st.subheader("Registro de nuevo usuario.")
            register()
            if st.button("Volver al inicio de sesión", key="back_to_login"):
                st.session_state['show_register_form'] = False
                st.rerun()
        else:
            st.subheader("Por favor, inicie sesión.")
            login_sucessful = login()
    else:
        if 'user' in st.session_state and st.session_state['user'] and 'uid' in st.session_state['user']:
             # Si no se ha cargado el rol, obténlo y recarga
            if 'role' not in st.session_state and st.session_state['user']:
                user_role = get_user_role(st.session_state['user']['uid'])
                st.session_state['role'] = user_role
                st.rerun()
            else:
                # Mostrar cabecera y contenido según rol
                display_header() 
                display_content()
        else:
            st.subheader("Por favor, inicie sesión.")
            login()