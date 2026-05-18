import streamlit as st
import folium
from streamlit_folium import st_folium
from etl import run_etl
import locale
from datetime import datetime

st.set_page_config(page_title = "Bikepoints Londres", layout = "wide")
st.title('Disponibilidad en ciclo estaciones')

if 'df' not in st.session_state:
    try:
        df = run_etl()
        df = df[df['Disponible'] == 'Si']
        st.session_state.df = df

        locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")
        st.session_state.last_updated = datetime.now().strftime("%d %b %Y, %H:%M")
    
    except Exception:
        st.session_state.df = None
        st.session_state.last_updated = 'Nunca'

col1, col2 = st.columns([1, 4])
with col1:
    if st.button('Actualizar'):
        with st.spinner('Obteniendo información... '):
            df = run_etl()
            st.session_state.df = df 
            st.session_state.last_updated = datetime.now().strftime("%d %b %Y, %H:%M")
        st.success('Listo')