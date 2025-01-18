import streamlit as st
import time
import random
import urllib.parse

# 5 opciones (2 sin premio y 3 con premio)
OPCIONES = [
    {"nombre": "Sin premio 😢", "file": "vasco_2.png"},
    {"nombre": "Sin premio 😢", "file": "vasco_3.png"},
    {"nombre": "5% Descuento 🤩", "file": "vasco_0.png"},
    {"nombre": "7% Descuento 🤑", "file": "vasco_1.png"},
    {"nombre": "Ganaste un Juguete 🧸🎉", "file": "vasco_4.png"},
]

def canjear_por_whatsapp(label):
    """Link a WhatsApp para canjear el premio con Joni."""
    telefono_joni = "5491144042904"
    mensaje = f"Hola Joni, gané {label} en la Ruleta y quiero canjear mi premio."
    msg_encoded = urllib.parse.quote(mensaje)
    wsp_url = f"https://api.whatsapp.com/send?phone={telefono_joni}&text={msg_encoded}"
    st.markdown(f"[Canjear ahora por WhatsApp]({wsp_url})", unsafe_allow_html=True)

def main():
    # Layout "wide" para que el contenedor se centre a lo ancho
    st.set_page_config(page_title="Push The Button - Mundo Peluche", layout="wide")

    # CSS: un contenedor de ancho fijo y centrado, con texto al centro
    st.markdown("""
    <style>
    /* Ajustamos el contenedor principal de Streamlit */
    .block-container {
        max-width: 600px; /* Ajustá el ancho deseado */
        margin: 0 auto;   /* Centra horizontalmente */
        text-align: center; /* Texto y elementos centrados */
    }
    /* Botón */
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
    </style>
    """, unsafe_allow_html=True)

    # Título y subtítulo (HTML) centrados
    st.markdown("<h1>Push The Button</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#ff006e;'>Mundo Peluche</h3>", unsafe_allow_html=True)

    st.markdown("Dale clic al botón y esperá unos segundos...")

    if "resultado" not in st.session_state:
        st.session_state.resultado = None

    # Botón para “tirar”
    if st.button("¡Presioná aquí! 🚀"):
        with st.spinner("Girando… un momento por favor…"):
            time.sleep(2)  # Simulamos 2s
        # Sorteo
        elegido = random.choice(OPCIONES)
        st.session_state.resultado = elegido

    # Mostrar resultado
    if st.session_state.resultado:
        r = st.session_state.resultado
        st.image(r["file"], width=180)
        if "Sin premio" in r["nombre"]:
            st.warning("¡No ganaste nada! Intentalo de nuevo.")
        else:
            st.balloons()
            st.success(f"¡Felicidades! Te tocó: {r['nombre']}")
            canjear_por_whatsapp(r["nombre"])

    # Footer con "powered by VASCO"
    st.markdown(
        "<p style='font-size:0.8rem; color:#888; margin-top:2rem;'>powered by <strong>VASCO</strong></p>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
