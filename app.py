import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

# --- 🎨 Estilo visual ANUEL: fondo negro con degradado rojo ---
st.markdown("""
    <style>
        /* Fondo degradado negro y rojo */
        .stApp {
            background: linear-gradient(to bottom right, #000000, #8B0000);
            font-family: 'Poppins', sans-serif;
        }

        /* Título con estilo fuerte y brillante */
        h1 {
            color: #ff0000;
            text-align: center;
            font-weight: 900;
            text-shadow: 2px 2px 10px #000000;
            letter-spacing: 2px;
            margin-bottom: 0.8em;
        }

        /* Texto blanco con toques rojos */
        p, label {
            color: #ffffff !important;
            font-weight: 500;
        }

        /* Estilo de botones (modo trap) */
        .stButton>button {
            background-color: #ff0000 !important;
            color: white !important;
            border-radius: 10px;
            border: 2px solid #fff;
            font-weight: bold;
            letter-spacing: 1px;
            transition: all 0.3s ease;
        }

        .stButton>button:hover {
            background-color: #000000 !important;
            color: #ff0000 !important;
            box-shadow: 0px 0px 20px #ff0000;
            transform: scale(1.1);
        }

        /* Slider estilo rojo */
        [data-testid="stSlider"] .st-ax {
            background-color: #ff0000 !important;
        }

        /* Mensaje de salida */
        .mqtt-output {
            background-color: rgba(255, 0, 0, 0.15);
            padding: 10px;
            border-radius: 10px;
            color: white;
            font-weight: bold;
            border: 1px solid #ff0000;
        }
    </style>
""", unsafe_allow_html=True)

# --- Encabezado principal ---
st.title("🎛️ CONTROL MQTT - MODO ANUEL 🔥")

# --- Versión de Python ---
st.write("💻 Versión de Python:", platform.python_version())

# --- Variables iniciales ---
values = 0.0
act1 = "OFF"
message_received = ""

# --- Funciones MQTT ---
def on_publish(client, userdata, result):
    print("✅ El dato ha sido publicado con éxito\n")

def on_message(client, userdata, message):
    global message_received
    time.sleep(1)
    message_received = str(message.payload.decode("utf-8"))
    st.markdown(f"<div class='mqtt-output'>📩 Mensaje recibido: {message_received}</div>", unsafe_allow_html=True)

# --- Configuración del broker MQTT ---
broker = "157.230.214.127"
port = 1883
client1 = paho.Client("GIT-HUB")
client1.on_message = on_message

# --- Botones de control ON/OFF ---
col1, col2 = st.columns(2)

with col1:
    if st.button('💡 ENCENDER (ON)'):
        act1 = "ON"
        client1 = paho.Client("GIT-HUB")
        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"Act1": act1})
        ret = client1.publish("cmqtt_s", message)
        st.success("🔥 Dispositivo encendido")

with col2:
    if st.button('💤 APAGAR (OFF)'):
        act1 = "OFF"
        client1 = paho.Client("GIT-HUB")
        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"Act1": act1})
        ret = client1.publish("cmqtt_s", message)
        st.warning("⚡ Dispositivo apagado")

# --- Slider para valor analógico ---
st.markdown("<br>", unsafe_allow_html=True)
values = st.slider('🎚️ Selecciona un valor analógico', 0.0, 100.0)
st.markdown(f"<p style='color:white;'>Valor seleccionado: <b>{values}</b></p>", unsafe_allow_html=True)

if st.button('📤 Enviar valor analógico'):
    client1 = paho.Client("GIT-HUB")
    client1.on_publish = on_publish
    client1.connect(broker, port)
    message = json.dumps({"Analog": float(values)})
    ret = client1.publish("cmqtt_a", message)
    st.success(f"📡 Valor {values} enviado correctamente al canal analógico")

# --- Mensaje final ---
st.markdown("""
<div style='text-align:center; margin-top:30px; font-size:1.1em; color:white;'>
🎶 Controla tu flow digital desde la consola de poder 🎶<br>
<span style='color:#ff0000;'>💯 ANUEL AI SYSTEM 💯</span>
</div>
""", unsafe_allow_html=True)
