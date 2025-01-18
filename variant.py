import streamlit as st
import time
import random
import urllib.parse

# Definimos 5 opciones (2 sin premio y 3 con premio)
OPCIONES = [
    # Sin premio
    {
        "nombre": "Sin premio 😢",
        "file": "vasco_2.png"
    },
    {
        "nombre": "Sin premio 😢",
        "file": "vasco_3.png"
    },
    # Premios
    {
        "nombre": "5% Descuento 🤩",
        "file": "vasco_0.png"
    },
    {
        "nombre": "7% Descuento 🤑",
        "file": "vasco_1.png"
    },
    {
        "nombre": "Ganaste un Juguete 🧸🎉",
        "file": "vasco_4.png"
    },
]

def canjear_por_whatsapp(label):
    """
    Link a WhatsApp para canjear el premio con Joni.
    """
    telefono_joni = "5491144042904"
    mensaje = f"Hola Joni, gané {label} en la Ruleta y quiero canjear mi premio."
    msg_encoded = urllib.parse.quote(mensaje)
    wsp_url = f"https://api.whatsapp.com/send?phone={telefono_joni}&text={msg_encoded}"
    st.markdown(f"[Canjear ahora por WhatsApp]({wsp_url})", unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Ruleta Centrada", layout="centered")

    # CSS para centrar todo el contenido
    st.markdown("""
    <style>
    /* Centrar todo en la página */
    main .block-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
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
    .resultado-img {
        display: block;
        margin: 1rem auto;
        width: 180px; /* Ajustar el tamaño de la imagen */
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("🎉🤞 ¡Bienvenid@ a la Ruleta de la Suerte! 🤞🎉")
    st.write("Dale clic al botón y esperá unos segundos para ver tu suerte…")

    if "resultado" not in st.session_state:
        st.session_state.resultado = None

    # Botón para tirar
    if st.button("¡Tirar la Ruleta! 🎁"):
        with st.spinner("Girando la Ruleta… un momento por favor…"):
            time.sleep(2)  # 2 segundos simulando giro
        elegido = random.choice(OPCIONES)
        st.session_state.resultado = elegido

    # Si ya tenemos un resultado, lo mostramos
    if st.session_state.resultado:
        r = st.session_state.resultado
        st.image(r["file"], caption="", width=180)
        
        if "Sin premio" in r["nombre"]:
            st.warning("¡No ganaste nada! Intentalo de nuevo.")
        else:
            st.balloons()
            st.success(f"¡Felicidades! Te tocó: {r['nombre']}")
            canjear_por_whatsapp(r["nombre"])

if __name__ == "__main__":
    main()
