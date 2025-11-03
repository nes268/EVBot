# 🏗️ EVBot Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  Browser (http://127.0.0.1:5000)                          │ │
│  │  ├─ HTML Form (templates/index.html)                       │ │
│  │  ├─ EV-Themed CSS (static/style.css)                       │ │
│  │  └─ Gradient Animations + Glass-morphism                   │ │
│  └───────────────────────────────────────────────────────────┘ │
└───────────────────────────┬─────────────────────────────────────┘
                            │ HTTP POST /predict
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FLASK WEB SERVER                           │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  app/app.py                                                │ │
│  │  ├─ Route: / (Home page)                                   │ │
│  │  ├─ Route: /predict (ML Prediction)                        │ │
│  │  └─ Request Processing                                      │ │
│  └───────────────────────────────────────────────────────────┘ │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                    ┌───────┴────────┬─────────────┐
                    ▼                ▼             ▼
            ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
            │  Preprocess  │  │  Encode      │  │  Predict     │
            │  Features    │→ │  Categorical │→ │  with ML     │
            │              │  │  Variables   │  │  Model       │
            └──────────────┘  └──────────────┘  └──────────────┘
                                                    │
                                                    ▼
                            ┌──────────────────────────────────┐
                            │   models/ev_model.pkl             │
                            │   RandomForest Classifier         │
                            │   (200 trees, 99.5% accuracy)     │
                            └───────────────┬──────────────────┘
                                            │
                                            ▼
                            ┌──────────────────────────────────┐
                            │   Result Classes:                 │
                            │   • Class 0: Short ⚡ (Green)     │
                            │   • Class 1: Medium ⚡ (Yellow)   │
                            │   • Class 2: Long ⚠️ (Red)        │
                            └───────────────┬──────────────────┘
                                            │
                                            ▼
                            ┌──────────────────────────────────┐
                            │   Display in UI with              │
                            │   Color-coded Styling             │
                            └──────────────────────────────────┘
```

## Component Details

### 1. Frontend (templates/index.html + static/style.css)
- **Purpose**: User interface for EV battery health analysis
- **Features**:
  - 12 input fields for battery parameters
  - EV-themed gradient design
  - Animated background particles
  - Glass-morphism cards
  - Responsive layout

### 2. Backend (app/app.py)
- **Framework**: Flask
- **Routes**:
  - `GET /`: Renders the main form
  - `POST /predict`: Processes form data and returns prediction
- **Responsibilities**:
  - Load model and encoders on startup
  - Validate and process user input
  - Coordinate data flow between model and UI

### 3. Machine Learning Pipeline

#### Training (train_model.py)
1. Load dataset (1000 samples, 13 features)
2. Clean data (remove nulls, duplicates)
3. Encode categorical variables:
   - Charging Mode: Fast(0), Normal(1), Slow(2)
   - Battery Type: Li-ion(0), LiFePO4(1)
   - EV Model: Model A(0), Model B(1), Model C(2)
4. Train-test split (80/20)
5. Train RandomForestClassifier
6. Save model and encoders

#### Inference (app/app.py)
1. Receive user input from form
2. Create DataFrame with feature names
3. Apply label encoders to categorical features
4. Predict optimal charging duration class
5. Map prediction to user-friendly message
6. Return result with color coding

### 4. Data Flow

```
User Input
    ↓
Form Submission (12 parameters)
    ↓
DataFrame Creation (correct feature order)
    ↓
Label Encoding (categorical → numeric)
    ↓
Model Prediction (RandomForest)
    ↓
Class Mapping (0/1/2 → Message + Color)
    ↓
Display Result (Styled UI)
```

### 5. Dependencies

- **Flask**: Web framework
- **Pandas**: Data manipulation
- **scikit-learn**: ML algorithms and preprocessing
- **Joblib**: Model serialization
- **NumPy**: Numerical operations

## File Structure

```
EVBot/
├── app/
│   └── app.py                 # Flask application entry point
├── templates/
│   └── index.html             # Main UI
├── static/
│   └── style.css              # EV-themed styling
├── models/
│   ├── ev_model.pkl           # Trained RandomForest model
│   └── label_encoders.pkl     # Categorical encoders
├── data/
│   └── ev_battery_charging_data.csv  # Training dataset
├── train_model.py             # Model training script
└── data_preprocessing.ipynb   # EDA and preprocessing

```

## Success Criteria ✅

- ✅ Model loads successfully
- ✅ Encoders applied correctly
- ✅ HTML form renders properly
- ✅ CSS styling applied
- ✅ Predictions work end-to-end
- ✅ Color-coded results displayed
- ✅ 99.5% model accuracy
- ✅ Responsive design
- ✅ Error handling implemented

## Next Steps (Future Enhancements)

- [ ] Add chatbot integration (app/chatbot.py)
- [ ] Real-time battery health monitoring
- [ ] Historical data visualization
- [ ] User authentication
- [ ] Multi-language support
- [ ] Mobile app version

