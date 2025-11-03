# ⚡ EVBot - AI-Powered Electric Vehicle Maintenance Advisor

A smart web application that predicts optimal charging duration for electric vehicles using machine learning.

## 🌟 Features

- **AI-Powered Predictions**: Random Forest Classifier with 99.5% accuracy
- **Beautiful EV-Themed Interface**: Modern gradient design with smooth animations
- **Real-time Predictions**: Instant battery health recommendations
- **Three Charging Classes**: Short, Medium, and Long duration recommendations
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Virtual environment (venv)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/nes268/EVBot.git
   cd EVBot
   ```

2. **Activate virtual environment**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies** (if needed)
   ```bash
   pip install -r requirements.txt
   ```

4. **Train the model** (first time only)
   ```bash
   python train_model.py
   ```

5. **Run the application**
   ```bash
   # Windows
   run_app.bat
   
   # Linux/Mac
   bash run_app.sh
   ```

6. **Open your browser**
   ```
   http://127.0.0.1:5000
   ```

## 📊 Dataset

The model is trained on 1,000 EV battery charging records with 13 features:
- SOC (State of Charge)
- Voltage, Current, Temperatures
- Charging Duration and Cycles
- Degradation Rate
- Battery Type, EV Model, Charging Mode

## 🎨 Design Features

- **Dark gradient background** with animated electric particles
- **Glass-morphism cards** with backdrop blur
- **Electric glow effects** on hover
- **Color-coded results**: Green (Excellent), Yellow (Normal), Red (Attention)
- **Smooth animations** and transitions
- **Mobile-responsive** grid layout

## 📁 Project Structure

```
EVBot/
├── app/
│   ├── app.py              # Flask application
│   ├── chatbot.py          # Chatbot interface (coming soon)
│   └── ml_model.py         # Model utilities
├── data/
│   └── ev_battery_charging_data.csv
├── models/
│   ├── ev_model.pkl        # Trained model
│   └── label_encoders.pkl  # Feature encoders
├── static/
│   └── style.css           # EV-themed styling
├── templates/
│   └── index.html          # Main interface
├── data_preprocessing.ipynb
├── train_model.py
└── requirements.txt
```

## 🧪 Model Performance

- **Accuracy**: 99.5%
- **Algorithm**: Random Forest Classifier (200 trees)
- **Classes**:
  - Class 0: Short duration (20%)
  - Class 1: Medium duration (40%)
  - Class 2: Long duration (40%)

## 🔧 Technologies Used

- **Backend**: Flask, scikit-learn
- **Frontend**: HTML5, CSS3 (Gradient animations, Glass-morphism)
- **ML**: Random Forest, Pandas, NumPy
- **Data**: Label Encoding, Train-Test Split

## 📝 Usage

1. Fill in the battery parameters in the form
2. Click "Predict" to get instant recommendations
3. Receive color-coded results with maintenance advice

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests!

## 📄 License

MIT License

## 👨‍💻 Author

nes268
