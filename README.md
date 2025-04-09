# ⛽ Fuel Fraud Detection – AI-Based Fuel Monitoring System

## 🔍 Overview
Fuel Fraud Detection is an AI- and IoT-powered system designed to monitor fuel dispensing activities at fuel stations. By integrating computer vision, sensor data, and real-time analytics, this system helps detect fuel theft, improper handling, and transaction anomalies.

---

## 🔹 Features

✅ **YOLOv6 Surveillance Monitoring** – Detects improper fuel gun usage from CCTV footage.  
✅ **Sensor-Based Fraud Detection** – Monitors flow rate, tank levels, and vehicle load to detect irregularities.  
✅ **Sentiment & Topic Analysis** – Analyzes customer feedback using RoBERTa and LDA.  
✅ **Real-Time Dashboard** – Displays live alerts, sensor data, and predictions.  
✅ **Modular Python Services** – Separate models for sentiment analysis, summarization, and topic extraction.  
✅ **Secure MQTT Communication** – Ensures fast and reliable data transfer from IoT devices.

---

## 📌 Problems Solved

1️⃣ Detects fuel theft or fraud in real-time using AI and sensor fusion.  
2️⃣ Automates customer feedback analysis to improve service.  
3️⃣ Reduces human supervision through real-time visual alerts.  
4️⃣ Helps station owners maintain accurate fuel logs and detect anomalies.  
5️⃣ Increases transparency through sensor-based verification of fuel dispensing.

---

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Flask (Python), Node.js  
- **AI/ML:** YOLOv6, RoBERTa, LDA, OpenCV  
- **Database:** MySQL  
- **IoT & Firmware:** ESP32, Flow Sensor, Load Cell, Ultrasonic Sensor, ESP32-CAM, Arduino C/C++  
- **Communication:** MQTT over Wi-Fi

---

## 🏗️ Project Structure

FUEL-DETECTION/
│── css/                      # Stylesheets
│── images/                   # Icons, camera frames, etc.
│── js/                       # Frontend JavaScript
│── models/                   # Python scripts for ML tasks
│   ├── sample.py
│   ├── sentimental.py
│   ├── summary.py
│   └── topicextractin.py
│── myenv/                    # Python virtual environment
│── node_modules/             # Node.js dependencies
│── webfonts/                 # Web fonts
├── app.py                    # Main Flask app
├── server.js                 # MQTT server handler (Node.js)
├── app.js                    # Client-side JavaScript
├── fuel_map.html             # Fuel tracking page
├── home.html                 # Landing page
├── index.html                # Dashboard interface
├── live.html                 # Live surveillance stream
├── signup.html               # Registration page
├── style.css                 # Custom CSS
├── package.json              # Node project metadata
├── package-lock.json         # Node dependency lock
├── .gitignore                # Git ignore rules

## ⚙️ Setup Instructions

### 1️⃣ Prerequisites

- Python 3.10+
- Node.js & npm
- MySQL Server
- Arduino IDE
- ESP32 & necessary sensors
- MQTT broker (like Mosquitto)

### 2️⃣ Backend Setup

```bash
# Create a virtual environment
python -m venv myenv
source myenv/bin/activate    # For Linux/Mac
myenv\Scripts\activate       # For Windows

# Install dependencies
pip install -r requirements.txt

# Start Flask server
python app.py
3️⃣ Node Server Setup
bash
Copy
Edit
# Install Node.js packages
npm install

# Start MQTT server
node server.js
🔎 Usage
📹 Monitor fuel gun usage via real-time video analysis.

🧠 Run sentiment and topic models on collected feedback.

📊 View data and alerts on the interactive dashboard.

⚙️ Connect and configure IoT devices via Wi-Fi.

🔭 Future Scope
Multilingual Feedback Analysis using Indian regional languages.

GPS Tracking Integration for delivery vehicle tracking.

Edge Computing Support for faster onsite processing.

Data Analytics Dashboard for long-term fraud trends.

Automated Report Generation and alerts to stakeholders.

📜 License
This project is licensed under the MIT License.
Feel free to use, modify, and share it with proper attribution.
