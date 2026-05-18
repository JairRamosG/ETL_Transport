# app.py

import streamlit as st
import folium
from streamlit_folium import st_folium
from etl import run_etl
import locale
from datetime import datetime

# Configuración de la app
st.set_page_config(page_title="Bikepoints Londres", layout="wide")
st.title("Disponibilidad Bikepoints en Londres — En vivo")

# Inicializar estado de la sesión
if "df" not in st.session_state:
    try:
        # Ejecutar pipeline y filtrar sólo estaciones disponibles
        df = run_etl()
        df = df[df['disponible']=='Si']
        st.session_state.df = df

        # Fijar fecha de última actualización (ejemplo: 20 Oct 2025, 06:20)
        locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")
        st.session_state.last_updated = datetime.now().strftime("%d %b %Y, %H:%M")

    except Exception:
        st.session_state.df = None
        st.session_state.last_updated = "Nunca"

# Botón actualizar ("col1") e info de la actualización ("col2")
col1, col2 = st.columns([1,4])
with col1:
    if st.button("Actualizar"):
        with st.spinner("Actualizando info estaciones..."):
            df = run_etl()
            st.session_state.df = df
            st.session_state.last_updated = datetime.now().strftime("%d %b %Y, %H:%M")
        st.success("¡Listo!")

with col2:
    st.markdown(f"**Última actualización:** {st.session_state.last_updated}")

if st.session_state.df is not None:
    df = st.session_state.df

    # Métrica general
    c1, c2, c3 = st.columns(3)
    c1.metric("Total estaciones disponibles", int(len(df)))

    # Crear mapa centrado en la primera estación (solo inicial)
    lat_in, lon_in = df.iloc[0][['latitud', 'longitud']]
    m = folium.Map(location=[lat_in, lon_in], zoom_start=12)

    # Crear grupo de marcadores
    fg = folium.FeatureGroup(name="Estaciones Londres")

    # Iterar de manera eficiente sobre cada estación
    for est in df.itertuples(index=False):
        nombre = est.nombre_estacion
        lat, lon = est.latitud, est.longitud
        espacios = est.nEspaciosDisp
        bicis_est = est.nBicisEstandar
        bicis_el = est.nBicisElectricas

        # Color del popup y del marcador según disponibilidad total
        total_bicis = bicis_est + bicis_el
        if total_bicis == 0:
            bg_color = "#ffe6e6"  # rojo
            color = "red"
        elif total_bicis < 5:
            bg_color = "#fff3cd"  # amarillo
            color = "orange"
        else:
            bg_color = "#e6ffe6"  # verde
            color = "green"

        # Código HTML del popup
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
            🚲 {bicis_est} estándar<br>
            ⚡ {bicis_el} eléctricas<br>
            🅿️ {espacios} espacios
        </div>
        """

        # Añadir marcador
        fg.add_child(
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_str, max_width=250),
                tooltip=nombre,
                icon=folium.Icon(color=color)
            )
        )

    # Ajustar automáticamente el zoom del mapa al área total
    m.fit_bounds(df[['latitud', 'longitud']].values.tolist())

    # Mostrar mapa
    st_folium(
        m,
        feature_group_to_add=fg,
        width="100%",  # se adapta al contenedor
        height=600,
        returned_objects=[]  # Para no re-renderizar el mapa cada vez que el usuario interactúa
    )
else:
    st.info("No hay datos. Click en actualizar")

