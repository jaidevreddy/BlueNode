# BlueNode

**BlueNode** is a Smart Water Quality Monitoring, Prediction, and Assistance Dashboard built with Flask, MQTT, OpenAI GPT-4o, and real-time Machine Learning.  
It connects to an ESP32-based TDS sensor to display live water quality metrics, predicts future water availability, and features a built-in AI chatbot for real-time guidance based on sensor data.

---

## Features

- Real-time TDS monitoring from ESP32 sensor via MQTT
- Simulated Temperature and Tank Level readings
- AI-powered **WaterSense Chatbot** using OpenAI GPT-4o, answering user queries based on live sensor data
- Live Graphs for TDS, Temperature, and Tank Level
- System Alerts triggered if TDS exceeds safe drinking limits
- Tank Empty Time Prediction using simple Linear Regression
- Water Usage Forecasting using simulated data 
- Interactive Issue Reporting Form
- Responsive and modern dashboard design

---

## Important Details

- **TDS values** are **real-time readings** from an **ESP32** and **TDS sensor**, sent using **MQTT**.
- **Temperature** and **Tank Level** are **randomly simulated** (for now, to simulate full functionality).
- **ESP32 setup** is required for TDS monitoring.
- **AI Chatbot** generates human-like, precise, and safe water-related responses using **OpenAI GPT-4o** based on live sensor readings.

---

## Tech Stack

- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, JavaScript (Chart.js)
- **AI Integration:** OpenAI GPT-4o
- **IoT Communication:** MQTT with ESP32
- **Machine Learning:** scikit-learn (Linear Regression)

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/jaidevreddy/BlueNode.git
cd BlueNode
```

### 2. Create and Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Example `requirements.txt`:

```
Flask
openai
paho-mqtt
scikit-learn
python-dotenv
```

### 4. Configure Environment Variables

Create a `.env` file:

```
OPENAI_API_KEY=your_openai_api_key_here
```

### 5. Run the Application

```bash
python app.py
```

Visit:

```
http://127.0.0.1:5000
```

---

## ESP32 and TDS Sensor Setup

- **Microcontroller:** ESP32
- **Sensor:** TDS Sensor Module
- **Communication:** MQTT
- **Topic:** `sensor/tds`

Your ESP32 must:

- Connect to the same Wi-Fi network as your laptop
- Publish TDS values to the MQTT broker on port 1883
- Broker Address: your laptop's local IP (example: `192.168.x.x`)

Example Arduino MQTT Publish Code Snippet:

```cpp
client.publish("sensor/tds", String(tdsValue).c_str());
```

Ensure Mosquitto or another MQTT broker is running locally.

---

## Project Structure

```
BlueNode/
├── app.py
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── requirements.txt
└── README.md
```

---

## Future Enhancements

- Replace simulated Temperature and Tank Level with actual sensors
- Notification system (SMS/Email) for water quality alerts
- Data history dashboard for analysis
- Full smart home integration (Home Assistant, Alexa)

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Author

Developed and maintained by 
K Jaidev Shankar Reddy,
Adoksh M Bharadwaj,
Manvitha R Kabbathi and
Ajay S Prakash


