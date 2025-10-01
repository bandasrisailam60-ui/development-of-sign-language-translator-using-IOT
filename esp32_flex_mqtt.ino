#include <WiFi.h>
#include <PubSubClient.h>


// --- CONFIG ---
const char* ssid = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";
const char* mqtt_server = "192.168.1.100"; // change to broker IP
const int mqtt_port = 1883;
const char* mqtt_topic = "signglove/sensors";


WiFiClient espClient;
PubSubClient client(espClient);


// analog pins for flex sensors
const int F1 = 32; // change to your pins
const int F2 = 33;
const int F3 = 34;
const int F4 = 35;
const int F5 = 36;


void setup_wifi() {
delay(10);
WiFi.begin(ssid, password);
while (WiFi.status() != WL_CONNECTED) {
delay(500);
}
}


void reconnect() {
while (!client.connected()) {
if (client.connect("ESP32SignGlove")) {
// connected
} else {
delay(2000);
}
}
}


void setup() {
Serial.begin(115200);
setup_wifi();
client.setServer(mqtt_server, mqtt_port);
}


void loop() {
if (!client.connected()) reconnect();
client.loop();


int v1 = analogRead(F1);
int v2 = analogRead(F2);
int v3 = analogRead(F3);
int v4 = analogRead(F4);
int v5 = analogRead(F5);


// normalize to 0-1 range (optional)
float n1 = v1 / 4095.0;
float n2 = v2 / 4095.0;
float n3 = v3 / 4095.0;
float n4 = v4 / 4095.0;
float n5 = v5 / 4095.0;


char payload[200];
snprintf(payload, sizeof(payload), "{\"sensors\":[%.4f,%.4f,%.4f,%.4f,%.4f],\"t\":%lu}", n1,n2,n3,n4,n5, millis());


client.publish(mqtt_topic, payload);
delay(100); // 10 Hz
}