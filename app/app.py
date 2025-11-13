from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
import plotly
import plotly.express as px
import json
try:
    from chatbot import chatbot
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from chatbot import chatbot

from ml_model import get_assets, predict_from_payload

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app = Flask(__name__, 
            template_folder=os.path.join(BASE_DIR, 'templates'),
            static_folder=os.path.join(BASE_DIR, 'static'))

try:
    get_assets()
    print("Model and encoders loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET'])
def predict_page():
    return render_template('predict.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        payload = {key: request.form.get(key) for key in (
            'soc', 'voltage', 'current', 'battery_temp', 'ambient_temp',
            'duration', 'degradation', 'mode', 'efficiency',
            'battery_type', 'cycles', 'ev_model'
        )}

        result = predict_from_payload(payload)
        return render_template(
            'predict.html',
            result=result['message'],
            result_type=result['result_type']
        )

    except Exception as e:
        return render_template('predict.html', result=f"Error: {str(e)}")

@app.route('/dashboard')
def dashboard():
    # Load dataset
    DATA_PATH = os.path.join(BASE_DIR, 'data', 'ev_battery_charging_data.csv')
    df = pd.read_csv(DATA_PATH)
    
    # Calculate dynamic statistics
    total_samples = len(df)
    avg_efficiency = df['Efficiency (%)'].mean()
    avg_degradation = df['Degradation Rate (%)'].mean()
    class_distribution = df['Optimal Charging Duration Class'].value_counts().to_dict()
    
    # Get unique values for filters
    ev_models = sorted(df['EV Model'].unique().tolist())
    battery_types = sorted(df['Battery Type'].unique().tolist())
    charging_modes = sorted(df['Charging Mode'].unique().tolist())
    
    # Chart 1: SOC vs Voltage
    fig1 = px.scatter(df, x='SOC (%)', y='Voltage (V)', 
                      color='Optimal Charging Duration Class',
                      title='State of Charge vs Voltage',
                      labels={'Optimal Charging Duration Class': 'Charging Class'},
                      hover_data=['EV Model', 'Battery Type', 'Charging Mode'])
    
    # Chart 2: Efficiency per EV Model (aggregated)
    efficiency_df = df.groupby(['EV Model', 'Battery Type'])['Efficiency (%)'].mean().reset_index()
    fig2 = px.bar(efficiency_df, x='EV Model', y='Efficiency (%)', 
                  color='Battery Type',
                  title='Average Efficiency per EV Model',
                  barmode='group')
    
    # Chart 3: Distribution of Charging Duration Classes
    fig3 = px.pie(df, names='Optimal Charging Duration Class',
                  title='Optimal Charging Duration Class Distribution',
                  labels={'Optimal Charging Duration Class': 'Class'})
    
    # Chart 4: Degradation vs Cycles
    fig4 = px.scatter(df, x='Charging Cycles', y='Degradation Rate (%)',
                      color='Optimal Charging Duration Class',
                      size='Efficiency (%)',
                      title='Battery Degradation vs Charging Cycles',
                      hover_data=['EV Model', 'SOC (%)'])
    
    # Convert to JSON for HTML rendering
    graphs = {
        "fig1": json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder),
        "fig2": json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder),
        "fig3": json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder),
        "fig4": json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
    }
    
    stats = {
        "total_samples": total_samples,
        "avg_efficiency": round(avg_efficiency, 2),
        "avg_degradation": round(avg_degradation, 2),
        "class_0": class_distribution.get(0, 0),
        "class_1": class_distribution.get(1, 0),
        "class_2": class_distribution.get(2, 0)
    }
    
    return render_template('dashboard.html', 
                         graphs=graphs, 
                         stats=stats,
                         has_data=stats["total_samples"] > 0,
                         ev_models=ev_models,
                         battery_types=battery_types,
                         charging_modes=charging_modes)

@app.route('/api/dashboard/data', methods=['GET'])
def get_dashboard_data():
    """API endpoint for dynamic data filtering"""
    DATA_PATH = os.path.join(BASE_DIR, 'data', 'ev_battery_charging_data.csv')
    df = pd.read_csv(DATA_PATH)
    
    # Get filter parameters
    ev_model = request.args.get('ev_model', 'all')
    battery_type = request.args.get('battery_type', 'all')
    charging_mode = request.args.get('charging_mode', 'all')
    
    # Apply filters
    filtered_df = df.copy()
    if ev_model != 'all':
        filtered_df = filtered_df[filtered_df['EV Model'] == ev_model]
    if battery_type != 'all':
        filtered_df = filtered_df[filtered_df['Battery Type'] == battery_type]
    if charging_mode != 'all':
        filtered_df = filtered_df[filtered_df['Charging Mode'] == charging_mode]
    
    # Calculate statistics
    stats = {
        "total_samples": len(filtered_df),
        "avg_efficiency": round(filtered_df['Efficiency (%)'].mean(), 2) if len(filtered_df) > 0 else 0,
        "avg_degradation": round(filtered_df['Degradation Rate (%)'].mean(), 2) if len(filtered_df) > 0 else 0,
        "avg_soc": round(filtered_df['SOC (%)'].mean(), 2) if len(filtered_df) > 0 else 0,
        "avg_voltage": round(filtered_df['Voltage (V)'].mean(), 2) if len(filtered_df) > 0 else 0,
        "class_0": len(filtered_df[filtered_df['Optimal Charging Duration Class'] == 0]),
        "class_1": len(filtered_df[filtered_df['Optimal Charging Duration Class'] == 1]),
        "class_2": len(filtered_df[filtered_df['Optimal Charging Duration Class'] == 2])
    }
    
    # Create charts with filtered data
    fig1 = px.scatter(filtered_df, x='SOC (%)', y='Voltage (V)', 
                      color='Optimal Charging Duration Class',
                      title='State of Charge vs Voltage',
                      labels={'Optimal Charging Duration Class': 'Charging Class'},
                      hover_data=['EV Model', 'Battery Type', 'Charging Mode'])
    
    if len(filtered_df) > 0:
        efficiency_df = filtered_df.groupby(['EV Model', 'Battery Type'])['Efficiency (%)'].mean().reset_index()
        fig2 = px.bar(efficiency_df, x='EV Model', y='Efficiency (%)', 
                      color='Battery Type',
                      title='Average Efficiency per EV Model',
                      barmode='group')
    else:
        fig2 = px.bar(title='Average Efficiency per EV Model')
    
    fig3 = px.pie(filtered_df, names='Optimal Charging Duration Class',
                  title='Optimal Charging Duration Class Distribution',
                  labels={'Optimal Charging Duration Class': 'Class'})
    
    fig4 = px.scatter(filtered_df, x='Charging Cycles', y='Degradation Rate (%)',
                      color='Optimal Charging Duration Class',
                      size='Efficiency (%)',
                      title='Battery Degradation vs Charging Cycles',
                      hover_data=['EV Model', 'SOC (%)'])
    
    return jsonify({
        "stats": stats,
        "fig1": json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder),
        "fig2": json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder),
        "fig3": json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder),
        "fig4": json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder),
        "has_data": len(filtered_df) > 0
    })

@app.route('/chatbot')
def chatbot_page():
    return render_template('chatbot.html')

@app.route('/api/chatbot', methods=['POST'])
def chat():
    """API endpoint for chatbot interactions"""
    try:
        data = request.get_json(force=True)
        user_message = data.get('message', '')
        payload = data.get('payload')

        response = chatbot.get_response(user_message, payload=payload)

        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'response': f'Sorry, I encountered an error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

