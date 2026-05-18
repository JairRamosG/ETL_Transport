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

with col2:
    st.markdown(f'Ultima actualización - {st.session_state.last_updated}')

if st.session_state.df is not None:
    df = st.session_state.df

    c1, c2, c3 = st.columns(3)
    c1.metric('Total de estaciones', len(df))

    lat,lon = df.iloc[0][['latitud', 'longitud']]
    m = folium.Map(location = [lat, lon], zoom_start = 12)
    fg = folium.FeatureGroup(name = "Estaciones Londres")


    # Iteración por cada estación
    for estacion in df.itertuples(index = False):
        nombre = estacion.nombre_estacion
        lat, lon = estacion.latitud, estacion.longitud
        espacios = estacion.nEspaciosDisp
        bicis_estandar = estacion.nBicisEstandar
        bicis_e = estacion.nBicisElectricas

        total_bicis = bicis_estandar + bicis_e
        # ponerle colores
        if total_bicis == 0:
            bg_color = "#a82424"
            color = "red"
        elif total_bicis <= 7:
            bg_color = "#c0e04d"
            color = "orange"   
        else:
            bg_color = "#88f09b"
            color = "green"
            
        # pupop de cada estación
        popup_str = f"""
        <div style="
            background-color:{bg_color};
            border-radius:8px;
            padding:8px 12px;
            font-size:13px;
            line-height:1.5;
            color:#333;
        ">
            <b style="font-size:14px;">{nombre}</b><br>
            🚲 {bicis_estandar} estándar<br>
            ⚡ {bicis_e} eléctricas<br>
            🅿️ {espacios} espacios
        </div> """

        # poner figurita en el mapa
        fg.add_child(
            folium.Marker(
                location = [lat, lon],
                popup = folium.Popup(popup_str, max_width = 250),
                tool_tip = nombre,
                icon = folium.Icon(color = color)
            )
        )

    st_folium(
        m,
        feature_group_to_add = fg,
        width = "100%",
        height = 700,
    )

else:
    st.info('Sin datos actualizados')