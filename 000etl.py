#!/usr/bin/env python3

"""
Este script es un flujo ETL (extract-transform-load)
que permite leer datos sobre disponibilidad de bicicletas
en la ciudad de Londres, realiza el pre-procesamiento y genera
un DataFrame como resultado.
"""

import streamlit as st
import requests
import pandas as pd

# Inicializar variables para acceder a la API
APP_ID = "api_bikepoint"
PRIMARY_KEY = st.secrets["api"]["API_PRIMARY_KEY"]
ENDPOINT = "https://api.tfl.gov.uk/BikePoint/"

params = {
    "app_id": APP_ID,
    "app_key": PRIMARY_KEY
}

# Extract
def get_api_data(endpoint, params):
    try:
        response = requests.get(endpoint, params=params)

        # Mostrar excepción si hay algún error
        response.raise_for_status()

        # Si no hay error extraer los datos en formato JSON
        data = response.json()
        return data
    
    # Si lo anterior no funciona imprimir error
    except requests.exceptions.RequestException as e:
        print(f"Error descargando los datos: {e}")
        return None

# Transform
def transform_load_data(data):
    # Diccionario donde se almacenará la información de cada estación
    info_stations = {
        'nombre_estacion': [], # stationName
        'disponible': [], # Locked
        'nBicis': [], # NbBikes
        'nEspaciosDisp': [], # nbEmptyDocks
        'nEspacios': [], # NbDocks
        'nBicisEstandar': [], # NbStandardBikes
        'nBicisElectricas': [], # NbEBikes
        'latitud': [],
        'longitud': []
    }

    for station in data:
        # Almacenar nombre de la estación, latitud y longitud
        info_stations['nombre_estacion'].append(station['commonName'])
        info_stations['latitud'].append(station['lat'])
        info_stations['longitud'].append(station['lon'])

        # Iterar por el key "additionalProperties" y extraer info actualizada de la estación
        for item in station['additionalProperties']:
            if item['key'] == 'NbBikes':
                info_stations['nBicis'].append(int(item['value']))   
            if item['key'] == 'NbEmptyDocks':
                info_stations['nEspaciosDisp'].append(int(item['value']))
            if item['key'] == 'NbDocks':
                info_stations['nEspacios'].append(int(item['value']))
            if item['key'] == 'NbStandardBikes':
                info_stations['nBicisEstandar'].append(int(item['value']))
            if item['key'] == 'NbEBikes':
                info_stations['nBicisElectricas'].append(int(item['value']))
            if item['key'] == 'Locked':
                if item['value']=="false":
                    info_stations['disponible'].append('Si')
                else:
                    info_stations['disponible'].append('No')

    # A DataFrame de Pandas
    df = pd.DataFrame(info_stations)
    return df

# Ejecutar pipeline
def run_etl():
    data = get_api_data(ENDPOINT, params)
    df = transform_load_data(data)
    return df