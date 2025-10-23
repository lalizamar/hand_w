import streamlit as st
import random
import pandas as pd
import time
from datetime import datetime
# Se añade el import para el Canvas de dibujo (puede causar error si no está disponible)
from streamlit_drawable_canvas import st_canvas 

# --- 1. Mapeo Creativo de Mensajes Estelares ---
# Mensajes que se usarán en la predicción
COSMIC_MESSAGES = {
    "0": "¡Cero es la órbita perfecta! Un anillo de asteroides sin fallas.",
    "1": "¡Uno es un cometa solitario! Un rastro de luz simple y fuerte.",
    "2": "¡Dos son planetas gemelos! La dualidad está clasificada correctamente.",
    "3": "¡Tres son estrellas en triángulo! La trinidad cósmica está clara.",
    "4": "¡Cuatro son las lunas de Júpiter! La formación es precisa.",
    "5": "¡Cinco son los dedos de tu mano! El escaneo manual fue un éxito.",
    "6": "¡Seis es el hexágono de Saturno! Una forma compleja bien resuelta.",
    "7": "¡Siete son las Pléyades! Un cúmulo de estrellas brillante y nítido.",
    "8": "¡Ocho es el símbolo de infinito! Un bucle de energía clasificado.",
    "9": "¡Nueve son las galaxias principales! El patrón del universo está completo."
}

# --- 2. Inyección de CSS para la Estética "Cosmic Cute" ---
def inject_cosmic_cute_css():
    st.markdown(f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Sniglet&family=Space+Mono:wght@400;700&display=swap');
            
            /* Colores Base: Pastel Space */
            :root {{
                --color-primary: #FFB3C1; /* Soft Pink Nebula */
                --color-secondary: #A7C7E7; /* Light Blue Sky */
                --color-background: #F5F7FA; /* Star White */
                --color-text: #483D8B; /* Dark Purple Comet */
                --color-accent: #FFD700; /* Gold Star */
            }}

            /* Fondo de la Aplicación */
            .stApp {{
                background: linear-gradient(135deg, var(--color-background) 0%, var(--color-secondary) 100%);
                color: var(--color-text);
                font-family: 'Sniglet', cursive; /* Fuente Cute */
            }}

            /* Títulos */
            h1, h2, h3, h4 {{
                font-family: 'Space Mono', monospace; /* Fuente Tech Space */
                color: var(--color-text);
                text-shadow: 2px 2px var(--color-primary);
                text-align: center;
                margin-top: 0.5em;
            }}
            
            /* Botón de Predicción (Estilo Asteroide) */
            .stButton > button {{
                background-color: var(--color-accent);
                color: var(--color-text);
                border: 3px solid var(--color-primary);
                border-radius: 20px;
                padding: 10px 20px;
                box-shadow: 4px 4px 0px var(--color-text);
                transition: all 0.2s;
                font-family: 'Space Mono', monospace;
            }}
            .stButton > button:hover {{
                background-color: var(--color-primary);
                box-shadow: 2px 2px 0px var(--color-accent);
                transform: translateY(2px);
            }}

            /* ** CSS ELIMINADO: Se quitó el estilo gigante del st.text_input. ** */
            
            /* Dataframe y Cajas de Información */
            .stDataFrame, .stAlert, .stInfo, .stWarning, .stSuccess {{
                border-radius: 10px;
                border: 2px solid var(--color-text);
                background-color: #FFFFFF;
                box-shadow: 3px 3px 0px var(--color-primary);
                color: var(--color-text);
                padding: 10px;
            }}
            
            /* Barra lateral */
            .css-1d3s3aw, .st-emotion-cache-1d3s3aw {{ /* Target the sidebar */
                background-color: var(--color-secondary);
                border-right: 2px solid var(--color-primary);
            }}
            
            /* Estilo para el Canvas de Dibujo */
            .main .block-container .st-emotion-cache-1ft911z, 
            .main .block-container .st-emotion-cache-1cpxdwv {{
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;
            }}

        </style>
    """, unsafe_allow_html=True)

# --- 3. Configuración de página Streamlit y CSS ---
st.set_page_config(
    page_title='El Crayon Cósmico',
    page_icon='⭐',
    layout='wide'
)

inject_cosmic_cute_css()

# --- 4. Función de SIMULACIÓN (Reemplaza a Keras/TensorFlow) ---
def simulate_digit_recognition(drawing_data):
    """
    Simula la predicción de dígitos.
    Si hay trazos (se ha dibujado), asigna un dígito aleatorio con alta confianza.
    Si no hay trazos, retorna None.
    """
    if drawing_data is None or drawing_data.shape[2] == 0:
        return None, None
        
    # Contar la cantidad de pixeles no transparentes como un indicador de que "algo" fue dibujado
    # El canal alpha (índice 3) indica la transparencia. Si es mayor a 0, hay trazo.
    non_transparent_pixels = (drawing_data[:, :, 3] > 0).sum()
    
    if non_transparent_pixels < 50: # Umbral muy bajo para confirmar el dibujo
        return None, None

    # SIMULACIÓN: Asignar un dígito aleatorio
    predicted_digit = random.randint(0, 9)
    predicted_digit_str = str(predicted_digit)
    
    # Generar probabilidades (simuladas)
    probabilities = [0.0] * 10 # 10 clases (0-9)
    probabilities[predicted_digit] = round(random.uniform(0.9, 0.99), 4) # Alta confianza en el "detectado"
    
    remaining_prob = 1.0 - probabilities[predicted_digit]
    if remaining_prob > 0:
        small_prob = remaining_prob / 9
        for i in range(10):
            if i != predicted_digit:
                probabilities[i] = round(small_prob * random.uniform(0.5, 1.5), 4)
    
    total = sum(probabilities)
    probabilities = [p / total for p in probabilities]
    
    return predicted_digit_str, probabilities


# --- 5. Lógica de UI Principal ---
st.title("⭐ EL CRAYON CÓSMICO: ORGANIZADOR ESTELAR DE NÚMEROS")

st.markdown(f"""
<div style='text-align: center; background-color: var(--color-primary); padding: 15px; border-radius: 10px; border: 2px solid var(--color-text); margin-bottom: 30px;'>
    <h3 style='font-family: "Sniglet", cursive; text-shadow: none; color: var(--color-text);'>
        ¡Bienvenido, pequeño explorador! 🚀
    </h3>
    <p style='font-family: "Sniglet", cursive; color: var(--color-text); margin-bottom: 0;'>
        Usa el ratón o tu dedo para **dibujar un dígito (0-9)** en el Bloc de Polvo Estelar. 
        Luego, presiona 'Clasificar Constelación' para que nuestro Ordenador Estelar lo analice.
    </p>
</div>
""", unsafe_allow_html=True)

# Contenedor para el "Canvas"
col_canvas, col_spacer = st.columns([1, 1])

with col_canvas:
    st.subheader("🌌 Bloc de Polvo Estelar (Dibuja aquí)")
    
    # Componente Canvas de Dibujo (Restaurado del código original)
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.0)",  # Color de relleno de fondo, transparente
        stroke_width=20, # Ancho de línea grueso para mejor visibilidad del dibujo
        stroke_color="#FFD700", # Color del trazo: Dorado Estelar
        background_color="#483D8B", # Fondo del bloc: Púrpura Cometa
        height=250,
        width=250,
        drawing_mode="freedraw",
        key="canvas",
    )
    
# Botón de Predicción
if st.button('Clasificar Constelación'):
    # Verificar si el canvas tiene datos de imagen (es decir, se ha dibujado)
    if canvas_result.image_data is not None:
        
        # El canvas retorna un array NumPy RGBA
        input_numpy_array = canvas_result.image_data 
        
        # Simular la predicción usando los datos del array
        predicted_digit_str, probabilities = simulate_digit_recognition(input_numpy_array)
        
        if predicted_digit_str is not None:
            # Mostrar animación de clasificación
            with st.spinner(f"Analizando la forma del trazo estelar..."):
                time.sleep(2) 
            
            # Mostrar resultados
            
            col_res1, col_res2 = st.columns(2)
            
            with col_res1:
                st.subheader("✅ Clasificación Exitosa")
                
                # Mensaje del Oráculo Estelar
                message = COSMIC_MESSAGES.get(predicted_digit_str, "El espacio es inmenso. Intenta un dígito del 0 al 9.")
                
                st.markdown(f"""
                    <div style='background-color: var(--color-secondary); padding: 15px; border-radius: 10px; border: 2px solid var(--color-text); color: var(--color-text); font-family: "Sniglet", cursive;'>
                        <h4 style='font-family: "Space Mono", monospace; text-shadow: none; color: var(--color-text); margin-top: 0;'>
                            [Organizador Estelar]: Digito {predicted_digit_str} detectado.
                        </h4>
                        <p>{message}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                # Mostrar el resultado del header para cumplir con el código original
                st.header(f'El Dígito es : {predicted_digit_str} (Confianza: {probabilities[int(predicted_digit_str)] * 100:.2f}%)')


            with col_res2:
                st.subheader("📈 Matriz de Confianza (Simulada)")
                
                # Crear DataFrame para mostrar la matriz de probabilidad
                prob_data = [{"Dígito": i, "Probabilidad (%)": f"{probabilities[i] * 100:.2f}"} for i in range(10)]
                df_prob = pd.DataFrame(prob_data)
                
                # Ordenar por Probabilidad descendente
                df_prob['Probabilidad (%)'] = df_prob['Probabilidad (%)'].str.replace('%', '').astype(float)
                df_prob = df_prob.sort_values(by='Probabilidad (%)', ascending=False)
                df_prob['Probabilidad (%)'] = df_prob['Probabilidad (%)'].apply(lambda x: f"{x:.2f}%")

                st.dataframe(df_prob.set_index('Dígito'), use_container_width=True, height=350)
        
        else:
            st.error('⚠️ ¡Alerta Estelar! Por favor, dibuja un dígito en el Bloc de Polvo Estelar antes de clasificar.')
            
    else:
        st.warning('⚠️ Por favor, dibuja un único dígito (0-9) en el bloc para simular la detección.')


# --- Barra lateral (Sidebar) ---
st.sidebar.title("🪐 Bitácora de Vuelo (Acerca de)")
st.sidebar.markdown("""
<div style='font-family: "Sniglet", cursive; color: var(--color-text);'>
    <p>Esta aplicación simula la clasificación de constelaciones (dígitos escritos a mano).</p>
    <p>La **Interacción Multimodal** se ilustra mediante la entrada de escritura (dibujar con el ratón/dedo).</p>
    <p>El sistema simula un modelo de Red Neuronal Convolucional (CNN) entrenado con datos MNIST (dígitos).</p>
    <br>
    <p>Hecho con amor cósmico.</p>
</div>
""", unsafe_allow_html=True)


# Información adicional y pie de página
st.markdown("---")
st.caption("""
**Acerca de la aplicación (El Crayon Cósmico)**: 
Esta interfaz es un trabajo de Interfaces Multimodales. Utiliza Streamlit y el componente de dibujo para la entrada de datos, y presenta una **simulación creativa del reconocimiento de dígitos** para ilustrar el concepto de Visión Artificial.
""")
