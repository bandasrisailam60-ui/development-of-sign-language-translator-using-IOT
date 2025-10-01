import paho.mqtt.client as mqtt
import json
import numpy as np
import pickle
from tensorflow.keras.models import load_model
from gtts import gTTS
import os
from queue import Queue
import threading


MODEL_PATH = 'sign_model.h5'
LE_PATH = 'label_encoder.pkl'
MQTT_BROKER = '192.168.1.100' # change
MQTT_TOPIC = 'signglove/sensors'


model = load_model(MODEL_PATH)
with open(LE_PATH,'rb') as f:
le = pickle.load(f)


q = Queue()


# create a small packet processor thread so inference isn't done on MQTT callback


def worker():
while True:
data = q.get()
if data is None:
break
sensors = np.array(data['sensors'], dtype=np.float32).reshape(1,-1)
probs = model.predict(sensors)
pred = np.argmax(probs, axis=1)[0]
label = le.inverse_transform([pred])[0]
print('Recognized:', label)
# speak
tts = gTTS(text=str(label))
tfile = 'out.mp3'
tts.save(tfile)
# play using mpg123 or other player available on system
os.system(f'mpg123 -q {tfile}')


threading.Thread(target=worker, daemon=True).start()


# MQTT callbacks


def on_connect(client, userdata, flags, rc):
client.subscribe(MQTT_TOPIC)
print('Connected to broker')


def on_message(client, userdata, msg):
try:
payload = msg.payload.decode('utf-8')
j = json.loads(payload)
# expected: {"sensors":[...], "t":...}
sensors = j.get('sensors')
if sensors:
q.put({'sensors': sensors})
except Exception as e:
print('Error processing message', e)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER, 1883, 60)
client.loop_forever()