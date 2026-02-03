# app.py
import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px
import os
import sys

sys.path.append(os.path.dirname(__file__))
from model import predict_probability, risk_category, explain_risk, FEATURES

# ================= Page Config =================
st.set_page_config(page_title="Student Placement Dashboard", layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ================= Load Data =================
students_path = os.path.join(BASE_DIR, "..", "data", "raw", "student_profile.xlsx")
companies_path = os.path.join(BASE_DIR, "..", "data", "raw", "companies_profile.xlsx")

df_students = pd.read_excel(students_path)
df_companies = pd.read_excel(companies_path)

# ================= FIXED CUSTOM CSS (IMPORTANT) =================
st.markdown("""
<style>

/* ===== APP BACKGROUND (FIXED) ===== */
.stApp {
    background: linear-gradient(to bottom right, #f0f4f8, #d9e2ec);
    font-family: 'Segoe UI', sans-serif;
}

/* ===== REMOVE STREAMLIT EXTRA SPACING ===== */
.block-container {
    padding-top: 0.8rem;
    padding-bottom: 0.8rem;
}

/* ===== MAIN TITLE ===== */
h1 {
    text-align: center;
    color: #0d3b66;
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 12px;
}

/* ===== CENTER SELECTBOX ===== */
.stSelectbox {
    display: flex;
    justify-content: center;
    margin-bottom: 15px;
}

/* ===== CARD UI ===== */
.card {
    background-color: #ffffff;
    padding: 15px;
    border-radius: 15px;
    border: 1px solid #d0d7de;
    box-shadow: 0 6px 20px rgba(0,0,0,0.12);
    margin-bottom: 10px;
    transition: transform 0.2s ease;
}

.card:hover {
    transform: translateY(-2px);
}

/* ===== PHOTO BORDER ===== */
img {
    border-radius: 15px;
    border: 2px solid #0d3b66;
}

/* ===== SMALL TEXT ===== */
.ai-summary p,
.risk-box p,
.company-box p {
    font-size: 13px;
    margin: 2px 0;
    color: #1f2933;
}

/* ===== PROGRESS BAR ===== */
.progress-bar {
    height: 20px;
    border-radius: 10px;
    background-color: #e0e0e0;
    margin-bottom: 10px;
}

.progress-fill {
    height: 100%;
    border-radius: 10px;
    font-weight: bold;
    color: white;
    padding-right: 6px;
}

/* ===== COMPANY HOVER ===== */
.company-box p {
    padding: 6px;
    border-radius: 8px;
    transition: background-color 0.2s ease, transform 0.2s ease;
}

.company-box p:hover {
    background-color: #f0f8ff;
    transform: translateX(5px);
}

/* ===== REMOVE COLUMN GAP ===== */
[data-testid="column"] > div {
    padding-left: 0px !important;
    padding-right: 0px !important;
}

</style>
""", unsafe_allow_html=True)

# ================= Title =================
st.markdown("<h1>🎓 Student Placement Prediction</h1>", unsafe_allow_html=True)

# ================= Student Selector =================
student_id = st.selectbox(
    "Select Student ID",
    df_students["student_id"],
    index=0,
    label_visibility="collapsed"
)

student = df_students[df_students["student_id"] == student_id].iloc[0]

# ================= Layout =================
col1, col2 = st.columns([1, 2], gap="small")

# ================= LEFT: STUDENT PROFILE =================
with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    photo_filename = os.path.basename(student["photo_path"])
    photo_path = os.path.join(BASE_DIR, "photos", photo_filename).replace("\\", "/")

    if os.path.exists(photo_path):
        img = Image.open(photo_path).resize((150, 190))
        st.image(img, caption=student["name"], width=150)
    else:
        st.error("❌ Photo not found")

    st.markdown(f"**Name:** {student['name']}")
    st.markdown(f"**Department:** {student['department']}")
    st.markdown(f"**Year:** {student['year']}")
    st.markdown(f"**CGPA:** {student['cgpa']}")
    st.markdown(f"**10th %:** {student['tenth_percent']}")
    st.markdown(f"**12th %:** {student['twelfth_percent']}")
    st.markdown(f"**Attendance:** {student['attendance']}%")
    st.markdown(f"**Aptitude:** {student['aptitude_score']}")
    st.markdown(f"**Coding:** {student['coding_score']}")
    st.markdown(f"**Training:** {student['placement_training_score']}")
    st.markdown(f"**Communication:** {student['communication_score']}")
    st.markdown(f"**Soft Skills:** {student['soft_skill_score']}")
    st.markdown(f"**Backlogs:** {student['backlogs']}")

    st.markdown("</div>", unsafe_allow_html=True)

# ================= RIGHT: AI PREDICTION =================
with col2:
    st.markdown("<div class='card ai-summary'>", unsafe_allow_html=True)
    st.subheader("🤖 AI Prediction Summary")

    student_features = [student[f] for f in FEATURES]
    placement_prob = predict_probability(student_features)
    risk = risk_category(placement_prob)

    color = "#27ae60" if placement_prob >= 80 else "#f1c40f" if placement_prob >= 60 else "#e74c3c"

    st.markdown(f"""
    <div class='progress-bar'>
        <div class='progress-fill' style='width:{placement_prob}%; background-color:{color};'>
            {placement_prob}%
        </div>
    </div>
    """, unsafe_allow_html=True)

    eligible = "✅ Eligible" if student["cgpa"] >= 6.5 and student["backlogs"] == 0 else "❌ Not Eligible"

    st.markdown(f"<p><b>Risk Category:</b> {risk}</p>", unsafe_allow_html=True)
    st.markdown(f"<p><b>Predicted Domain / Role:</b> {student['domain_interest']}</p>", unsafe_allow_html=True)
    st.markdown(f"<p><b>Placement Eligibility:</b> {eligible}</p>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ===== Risk Explanation =====
    st.markdown("<div class='card risk-box'>", unsafe_allow_html=True)
    st.markdown("<b>🔍 Reason for Risk Category & Improvement</b>", unsafe_allow_html=True)
    for f, v in explain_risk(student_features):
        st.markdown(f"<p>{f.replace('_',' ').title()} – Improve this skill</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ===== Visual Analytics =====
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📊 Visual Analytics")

    fig_bar = px.bar(
        x=[f.replace("_"," ").title() for f in FEATURES],
        y=student_features,
        title="Key Metrics"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    fig_radar = px.line_polar(
        r=student_features,
        theta=[f.replace("_"," ").title() for f in FEATURES],
        line_close=True,
        title="Skill Radar"
    )
    st.plotly_chart(fig_radar, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ===== Recommended Companies =====
    st.markdown("<div class='card company-box'>", unsafe_allow_html=True)
    st.subheader("🏢 Recommended Companies")

    eligible_companies = df_companies[
        (df_companies["min_cgpa"] <= student["cgpa"]) &
        (df_companies["required_domain"] == student["domain_interest"])
    ]

    if not eligible_companies.empty:
        for _, row in eligible_companies.iterrows():
            st.markdown(f"<p><b>{row['company_name']} – {row['role']}</b></p>", unsafe_allow_html=True)
            st.markdown(f"<p>📅 {row['interview_date']} | 🧑‍💻 {row['mode']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p><a href='{row['apply_link']}' target='_blank'>Apply Now</a></p>", unsafe_allow_html=True)
    else:
        st.info("No matching companies found")

    st.markdown("</div>", unsafe_allow_html=True)
