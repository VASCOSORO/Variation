import streamlit as st
from streamlit_lottie import st_lottie
import json
import random
import time

def ruleta_lottie_local():
    st.title("Ruleta Lottie Copada (Local JSON)")
    st.write("Usamos un archivo .json descargado, así evitamos problemas de URL.")

    # Leemos el JSON local
    with open("wheel.json", "r") as f:
        wheel_anim = json.load(f)

    sectores = [
        "5% Descuento", "7% Descuento", "12% Descuento",
        "Ganaste un Peluche", "Ganaste un Juguete",
        "Sin premio", "Sin premio", "Sin premio"
    ]

    if "ruleta_result" not in st.session_state:
        st.session_state.ruleta_result = None

    if st.button("¡Girar la Ruleta!"):
        st_lottie(wheel_anim, key="spin", loop=False, height=300)
        st.info("Girando la ruleta... Esperá un momento...")
        time.sleep(3)
        st.session_state.ruleta_result = random.choice(sectores)

    # Mostramos resultado
    if st.session_state.ruleta_result:
        if "Sin premio" in st.session_state.ruleta_result:
            st.warning("¡No ganaste nada! Volvé a probar.")
        else:
            st.balloons()
            st.success(f"¡Felicidades! Te tocó: {st.session_state.ruleta_result}")

def main():
    st.set_page_config(page_title="Ruleta Lottie (Local)", layout="centered")
    ruleta_lottie_local()

if __name__ == "__main__":
    main()
