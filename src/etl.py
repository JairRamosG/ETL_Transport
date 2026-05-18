import pandas as pd
import requests
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv('APP_ID')
PRIMARY_KEY = os.getenv('PRIMARY_KEY')
ENDPOINT = os.getenv('ENDPOINT')

params = {
    'app_id': API_ID,
    'app_key': PRIMARY_KEY
}

def get_api_data(endpoint, params):
    try:
        response = requests.get(endpoint, params = params)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f'Error cargando datos: {str(e)}')
        return None

def transform_load(data):

    info_estaciones = {
        'nombre_estacion' : [], #TerminalName
        'latitud' : [], #lat
        'longitud' : [], #lon

        'disponible' : [], #Locked
        'nBicis' : [], #NnBikes
        'nEspaciosDisp' : [], #NbEmptyDocks
        'nEspacios' : [], #NbDocks
        'nBicisEstandar' : [], #NbStandardBikes
        'nBicisElectricas' : [], #NbEBikes
        'ultima_actualizacion' : []}
    
    for estacion in data:
        # Capa exterior
        info_estaciones['nombre_estacion'].append(estacion['commonName'])
        info_estaciones['latitud'].append(estacion['lat'])
        info_estaciones['longitud'].append(estacion['lon'])

        # Capa additionalProperties
        #Iterar por el key "additionalProperties" y extraer info actualizada de la estación
        for item in estacion['additionalProperties']:
            if item['key'] == 'NbBikes':
                info_estaciones['nBicis'].append(int(item['value']))

                # Extraer marca de tiempo última actualización
                datetime_update = pd.to_datetime(item['modified'])

                # Preservar únicamente hasta horas, minutos y segundos
                datetime_update = datetime_update.strftime("%Y-%m-%d %H:%M:%S")
                info_estaciones['ultima_actualizacion'].append(datetime_update)
                
            if item['key'] == 'NbEmptyDocks':
                info_estaciones['nEspaciosDisp'].append(int(item['value']))
            if item['key'] == 'NbDocks':
                info_estaciones['nEspacios'].append(int(item['value']))
            if item['key'] == 'NbStandardBikes':
                info_estaciones['nBicisEstandar'].append(int(item['value']))
            if item['key'] == 'NbEBikes':
                info_estaciones['nBicisElectricas'].append(int(item['value']))
            if item['key'] == 'Locked':
                if item['value']=="false":
                    info_estaciones['disponible'].append('Si')
                else:
                    info_estaciones['disponible'].append('No')
        
    df = pd.DataFrame(info_estaciones)
    return df

def run_etl():
    data = get_api_data(ENDPOINT, params)
    if data is None:
        st.error('Verificar las credenciales de la API')
        return None
    df = transform_load(data)
    return df