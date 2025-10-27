"""
Student Dashboard Page
"""
import streamlit as st


def student_page():
    st.set_page_config(page_title="Student Dashboard", page_icon="👨‍🎓", layout="wide")

    st.title("👨‍🎓 Student Dashboard")
    st.write("Practice tests, registrations, exams, and results.")

    tabs = st.tabs([
        "Practice Tests",
        "Register for Exams",
        "My Exams",
        "Results",
    ])

    with tabs[0]:
        st.subheader("Practice Tests")
        st.info("AI-randomized questions from uploaded docs (to implement with DB)")

    with tabs[1]:
        st.subheader("Register for Exams")
        st.info("View eligible exams and request registration")

    with tabs[2]:
        st.subheader("My Exams")
        st.info("Take exams once approved by Admin")

    with tabs[3]:
        st.subheader("Results & Feedback")
        st.info("View scores and generated feedback")


if __name__ == "__main__":
    student_page()


