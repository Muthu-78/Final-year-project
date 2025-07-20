Project Overview
This project is an IoT-based gas level detection system that uses sensor data (Temperature, Humidity, Gas Concentration) to predict gas levels (Safe, Warning, or Danger). It provides real-time alerts via email and sound warnings when hazardous levels are detected. The system includes an interactive Streamlit dashboard for monitoring and analysis.

Key Features
Real-Time Monitoring: Fetches live sensor data using ThingSpeak API.

Automated Alerts: Sends email notifications and plays warning sounds for dangerous gas levels.

Interactive Dashboard:

Manual Input: Test custom sensor values.

Automatic Mode: Continuously checks and logs predictions.

Data Visualization: Displays gas concentration trends.

Machine Learning Model: Uses a stacked ensemble model (Random Forest, SVM, KNN, etc.) with 100% accuracy on test data.

Technologies Used
Backend: Python (scikit-learn, pandas, numpy)

Machine Learning: Stacked ensemble model with StandardScaler

Frontend: Streamlit

IoT Integration: ThingSpeak API for real-time sensor data
