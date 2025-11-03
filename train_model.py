import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# Load the cleaned dataset (same file you used)
df = pd.read_csv("data/ev_battery_charging_data.csv")

# Clean the data
df = df.dropna()
df = df.drop_duplicates()

print(f"Dataset shape: {df.shape}")

# Define features and target
X = df.drop("Optimal Charging Duration Class", axis=1)
y = df["Optimal Charging Duration Class"]

# Encode categorical variables
label_encoders = {}
categorical_cols = ['Charging Mode', 'Battery Type', 'EV Model']

for col in categorical_cols:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])
    label_encoders[col] = le
    print(f"Encoded {col}: {dict(zip(le.classes_, range(len(le.classes_))))}")

# Split into training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"\nTraining set: {X_train.shape[0]} samples")
print(f"Test set: {X_test.shape[0]} samples")

# Train model
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Evaluate
predictions = model.predict(X_test)
print("\n" + "="*60)
print("Model Evaluation")
print("="*60)
print(f"Accuracy: {accuracy_score(y_test, predictions):.4f}")
print("\nClassification Report:\n", classification_report(y_test, predictions))

# Create models directory if it doesn't exist
os.makedirs("models", exist_ok=True)

# Save the model
model_path = "models/ev_model.pkl"
joblib.dump(model, model_path)
print(f"\nModel saved as {model_path}")

# Also save the label encoders for later use
encoders_path = "models/label_encoders.pkl"
joblib.dump(label_encoders, encoders_path)
print(f"Label encoders saved as {encoders_path}")

print("\n[OK] Training completed successfully!")

