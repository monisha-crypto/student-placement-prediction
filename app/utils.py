import pandas as pd
import plotly.express as px
import os
from PIL import Image
from sklearn.preprocessing import MinMaxScaler

def load_data(base_dir):
    students_path = os.path.join(base_dir, "..", "data", "raw", "student_profile.xlsx")
    companies_path = os.path.join(base_dir, "..", "data", "raw", "companies_profile.xlsx")
    df_students = pd.read_excel(students_path)
    df_companies = pd.read_excel(companies_path)
    return df_students, df_companies

def get_student_photo(base_dir, photo_path):
    path = os.path.join(base_dir, "photos", photo_path)
    if os.path.exists(path):
        return Image.open(path)
    return None

def plot_student_metrics(student):
    metrics = ["cgpa", "aptitude_score", "coding_score",
               "placement_training_score", "communication_score", "soft_skill_score"]
    fig_bar = px.bar(
        x=["CGPA", "Aptitude", "Coding", "Training", "Communication", "Soft Skills"],
        y=[student[m] for m in metrics],
        title="Student Key Metrics",
        labels={"x": "Metrics", "y": "Score"}
    )
    fig_radar = px.line_polar(
        r=[student[m] for m in metrics],
        theta=["CGPA", "Aptitude", "Coding", "Training", "Communication", "Soft Skills"],
        line_close=True,
        title="Skill Radar"
    )
    return fig_bar, fig_radar
