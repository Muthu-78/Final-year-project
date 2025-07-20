import streamlit as st
import pandas as pd
import numpy as np
import joblib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import winsound
import datetime
import requests
import random
import matplotlib.pyplot as plt
import time 
from streamlit_option_menu import option_menu

# ------------------ Load Models ------------------
model = joblib.load("stacked_gas_level_classifier_model.joblib")
label_encoder = joblib.load("gas_level_label_encoder.joblib")
scaler = joblib.load("scaler.joblib")
# ------------------ Helper Functions ------------------

THINGSPEAK_CHANNEL_ID = "YOUR_CHANNEL_ID"
THINGSPEAK_READ_API_KEY = "YOUR_READ_API_KEY"
THINGSPEAK_URL = f"https://api.thingspeak.com/channels/2952154/feeds.json?api_key=0E6CE8GIUVU8FXMS&results=10"

def send_email(data, prediction, timestamp):
    """
    Send an email with prediction details.
    Args:
        data (dict): Sensor data values.
        prediction (str): Predicted gas level.
        timestamp (str): Timestamp of prediction.
    """
   
    sender_email = "your_email@gmail.com"  # ← User should replace this
    receiver_email="receiver_email@gmail.com" # ← User should replace this
    password = "your_app_password"         # ← User should replace this
    
    subject = f"Gas Level Prediction - {prediction}"
    body = f"Prediction Time: {timestamp}\n\nSensor Data:\n"
    for key, value in data.items():
        body += f"{key}: {value}\n"
    body += f"\nPrediction: {prediction}"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            st.success("📧 Email sent successfully!")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

def predict_gas_level(temperature, humidity, gas_concentration):
    X = pd.DataFrame([[temperature, humidity, gas_concentration]], columns=["Temperature", "Humidity", "GasConcentrationPPM"])
    X_scaled = scaler.transform(X)
    y_pred = model.predict(X_scaled)
    prediction = label_encoder.inverse_transform(y_pred)[0]
    return prediction
# ------------------ Streamlit App ------------------
st.set_page_config(page_title="Gas Level Prediction", layout="wide")

# Sidebar navigation
with st.sidebar:
    tab = option_menu(
        menu_title="Gas Level Detection",
        options=["Dashboard", "Manual Prediction", "Automatic Prediction"],
        icons=["graph-up", "wrench", "robot"],
        menu_icon="cast",
        default_index=0,
        orientation="vertical"
    )

# ------------------ Dashboard ------------------
if tab == "Dashboard":
    st.title("📊 Gas Level Prediction & Anomaly Detection")
    st.image("img.png", width=1700)
    st.markdown("""
    ### Overview
    - This application predicts gas levels based on sensor readings.
    - Possible gas levels: **Safe**, **Warning**, **Danger**.
    - Modes: **Manual** input or **Automatic** predictions from live data.
    """)

# ------------------ Manual Prediction ------------------
elif tab == "Manual Prediction":
    st.title("🧑‍🔧 Manual Gas Level Prediction")
    st.markdown("**Enter sensor readings to predict gas level**")

    temperature = st.number_input("Temperature (°C)", min_value=0.0, max_value=100.0, step=0.1)
    humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, step=0.1)
    gas_concentration = st.number_input("Gas Concentration (PPM)", min_value=0.0, step=0.1)

    if st.button("Predict Gas Level"):
        if temperature == 0 and humidity == 0 and gas_concentration == 0:
            st.error("⚠️ Enter valid input values. All fields are zero.")
        else:
            prediction = predict_gas_level(temperature, humidity, gas_concentration)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Color-coded prediction output
            if prediction == "Danger":
                st.error(f"❌ Prediction: {prediction}")
                winsound.Beep(1000, 500)
                send_email(
                    {
                        "Temperature": temperature,
                        "Humidity": humidity,
                        "Gas Concentration": gas_concentration,
                    },
                    prediction,
                    timestamp,
                )
            elif prediction == "Warning":
                st.warning(f"⚠️ Prediction: {prediction}")
                winsound.Beep(800, 500)
            elif prediction == "Safe":
                st.success(f"✅ Prediction: {prediction}")
            else:
                st.info(f"ℹ️ Prediction: {prediction}")

            

elif tab == "Automatic Prediction":
    st.title("🤖 Automatic Gas Level Prediction")

    # Session state
    if 'prediction_running' not in st.session_state:
        st.session_state.prediction_running = False
    if 'data_records' not in st.session_state:
        st.session_state.data_records = []
    if 'last_entry_id' not in st.session_state:
        st.session_state.last_entry_id = None

    # Buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ Start Prediction"):
            st.session_state.prediction_running = True
            st.success("Prediction started.")
    with col2:
        if st.button("⏹ Stop Prediction"):
            st.session_state.prediction_running = False
            

    placeholder_table = st.empty()
    placeholder_plot = st.empty()

    if st.session_state.prediction_running:
        st.info("🔄 Fetching and predicting gas levels... (updates every 2 seconds)")

        # Continuous loop while running
        while st.session_state.prediction_running:
            try:
                # Fetch most recent feed (last record only)
                url = "https://api.thingspeak.com/channels/2952154/feeds.json?api_key=0E6CE8GIUVU8FXMS&results=1"
                response = requests.get(url)
                data = response.json()
                feed = data["feeds"][0]
                entry_id = feed["entry_id"]

                # Skip if already processed
                if entry_id == st.session_state.last_entry_id:
                    time.sleep(2)
                    continue
                st.session_state.last_entry_id = entry_id

                gas = float(feed["field1"])
                timestamp = feed["created_at"]
                temp = random.uniform(20, 30)
                humidity = random.uniform(40, 70)
                status = predict_gas_level(temp, humidity, gas)

                # Alerts
                if status == "Danger":
                    winsound.Beep(1000, 500)
                    send_email({"Temperature": temp, "Humidity": humidity, "Gas Concentration": gas}, status, timestamp)
                elif status == "Warning":
                    winsound.Beep(800, 500)

                # Record
                st.session_state.data_records.append({
                    "Timestamp": timestamp,
                    "Temperature (°C)": round(temp, 2),
                    "Humidity (%)": round(humidity, 2),
                    "Gas (PPM)": round(gas, 2),
                    "Prediction": status
                })

                # Limit history (optional)
                st.session_state.data_records = st.session_state.data_records[-20:]

                # Display updated table
                df = pd.DataFrame(st.session_state.data_records)
                placeholder_table.dataframe(df, use_container_width=True)

                # Plot updated graph
                fig, ax = plt.subplots(figsize=(10, 4))
                ax.plot(df["Timestamp"], df["Gas (PPM)"], marker='o', linestyle='-', color='purple')
                ax.set_title(" Gas Concentration Over Time")
                ax.set_xlabel("Timestamp")
                ax.set_ylabel("Gas (PPM)")
                plt.xticks(rotation=45)
                placeholder_plot.pyplot(fig)

                time.sleep(1)  # Delay before next fetch

            except Exception as e:
                st.error(f"❌ Error: {e}")
                break
    else:
        st.info("Press ▶️ Start Prediction to begin automatic detection.")
