import streamlit as st
import time
import random
import urllib.parse

# Definimos 5 opciones (2 sin premio, 3 con premio)
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
    Muestra un link a WhatsApp para canjear el premio con Joni.
    """
    telefono_joni = "5491144042904"
    mensaje = f"Hola Joni, gané {label} en la Ruleta y quiero canjear mi premio."
    msg_encoded = urllib.parse.quote(mensaje)
    wsp_url = f"https://api.whatsapp.com/send?phone={telefono_joni}&text={msg_encoded}"
    st.markdown(f"[Canjear ahora por WhatsApp]({wsp_url})", unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Push The Button - Mundo Peluche", layout="centered")

    # CSS para centrar todo y definir estilos
    st.markdown("""
    <style>
    /* Centrar todo el contenido */
    main .block-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
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
    /* Imagen de resultado */
    .resultado-img {
        display: block;
        margin: 1rem auto;
        width: 180px; /* Ajustar el tamaño de la imagen */
    }
    </style>
    """, unsafe_allow_html=True)

    # Título y subtítulo centrados
    st.markdown("<h1 style='text-align:center;'>Push The Button</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center; color:#ff006e;'>Mundo Peluche</h3>", unsafe_allow_html=True)

    st.write("Dale clic al botón y esperá unos segundos...")

    if "resultado" not in st.session_state:
        st.session_state.resultado = None

    # Botón
    if st.button("¡Presioná aquí! 🚀"):
        with st.spinner("Girando… un momento por favor…"):
            time.sleep(2)  # Simulamos 2s
        elegido = random.choice(OPCIONES)
        st.session_state.resultado = elegido

    # Mostrar resultado
    if st.session_state.resultado:
        r = st.session_state.resultado
        # Mostrar imagen
        st.image(r["file"], caption="", width=180)
        if "Sin premio" in r["nombre"]:
            st.warning("¡No ganaste nada! Intentalo de nuevo.")
        else:
            st.balloons()
            st.success(f"¡Felicidades! Te tocó: {r['nombre']}")
            canjear_por_whatsapp(r["nombre"])

if __name__ == "__main__":
    main()
