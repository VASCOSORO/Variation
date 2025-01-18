import streamlit as st
import time
import random
import urllib.parse

# Configuramos 5 “opciones”
OPCIONES = [
    # Sin premio
    {
        "nombre": "Sin premio",
        "file": "vasco_2.png"  # hongo triste
    },
    {
        "nombre": "Sin premio",
        "file": "vasco_3.png"  # fantasma
    },
    # Premios
    {
        "nombre": "5% Descuento",
        "file": "vasco_0.png"
    },
    {
        "nombre": "7% Descuento",
        "file": "vasco_1.png"
    },
    {
        "nombre": "Ganaste un Juguete",
        "file": "vasco_4.png"
    },
]

def canjear_por_whatsapp(label):
    """
    Link de WhatsApp para canjear el premio con Joni.
    """
    telefono_joni = "5491144042904"
    mensaje = f"Hola Joni, gané un {label} en la Ruleta y quiero canjear mi premio."
    msg_encoded = urllib.parse.quote(mensaje)
    wsp_url = f"https://api.whatsapp.com/send?phone={telefono_joni}&text={msg_encoded}"
    st.markdown(f"[Canjear ahora por WhatsApp]({wsp_url})", unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Girá y Mirá tu Premio", layout="centered")
    st.title("Girá la Ruleta y Participá de Lindos Premios (Sin Círculo)")
    st.write("Hacé clic, se mostrará 'Girando...' y después te diremos si ganaste algo o no.")

    # Almacenamos el resultado en session_state
    if "resultado" not in st.session_state:
        st.session_state.resultado = None  # guardará un dict con {nombre, file}

    # CSS para botón y mensaje
    st.markdown("""
    <style>
    div.stButton > button {
        color: #fff;
        background-color: #e91e63;
        font-size: 1.2rem;
        border-radius: 12px;
        border: 2px solid #b00046;
        padding: 0.6rem 1.5rem;
        margin-bottom: 1rem;
    }
    div.stButton > button:hover {
        background-color: #b00046;
        color: #eee;
    }
    .girando-msg {
        font-size: 1.3rem;
        color: #ff006e;
        text-align: center;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    .premio-img {
        display: block;
        margin: 0 auto;
        width: 120px; /* Ajustar si querés */
    }
    </style>
    """, unsafe_allow_html=True)

    # Botón para “girar”
    girar = st.button("¡Tirar la Ruleta!")
    if girar:
        # Mostramos un mensaje grande
        st.markdown("<div class='girando-msg'>Girando la Ruleta...</div>", unsafe_allow_html=True)
        # Forzamos flush de la interfaz
        st.experimental_rerun()

    # Si se hizo click, pero no hay resultado => simular giro
    if girar and st.session_state.resultado is None:
        time.sleep(2)  # Simulamos 2s de “giro”
        # Elegimos aleatorio
        elegido = random.choice(OPCIONES)
        st.session_state.resultado = elegido
        st.experimental_rerun()

    # Mostrar resultado
    if st.session_state.resultado is not None:
        r = st.session_state.resultado
        st.image(r["file"], caption="", width=150)
        if "Sin premio" in r["nombre"]:
            st.warning("¡No ganaste nada! Probá de nuevo.")
        else:
            st.balloons()
            st.success(f"¡Felicidades! Te tocó: {r['nombre']}")
            canjear_por_whatsapp(r["nombre"])

if __name__ == "__main__":
    main()
