import paho.mqtt.client as paho
import time
import streamlit as st
import json

# 🧠 Configuración general de la página
st.set_page_config(
    page_title="🔥 Panel de Control MQTT - Estilo Anuel 🔥",
    page_icon="🎤",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 🎨 Estilos personalizados: Degradado negro y rojo con efectos neón
st.markdown("""
    <style>
        /* Fondo degradado oscuro con estilo urbano */
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #000000 30%, #8b0000 100%);
            color: #f5f5f5;
            font-family: 'Poppins', sans-serif;
        }

        /* Título principal */
        h1 {
            color: #ff1e56;
            text-shadow: 0 0 25px rgba(255, 0, 0, 0.8);
            text-align: center;
            font-size: 3em;
            font-weight: 900;
            letter-spacing: 2px;
        }

        /* Subtítulos y textos */
        h2, h3, label, p {
            color: #f8d7da;
            text-align: center;
        }

        /* Caja principal */
        .main {
            background-color: rgba(20, 20, 20, 0.7);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 0 25px rgba(255, 0, 0, 0.3);
        }

        /* Botones con efectos neón */
        .stButton>button {
            color: #fff;
            border: none;
            border-radius: 12px;
            height: 50px;
            width: 100%;
            font-size: 1.2em;
            font-weight: bold;
            letter-spacing: 1px;
            transition: all 0.3s ease;
            background: linear-gradient(90deg, #ff0033, #ff1e56);
            box-shadow: 0 0 15px rgba(255, 0, 0, 0.5);
        }

        .stButton>button:hover {
            background: linear-gradient(90deg, #1e90ff, #0077ff);
            box-shadow: 0 0 25px rgba(0, 153, 255, 0.8);
            transform: scale(1.07);
        }

        /* Slider estilo metálico */
        .stSlider label {
            color: #ffcccc;
            font-weight: bold;
        }

        .stMarkdown h3 {
            color: #ff6666;
        }

        /* Línea separadora personalizada */
        hr {
            border: 1px solid #ff1e56;
            box-shadow: 0 0 10px rgba(255, 0, 0, 0.6);
        }
    </style>
""", unsafe_allow_html=True)

# ⚙️ Variables globales
values = 0.0
act1 = "OFF"

def on_publish(client, userdata, result):
    print("✅ Dato publicado correctamente")

def on_message(client, userdata, message):
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.write(f"📩 Mensaje recibido: `{message_received}`")

# 🛰️ Conexión MQTT
broker = "157.230.214.127"
port = 1883
client1 = paho.Client("ANUEL-MQTT")
client1.on_message = on_message

# 🎤 INTERFAZ PRINCIPAL
st.title("🔥 PANEL DE CONTROL MQTT 🔥")
st.markdown("### 💀 By: Flow Inteligente")

st.markdown("<hr>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    if st.button('🚨 ENCENDER DISPOSITIVO'):
        act1 = "ON"
        client1 = paho.Client("ANUEL-MQTT")
        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"Act1": act1})
        client1.publish("cmqtt_s", message)
        st.success("💡 Dispositivo ENCENDIDO - 🔥 Real Hasta la Muerte 🔥")

with col2:
    if st.button('💤 APAGAR DISPOSITIVO'):
        act1 = "OFF"
        client1 = paho.Client("ANUEL-MQTT")
        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"Act1": act1})
        client1.publish("cmqtt_s", message)
        st.error("💀 Dispositivo APAGADO")

st.markdown("<hr>", unsafe_allow_html=True)

# 🎚️ Control analógico
st.markdown("### ⚙️ CONTROL ANALÓGICO")
values = st.slider('Selecciona un valor para enviar', 0.0, 100.0, 50.0)
st.write(f"🎛️ Valor seleccionado: `{values}`")

if st.button('📤 ENVIAR VALOR ANALÓGICO'):
    client1 = paho.Client("ANUEL-MQTT")
    client1.on_publish = on_publish
    client1.connect(broker, port)
    message = json.dumps({"Analog": float(values)})
    client1.publish("cmqtt_a", message)
    st.success(f"🚀 Valor analógico enviado: `{values}`")

st.markdown("<hr>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#ffcccc;'>🎶 “Brrr... Real Hasta la Muerte 🔥”</p>", unsafe_allow_html=True)
