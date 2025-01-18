import streamlit as st
import time
import random
import urllib.parse

# Definimos 5 opciones (2 sin premio, 3 premios), con su nombre e imagen
OPCIONES = [
    # Sin premio
    {
        "nombre": "Sin premio 😢",
        "file": "vasco_2.png"  # Ej: hongo triste
    },
    {
        "nombre": "Sin premio 😢",
        "file": "vasco_3.png"  # Ej: fantasmita
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
    Muestra link a WhatsApp para canjear el premio con Joni.
    """
    telefono_joni = "5491144042904"
    mensaje = f"Hola Joni, gané {label} en la Ruleta y quiero canjear mi premio."
    msg_encoded = urllib.parse.quote(mensaje)
    wsp_url = f"https://api.whatsapp.com/send?phone={telefono_joni}&text={msg_encoded}"
    st.markdown(f"[Canjear ahora por WhatsApp]({wsp_url})", unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Ruleta Simple", layout="centered")

    st.title("🎉🤞 ¡Bienvenid@ a la Ruleta de la Suerte! 🤞🎉")
    st.write("Dale clic al botón y esperá unos segundos para ver tu suerte…")

    if "resultado" not in st.session_state:
        st.session_state.resultado = None

    # Estilos para el botón e imágenes
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
        width: 180px; /* Ajustá el tamaño de la imagen */
    }
    </style>
    """, unsafe_allow_html=True)

    if st.button("¡Tirar la Ruleta! 🎁"):
        # Spinner "Girando..."
        with st.spinner("Girando la Ruleta… un momento por favor…"):
            time.sleep(2)  # 2s simulando giro
        # Sorteo
        elegido = random.choice(OPCIONES)
        st.session_state.resultado = elegido

    # Mostrar resultado si está definido
    if st.session_state.resultado:
        r = st.session_state.resultado
        # Mostrar la imagen en tamaño fijo (width=180)
        st.image(r["file"], caption="", width=180)
        
        if "Sin premio" in r["nombre"]:
            st.warning("¡No ganaste nada! Intentalo de nuevo.")
        else:
            st.balloons()
            st.success(f"¡Felicidades! Te tocó: {r['nombre']}")
            canjear_por_whatsapp(r["nombre"])

if __name__ == "__main__":
    main()
