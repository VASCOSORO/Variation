import streamlit as st
import streamlit.components.v1 as components
import time
import random
import urllib.parse

# Definimos 8 sectores, todos con el mismo color
WHEEL_SECTORS = [
    {"label": "5% Descuento",       "color": "#0080ff"},
    {"label": "7% Descuento",       "color": "#0080ff"},
    {"label": "12% Descuento",      "color": "#0080ff"},
    {"label": "Ganaste un Peluche", "color": "#0080ff"},
    {"label": "Ganaste un Juguete", "color": "#0080ff"},
    {"label": "Sin premio",         "color": "#0080ff"},
    {"label": "Sin premio",         "color": "#0080ff"},
    {"label": "Sin premio",         "color": "#0080ff"},
]

def generar_ruleta_html(angle):
    """
    Genera el HTML/CSS de la ruleta con clip-path y un color único.
    El parámetro 'angle' es el total de rotación acumulado (grados).
    """
    slices_html = []
    # Cada sector se ubica a i * 45°
    for i, sec in enumerate(WHEEL_SECTORS):
        deg_start = i * 45
        slice_html = f"""
        <div class="slice slice-{i}" style="
             background-color:{sec['color']};
             transform: rotate({deg_start}deg);">
            <div class="slice-text">{sec['label']}</div>
        </div>
        """
        slices_html.append(slice_html)

    slices_joined = "\n".join(slices_html)

    # CSS: cada porción se recorta con clip-path
    # para formar un "wedge" de 45°.
    html_code = f"""
    <style>
    .ruleta-container {{
        width: 400px;
        height: 400px;
        margin: 0 auto;
        position: relative;
    }}
    .arrow {{
        width: 0;
        height: 0;
        border-left: 20px solid transparent;
        border-right: 20px solid transparent;
        border-bottom: 30px solid #ff006e;
        position: absolute;
        top: -50px; /* un poco más arriba */
        left: calc(50% - 20px);
        z-index: 999;
    }}
    .ruleta-wheel {{
        width: 100%;
        height: 100%;
        border-radius: 50%;
        border: 6px solid #333;
        position: relative;
        /* 4s para que se note el giro */
        transition: all 4s cubic-bezier(0.25, 0.1, 0.25, 1);
        transform: rotate({angle}deg);
        overflow: hidden;
    }}
    .slice {{
        width: 100%;
        height: 100%;
        position: absolute;
        top: 0;
        left: 0;
        /* "rebanada" de 45° usando clip-path */
        clip-path: polygon(50% 50%, 100% 0%, 100% 100%);
        transform-origin: 50% 50%;
    }}
    .slice-text {{
        /* giramos en contra 22.5° para que quede horizontal */
        transform: rotate(-22.5deg);
        transform-origin: center center;
        position: absolute;
        top: 0;
        left: 50%;
        margin-left: -40px;
        margin-top: 10px;
        width: 80px;
        text-align: center;
        font-size: 0.9rem;
        color: #fff;
        font-weight: bold;
        pointer-events: none; 
    }}
    </style>

    <div class="ruleta-container">
      <div class="arrow"></div>
      <div class="ruleta-wheel">
        {slices_joined}
      </div>
    </div>
    """
    return html_code

def canjear_por_whatsapp(label):
    """
    Link a WhatsApp para canjear el premio con Joni.
    """
    telefono_joni = "5491144042904"
    mensaje = f"Hola Joni, gané un {label} en la Ruleta y quiero canjear mi premio."
    msg_encoded = urllib.parse.quote(mensaje)
    wsp_url = f"https://api.whatsapp.com/send?phone={telefono_joni}&text={msg_encoded}"
    st.markdown(f"[Canjear ahora por WhatsApp]({wsp_url})", unsafe_allow_html=True)

def modulo_ruleta():
    st.title("Ruleta Clip-Path (Color Único)")
    st.write("Giramos 5 vueltas por tirada, sin distinguir sectores por color.")

    # Angulo acumulado y resultado
    if "ruleta_angle" not in st.session_state:
        st.session_state.ruleta_angle = 0
    if "ruleta_result" not in st.session_state:
        st.session_state.ruleta_result = None

    # Estilo del botón
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
    </style>
    """, unsafe_allow_html=True)

    # Botón para girar
    if st.button("¡Tirar la Ruleta!"):
        # Elegimos uno de los 8 sectores
        chosen_index = random.randint(0, 7)
        # 5 vueltas = 5*360=1800°, + (sector)*45°, + offset
        offset = random.randint(0, 44)
        final_angle = st.session_state.ruleta_angle + 1800 + (chosen_index * 45) + offset

        st.session_state.ruleta_angle = final_angle
        # Guardamos el label (ej: "Sin premio", "5% Descuento", etc.)
        st.session_state.ruleta_result = WHEEL_SECTORS[chosen_index]["label"]

        with st.spinner("Girando la ruleta..."):
            time.sleep(4)  # para coincidir con la transition (4s)

    # Mostramos la ruleta con su ángulo actual
    ruleta_html = generar_ruleta_html(st.session_state.ruleta_angle)
    components.html(ruleta_html, height=450, scrolling=False)

    # Si ya tenemos un resultado
    if st.session_state.ruleta_result:
        if "Sin premio" in st.session_state.ruleta_result:
            st.warning("¡No ganaste nada! Seguimos intentando.")
        else:
            st.balloons()
            st.success(f"¡Felicidades! Te tocó: {st.session_state.ruleta_result}")
            canjear_por_whatsapp(st.session_state.ruleta_result)

if __name__ == "__main__":
    st.set_page_config(page_title="Ruleta Clip-Path", layout="centered")
    modulo_ruleta()
