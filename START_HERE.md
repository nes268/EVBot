# 🚀 GET STARTED WITH EVBot

## Quick Start Guide

### ✅ Prerequisites Check

Your setup should already be complete! Let's verify:

1. ✅ Virtual environment (venv) - **READY**
2. ✅ Model trained - **READY** (99.5% accuracy)
3. ✅ Frontend created - **READY** (EV-themed UI)
4. ✅ All dependencies installed - **READY**

## 🎯 How to Run the App

### Method 1: Using Batch File (Easiest)
```bash
run_app.bat
```

### Method 2: Using Python Directly
```bash
.\venv\Scripts\activate
python app/app.py
```

### Method 3: Using Launcher Script (Linux/Mac)
```bash
bash run_app.sh
```

## 🌐 Access the Application

Once running, open your browser and go to:
```
http://127.0.0.1:5000
```

You should see the beautiful EV-themed interface!

## 🧪 Try a Sample Prediction

Use these sample values from the dataset:

- **SOC (%)**: 43.7
- **Voltage (V)**: 3.63
- **Current (A)**: 33.55
- **Battery Temp (°C)**: 33.45
- **Ambient Temp (°C)**: 26.44
- **Charging Duration (min)**: 59.36
- **Degradation Rate (%)**: 8.81
- **Charging Mode**: Fast
- **Efficiency (%)**: 98.24
- **Battery Type**: Li-ion
- **Charging Cycles**: 112
- **EV Model**: Model B

**Expected Result**: Medium Duration (Class 1) ⚡

## 🎨 What You'll See

1. **Dark gradient background** with electric particle effects
2. **Glass-morphism form** with smooth animations
3. **Color-coded results**:
   - 🟢 Green: Excellent battery health
   - 🟡 Yellow: Normal battery condition  
   - 🔴 Red: Battery needs attention

## 🔧 Troubleshooting

### "Model not loaded" error
```bash
# Retrain the model
python train_model.py
```

### Port 5000 already in use
```bash
# Kill existing process or change port in app/app.py
app.run(debug=True, port=5001)
```

### CSS not loading
```bash
# Clear browser cache (Ctrl+Shift+Delete)
# Or hard refresh (Ctrl+F5)
```

## 📊 Full System Status

| Component | Status | Notes |
|-----------|--------|-------|
| Model | ✅ Loaded | 99.5% accuracy |
| Encoders | ✅ Loaded | All 3 encoders ready |
| Frontend | ✅ Ready | EV-themed UI |
| Backend | ✅ Ready | Flask server |
| Data | ✅ Ready | 1000 samples |

## 🎓 What's Next?

Your EVBot is fully functional! You can:
1. Test with different values
2. Analyze the predictions
3. View the architecture diagram (ARCHITECTURE.md)
4. Read the full README (README.md)

## 💡 Pro Tips

- Use realistic EV battery values for best results
- Check the color-coded results for quick insights
- The interface is fully responsive (try mobile view!)
- All predictions are instant thanks to pre-trained ML model

---

**Ready to go?** Run `run_app.bat` and open http://127.0.0.1:5000! 🚗⚡

