# Disponibilidad en Cicloestaciones de Londres

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)
![Folium](https://img.shields.io/badge/Folium-77B829?style=flat&logo=leaflet&logoColor=white)
![Requests](https://img.shields.io/badge/Requests-2CA5E0?style=flat&logo=python&logoColor=white)
![dotenv](https://img.shields.io/badge/dotenv-ECD53F?style=flat&logo=dotenv&logoColor=black)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)

Aplicación web interactiva que implementa un pipeline **ETL** (Extract, Transform, Load) para consultar en tiempo real la disponibilidad de bicicletas y espacios en las cicloestaciones de Londres, visualizándolas sobre un mapa interactivo.

---

## ¿Cómo funciona?

El proyecto sigue el flujo básico de un ETL:

- **Extract** — Consume el endpoint `BikePoint` de la API pública de Transport for London (TfL): [`GET /BikePoint`](https://api-portal.tfl.gov.uk/api-details#api=BikePoint&operation=BikePoint_GetAll), que devuelve la información en tiempo real de todas las cicloestaciones de la ciudad.
- **Transform** — Limpia y estructura la respuesta JSON: extrae nombre, coordenadas, número de bicicletas estándar, bicicletas eléctricas, espacios disponibles y última actualización de cada estación.
- **Load** — Carga los datos procesados en un `DataFrame` de Pandas y los presenta en una interfaz web con mapa interactivo construida con Streamlit y Folium.

---

## Características

- Tiene un mapa interactivo con un marcador por cada cicloestación activa.
- Código de colores por disponibilidad:
  - **Verde** — más de 5 bicicletas disponibles
  - **Naranja** — entre 1 y 5 bicicletas disponibles
  - **Rojo** — sin bicicletas disponibles
- Popup por estación con detalle de bicicletas estándar, eléctricas y espacios libres.
- Botón para actualizar los datos en cualquier momento sin recargar la página.
- Marca de tiempo de la última actualización.

---


## Despliegue en Streamlit Cloud

Para desplegar en [Streamlit Cloud](https://streamlit.io/cloud), las variables de entorno deben configurarse desde **Settings → Secrets** del proyecto, en lugar del archivo `.env`:

---

## API utilizada

Este proyecto consume la API pública de **Transport for London (TfL)**:

| Campo | Detalle |
|---|---|
| Proveedor | Transport for London (TfL) |
| Endpoint | `GET /BikePoint` |
| Documentación | [api-portal.tfl.gov.uk](https://api-portal.tfl.gov.uk/api-details#api=BikePoint&operation=BikePoint_GetAll) |
| Autenticación | `app_id` + `app_key` como query params |
| Formato | JSON |

---

![alt text](image.png)

---

## Enlace

https://etl-bicis.streamlit.app/