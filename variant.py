import streamlit as st
import streamlit.components.v1 as components
import time
import random
import urllib.parse

# Ocho sectores; uso tus 5 imágenes repitiéndolas en algunos sectores.
# Ajustá los 'label' y la lógica "Sin premio" como quieras.
WHEEL_SECTORS = [
    {
        "label": "5% Descuento",
        "color": "#47a8bd",
        "icon": "vasco_0.png"  # la seta roja
    },
    {
        "label": "7% Descuento",
        "color": "#47a8bd",
        "icon": "vasco_1.png"  # la estrella
    },
    {
        "label": "Ganaste un Peluche",
        "color": "#47a8bd",
        "icon": "vasco_2.png"  # la seta con cara
    },
    {
        "label": "Sin premio",
        "color": "#47a8bd",
        "icon": "vasco_3.png"  # el fantasmita
    },
    {
        "label": "Ganaste un Juguete",
        "color": "#47a8bd",
        "icon": "vasco_4.png"  # la bolsita con diamante
    },
    {
        "label": "Sin premio",
        "color": "#47a8bd",
        "icon": "vasco_2.png"  # repetimos fantasma
    },
    {
        "label": "12% Descuento",
        "color": "#47a8bd",
        "icon": "vasco_0.png"  # repetimos estrella
    },
    {
        "label": "Sin premio",
        "color": "#47a8bd",
        "icon": "vasco_2.png"  # repetimos fantasma
    },
]

def generar_ruleta_html(angle):
    """
    Genera el HTML/CSS de la ruleta, usando clip-path, con un ícono local para cada sector.
    'angle' es la rotación acumulada en grados.
    """
    slices_html = []
    for i, sec in enumerate(WHEEL_SECTORS):
        deg_start = i * 45  # cada sector abarca 45°
        slice_html = f"""
        <div class="slice slice-{i}" 
             style="background-color:{sec['color']}; transform: rotate({deg_start}deg);">
            <div class="slice-content">
                <img src="{sec['icon']}" class="slice-icon" alt="{sec['label']}"/>
                <div class="slice-label">{sec['label']}</div>
            </div>
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
        border-left: 25px solid transparent;
        border-right: 25px solid transparent;
        border-bottom: 40px solid #ff006e;
        position: absolute;
        top: -55px; 
        left: calc(50% - 25px);
        z-index: 999;
    }}
    .ruleta-wheel {{
        width: 100%;
        height: 100%;
        border-radius: 50%;
        border: 6px solid #333;
        position: relative;
        /* 4s para notar el giro */
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
    /* Contenido de cada slice: el icono y su label */
    .slice-content {{
        position: absolute;
        top: 0;
        left: 50%;
        transform: rotate(-22.5deg); /* compensa la rotación de la slice */
        transform-origin: center center;
        width: 80px;
        margin-left: -40px;
        margin-top: 20px; 
        text-align: center;
    }}
    .slice-icon {{
        width: 40px;
        height: 40px;
        margin-bottom: 4px;
    }}
    .slice-label {{
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
    st.title("Ruleta Estilo Mario con tus Iconos Locales")
    st.write("Giramos 5 vueltas cada tirada. Las imágenes .png están subidas en tu repo.")

    # Ángulo acumulado (no se resetea) y resultado
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

    if st.button("¡Tirar la Ruleta!"):
        chosen_index = random.randint(0, 7)
        # 5 vueltas = 5*360=1800°, más el sector (chosen_index*45) y offset
        offset = random.randint(0, 44)
        final_angle = st.session_state.ruleta_angle + 1800 + (chosen_index * 45) + offset

        st.session_state.ruleta_angle = final_angle
        st.session_state.ruleta_result = WHEEL_SECTORS[chosen_index]["label"]

        with st.spinner("Girando la ruleta..."):
            time.sleep(4)

    # Mostrar la ruleta con su ángulo actual
    ruleta_html = generar_ruleta_html(st.session_state.ruleta_angle)
    components.html(ruleta_html, height=450, scrolling=False)

    # Mostrar resultado
    if st.session_state.ruleta_result:
        res = st.session_state.ruleta_result
        if "Sin premio" in res:
            st.warning("¡No ganaste nada! Dale otra vez.")
        else:
            st.balloons()
            st.success(f"¡Felicidades! Te tocó: {res}")
            canjear_por_whatsapp(res)

if __name__ == "__main__":
    st.set_page_config(page_title="Ruleta Mario con Iconos", layout="centered")
    modulo_ruleta()
