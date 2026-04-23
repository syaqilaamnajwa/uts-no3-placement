import streamlit as st
import pandas as pd
import pickle

# page config
st.set_page_config(
    page_title="Student Career Prediction",
    layout="wide"
)


#load model
@st.cache_resource
def load_models():
    with open("best_model.pkl", "rb") as f:
        placement_model = pickle.load(f)

    with open("salary_model.pkl", "rb") as f:
        salary_model = pickle.load(f)

    return placement_model, salary_model


placement_model, salary_model = load_models()


#sidebar
st.sidebar.title("Menu")

prediction_mode = st.sidebar.selectbox(
    "Choose Prediction",
    ["Placement Prediction", "Salary Prediction"]
)

st.sidebar.markdown("---")
st.sidebar.write("Model Deployment Project")
st.sidebar.write("Using Streamlit + Pickle Model")


#title
st.title("Student Career Prediction")
st.write("Input student data below to get prediction results.")


#form input
with st.form("form"):

    col1, col2 = st.columns(2)

    with col1:
        cgpa = st.slider("CGPA", 0.0, 10.0, 7.0)
        coding = st.slider("Coding Skill", 1, 10, 7)
        communication = st.slider("Communication Skill", 1, 10, 7)
        aptitude = st.slider("Aptitude Skill", 1, 10, 7)
        internships = st.slider("Internships", 0, 5, 1)
        projects = st.slider("Projects", 0, 10, 2)

    with col2:
        tenth = st.slider("10th Percentage", 0, 100, 75)
        twelfth = st.slider("12th Percentage", 0, 100, 75)
        attendance = st.slider("Attendance", 0, 100, 85)
        study_hours = st.slider("Study Hours", 0, 12, 4)
        sleep_hours = st.slider("Sleep Hours", 0, 12, 7)
        stress = st.slider("Stress Level", 1, 10, 5)

    submit = st.form_submit_button("Predict")


#prediction
if submit:

    input_data = pd.DataFrame([{
        "Student_ID": 1001,
        "gender": "Male",
        "branch": "CSE",
        "cgpa": cgpa,
        "tenth_percentage": tenth,
        "twelfth_percentage": twelfth,
        "backlogs": 0,
        "study_hours_per_day": study_hours,
        "attendance_percentage": attendance,
        "projects_completed": projects,
        "internships_completed": internships,
        "coding_skill_rating": coding,
        "communication_skill_rating": communication,
        "aptitude_skill_rating": aptitude,
        "hackathons_participated": 0,
        "certifications_count": 1,
        "sleep_hours": sleep_hours,
        "stress_level": stress,
        "part_time_job": "No",
        "family_income_level": "Medium",
        "city_tier": 1,
        "internet_access": "Yes",
        "extracurricular_involvement": None
    }])

    #simple chart
    st.subheader("Skill Summary")

    chart = pd.DataFrame({
        "Skill": ["Coding", "Communication", "Aptitude"],
        "Score": [coding, communication, aptitude]
    })

    st.bar_chart(chart.set_index("Skill"))

    st.subheader("Prediction Result")

    # predict placement first
    placement = placement_model.predict(input_data)[0]

    #placement mode
    if prediction_mode == "Placement Prediction":

        if str(placement).lower() == "placed":
            st.success("Placed")
        else:
            st.error("Not Placed")

    #salary mode
    else:

        if str(placement).lower() != "placed":

            st.error("Not Placed")
            st.warning("Estimated Salary: 0 LPA")

            st.metric(
                "Predicted Salary",
                "0 LPA"
            )

        else:

            salary = salary_model.predict(input_data)[0]

            st.success("Placed")
            st.success(f"Estimated Salary: {round(salary,2)} LPA")

            st.metric(
                "Predicted Salary",
                f"{round(salary,2)} LPA"
            )