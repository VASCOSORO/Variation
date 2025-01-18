import streamlit as st
import streamlit.components.v1 as components  # <-- Importamos
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
    slices_html = []
    for i, sec in enumerate(WHEEL_SECTORS):
        deg_start = i * 45
        slice_html = f"""
        <div class="slice slice-{i}" style="background-color:{sec['color']}; transform: rotate({deg_start}deg);">
            <div class="slice-text">{sec['label']}</div>
        </div>
        """
        slices_html.append(slice_html)

    slices_joined = "\n".join(slices_html)
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
        transform: rotate({angle}deg);
        transition: all 3s cubic-bezier(0.25, 0.1, 0.25, 1);
    }}
    .slice {{
        width: 50%;
        height: 50%;
        position: absolute;
        top: 0;
        left: 50%;
        transform-origin: left center;
        border: 1px solid #fff;
        box-sizing: border-box;
    }}
    .slice-text {{
        transform: rotate(-22.5deg);
        transform-origin: center center;
        margin-top: 60px;
        margin-left: -40px;
        width: 80px;
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
    mensaje_encode = urllib.parse.quote(mensaje)
    whatsapp_url = f"https://api.whatsapp.com/send?phone={telefono_joni}&text={mensaje_encode}"
    st.markdown(f"[Canjear ahora por WhatsApp]({whatsapp_url})", unsafe_allow_html=True)

def modulo_ruleta():
    st.title("🎡 Ruleta Animada: Descuentos y Premios")
    st.write("¡Probá tu suerte con esta ruleta visual más realista!")

    if "ruleta_angle" not in st.session_state:
        st.session_state.ruleta_angle = 0
    if "ruleta_result" not in st.session_state:
        st.session_state.ruleta_result = None

    st.markdown(
        """
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
        """,
        unsafe_allow_html=True
    )

    if st.button("¡Tirar la Ruleta!"):
        chosen_index = random.randint(0, 7)
        offset = random.randint(0, 44)
        final_angle = 1080 + (chosen_index * 45) + offset

        st.session_state.ruleta_angle = final_angle
        st.session_state.ruleta_result = WHEEL_SECTORS[chosen_index]["label"]

        with st.spinner("Girando la ruleta..."):
            time.sleep(3)

    # Generamos el HTML final de la ruleta
    ruleta_html = generar_ruleta_html(st.session_state.ruleta_angle)
    # En vez de st.markdown, usamos st.components.v1.html:
    components.html(ruleta_html, height=400, scrolling=False)  # height ajustable

    if st.session_state.ruleta_result:
        resultado = st.session_state.ruleta_result
        if "Sin premio" in resultado:
            lanzar_emojis_tristes()
            st.error("¡No hubo suerte esta vez!")
        else:
            st.balloons()
            st.success(f"¡Felicidades! Te tocó: {resultado}")
            canjear_por_whatsapp(resultado)

if __name__ == "__main__":
    st.set_page_config(page_title="Ruleta Animada", layout="centered")
    modulo_ruleta()
