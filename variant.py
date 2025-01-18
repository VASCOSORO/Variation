import streamlit as st
from streamlit_lottie import st_lottie
import requests
import random
import time

def load_lottieurl(url: str):
    """Carga un JSON Lottie desde una URL."""
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def ruleta_lottie():
    st.title("Ruleta Lottie Copada")
    st.write("Este ejemplo muestra una animación 'de adorno' y luego se elige aleatoriamente el premio.")

    # Un Lottie de ruleta cualquiera
    # (Podés buscar otro en https://lottiefiles.com/ que te guste más)
    wheel_url = "https://assets2.lottiefiles.com/packages/lf20_qcqixj0x.json"
    wheel_anim = load_lottieurl(wheel_url)

    # Sectores / resultados
    sectores = [
        "5% Descuento", "7% Descuento", "12% Descuento",
        "Ganaste un Peluche", "Ganaste un Juguete",
        "Sin premio", "Sin premio", "Sin premio"
    ]

    # Guardamos el último resultado en session_state
    if "ruleta_result" not in st.session_state:
        st.session_state.ruleta_result = None

    if st.button("¡Girar la Ruleta!"):
        # Mostramos la animación Lottie con loop=False
        st_lottie(wheel_anim, key="spin", loop=False, height=300)
        st.info("Girando la ruleta... Esperá un momento...")
        time.sleep(3)  # Simulamos 3s de 'giro'
        
        # Elegimos un resultado aleatorio
        st.session_state.ruleta_result = random.choice(sectores)

    # Mostramos el resultado si ya se definió
    if st.session_state.ruleta_result:
        if st.session_state.ruleta_result.startswith("Sin"):
            st.warning("¡No ganaste nada! Volvé a probar.")
        else:
            st.balloons()
            st.success(f"¡Felicidades! Te tocó: {st.session_state.ruleta_result}")
            # Si querés el link a WhatsApp:
            # canjear_por_whatsapp(st.session_state.ruleta_result)

def main():
    st.set_page_config(page_title="Ruleta Lottie", layout="centered")
    ruleta_lottie()

if __name__ == "__main__":
    main()
