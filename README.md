# 🩺 Aplicación de Gestión para Pacientes con Diabetes Tipo 1

Esta es una aplicación web desarrollada con **Streamlit** y autenticada mediante **Firebase**, diseñada para asistir a pacientes con diabetes tipo 1, sus cuidadores y profesionales de la salud. Ofrece funcionalidades como navegación personalizada por usuario, detección de carbohidratos, historial de glucosa, módulo de medicamentos, chatbot médico y más.

## 🚀 Funcionalidades

- 🔐 **Autenticación segura** con Firebase (registro, inicio de sesión, cierre de sesión).
- 👨‍⚕️ **Roles dinámicos:** Administrador y pacientes (`P001`, `P002`, `P003`) con acceso personalizado.
- 🧭 **Menú de navegación contextual** según el usuario autenticado.
- 💉 **Gestión de medicamentos** por paciente.
- 🥼 **Módulo de resultados de laboratorio.**
- 🥘 **Detección de carbohidratos a partir de imágenes.**
- 🤖 **Chatbot clínico** y asistente virtual nutricional.
- 📊 **Historial de mediciones de glucosa.**
- 🧠 **Análisis de filtrado glomerular.**

## 📁 Estructura del Proyecto

### 📦project-root
├── assets/ # Imágenes y logotipo  
├── css/style.css # Estilos personalizados  
├── views/  
│ ├── P001/ # Vistas específicas del paciente P001  
│ ├── P002/ # Vistas específicas del paciente P002  
│ ├── P003/ # Vistas específicas del paciente P003  
│ └── general/ # Vistas compartidas: chatbot, nutrición, detección, etc.  
│ └── main.py # Vista principal  
├── login.py # Módulo de inicio de sesión  
├── logout.py # Módulo de cierre de sesión  
├── register.py # Registro de usuarios  
├── firebase_utils.py # Inicialización y configuración de Firebase  
├── streamlit_app.py # Archivo principal  
└── README.md # Documentación del proyecto  

### **Autenticación y Navegación**

- Los usuarios se autentican mediante correo y contraseñal. 
- El sistema identifica al usuario mediante su UID asignado previamente (P001, P002, P003, Administrador).
- Según el UID detectado, se habilitan las secciones correspondientes en la navegación lateral.
