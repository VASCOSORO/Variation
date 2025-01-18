import streamlit as st
import streamlit.components.v1 as components
import time
import random
import urllib.parse

# Ajustá acá los nombres exactos de tus PNG
WHEEL_SECTORS = [
    {
        "label": "5% Descuento",
        "color": "#47a8bd",
        "icon": "./vasco.png"
    },
    {
        "label": "7% Descuento",
        "color": "#47a8bd",
        "icon": "./vasco (1).png"
    },
    {
        "label": "Ganaste un Peluche",
        "color": "#47a8bd",
        "icon": "./vasco (2).png"
    },
    {
        "label": "Sin premio",
        "color": "#47a8bd",
        "icon": "./vasco (3).png"
    },
    {
        "label": "Ganaste un Juguete",
        "color": "#47a8bd",
        "icon": "./vasco (4).png"
    },
    {
        "label": "Sin premio",
        "color": "#47a8bd",
        "icon": "./vasco (3).png"
    },
    {
        "label": "12% Descuento",
        "color": "#47a8bd",
        "icon": "./vasco (1).png"
    },
    {
        "label": "Sin premio",
        "color": "#47a8bd",
        "icon": "./vasco (3).png"
    },
]

def generar_ruleta_html(angle):
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

    st.write("¡Dale clic al botón para ver si ganás un juguete, un descuento o nada!")

    # Ángulo acumulado
    if "ruleta_angle" not in st.session_state:
        st.session_state.ruleta_angle = 0
    if "ruleta_result" not in st.session_state:
        st.session_state.ruleta_result = None

    # Botón
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
    .msg-ruleta {
        text-align: center;
        font-size: 1.3rem;
        color: #ff006e;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

    clicked = st.button("¡Tirar la Ruleta!")
    if clicked:
        # Mostramos un mensaje grande en la app
        st.markdown("<div class='msg-ruleta'>Girando la Ruleta...</div>", unsafe_allow_html=True)
        # Elegimos sector
        chosen_index = random.randint(0, 7)
        offset = random.randint(0, 44)
        final_angle = st.session_state.ruleta_angle + 1800 + (chosen_index * 45) + offset
        st.session_state.ruleta_angle = final_angle
        st.session_state.ruleta_result = WHEEL_SECTORS[chosen_index]["label"]
        time.sleep(4)  # coincidimos con la transición

    ruleta_html = generar_ruleta_html(st.session_state.ruleta_angle)
    components.html(ruleta_html, height=450, scrolling=False)

    # Resultado
    if st.session_state.ruleta_result:
        res = st.session_state.ruleta_result
        if "Sin premio" in res:
            st.warning("¡No ganaste nada! Dale otra vez.")
        else:
            st.balloons()
            st.success(f"¡Felicidades! Te tocó: {res}")
            canjear_por_whatsapp(res)

if __name__ == "__main__":
    st.set_page_config(page_title="Ruleta con PNG locales", layout="centered")
    modulo_ruleta()
