# ⚡ EVBot – EV Battery Intelligence Hub

A full-stack assistant that predicts optimal charging duration, visualizes fleet health, and answers EV battery questions with AI-powered context.

## 🚀 Highlights

- **Smart Predictions** – Random Forest classifier (99.5% accuracy) suggests short/medium/long charging strategies.
- **Interactive Dashboard** – Filterable analytics with always-on sample visualisations so charts never go blank.
- **Conversational Advisor** – Chatbot can blend ML predictions with curated EV guidance and optional read-aloud answers.
- **Responsive UI** – Gradient-driven theme, glassmorphism cards, and polished mobile experience.

## 🧰 Tech Stack

| Layer        | Tools |
|--------------|-------|
| Backend      | Flask, Python 3, scikit-learn, pandas, NumPy, joblib |
| Frontend     | HTML5, Jinja2, Bootstrap 5, Plotly.js, custom CSS |
| Chatbot APIs | OpenAI SDK, Hugging Face `InferenceClient`, python-dotenv |
| UX Extras    | Web Speech API (read-aloud), Plotly animations |
| Data         | CSV dataset (`data/ev_battery_charging_data.csv`), label encoders |

## 📦 Quick Start

### 1. Clone & enter the project
```bash
git clone https://github.com/nes268/EVBot.git
cd EVBot
```

### 2. Activate the virtual environment
```bash
# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 4. Train the model (first run only)
```bash
python train_model.py
```

### 5. Configure chatbot credentials (pick one provider)
**OpenAI**
```bash
# Windows (persist across sessions)
setx OPENAI_API_KEY "your_openai_key"
setx OPENAI_MODEL "gpt-4o-mini"   # optional override

# Current shell only
$env:OPENAI_API_KEY="your_openai_key"
```

**Hugging Face**
```bash
# Windows (persist across sessions)
setx HF_API_KEY "your_hf_key"
setx HF_MODEL "HuggingFaceH4/zephyr-7b-beta"   # optional override

# Current shell only
$env:HF_API_KEY="your_hf_key"
```
> Restart your terminal after using `setx`, or export in-session variables before launching the app.

### 6. Launch EVBot
```bash
# Windows
run_app.bat

# macOS / Linux
bash run_app.sh
```
Then open the browser at http://127.0.0.1:5000

## 🗂 Project Structure
```
EVBot/
├── app/
│   ├── app.py          # Flask entry-point & REST endpoints
│   ├── chatbot.py      # API clients + ML-assisted responses
│   └── ml_model.py     # Shared preprocessing & prediction helpers
├── data/
│   └── ev_battery_charging_data.csv
├── models/
│   ├── ev_model.pkl
│   └── label_encoders.pkl
├── static/
│   └── style.css
├── templates/
│   ├── index.html
│   ├── predict.html
│   ├── dashboard.html
│   └── chatbot.html
├── data_preprocessing.ipynb
├── requirements.txt
└── train_model.py
```

## 📊 Dataset & Model
- 1,000 charging sessions with 13 engineered features (SOC, temps, cycles, mode, etc.).
- Random Forest (200 estimators) classifies optimal charge window (short/medium/long).
- Encoders + model stored under `models/` for quick reuse.

## 🧭 Using EVBot

### Predict Charging Duration
1. Visit **Check Charge**.
2. Enter SOC, voltage, current, temperatures, cycles, and categorical meta-data.
3. Review instant recommendation plus colour-coded result card.

### Explore the Dashboard
- Filter by EV model, battery type, and charging mode.
- Stats animate sequentially; if filters remove all rows, sample trends keep charts informative.
- Plotly visuals: SOC vs Voltage, Efficiency by Model, Charging Class Mix, Degradation vs Cycles.

### Chat with EVBot
- Ask for guidance or toggle **Include EV parameters** to have the ML model inform the conversation.
- Optional **Read responses aloud** checkbox uses the browser’s speech synthesis.
- Supports OpenAI or Hugging Face API keys without code changes.

## 🤝 Contributing & Support
- Issues and pull requests are welcome — please open a ticket describing bugs, enhancements, or data questions.
- Feel free to fork the repo and submit PRs with improvements.

## 📄 License
Released under the MIT License.

## 👤 Author
**nes268**
