import streamlit as st
import time
import random
import urllib.parse

OPCIONES = [
    {"nombre": "Sin premio 😢", "file": "vasco_2.png"},
    {"nombre": "Sin premio 😢", "file": "vasco_3.png"},
    {"nombre": "5% Descuento 🤩", "file": "vasco_0.png"},
    {"nombre": "7% Descuento 🤑", "file": "vasco_1.png"},
    {"nombre": "Ganaste un Juguete 🧸🎉", "file": "vasco_4.png"},
]

def canjear_por_whatsapp(label):
    telefono_joni = "5491144042904"
    mensaje = f"Hola Joni, gané {label} en la Ruleta y quiero canjear mi premio."
    msg_encoded = urllib.parse.quote(mensaje)
    wsp_url = f"https://api.whatsapp.com/send?phone={telefono_joni}&text={msg_encoded}"
    st.markdown(f"[Canjear ahora por WhatsApp]({wsp_url})", unsafe_allow_html=True)

def main():
    # layout="wide" para poder centrar
    st.set_page_config(page_title="Push The Button - Mundo Peluche", layout="wide")

    # CSS para contenedor centrado
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

    st.markdown("Dale clic al botón y esperá unos segundos...")

    if "resultado" not in st.session_state:
        st.session_state.resultado = None

    # Botón
    if st.button("¡Presioná aquí! 🚀"):
        with st.spinner("Girando… un momento por favor…"):
            time.sleep(2)
        elegido = random.choice(OPCIONES)
        st.session_state.resultado = elegido

    # Mostrar resultado
    if st.session_state.resultado:
        r = st.session_state.resultado

        # HTML: imagen arriba y texto debajo, ambos centrados
        st.markdown(f"""
        <div style="display:flex; flex-direction:column; align-items:center; margin:20px 0;">
            <img src="{r['file']}" alt="{r['nombre']}" style="width:180px; margin-bottom:10px;" />
            <h3 style="margin:0;">{r['nombre']}</h3>
        </div>
        """, unsafe_allow_html=True)

        # Luego los mensajes de premio o no
        if "Sin premio" in r["nombre"]:
            st.warning("¡No ganaste nada! Intentalo de nuevo.")
        else:
            st.balloons()
            st.success(f"¡Felicidades! Te tocó: {r['nombre']}")
            canjear_por_whatsapp(r["nombre"])

    # Footer
    st.markdown("<div class='footer-vasco'>powered by <strong>VASCO</strong></div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
