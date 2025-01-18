import streamlit as st
import streamlit.components.v1 as components
import time
import random
import urllib.parse

# Ocho sectores de la rueda. Todos color "#00cfcf" para que no se note
# cuál es "Sin premio" ni su probabilidad.
WHEEL_SECTORS = [
    {"label": "5% Descuento",       "color": "#00cfcf"},
    {"label": "7% Descuento",       "color": "#00cfcf"},
    {"label": "12% Descuento",      "color": "#00cfcf"},
    {"label": "Ganaste un Peluche", "color": "#00cfcf"},
    {"label": "Ganaste un Juguete", "color": "#00cfcf"},
    {"label": "Sin premio",         "color": "#00cfcf"},
    {"label": "Sin premio",         "color": "#00cfcf"},
    {"label": "Sin premio",         "color": "#00cfcf"},
]

def generar_ruleta_html(angle):
    """
    Genera el HTML/CSS de la ruleta con una sola tonalidad (clip-path para cuñas).
    angle = grados totales de rotación acumulados.
    """
    slices_html = []
    for i, sec in enumerate(WHEEL_SECTORS):
        deg_start = i * 45  # cada porción 45°
        slice_html = f"""
        <div class="slice slice-{i}" 
             style="background-color:{sec['color']}; transform: rotate({deg_start}deg);">
            <div class="slice-text">{sec['label']}</div>
        </div>
        """
        slices_html.append(slice_html)

    slices_joined = "\n".join(slices_html)

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
        top: -50px; /* un poquito más arriba */
        left: calc(50% - 20px);
        z-index: 999;
    }}
    .ruleta-wheel {{
        width: 100%;
        height: 100%;
        border-radius: 50%;
        border: 8px solid #333;
        position: relative;
        /* 4s de transición para que se vea girar */
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
        clip-path: polygon(50% 50%, 100% 0%, 100% 100%);
        transform-origin: 50% 50%;
    }}
    .slice-text {{
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
    Muestra link a WhatsApp para canjear el premio con Joni.
    """
    telefono_joni = "5491144042904"
    mensaje = f"Hola Joni, gané un {label} en la Ruleta y quiero canjear mi premio."
    msg_enc = urllib.parse.quote(mensaje)
    wsp_url = f"https://api.whatsapp.com/send?phone={telefono_joni}&text={msg_enc}"
    st.markdown(f"[Canjear ahora por WhatsApp]({wsp_url})", unsafe_allow_html=True)

def modulo_ruleta():
    st.title("Ruleta Estilo Casino")
    st.write("¡7 vueltas por tirada, color único, no sabés si ganás hasta que se detenga!")

    # Guardamos el ángulo en session_state y el último resultado
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

    # BOTÓN TIRAR
    if st.button("¡Tirar la Ruleta!"):
        chosen_index = random.randint(0, 7)
        # 7 vueltas = 7 * 360° = 2520
        offset = random.randint(0, 44)  # para no caer siempre igual
        # Sumamos al ángulo actual, así gira desde donde quedó
        final_angle = st.session_state.ruleta_angle + 2520 + (chosen_index * 45) + offset

        st.session_state.ruleta_angle = final_angle
        st.session_state.ruleta_result = WHEEL_SECTORS[chosen_index]["label"]

        with st.spinner("Girando la ruleta..."):
            time.sleep(4)  # coincide con la transition: 4s

    # Mostramos la ruleta con su ángulo actual
    ruleta_html = generar_ruleta_html(st.session_state.ruleta_angle)
    components.html(ruleta_html, height=450, scrolling=False)

    # Mostramos el resultado si existe
    if st.session_state.ruleta_result:
        res = st.session_state.ruleta_result
        if "Sin premio" in res:
            st.warning("¡No ganaste nada, probá de nuevo!")
        else:
            st.balloons()
            st.success(f"¡Felicidades! Te tocó: {res}")
            canjear_por_whatsapp(res)

if __name__ == "__main__":
    st.set_page_config(page_title="Ruleta Estilo Casino", layout="centered")
    modulo_ruleta()
