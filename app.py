import os
import streamlit as st
from bokeh.models import Button  # ✅ Corrección aquí
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import glob
import paho.mqtt.client as paho
import json
from gtts import gTTS
import base64
from googletrans import Translator

# ---- MQTT Setup ----
def on_publish(client, userdata, result):
    print("✅ Dato publicado en el broker MQTT.")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.write(f"📡 Mensaje recibido: {message_received}")

broker = "broker.mqttdashboard.com"
port = 1883
client1 = paho.Client("ANUEL-VOICE-CONTROL")
client1.on_message = on_message

# ---- Estilo CSS inspirado en Anuel ----
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #000000, #4b0000, #ff0000);
            color: white;
            font-family: 'Poppins', sans-serif;
        }
        h1 {
            text-align: center;
            color: #ff3b3b;
            font-size: 2.5em;
            font-weight: 800;
            text-shadow: 0px 0px 15px #ff0000;
        }
        h2, h3 {
            text-align: center;
            color: #f7dada;
            font-weight: 600;
            text-shadow: 0px 0px 8px #a00000;
        }
        p, div, span {
            color: #f5f5f5 !important;
            font-size: 1.1em;
        }
        img {
            display: block;
            margin-left: auto;
            margin-right: auto;
            border-radius: 20px;
            border: 3px solid #ff0000;
            box-shadow: 0px 0px 25px rgba(255, 0, 0, 0.6);
        }
        div[data-testid="stButton"] > button {
            background: linear-gradient(90deg, #ff0000, #660000);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.6em 2em;
            font-size: 1.1em;
            font-weight: 600;
            box-shadow: 0px 0px 15px #ff1a1a;
            transition: all 0.3s ease;
        }
        div[data-testid="stButton"] > button:hover {
            transform: scale(1.08);
            box-shadow: 0px 0px 25px #ff3333;
        }
        .footer {
            text-align: center;
            margin-top: 25px;
            font-size: 1.1em;
            color: #ff4d4d;
        }
    </style>
""", unsafe_allow_html=True)

# ---- Interfaz Principal ----
st.title("🎤 INTERFACES MULTIMODALES")
st.subheader("🔥 CONTROL POR VOZ - ESTILO ANUEL 🔥")
st.markdown("💬 *“Yo soy leyenda, no por fama… por respeto.”* — Anuel AA")

# Imagen de portada
try:
    image = Image.open('voice_ctrl.jpg')
    st.image(image, width=250)
except:
    st.warning("⚠️ No se encontró la imagen 'voice_ctrl.jpg'. Puedes agregarla para más flow.")

# Indicaciones
st.write("Toca el botón y **habla con poder** — deja que la voz controle la acción 💯")

# Botón de reconocimiento de voz
stt_button = Button(label="🎙️ INICIAR VOZ", width=200)
stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;

    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if (value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
"""))

# Escucha del evento de voz
result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0
)

# Procesamiento de voz
if result and "GET_TEXT" in result:
    comando = result.get("GET_TEXT").strip()
    st.success(f"🎧 Comando detectado: {comando}")

    # Publicar en MQTT
    client1.on_publish = on_publish
    client1.connect(broker, port)
    mensaje = json.dumps({"Act1": comando})
    client1.publish("voice_ctrl", mensaje)

    # Crear carpeta temporal
    os.makedirs("temp", exist_ok=True)

    # Convertir a audio con gTTS
    tts = gTTS(comando, lang='es')
    audio_path = f"temp/{comando[:15].replace(' ', '_')}.mp3"
    tts.save(audio_path)

    with open(audio_path, "rb") as f:
        audio_bytes = f.read()
    st.audio(audio_bytes, format="audio/mp3")

# Footer
st.markdown("""
<div class="footer">
    💥 Proyecto inspirado en la energía de Anuel AA 💥<br>
    "Real hasta la muerte 🔥"
</div>
""", unsafe_allow_html=True)
