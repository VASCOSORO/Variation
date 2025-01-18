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
    wsp_text = urllib.parse.quote(mensaje)
    wsp_url = f"https://api.whatsapp.com/send?phone={telefono_joni}&text={wsp_text}"
    st.markdown(f"[Canjear ahora por WhatsApp]({wsp_url})", unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Push The Button - Mundo Peluche", layout="wide")

    # CSS contenedor 600px centrado
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

    # Título y subtítulo
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

    # Mostrar resultado si hay uno
    if st.session_state.resultado:
        r = st.session_state.resultado

        # Renderizamos imagen + label JUNTOS y centrados, sin texto extra
        st.markdown(f"""
        <div style="display:flex; flex-direction:column; align-items:center; margin:20px 0;">
            <img src="{r['file']}" alt="{r['nombre']}" style="width:180px; margin-bottom:10px;" />
            <h3 style="margin:0;">{r['nombre']}</h3>
        </div>
        """, unsafe_allow_html=True)

        if "Sin premio" in r["nombre"]:
            st.warning("¡No ganaste nada! Intentalo de nuevo.")
        else:
            # Premio, sin repetir el label otra vez
            st.balloons()
            st.success("¡Felicidades! Ganaste un premio.")
            canjear_por_whatsapp(r["nombre"])

    # Footer
    st.markdown("<div class='footer-vasco'>powered by <strong>VASCO</strong></div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
