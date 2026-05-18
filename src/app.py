import streamlit as st
import folium
from streamlit_folium import st_folium
from etl import run_etl
import locale
from datetime import datetime

st.set_page_config(page_title = "Bikepoints Londres", layout = "wide")
st.title('Disponibilidad en ciclo estaciones')