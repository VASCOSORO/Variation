import streamlit as st
import streamlit.components.v1 as components
import time
import random
import urllib.parse

# Ocho sectores, todos con color "#47a8bd" y las imágenes renombradas
WHEEL_SECTORS = [
    {
        "label": "5% Descuento",
        "color": "#47a8bd",
        "icon": "vasco_0.png"  # correspondía a "vasco.png"
    },
    {
        "label": "7% Descuento",
        "color": "#47a8bd",
        "icon": "vasco_1.png"  # correspondía a "vasco (1).png"
    },
    {
        "label": "Ganaste un Peluche",
        "color": "#47a8bd",
        "icon": "vasco_2.png"  # correspondía a "vasco (2).png"
    },
    {
        "label": "Sin premio",
        "color": "#47a8bd",
        "icon": "vasco_3.png"  # correspondía a "vasco (3).png" (fantasma)
    },
    {
        "label": "Ganaste un Juguete",
        "color": "#47a8bd",
        "icon": "vasco_4.png"  # correspondía a "vasco (4).png"
    },
    {
        "label": "Sin premio",
        "color": "#47a8bd",
        "icon": "vasco_3.png"  # fantasma
    },
    {
        "label": "12% Descuento",
        "color": "#47a8bd",
        "icon": "vasco_1.png"
    },
    {
        "label": "Sin premio",
        "color": "#47a8bd",
        "icon": "vasco_3.png"
    },
]

def generar_ruleta_html(angle):
    """
    Genera el HTML/CSS de la ruleta con clip-path y tus 5 imágenes renombradas.
    'angle' = rotación acumulada en grados.
    """
    slices_html = []
    for i, sec in enumerate(WHEEL_SECTORS):
        deg_start = i * 45
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
        /* "rebanada" de 45° con clip-path */
        clip-path: polygon(50% 50%, 100% 0%, 100% 100%);
        transform-origin: 50% 50%;
    }}
    .slice-content {{
        position: absolute;
        top: 0;
        left: 50%;
        transform: rotate(-22.5deg);
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
    telefono_joni = "5491144042904"
    mensaje = f"Hola Joni, gané un {label} en la Ruleta y quiero canjear mi premio."
    msg_encoded = urllib.parse.quote(mensaje)
    wsp_url = f"https://api.whatsapp.com/send?phone={telefono_joni}&text={msg_encoded}"
    st.markdown(f"[Canjear ahora por WhatsApp]({wsp_url})", unsafe_allow_html=True)

def modulo_ruleta():
    st.title("Girá la Ruleta y Participá de Lindos Premios")
    st.write("¡Hacé clic, mirá el giro, y descubrí si ganaste!")

    # Ángulo acumulado
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
        # 5 vueltas (1800°) + sector * 45° + offset
        offset = random.randint(0, 44)
        final_angle = st.session_state.ruleta_angle + 1800 + (chosen_index * 45) + offset

        st.session_state.ruleta_angle = final_angle
        st.session_state.ruleta_result = WHEEL_SECTORS[chosen_index]["label"]

        with st.spinner("Girando la Ruleta..."):
            time.sleep(4)  # coincide con la transición

    # Generamos el HTML
    ruleta_html = generar_ruleta_html(st.session_state.ruleta_angle)
    components.html(ruleta_html, height=450, scrolling=False)

    # Resultado
    if st.session_state.ruleta_result:
        res = st.session_state.ruleta_result
        if "Sin premio" in res:
            st.warning("¡No ganaste nada! Probá de nuevo.")
        else:
            st.balloons()
            st.success(f"¡Felicidades! Te tocó: {res}")
            canjear_por_whatsapp(res)

if __name__ == "__main__":
    st.set_page_config(page_title="Ruleta con vasco_*.png", layout="centered")
    modulo_ruleta()
