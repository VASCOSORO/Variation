import streamlit as st
import random
import time
import plotly.graph_objects as go
import urllib.parse

def modulo_ruleta():
    st.title("🎡 Ruleta de Premios y Descuentos")
    st.write("¡Girá la ruleta y divertite con descuentos y premios instantáneos!")

    # Elementos de la ruleta
    opciones = [
        "5% Descuento",
        "7% Descuento",
        "12% Descuento",
        "Ganaste un Peluche",
        "Ganaste un Juguete",
        "Sin premio",
        "Sin premio",
        "Sin premio"
    ]

    # Probabilidades (si todas en 1 => igual probabilidad)
    valores = [1, 1, 1, 1, 1, 1, 1, 1]

    # Colores
    colores = [
        "#FF5733",  # Naranja/rojo
        "#FFC300",  # Amarillo
        "#DAF7A6",  # Verde claro
        "#28B463",  # Verde más oscuro
        "#3498DB",  # Celeste
        "#9B59B6",  # Violeta
        "#C70039",  # Rojo oscuro
        "#F39C12",  # Naranja intenso
    ]

    # Graficamos la ruleta con Plotly
    fig = go.Figure(
        data=[go.Pie(
            labels=opciones, 
            values=valores, 
            textinfo='label',
            marker_colors=colores
        )]
    )
    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

    # Botón para girar la ruleta
    st.markdown(
        """
        <style>
        div.stButton > button {
            color: #FFF;
            background-color: #D81B60;
            font-size: 1.2rem;
            border-radius: 10px;
            border: 2px solid #9C0030;
            padding: 0.6rem 1.2rem;
            margin-bottom: 1rem;
        }
        div.stButton > button:hover {
            background-color: #9C0030;
            color: #EEE;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    boton_tirar = st.button("TIRAR!", help="¡Probar suerte!", key="boton_tirar")

    if boton_tirar:
        # Mostramos un spinner "Girando..."
        with st.spinner("Girando la ruleta..."):
            time.sleep(2.5)  # Pausa simulando "giro"

        # Obtenemos resultado aleatorio
        resultado = random.choices(opciones, weights=valores, k=1)[0]

        # Animación para hacerlo más vistoso:
        if resultado == "Sin premio":
            # Si no hay premio, nieve en pantalla
            st.snow()
            st.warning("¡No hubo suerte esta vez... probá de nuevo!")
        else:
            # Si hay premio o descuento, globos
            st.balloons()
            st.success(f"¡Felicitaciones! Obtuviste: **{resultado}**")

            # Armamos link de WhatsApp con mensaje prellenado
            telefono_joni = "5491144042904"  # sin guiones, ni +, ni espacios
            mensaje = f"Hola Joni, gané un {resultado} en la Ruleta y quiero canjear mi premio."
            mensaje_encode = urllib.parse.quote(mensaje)
            whatsapp_url = f"https://api.whatsapp.com/send?phone={telefono_joni}&text={mensaje_encode}"

            # Botón / link para canjear por WhatsApp Web
            st.markdown(
                f"[Canjear ahora por WhatsApp]({whatsapp_url})",
                unsafe_allow_html=True
            )

if __name__ == "__main__":
    # Configuramos la página de Streamlit
    st.set_page_config(page_title="Ruleta de Premios", layout="centered")
    modulo_ruleta()
