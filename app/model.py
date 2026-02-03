# model.py
import os
import joblib
import pandas as pd

# ===== Correct path to model =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "placement_model.pkl")

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"❌ Model not found at {MODEL_PATH}")

# Load your trained placement model
model = joblib.load(MODEL_PATH)

# Features used for prediction
FEATURES = [
    "cgpa",
    "aptitude_score",
    "coding_score",
    "placement_training_score",
    "communication_score",
    "soft_skill_score"
]

def predict_probability(student_features):
    """
    Predict placement probability using the trained model.
    Input: list of 6 feature values
    Output: int percentage (0-100)
    """
    X = pd.DataFrame([student_features], columns=FEATURES)
    prob = model.predict_proba(X)[0][1] * 100  # probability of success
    return int(prob)

def risk_category(prob):
    """
    Determine risk category based on probability
    """
    if prob >= 80:
        return "🟢 Low Risk"
    elif prob >= 60:
        return "🟡 Medium Risk"
    else:
        return "🔴 High Risk"

def explain_risk(student_features):
    """
    Dummy explanation without SHAP
    Returns top 3 features with lowest values
    """
    features_low = sorted(zip(FEATURES, student_features), key=lambda x: x[1])
    return features_low[:3]  # top 3 lowest features
