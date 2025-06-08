import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

def init_firebase():
    if not firebase_admin._apps:
        try:
            cred = credentials.Certificate({
                "type": st.secrets["firebase_credentials_type"],
                "project_id" : st.secrets["firebase_project_id"],
                "private_key_id" : st.secrets["firebase_private_key_id"],
                "private_key" : st.secrets["firebase_private_key"],
                "client_email" : st.secrets["firebase_client_email"],
                "client_id" : st.secrets["firebase_client_id"],
                "auth_uri" : st.secrets["firebase_auth_uri"],
                "token_uri" : st.secrets["firebase_token_uri"],
                "auth_provider_x509_cert_url" : st.secrets["firebase_auth_provider_x509_cert_url"],
                "client_x509_cert_url" : st.secrets["firebase_client_x509_cert_url"]
            })
            firebase_admin.initialize_app(cred)
        except KeyError as e:
            st.error(f'Falta la clave {e} en secrets.toml')
            st.stop()
        except Exception as e:
            st.error(f'Error al iniciar firebase: {e}')
            st.stop()
    return {
        "db" : firestore.client(),
    }
