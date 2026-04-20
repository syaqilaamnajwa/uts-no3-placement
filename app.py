import streamlit as st
import pandas as pd
import pickle


# Load Model
with open("best_model.pkl", "rb") as file:
    model = pickle.load(file)


# Page Config
st.set_page_config(
    page_title="Placement Prediction",
    layout="wide"
)


# Sidebar
st.sidebar.title("Navigation")
st.sidebar.success("Model Loaded Successfully")
st.sidebar.info("MID Exam - No.3")


# Main Title
st.title("Student Placement Prediction")
st.caption("Monolithic Deployment using Streamlit")
st.write("Fill in the student data below, then click Predict.")


# Form Input
with st.form("predict_form"):
    col1, col2 = st.columns(2)
    with col1:
        cgpa = st.slider("CGPA", 0.0, 10.0, 7.0)

        tenth = st.slider(
            "10th Percentage",
            0.0, 100.0, 75.0
        )

        twelfth = st.slider(
            "12th Percentage",
            0.0, 100.0, 75.0
        )

        attendance = st.slider(
            "Attendance Percentage",
            0.0, 100.0, 80.0
        )

        internships = st.number_input(
            "Internships Completed",
            0, 10, 1
        )

        projects = st.number_input(
            "Projects Completed",
            0, 10, 2
        )

        cert = st.number_input(
            "Certifications Count",
            0, 10, 1
        )

        hackathon = st.number_input(
            "Hackathons Participated",
            0, 10, 0
        )

    with col2:
        coding = st.slider(
            "Coding Skill",
            1, 10, 7
        )

        communication = st.slider(
            "Communication Skill",
            1, 10, 7
        )

        aptitude = st.slider(
            "Aptitude Skill",
            1, 10, 7
        )

        backlogs = st.number_input(
            "Backlogs",
            0, 10, 0
        )

        study = st.slider(
            "Study Hours Per Day",
            0.0, 12.0, 4.0
        )

        sleep = st.slider(
            "Sleep Hours",
            0.0, 12.0, 7.0
        )

        stress = st.slider(
            "Stress Level",
            1, 10, 5
        )

        gender = st.selectbox(
            "Gender",
            ["Male", "Female"]
        )

        branch = st.selectbox(
            "Branch",
            ["CSE", "ECE", "ME", "CE"]
        )

        city = st.selectbox(
            "City Tier",
            [1, 2, 3]
        )

        income = st.selectbox(
            "Family Income Level",
            ["Low", "Medium", "High"]
        )

        internet = st.selectbox(
            "Internet Access",
            ["Yes", "No"]
        )

        job = st.selectbox(
            "Part Time Job",
            ["Yes", "No"]
        )

        extra = st.selectbox(
            "Extracurricular Involvement",
            ["Low", "Medium", "High"]
        )

    submit = st.form_submit_button("Predict")


# Visualization
st.subheader("Skill Visualization")
chart = pd.DataFrame(
    {
        "Score": [
            coding,
            communication,
            aptitude
        ]
    },
    index=[
        "Coding",
        "Communication",
        "Aptitude"
    ]
)
st.bar_chart(chart)


# Prediction
if submit:
    total_skills = coding + communication + aptitude
    data = pd.DataFrame([{
        "cgpa": cgpa,
        "tenth_percentage": tenth,
        "twelfth_percentage": twelfth,
        "attendance_percentage": attendance,
        "internships_completed": internships,
        "projects_completed": projects,
        "certifications_count": cert,
        "hackathons_participated": hackathon,
        "coding_skill_rating": coding,
        "communication_skill_rating": communication,
        "aptitude_skill_rating": aptitude,
        "backlogs": backlogs,
        "study_hours_per_day": study,
        "sleep_hours": sleep,
        "stress_level": stress,
        "gender": gender,
        "branch": branch,
        "city_tier": city,
        "family_income_level": income,
        "internet_access": internet,
        "part_time_job": job,
        "extracurricular_involvement": extra,
        "total_skills": total_skills
    }])

    result = model.predict(data)[0]

    st.divider()
    st.subheader("Prediction Result")

    if result == "Placed":
        st.success("Placed")
    else:
        st.error("Not Placed")