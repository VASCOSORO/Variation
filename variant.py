import streamlit as st
import requests
import json

# URL de la API de Node.js expuesta por ngrok
API_URL = "https://839c-186-128-183-44.ngrok-free.app/"  # Reemplazá con tu URL de ngrok

st.title("CRM - Batibot")

try:
    # Intentamos obtener los mensajes desde la API
    response = requests.get(API_URL)
    response.raise_for_status()  # Verifica que no haya errores HTTP
    mensajes = response.json()   # Decodificamos la respuesta JSON

    if mensajes:
        st.subheader("Mensajes de WhatsApp")
        for mensaje in mensajes:
            st.write(f"De: {mensaje['numero']}")
            st.write(f"Mensaje: {mensaje['mensaje']}")
            st.write("---")
    else:
        st.info("No hay mensajes disponibles en este momento.")
except requests.exceptions.RequestException as e:
    st.error(f"No se pudo conectar con la API: {e}")
except json.decoder.JSONDecodeError:
    st.error("Error decodificando la respuesta JSON. La API no devolvió un JSON válido.")
