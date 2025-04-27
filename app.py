from flask import Flask, render_template, request, redirect, url_for, jsonify
import openai
import random
from datetime import datetime, timedelta
import numpy as np
from sklearn.linear_model import LinearRegression
import threading
import paho.mqtt.client as mqtt

app = Flask(__name__)

# OpenAI Setup
client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

chat_history = []
tank_history = []
current_tds = 0

# MQTT Setup
MQTT_BROKER = "192.168.106.124"
MQTT_PORT = 1883
MQTT_TOPIC = "sensor/tds"

mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ MQTT Connected Successfully")
        client.subscribe(MQTT_TOPIC)
    else:
        print("❌ MQTT Connection Failed with rc=", rc)

def on_message(client, userdata, msg):
    global current_tds
    try:
        current_tds = float(msg.payload.decode())
        print(f"📡 Received TDS: {current_tds} ppm")
    except:
        print("Error decoding TDS value.")

def start_mqtt():
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_forever()

mqtt_thread = threading.Thread(target=start_mqtt)
mqtt_thread.daemon = True
mqtt_thread.start()

# Pre-fill tank history
current_time = datetime.now()
current_level = random.randint(60, 100)
for i in range(10):
    tank_history.append((current_time - timedelta(minutes=5 * (9 - i)), current_level))
    current_level = max(0, current_level - random.randint(1, 5))

def generate_sensor_data():
    temperature = round(random.uniform(15, 35), 2)
    tank_level = random.randint(0, 100)
    return temperature, tank_level

def predict_tank_levels(history):
    if len(history) < 5:
        return None, None

    times = np.array([(t - history[0][0]).total_seconds() / 3600 for t, _ in history]).reshape(-1, 1)
    levels = np.array([lvl for _, lvl in history])

    model = LinearRegression()
    model.fit(times, levels)

    future_hours = np.array([2, 4, 6]).reshape(-1, 1)
    predicted_levels = model.predict(future_hours)

    if model.coef_[0] >= 0:
        empty_time = None
    else:
        empty_hours = -model.intercept_ / model.coef_[0]
        empty_time = history[0][0] + timedelta(hours=empty_hours)

    return predicted_levels, empty_time

def generate_usage_prediction():
    times = np.array(range(0, 10)).reshape(-1, 1)
    usage = 5 + np.random.rand(10) * 5  # random usage between 5-10 liters/hr
    model = LinearRegression()
    model.fit(times, usage)
    future_times = np.array(range(10, 20)).reshape(-1, 1)
    predictions = model.predict(future_times)
    return predictions.tolist()

@app.route("/", methods=["GET", "POST"])
def index():
    global chat_history, tank_history

    if request.method == "POST":
        user_input = request.form.get("message")
        temperature, tank_level = generate_sensor_data()

        timestamp = datetime.now()
        tank_history.append((timestamp, tank_level))
        if len(tank_history) > 20:
            tank_history.pop(0)

        # 🆕 SHORT, ON-POINT PROMPT
        full_prompt = f"""
Sensor Readings:
- TDS: {current_tds} ppm
- Temperature: {temperature} °C
- Tank Level: {tank_level} %

User Question: {user_input}

Instructions:
Reply in 2-3 lines maximum.
Directly answer whether the water is safe or unsafe.
Mention TDS, temperature, and tank level briefly.
No long explanations. Be clear, short, and on-point like a technician.
"""

        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful, technical water management assistant."},
                    {"role": "user", "content": full_prompt}
                ],
                temperature=0.5,
            )
            bot_message = response.choices[0].message.content.strip()
        except Exception as e:
            bot_message = "Error fetching response."

        chat_history.append({
            "sender": "user",
            "text": user_input,
            "time": datetime.now().strftime("%I:%M %p")
        })
        chat_history.append({
            "sender": "bot",
            "text": bot_message,
            "time": datetime.now().strftime("%I:%M %p")
        })

        return redirect(url_for('index'))

    else:
        temperature, tank_level = generate_sensor_data()
        timestamp = datetime.now()
        tank_history.append((timestamp, tank_level))
        if len(tank_history) > 20:
            tank_history.pop(0)

    predicted_levels, empty_time = predict_tank_levels(tank_history)
    usage_predictions = generate_usage_prediction()
    return render_template("index.html", chat_history=chat_history, predicted_levels=predicted_levels, empty_time=empty_time, usage_predictions=usage_predictions)

@app.route("/latest-tds")
def latest_tds():
    global current_tds
    return jsonify({"tds": current_tds})

if __name__ == "__main__":
    app.run(debug=True, port=5000)