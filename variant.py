import streamlit as st
import streamlit.components.v1 as components
import time
import random
import urllib.parse

# Ocho sectores de la rueda
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
    Genera el HTML/CSS de la ruleta usando clip-path para cuñas,
    y un 'angle' de rotación que define el giro final.
    """
    slices_html = []
    for i, sec in enumerate(WHEEL_SECTORS):
        deg_start = i * 45
        # Cada cuña abarca 45° del círculo
        slice_html = f"""
        <div class="slice slice-{i}" 
             style="background-color:{sec['color']}; transform: rotate({deg_start}deg);">
            <div class="slice-text">{sec['label']}</div>
        </div>
        """
        slices_html.append(slice_html)

    slices_joined = "\n".join(slices_html)

    # CSS: clip-path para cada slice, texto alineado al borde
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
        /* Ajustá "4s" si querés el giro más o menos largo */
        transition: all 4s cubic-bezier(0.25, 0.1, 0.25, 1);
        transform: rotate({angle}deg);
        overflow: hidden;
    }}

    /* Clip-path para cuña de 45°,
       con su rotación propia. */
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
        /* Giramos en contra la mitad de 45°, o sea 22.5°, para que el texto 
           quede más o menos horizontal */
        transform: rotate(-22.5deg);
        transform-origin: center center;
        
        /* Ubicación */
        position: absolute;
        top: 0;
        left: 50%; 
        /* movemos un poco hacia afuera */
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

def lanzar_emojis_tristes():
    """Muestra emojis de tristeza en caso de perder."""
    for _ in range(5):
        st.markdown("😢😢😢", unsafe_allow_html=True)

def canjear_por_whatsapp(label):
    """Muestra link a WhatsApp para canjear premio con Joni."""
    telefono_joni = "5491144042904"
    mensaje = f"Hola Joni, gané un {label} en la Ruleta y quiero canjear mi premio."
    msg_enc = urllib.parse.quote(mensaje)
    wsp_url = f"https://api.whatsapp.com/send?phone={telefono_joni}&text={msg_enc}"
    st.markdown(f"[Canjear ahora por WhatsApp]({wsp_url})", unsafe_allow_html=True)

def modulo_ruleta():
    st.title("🎡 Ruleta con Clip-Path (5 vueltas)")
    st.write("¡Probá tu suerte con esta ruleta! Se ve el giro y los premios en los bordes.")

    # Guardamos en session_state el ángulo y resultado
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
        # Elegimos índice 0..7
        chosen_index = random.randint(0, 7)
        # 5 vueltas = 1800°, + chosen_index * 45°, + offset extra
        offset = random.randint(0, 44)
        final_angle = 1800 + (chosen_index * 45) + offset

        st.session_state.ruleta_angle = final_angle
        st.session_state.ruleta_result = WHEEL_SECTORS[chosen_index]["label"]

        with st.spinner("Girando la ruleta..."):
            time.sleep(4)  # coincide con 4s del CSS

    # Generamos HTML y lo embebemos como componente
    ruleta_html = generar_ruleta_html(st.session_state.ruleta_angle)
    components.html(ruleta_html, height=400, scrolling=False)

    # Mostrar resultado
    if st.session_state.ruleta_result:
        res = st.session_state.ruleta_result
        if "Sin premio" in res:
            lanzar_emojis_tristes()
            st.error("¡No hubo suerte esta vez!")
        else:
            st.balloons()
            st.success(f"¡Felicidades! Te tocó: {res}")
            canjear_por_whatsapp(res)

# Para correr directo
if __name__ == "__main__":
    st.set_page_config(page_title="Ruleta con Clip-Path", layout="centered")
    modulo_ruleta()
