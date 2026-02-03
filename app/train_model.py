# train_model.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# ===== Load data =====
students_file = r"D:\student_placement_prediction\data\raw\student_profile.xlsx"
df = pd.read_excel(students_file)

# ===== Check the columns =====
print("Columns in Excel:", df.columns.tolist())

# ===== Features and target =====
features = ["cgpa","aptitude_score","coding_score",
            "placement_training_score","communication_score","soft_skill_score"]

# Make sure Excel has a column 'placed' with 1/0
target_column = "placed"  # 1 = placed, 0 = not placed

X = df[features]
y = df[target_column]

# ===== Split data =====
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ===== Train model =====
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# ===== Evaluate =====
preds = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, preds))

# ===== Save model =====
joblib.dump(model, r"D:\student_placement_prediction\app\placement_model.pkl")
print("Model saved as placement_model.pkl")
