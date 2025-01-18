import streamlit as st
import random
import plotly.graph_objects as go

def modulo_ruleta():
    st.title("🎡 Ruleta de Descuentos y Premios")

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

    # Porciones asociadas (podés ajustar para cambiar probabilidades)
    # Si querés que tengan igual probabilidad, usá todos 1.
    valores = [1, 1, 1, 1, 1, 1, 1, 1]

    # Colores de cada porción
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

    st.subheader("¡Girá la ruleta y probá tu suerte!")
    
    # Mostramos la ruleta (gráfico de torta de Plotly)
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

    # Botón Rojo "Tirar"
    boton_tirar = st.button("TIRAR!", help="¡Probar suerte!", 
                            key="boton_tirar", 
                            # Un poco de CSS para que se vea rojo:
                            on_click=None)

    if boton_tirar:
        # Elegimos un resultado random
        resultado = random.choices(opciones, weights=valores, k=1)[0]
        
        if resultado == "Sin premio":
            st.warning("¡No hubo suerte esta vez, seguí intentando!")
        else:
            st.success(f"¡Felicitaciones! Obtuviste: **{resultado}**")

# Si querés que se ejecute directamente al correr con streamlit:
if __name__ == "__main__":
    st.set_page_config(page_title="Ruleta de Premios", layout="centered")
    modulo_ruleta()
