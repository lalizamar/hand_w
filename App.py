import streamlit as st
import random
import pandas as pd
import time
from datetime import datetime
from streamlit_drawable_canvas import st_canvas 

# --- IMPORTS DE APRENDIZAJE AUTOMÁTICO RESTAURADOS ---
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np
# Se omite matplotlib.pyplot ya que no es necesario para la funcionalidad principal.
# --- FIN IMPORTS RESTAURADOS ---

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

# --- 4. Funciones de Predicción REAL (Restauradas) ---

@st.cache_resource
def load_model():
    """Carga el modelo de Keras una sola vez, si es posible."""
    try:
        # Nota: El archivo 'handwritten.h5' debe existir en la carpeta 'model/'
        model = tf.keras.models.load_model("model/handwritten.h5")
        return model
    except Exception as e:
        # Captura el error si TensorFlow o el archivo no están disponibles.
        st.error(f"¡Alerta Estelar! No se pudo cargar el modelo de IA. El archivo 'model/handwritten.h5' o las librerías (TensorFlow/Keras) podrían faltar. Detalles: {e}")
        return None

def predictDigit(image_data, model):
    """Procesa la imagen del Canvas y predice el dígito usando el modelo."""
    
    # 1. Convertir datos del Canvas (RGBA array) a imagen PIL
    # El código original usaba Image.fromarray(..., 'RGBA')
    input_image = Image.fromarray(image_data.astype('uint8'),'RGBA')
    
    # 2. Preprocesamiento (como en el código original)
    image = ImageOps.grayscale(input_image)
    img = image.resize((28,28))
    img = np.array(img, dtype='float32')
    img = img/255
    
    # 3. Preparar para el modelo (reshape: (1, 28, 28, 1) para CNN)
    img = img.reshape((1, 28, 28, 1))
    
    # 4. Predicción
    pred = model.predict(img)
    probabilities_list = pred[0].tolist() # Lista de 10 probabilidades
    result = np.argmax(pred[0])
    
    # 5. Formatear las probabilidades como un diccionario para el DataFrame
    probabilities_dict = {i: prob for i, prob in enumerate(probabilities_list)}

    return str(result), probabilities_dict


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
    
    # Componente Canvas de Dibujo
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
    # Cargar el modelo
    model = load_model()
    
    if model is None:
        # El error ya se mostró dentro de load_model
        st.error("¡Emergencia Cósmica! La clasificación de constelaciones no puede continuar sin el modelo de IA.")
    elif canvas_result.image_data is not None:
        
        # El canvas retorna un array NumPy RGBA
        input_numpy_array = canvas_result.image_data 
        
        # Verificar si se ha dibujado algo significativo
        non_transparent_pixels = (input_numpy_array[:, :, 3] > 0).sum()
        
        if non_transparent_pixels < 50:
            st.error('⚠️ ¡Alerta Estelar! Por favor, dibuja un dígito visible en el Bloc de Polvo Estelar antes de clasificar.')
        else:
            # Predicción REAL con la lógica restaurada
            predicted_digit_str, probabilities_dict = predictDigit(input_numpy_array, model)
            
            # Obtener la probabilidad principal para el encabezado
            main_probability = probabilities_dict.get(int(predicted_digit_str), 0.0)
            
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
                
                # Mostrar el resultado del header 
                st.header(f'El Dígito es : {predicted_digit_str} (Confianza: {main_probability * 100:.2f}%)')


            with col_res2:
                st.subheader("📈 Matriz de Confianza")
                
                # Crear DataFrame para mostrar la matriz de probabilidad
                prob_data = [{"Dígito": i, "Probabilidad (%)": f"{probabilities_dict[i] * 100:.2f}"} for i in range(10)]
                df_prob = pd.DataFrame(prob_data)
                
                # Ordenar por Probabilidad descendente
                df_prob['Probabilidad (%)'] = df_prob['Probabilidad (%)'].str.replace('%', '').astype(float)
                df_prob = df_prob.sort_values(by='Probabilidad (%)', ascending=False)
                df_prob['Probabilidad (%)'] = df_prob['Probabilidad (%)'].apply(lambda x: f"{x:.2f}%")

                st.dataframe(df_prob.set_index('Dígito'), use_container_width=True, height=350)
        
    else:
        st.warning('⚠️ Por favor, dibuja un único dígito (0-9) en el bloc para simular la detección.')


# --- Barra lateral (Sidebar) ---
st.sidebar.title("🪐 Bitácora de Vuelo (Acerca de)")
st.sidebar.markdown("""
<div style='font-family: "Sniglet", cursive; color: var(--color-text);'>
    <p>Esta aplicación utiliza un modelo de Red Neuronal Convolucional (CNN) entrenado con datos MNIST (dígitos).</p>
    <p>La **Interacción Multimodal** se ilustra mediante la entrada de escritura (dibujar con el ratón/dedo) y el posterior procesamiento por la máquina.</p>
    <br>
    <p>Hecho con amor cósmico. ¡Clasifica una constelación!</p>
</div>
""", unsafe_allow_html=True)


# Información adicional y pie de página
st.markdown("---")
st.caption("""
**Acerca de la aplicación (El Crayon Cósmico)**: 
Esta interfaz es un trabajo de Interfaces Multimodales. Utiliza Streamlit y el componente de dibujo para la entrada de datos, y **ahora emplea el modelo de Aprendizaje Automático original** para realizar la clasificación real de dígitos, ilustrando el concepto de Visión Artificial.
""")
