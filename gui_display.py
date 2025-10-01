import tkinter as tk
import threading
import paho.mqtt.client as mqtt
import json


MQTT_BROKER = '192.168.1.100'
MQTT_TOPIC = 'signglove/recognized'


root = tk.Tk()
root.title('Sign Language Translator')
label_var = tk.StringVar(value='— waiting —')
label = tk.Label(root, textvariable=label_var, font=('Arial', 48))
label.pack(padx=20,pady=20)


# If you prefer, have the inference_server publish recognized labels to this topic.


def on_connect(client, userdata, flags, rc):
client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):
j = json.loads(msg.payload.decode())
label_var.set(j.get('label',''))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER,1883,60)


def mqtt_loop():
client.loop_forever()


threading.Thread(target=mqtt_loop, daemon=True).start()


root.mainloop()