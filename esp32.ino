#include <WiFi.h>
#include <PubSubClient.h>

// WiFi credentials
const char* ssid = "P";      // 🛠️ Change this
const char* password = "12345678";  // 🛠️ Change this

// MQTT Broker IP
const char* mqtt_server = "192.168.106.124";  // 🛠️ Your Mac's Wi-Fi IP

WiFiClient espClient;
PubSubClient client(espClient);

// TDS sensor pin
const int tdsPin = 34; // example pin (ADC pin on ESP32)

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to WiFi ");

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi Connected. IP Address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("ESP32Client")) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 3 seconds");
      delay(3000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  int tdsValue = analogRead(tdsPin);
  float voltage = tdsValue * (3.3 / 4095.0);
  float tds = (133.42 * voltage * voltage * voltage
               - 255.86 * voltage * voltage
               + 857.39 * voltage) * 0.5;

  String payload = String(tds, 2); // keep two decimal points
  Serial.print("Publishing TDS: ");
  Serial.println(payload);

  client.publish("sensor/tds", payload.c_str());

  delay(3000); // Publish every 3 seconds
}