import streamlit as st
import streamlit.components.v1 as components
import time
import random
import urllib.parse

WHEEL_SECTORS = [
    {"label": "5% Descuento",       "color": "#FF5733"},
    {"label": "7% Descuento",       "color": "#FFC300"},
    {"label": "12% Descuento",      "color": "#DAF7A6"},
    {"label": "Ganaste un Peluche", "color": "#28B463"},
    {"label": "Ganaste un Juguete", "color": "#3498DB"},
    {"label": "Sin premio",         "color": "#9B59B6"},
    {"label": "Sin premio",         "color": "#C70039"},
    {"label": "Sin premio",         "color": "#F39C12"},
]

def generar_ruleta_html(angle):
    """
    Genera el bloque HTML/CSS de la ruleta, con 'clip-path' para
    que cada slice sea una cuña y no un cuadrado.
    angle: grados totales de rotación de la rueda.
    """
    slices_html = []
    for i, sec in enumerate(WHEEL_SECTORS):
        deg_start = i * 45
        # Cada "slice" abarca un wedge de 45°
        slice_html = f"""
        <div class="slice slice-{i}" 
             style="background-color:{sec['color']};
                    transform: rotate({deg_start}deg);">
            <div class="slice-text">{sec['label']}</div>
        </div>
        """
        slices_html.append(slice_html)

    slices_joined = "\n".join(slices_html)

    # CSS con clip-path para que cada rectángulo sea una cuña
    html_code = f"""
    <style>
    .ruleta-container {{
        width: 350px;
        height: 350px;
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
        top: -40px;
        left: calc(50% - 20px);
        z-index: 999;
    }}
    .ruleta-wheel {{
        width: 100%;
        height: 100%;
        border-radius: 50%;
        border: 6px solid #333;
        position: relative;
        /* rotamos la rueda */
        transform: rotate({angle}deg);
        transition: all 3s cubic-bezier(0.25, 0.1, 0.25, 1);
        overflow: hidden;
    }}
    /* Cada porción (slice) es 100% de la rueda, 
       y se recorta con clip-path en forma de cuña de 45°. */
    .slice {{
        width: 100%;
        height: 100%;
        position: absolute;
        top: 0;
        left: 0;
        /* Para que sea una "rebanada" de 45° del círculo */
        clip-path: polygon(50% 50%, 100% 0%, 100% 100%);
        /* Ubicada según su rotación (rotate(N*45deg)) */
        transform-origin: 50% 50%;
    }}
    .slice-text {{
        /* giramos en contra para que el texto quede horizontal */
        transform: rotate(-22.5deg);
        transform-origin: center center;
        position: absolute;
        top: 20%;
        left: 50%;
        width: 80px;
        margin-left: -40px; 
        text-align: center;
        font-size: 0.8rem;
        color: #fff;
        font-weight: bold;
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

def lanzar_emojis_tristes():
    for _ in range(5):
        st.markdown("😢😢😢", unsafe_allow_html=True)

def canjear_por_whatsapp(label):
    telefono_joni = "5491144042904"
    mensaje = f"Hola Joni, gané un {label} en la Ruleta y quiero canjear mi premio."
    msg_enc = urllib.parse.quote(mensaje)
    wsp_url = f"https://api.whatsapp.com/send?phone={telefono_joni}&text={msg_enc}"
    st.markdown(f"[Canjear ahora por WhatsApp]({wsp_url})", unsafe_allow_html=True)

def modulo_ruleta():
    st.title("🎡 Ruleta Animada (con clip-path)")
    st.write("¡Probá tu suerte con una ruleta más realista (cuñas en vez de cuadrados)!")

    if "ruleta_angle" not in st.session_state:
        st.session_state.ruleta_angle = 0
    if "ruleta_result" not in st.session_state:
        st.session_state.ruleta_result = None

    # Estilo botón
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

    if st.button("¡Tirar la Ruleta!"):
        chosen_index = random.randint(0, 7)
        offset = random.randint(0, 44)
        final_angle = 1080 + (chosen_index * 45) + offset

        st.session_state.ruleta_angle = final_angle
        st.session_state.ruleta_result = WHEEL_SECTORS[chosen_index]["label"]

        with st.spinner("Girando la ruleta..."):
            time.sleep(3)

    # Generamos HTML y lo embebemos como componente
    ruleta_html = generar_ruleta_html(st.session_state.ruleta_angle)
    st.components.v1.html(ruleta_html, height=400, scrolling=False)

    # Resultado
    if st.session_state.ruleta_result:
        res = st.session_state.ruleta_result
        if "Sin premio" in res:
            lanzar_emojis_tristes()
            st.error("¡No hubo suerte esta vez!")
        else:
            st.balloons()
            st.success(f"¡Felicidades! Te tocó: {res}")
            canjear_por_whatsapp(res)

if __name__ == "__main__":
    st.set_page_config(page_title="Ruleta con Clip-Path", layout="centered")
    modulo_ruleta()
