import streamlit as st
import random
import time
import urllib.parse

# 8 sectores de la ruleta: label + color
WHEEL_SECTORS = [
    {"label": "5% Descuento", "color": "#FF5733"},
    {"label": "7% Descuento", "color": "#FFC300"},
    {"label": "12% Descuento", "color": "#DAF7A6"},
    {"label": "Ganaste un Peluche", "color": "#28B463"},
    {"label": "Ganaste un Juguete", "color": "#3498DB"},
    {"label": "Sin premio", "color": "#9B59B6"},
    {"label": "Sin premio", "color": "#C70039"},
    {"label": "Sin premio", "color": "#F39C12"},
]

def modulo_ruleta():
    st.title("🎡 Ruleta Piola con Descuentos y Premios")
    st.write("¡Tirá la ruleta y divertite con premios reales (o no... 😅)!")

    # Si no existe en session_state, inicializamos
    if "random_angle" not in st.session_state:
        st.session_state.random_angle = 0
    if "selected_label" not in st.session_state:
        st.session_state.selected_label = None

    # Botón de estilo piola
    st.markdown(
        """
        <style>
        div.stButton > button {
            color: #fff;
            background-color: #ff006e;
            font-size: 1.2rem;
            border-radius: 10px;
            border: 2px solid #c70055;
            padding: 0.6rem 1.5rem;
            margin-bottom: 1rem;
        }
        div.stButton > button:hover {
            background-color: #c70055;
            color: #eee;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # BOTÓN TIRAR
    if st.button("¡Tirar la Ruleta!"):
        # Elegimos un sector aleatorio (0..7)
        chosen_index = random.randint(0, 7)
        # Cada sector son 45°, hacemos un par de vueltas (3 giros = 1080°)
        # Sumamos un pequeño offset random (0..44°) para no caer siempre centrado
        offset = random.randint(0, 44)
        final_angle = 1080 + chosen_index * 45 + offset

        st.session_state.random_angle = final_angle
        st.session_state.selected_label = WHEEL_SECTORS[chosen_index]["label"]

        # Simulamos un pequeño "tiempo de giro"
        with st.spinner("Girando la ruleta..."):
            time.sleep(3)  # 3 seg

    # Mostrar la ruleta con HTML + CSS
    wheel_html = generar_ruleta_html(
        sectors=WHEEL_SECTORS,
        angle=st.session_state.random_angle
    )
    st.markdown(wheel_html, unsafe_allow_html=True)

    # Mostrar resultado, si ya tiró
    if st.session_state.selected_label:
        if "Sin premio" in st.session_state.selected_label:
            # "Tiramos" emojis tristes
            lanzar_emojis_tristes()
            st.error("¡No hubo suerte esta vez! 😢 Seguí intentando...")
        else:
            # Alegría
            st.balloons()
            st.success(f"¡Felicitaciones! Obtuviste: {st.session_state.selected_label}")
            # Link de canje por WhatsApp
            canjear_por_whatsapp(st.session_state.selected_label)

def generar_ruleta_html(sectors, angle):
    """
    Genera el HTML + CSS para mostrar una ruleta con 'sectors' (lista de dicts con 'label' y 'color')
    rotada 'angle' grados.
    """
    # Creamos el HTML de los slices
    # Cada slice se posiciona con rotate(i * 45deg)
    slices_html = []
    for i, sec in enumerate(sectors):
        deg_start = i * 45  # cada sector abarca 45 grados
        # Texto al medio del slice => usaremos transform: rotate(-22.5deg) para centrar el texto.
        slice_block = f"""
        <div class="slice slice-{i}" style="background-color:{sec['color']}; transform: rotate({deg_start}deg);">
            <div class="slice-text">{sec['label']}</div>
        </div>
        """
        slices_html.append(slice_block)

    slices_joined = "\n".join(slices_html)

    # Insertamos todo en la plantilla
    html_ruleta = f"""
    <style>
    .ruleta-container {{
        width: 350px;
        height: 350px;
        margin: 0 auto;
        position: relative;
    }}
    .ruleta-wheel {{
        width: 100%;
        height: 100%;
        border-radius: 50%;
        border: 6px solid #333;
        position: relative;
        transition: all 3s cubic-bezier(0.25, 0.1, 0.25, 1);
        transform: rotate({angle}deg);
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
    .arrow {{
        width: 0; 
        height: 0; 
        border-left: 20px solid transparent;
        border-right: 20px solid transparent;
        border-bottom: 30px solid #ff006e;
        position: absolute;
        top: -40px;
        left: calc(50% - 20px);
        z-index: 10;
    }}
    </style>
    <div class="ruleta-container">
        <div class="arrow"></div>
        <div class="ruleta-wheel">
            {slices_joined}
        </div>
    </div>
    """
    return html_ruleta

def lanzar_emojis_tristes():
    """
    Muestra varios emojis tristes con un trick de `st.markdown` repetido.
    """
    # Podés cambiar la cantidad o el emoji que quieras
    for _ in range(8):
        st.markdown("😢😢😢", unsafe_allow_html=True)

def canjear_por_whatsapp(label):
    """
    Muestra link para abrir WhatsApp Web con mensaje de canje hacia Joni.
    """
    telefono_joni = "5491144042904"  # sin espacios ni '+'
    mensaje = f"Hola Joni, gané un {label} en la Ruleta y quiero canjear mi premio."
    mensaje_encode = urllib.parse.quote(mensaje)
    whatsapp_url = f"https://api.whatsapp.com/send?phone={telefono_joni}&text={mensaje_encode}"

    st.markdown(
        f"**[Canjear ahora por WhatsApp]({whatsapp_url})**",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    st.set_page_config(page_title="Ruleta Piola", layout="centered")
    modulo_ruleta()
