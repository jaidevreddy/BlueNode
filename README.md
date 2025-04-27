# BlueNode

**BlueNode** is a Smart Water Quality Monitoring and Prediction Dashboard built with Flask, MQTT, OpenAI GPT-4o, and real-time Machine Learning. It combines sensor data with AI-driven predictions to improve water management.

## Features

- Live real-time graphs for TDS, Temperature, and Tank Level
- WaterSense AI Chatbot powered by OpenAI GPT-4o
- System Alerts when unsafe TDS levels are detected
- Future Tank Level Predictions using Linear Regression
- Water Usage Prediction with a lightweight Machine Learning model
- Issue Reporting Form for users
- Responsive and minimalistic dashboard design

## Tech Stack

- **Backend:** Flask, Python
- **Frontend:** HTML, CSS, JavaScript (Chart.js)
- **AI Integration:** OpenAI API (GPT-4o)
- **IoT Communication:** MQTT (ESP32 with TDS Sensor)
- **Machine Learning:** scikit-learn (Linear Regression)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/jaidevreddy/BlueNode.git
cd BlueNode
```

### 2. Create and Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate    # For Windows: venv\Scripts\activate
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

Create a `.env` file in the root directory:

```
OPENAI_API_KEY=your_openai_api_key_here
```

Never push your `.env` file to GitHub for security reasons.

### 5. Run the Application

```bash
python app.py
```

Then open your browser at:

```
http://127.0.0.1:5000
```

## MQTT Setup

Make sure your ESP32 device is publishing TDS sensor data using:

- **Broker IP:** Your laptop's local IP (e.g., 192.168.x.x)
- **Port:** 1883
- **Topic:** `sensor/tds`

The dashboard will automatically reflect live sensor data.

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

## Future Improvements

- Historical water quality reporting
- SMS and email system alerts
- Smart home integration
- Predictive maintenance notifications

## License

This project is licensed under the [MIT License](LICENSE).

## Author

Developed by 
K Jaidev Shankar Reddy,
Adoksh M Bharadwaj,
Manvitha R Kabbathi and
Ajay S Prakash


