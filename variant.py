import streamlit as st
import time
import random
import urllib.parse

# Definimos algunas opciones de "premio" o "sin premio"
# con su imagen correspondiente.
OPCIONES = [
    # Dos "sin premio" (vasco_2 y vasco_3)
    {
        "nombre": "Sin premio 😢",
        "file": "vasco_2.png"
    },
    {
        "nombre": "Sin premio 😢",
        "file": "vasco_3.png"
    },
    # Tres "premios"
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
    Muestra un link a WhatsApp Web para canjear el premio con Joni.
    """
    telefono_joni = "5491144042904"
    mensaje = f"Hola Joni, gané {label} en la Ruleta y quiero canjear mi premio."
    msg_encoded = urllib.parse.quote(mensaje)
    wsp_url = f"https://api.whatsapp.com/send?phone={telefono_joni}&text={msg_encoded}"
    st.markdown(f"[Canjear ahora por WhatsApp]({wsp_url})", unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Ruleta Sencilla con Emojis", layout="centered")

    # Título con emojis
    st.title("🎉🤞 ¡Bienvenid@ a la Ruleta de la Suerte! 🤞🎉")
    st.write("Dale clic al botón y esperá unos segundos para ver tu suerte…")

    if "resultado" not in st.session_state:
        st.session_state.resultado = None  # Guardará un dict {'nombre':..., 'file':...}

    # Estilo del botón
    st.markdown("""
    <style>
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
        width: 180px; /* Ajustar tamaño de la imagen según quieras */
    }
    </style>
    """, unsafe_allow_html=True)

    # Botón para "tirar"
    if st.button("¡Tirar la Ruleta! 🎁"):
        # Mostramos un spinner con mensaje
        with st.spinner("Girando la Ruleta… un momento por favor…"):
            time.sleep(2)  # Simula 2s de "giro"
        # Elegimos resultado al azar
        elegido = random.choice(OPCIONES)
        st.session_state.resultado = elegido

    # Si tenemos un resultado en session_state, lo mostramos
    if st.session_state.resultado:
        r = st.session_state.resultado
        # Mostramos la imagen centrada
        st.image(r["file"], caption="", use_column_width=False, width=180)
        
        # Vemos si es sin premio o no
        if "Sin premio" in r["nombre"]:
            st.warning(f"¡No ganaste nada! 😭 Volvé a intentar.")
        else:
            st.balloons()
            st.success(f"🎉 ¡Felicidades! Te tocó: {r['nombre']}")
            canjear_por_whatsapp(r["nombre"])

if __name__ == "__main__":
    main()
