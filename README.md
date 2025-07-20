# Gas Level Detection and Alert System


## Project Overview
An IoT-based system that predicts gas levels (Safe/Warning/Danger) using sensor data (Temperature, Humidity, Gas Concentration) and triggers real-time alerts through email and sound notifications. Includes an interactive Streamlit dashboard for monitoring and analysis.

## Key Features
- **Real-Time Monitoring**
  - Fetches live sensor data using ThingSpeak API
  - Continuously updates gas level predictions

- **Alert System**
  - Email notifications for hazardous levels
  - Audio warnings for immediate danger detection

- **Interactive Dashboard**
  - Manual input for custom sensor testing
  - Automatic mode for continuous monitoring
  - Data visualization of gas concentration trends

- **Machine Learning Model**
  - Stacked ensemble model (Random Forest, SVM, KNN)
  - 100% accuracy on test data
  - Scalable for additional sensor inputs

## Technologies Used
### Backend
- Python 3
- scikit-learn
- pandas
- numpy

### Machine Learning
- Stacked ensemble classifier
- StandardScaler for feature normalization
- LabelEncoder for target classes

### Frontend
- Streamlit for web interface
- Matplotlib/Seaborn for visualization

### IoT Integration
- ThingSpeak API for sensor data
- SMTP for email alerts
- Winsound for audio warnings

## Before Running
1. Edit these lines in `app.py`:
   ```python
   #Email Configuration (lines 12-13)
   sender_email = "your_email@gmail.com"  
   password = "your_app_password"  

   # ThingSpeak API (line 8)
   THINGSPEAK_URL = "https://api.thingspeak.com/..."



