"""
filtrado.py

Módulo de cálculo de tasa de filtrado glomerular (TFG) usando distintas fórmulas:
Cockcroft-Gault, MDRD-4 y CKD-EPI.

Este módulo utiliza Streamlit para desplegar una interfaz interactiva que permite
introducir los datos clínicos del paciente y calcular la TFG estimada según las fórmulas seleccionadas.

Funciones principales:
    - Cálculo de la TFG usando Cockcroft-Gault.
    - Cálculo de la TFG usando MDRD-4.
    - Cálculo de la TFG usando CKD-EPI.
"""

import streamlit as st

tab1, tab2, tab3 = st.tabs(["Cockcroft-Gault", "MDRD-4", "CKD-EPI"])

with tab1: 
    valor_creatinina_cg = st.number_input("Valor de creatinina (mg/dL)", key="valor_creatinina_cg")
    edad_cg = st.number_input("Edad (años)", min_value=0, key="edad_cg")
    peso_cg = st.number_input("Peso (kg)", min_value=0, key="peso_cg")
    sexo_cg = st.selectbox("Sexo", ["Masculino", "Femenino"], key="sexo_cg")
    cg_boton = st.button("Calcular filtrado Cockcroft-Gault", key="cg_boton")
    st.write("Esta fórmula es sencilla y rápida, pero es menos precisa cuando existe obesidad. De igual forma es menos precisa en ancianos y pacientes con masa muscular anormal")
    
    # Cockcroft-Gault filtración
    def cockcroft_gault_filtracion(creatinina, peso, edad, sexo):
        """
        Calcula la tasa de filtrado glomerular (TFG) utilizando la fórmula de Cockcroft-Gault.
        
        Parameters:
            creatinina (float): valor de creatinina en mg/dL.
            peso (float): peso del paciente en kg.
            edad (float): edad del paciente en años.
            sexo (str): sexo del paciente (Masculino o Femenino).

        Returns:
            float: tasa de filtrado glomerular estimada.
        """
        resultado_cg = ((140 - edad) * peso) / (72 * creatinina)
        if sexo == "Femenino":
            resultado_cg *= 0.85
        return resultado_cg

    if cg_boton:
        if valor_creatinina_cg is None or edad_cg is None or peso_cg is None or sexo_cg is None:
            st.error("Por favor, rellene todos los campos.")
        if valor_creatinina_cg == 0 or edad_cg == 0 or peso_cg == 0:
            st.error("Los valores no pueden ser cero.")
        resultado_cg = cockcroft_gault_filtracion(valor_creatinina_cg, peso_cg, edad_cg, sexo_cg)
        st.info(f"El filtrado glomerular es de {resultado_cg:.2f}")
    
with tab2:
    valor_creatinina_md = st.number_input("Valor de creatinina (mg/dL)", key="valor_creatinina_md")
    edad_md = st.number_input("Edad (años)", min_value=0, key="edad_md")
    sexo_md = st.selectbox("Sexo", ["Masculino", "Femenino"], key="sexo_md")
    raza_md = st.selectbox("¿Es afrodescendiente?", ["Si", "No"], key="raza_md")
    mdrd4_boton = st.button("Calcular filtrado MDRD4", key="mdrd4_boton")
    st.write("Esta fórmula es más precisa que la anterior, excepto cuando la TFG es > 60 ml/min/1.73m².")

    def mdrd4_filtracion(creatinina, edad, sexo, raza):
        """
        Calcula la tasa de filtrado glomerular (TFG) utilizando la fórmula de MDRD-4.
        
        Parameters:
            creatinina (float): valor de creatinina en mg/dL.
            edad (float): edad del paciente en años.
            sexo (str): sexo del paciente (Masculino o Femenino).
            raza (str): raza del paciente (Si o No).

        Returns:
            float: tasa de filtrado glomerular estimada.
        """
        resultado_mdrd4 = 175 * (creatinina)**-1.154 * (edad)**-0.203
        if sexo == "Femenino":
            resultado_mdrd4 *= 0.742
        elif raza == "Si":
            resultado_mdrd4 *= 1.210
        return resultado_mdrd4

    if mdrd4_boton:
        if valor_creatinina_md is None or edad_md is None or sexo_md is None or raza_md is None:
            st.error("Por favor, rellene todos los campos.")
        if valor_creatinina_md == 0 or edad_md == 0:
            st.error("Los valores no pueden ser cero.")
        resultado_mdr4 = mdrd4_filtracion(valor_creatinina_md, edad_md, sexo_md, raza_md)
        st.info(f"El filtrado MDRD-4 es de {resultado_mdr4:.2f}")
        
with tab3:
    valor_creatinina_ckd = st.number_input("Valor de creatinina (mg/dL)", key="valor_creatinina_ckd")
    edad_ckd = st.number_input("Edad (años)", min_value=0, key="edad_ckd")
    sexo_ckd = st.selectbox("Sexo", ["Masculino", "Femenino"], key="sexo_ckd")
    raza_ckd = st.selectbox("¿Es afrodescendiente?", ["Si", "No"], key="raza_ckd")
    ckd_epi_boton = st.button("Calcular filtrado CKD-EPI", key="ckd_epi_boton")
    st.write("Esta fórmula es más precisa que la anterior, especialmente si la TFG es alta. Se recomienda en guías actuales.")   
    
    def ckd_epi_filtracion(creatinina, edad, sexo, raza):
        """
        Calcula la tasa de filtrado glomerular (TFG) utilizando la fórmula de CKD-EPI.
        
        Parameters:
            creatinina (float): valor de creatinina en mg/dL.
            edad (float): edad del paciente en años.
            sexo (str): sexo del paciente (Masculino o Femenino).
            raza (str): raza del paciente (Si o No).

        Returns:    
            float: tasa de filtrado glomerular estimada.
        """
        if sexo == "Femenino":
            k = 0.7
            a = - 0.329
            s = 1.018
        else:
            k = 0.9
            a = - 0.411
            s = 1.037
        r = 1.159 if raza == "Si" else 1.0
        cr_k = creatinina / k
        resultado_ckd_epi = 141 * min(cr_k, 1)**a * max(cr_k, 1)**(-1.209) * (0.993**edad) * s * r
        return resultado_ckd_epi
    
    if ckd_epi_boton:
        if valor_creatinina_ckd is None or edad_ckd is None or sexo_ckd is None or raza_ckd is None:
            st.error("Por favor, rellene todos los campos.")
        if valor_creatinina_ckd == 0 or edad_ckd == 0:
            st.error("Los valores no pueden ser cero.")
        resultado_ckd = ckd_epi_filtracion(valor_creatinina_ckd, edad_ckd, sexo_ckd, raza_ckd)
        st.info(f"El filtrado CKD-EPI es de {resultado_ckd:.2f}")
        
        