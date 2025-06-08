import streamlit as st
import plotly.graph_objects as go
from firebase_utils import init_firebase

firebase = init_firebase()
db = firebase["db"]

doc_ref = db.collection("pacientes").document("P002")
doc = doc_ref.get()

st.title("Laboratoriales del paciente")

def gauge_chart(value, title, reference, min_bajo, normal_min, normal_max, min_alto, max_alto):
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={"x": [0, 1], "y": [0, 1]},
        title={"text": title, "font": {"size": 20}},
        delta={"reference": reference, 
               "decreasing": {"color": "#1ed14b"},
               "increasing": {"color": "#f86368"}},
        gauge={
            "axis": {"range": [None, max_alto], "tickwidth": 3, "tickcolor": "#F5F5F5"},
            "bar": {"color": "#CBD6E2"},
            "bgcolor": "white",
            "borderwidth": 1, "bordercolor": "#F5F5F5",
            "steps": [
                {"range": [0, min_bajo], "color": "#00A7C3"},
                {"range": [normal_min, normal_max], "color": "#4FB06D"},
                {"range": [min_alto, max_alto], "color": "#BF2C34"}
            ],
            "threshold": {
                "line": {"color": "black", "width": 4},
                "thickness": 1, "value": reference
            }
        }
    ))
    fig.update_layout(margin={"l": 1, "r": 1, "t": 1, "b": 1},
        font = {'color': "#F5F5F5", 'family': "Quicksand"})
    return fig

def obtener_laboratorio():
    if doc.exists:
        data = doc.to_dict()
        data = data.get("laboratoriales", {})
        return data
    else:
        st.error("No se encontró el documento del paciente.")
        return {}
    
st.header("Bioquímica sanguínea")

bioquimica_tab1, bioquimica_tab2, bioquimica_tab3, bioquimica_tab4, bioquimica_tab5, bioquimica_tab6, bioquimica_tab7 = st.tabs([
    "Glucosa", "Ácido úrico", "Enzimas hepáticas", "Proteínas", "Bilirrubina", "Lípidos", "Función renal"
    ])
data = obtener_laboratorio()

# --- BIOQUÍMICA SANGUÍNEA --
# --- GLUCOSA ---
glucosa = data.get("glucosa", None)
# --- ÁCIDO ÚRICO ---
acido_urico = data.get("acido urico", None)
# --- ENZIMAS HEPÁTICAS ---
alanina = data.get("alanina aminotransferasa", None)
aspartato = data.get("aspartato aminotransferasa", None)
# --- PROTEÍNAS ---
albumina = data.get("albumina", None)
globulina = data.get("globulina", None)
# --- BILIRRUBINA ---
directa = data.get("bilirrubina directa", None)
indirecta = data.get("bilirrubina indirecta", None)
total = data.get("bilirrubina total", None)
# --- LIPIDOS ---
colesterol = data.get("colesterol", None)
trigliceridos = data.get("trigliceridos", None)
# --- FUNCION RENAL ---
creatinina = data.get("creatinina", None)
urea = data.get("urea", None)

with bioquimica_tab1:
    fig_glucosa = gauge_chart(glucosa, "Glucosa", 100, 79, 80, 115, 116, 300)
    st.plotly_chart(fig_glucosa)   
with bioquimica_tab2:
    fig_urico = gauge_chart(acido_urico, "Ácido úrico", 7.7, 3.69, 3.7, 7.7, 7.71, 15)
    st.plotly_chart(fig_urico)   
with bioquimica_tab3:
    fig_alanina = gauge_chart(alanina, "Alanina aminotransferasa", 36, 3.9, 4, 36, 36.5, 50)
    st.plotly_chart(fig_alanina)
    fig_aspartato = gauge_chart(aspartato, "Aspartato aminotransferasa", 33, 7.9, 8, 33, 33.1, 50)
    st.plotly_chart(fig_aspartato)
with bioquimica_tab4:
    fig_albumina = gauge_chart(albumina, "Albumina", 5.4, 3.3, 3.4, 5.4, 5.45, 15)
    st.plotly_chart(fig_albumina)
    fig_globulina = gauge_chart(globulina, "Globulina", 3.5, 1.9, 2, 3.5, 3.6, 15)
    st.plotly_chart(fig_globulina)  
with bioquimica_tab5:
    fig_directa = gauge_chart(directa, "Bilirrubina directa", 0.3, 0, 0, 0.3, 0.301, 1)
    st.plotly_chart(fig_directa)
    fig_indirecta = gauge_chart(indirecta, "Bilirrubina indirecta", 10, 0.99, 1, 10, 10.1, 15)
    st.plotly_chart(fig_indirecta)
    fig_total = gauge_chart(total, "Bilirrubina total", 10, 0.99, 1, 10, 10.1, 15)
    st.plotly_chart(fig_total)
with bioquimica_tab6:
    fig_colesterol = gauge_chart(colesterol, "Colesterol", 200, 124, 125, 200, 201, 500)
    st.plotly_chart(fig_colesterol)
    fig_trigliceridos = gauge_chart(trigliceridos, "Trigliceridos", 150, 40, 41, 150, 151, 500)
    st.plotly_chart(fig_trigliceridos) 
with bioquimica_tab7:
    fig_creatinina = gauge_chart(creatinina, "Creatinina", 1.11, 0.49, 0.5, 1.1, 1.11, 3)
    st.plotly_chart(fig_creatinina)
    fig_urea = gauge_chart(urea, "Urea", 40, 14.9, 15, 40, 40.1, 100)    
    st.plotly_chart(fig_urea)
    
# --- ELECTROLITOS ---
st.header("Electrolitos")
electrolitos_tab1, electrolitos_tab2, electrolitos_tab3, electrolitos_tab4 = st.tabs(["Calcio", "Fósforo", "Potasio", "Sodio"])
electrolitos = obtener_laboratorio().get("electrolitos", {})
calcio = electrolitos.get("calcio", None)
fosforo = electrolitos.get("fosforo", None)
potasio = electrolitos.get("potasio", None)
sodio = electrolitos.get("sodio", None)

with electrolitos_tab1:
    fig_calcio = gauge_chart(calcio, "Calcio", 10, 8.75, 8.8, 10, 10.1, 15)
    st.plotly_chart(fig_calcio, use_container_width=True)
with electrolitos_tab2:   
    fig_fosforo = gauge_chart(fosforo, "Fósforo", 4.7, 2.99, 3, 4.7, 4.71, 10)
    st.plotly_chart(fig_fosforo, use_container_width=True)
with electrolitos_tab3:
    fig_potasio = gauge_chart(potasio, "Potasio", 5.1, 3.49, 3.5, 5.1, 5.11, 10)
    st.plotly_chart(fig_potasio, use_container_width=True)
with electrolitos_tab4:
    fig_sodio = gauge_chart(sodio, "Sodio", 145, 135.99, 136, 145, 145.01, 160)
    st.plotly_chart(fig_sodio, use_container_width=True)
    