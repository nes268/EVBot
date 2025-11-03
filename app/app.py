from flask import Flask, render_template, request
import joblib
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app = Flask(__name__, 
            template_folder=os.path.join(BASE_DIR, 'templates'),
            static_folder=os.path.join(BASE_DIR, 'static'))

# Load model and encoders when the app starts
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'ev_model.pkl')
ENCODERS_PATH = os.path.join(BASE_DIR, 'models', 'label_encoders.pkl')

try:
    model = joblib.load(MODEL_PATH)
    encoders = joblib.load(ENCODERS_PATH)
    print("Model and encoders loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None
    encoders = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None or encoders is None:
        return render_template('index.html', result="Error: Model not loaded")
    
    try:
        # Get form data
        soc = float(request.form['soc'])
        voltage = float(request.form['voltage'])
        current = float(request.form['current'])
        battery_temp = float(request.form['battery_temp'])
        ambient_temp = float(request.form['ambient_temp'])
        duration = float(request.form['duration'])
        degradation = float(request.form['degradation'])
        mode = request.form['mode']
        efficiency = float(request.form['efficiency'])
        battery_type = request.form['battery_type']
        cycles = int(request.form['cycles'])
        ev_model = request.form['ev_model']
        
        # Create DataFrame in the correct order
        features = pd.DataFrame({
            'SOC (%)': [soc],
            'Voltage (V)': [voltage],
            'Current (A)': [current],
            'Battery Temp (°C)': [battery_temp],
            'Ambient Temp (°C)': [ambient_temp],
            'Charging Duration (min)': [duration],
            'Degradation Rate (%)': [degradation],
            'Charging Mode': [mode],
            'Efficiency (%)': [efficiency],
            'Battery Type': [battery_type],
            'Charging Cycles': [cycles],
            'EV Model': [ev_model]
        })
        
        # Encode categorical variables
        features['Charging Mode'] = encoders['Charging Mode'].transform(features['Charging Mode'])
        features['Battery Type'] = encoders['Battery Type'].transform(features['Battery Type'])
        features['EV Model'] = encoders['EV Model'].transform(features['EV Model'])
        
        # Make prediction
        prediction = model.predict(features)[0]
        
        # Map prediction to meaningful message
        class_messages = {
            0: "Optimal Charging Duration: Short - Ideal battery health, standard charging acceptable.",
            1: "Optimal Charging Duration: Medium - Normal battery condition, moderate charging recommended.",
            2: "Optimal Charging Duration: Long - Battery needs attention, extended charging required."
        }
        
        result_message = class_messages.get(prediction, f"Prediction: Class {prediction}")
        
        return render_template('index.html', result=result_message)
        
    except Exception as e:
        return render_template('index.html', result=f"Error: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

