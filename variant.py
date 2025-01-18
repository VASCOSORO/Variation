import streamlit as st
import time
import random
import urllib.parse
import os

# 5 opciones (2 sin premio, 3 con premio), 
# con su label y el filename
OPCIONES = [
    {"nombre": "Sin premio 😢",        "file": "vasco_2.png"},
    {"nombre": "Sin premio 😢",        "file": "vasco_3.png"},
    {"nombre": "5% Descuento 🤩",     "file": "vasco_0.png"},
    {"nombre": "7% Descuento 🤑",     "file": "vasco_1.png"},
    {"nombre": "Ganaste un Juguete 🧸🎉", "file": "vasco_4.png"},
]

def canjear_por_whatsapp(label):
    """Muestra link a WhatsApp para canjear el premio."""
    telefono_joni = "5491144042904"
    mensaje = f"Hola Joni, gané {label} en la Ruleta y quiero canjear mi premio."
    msg_encoded = urllib.parse.quote(mensaje)
    wsp_url = f"https://api.whatsapp.com/send?phone={telefono_joni}&text={msg_encoded}"
    st.markdown(f"[Canjear ahora por WhatsApp]({wsp_url})", unsafe_allow_html=True)

def main():
    # Layout WIDE y un título de la página
    st.set_page_config(page_title="Push The Button - Mundo Peluche", layout="wide")

    # CSS para centrar contenido a 600px de ancho
    st.markdown("""
    <style>
    .block-container {
        max-width: 600px;
        margin: 0 auto; 
        text-align: center; 
    }
    div.stButton > button {
        color: #fff;
        background-color: #d81b60;
        font-size: 1.2rem;
        border-radius: 12px;
        border: 2px solid #92093a;
        padding: 0.6rem 1.5rem;
        margin-bottom: 1rem;
    }
    div.stButton > button:hover {
        background-color: #92093a;
        color: #eee;
    }
    .footer-vasco {
        font-size: 0.8rem;
        color: #888;
        margin-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

    # Títulos centrados
    st.markdown("<h1>Push The Button</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#ff006e;'>Mundo Peluche</h3>", unsafe_allow_html=True)

    # Instrucciones
    st.write("Dale clic al botón y esperá unos segundos...")

    # Chequeo si la variable 'resultado' existe
    if "resultado" not in st.session_state:
        st.session_state.resultado = None

    # Botón
    if st.button("¡Presioná aquí! 🚀"):
        with st.spinner("Girando… un momento por favor…"):
            time.sleep(2)
        elegido = random.choice(OPCIONES)
        st.session_state.resultado = elegido

    # Si ya tenemos un resultado
    if st.session_state.resultado:
        r = st.session_state.resultado

        # Leemos la imagen local como bytes
        try:
            with open(r["file"], "rb") as f:
                data = f.read()
        except FileNotFoundError:
            # Si no lo encuentra, mostramos un warning
            st.warning(f"No se encontró la imagen '{r['file']}'. Verifica nombres y ubicación.")
            return

        # Mostramos la imagen con st.image, centrada por el contenedor
        st.image(data, width=180)

        # Label debajo, solo si querés 
        st.markdown(f"### {r['nombre']}")

        # Mensaje de sin premio o premio
        if "Sin premio" in r["nombre"]:
            st.warning("¡No ganaste nada! Intentalo de nuevo.")
        else:
            st.balloons()
            st.success("¡Felicidades! Ganaste un premio.")
            canjear_por_whatsapp(r["nombre"])

    # Footer
    st.markdown("<div class='footer-vasco'>powered by <strong>VASCO</strong></div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
