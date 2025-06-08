import streamlit as st
from firebase_admin import auth
from firebase_utils import init_firebase

firebase = init_firebase()
db = firebase["db"]

def register():
    st.write("Si ya posee una cuenta, por favor, inicie sesión. De lo contrario, complete el siguiente formulario.")
    new_email = st.text_input("Correo electrónico", key="register_email")
    new_password = st.text_input("Contraseña", type="password", placeholder="••••••••", key="register_password")
    confirm_password = st.text_input("Confirmar contraseña", type="password", placeholder="••••••••", key="register_confirm_password")
    uid = st.text_input("Nombre de usuario (Su ID único de paciente)", key="register_username")
    register_button = st.button("Registrarse", key="register_button")

    if register_button:
        if new_password != confirm_password:
            st.error("Las contraseñas no coinciden.")
            return
        try:
            paciente_ref = db.collection("pacientes").document(uid).get()
            if not paciente_ref.exists:
                st.error("❌ Error al registrar el usuario: ID de paciente no válido.")
                return
            else:
                user = auth.create_user(email=new_email, password=new_password, uid=uid)
                user_data = {"email": new_email, "role": "Paciente", "uid": uid}
                st.error("❌ Error al registrar el usuario: ID de paciente no válido.")
                db.collection("users").document(uid).set(user_data)
                st.success(f"✔️ Su usuario se ha registrado correctamente con el ID asociado: {uid}")
        except auth.EmailAlreadyExistsError:
            st.error("❗ El correo electrónico ya está registrado.")
        except Exception as e:
            st.error(f"❌ Error al registrar el usuario: {e}")
