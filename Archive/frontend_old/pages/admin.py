"""
Admin Dashboard Page
"""
import streamlit as st


def admin_page():
    st.set_page_config(page_title="Admin Dashboard", page_icon="👨‍💼", layout="wide")

    st.title("👨‍💼 Admin Dashboard")
    st.write("Manage students, exams, approvals, and results.")

    tabs = st.tabs([
        "Users",
        "Question Papers",
        "Registrations",
        "Schedule Exams",
        "Results & Analytics",
    ])

    with tabs[0]:
        st.subheader("User Management")
        st.info("List/add/remove users here (connect to DB in next step)")

    with tabs[1]:
        st.subheader("Question Papers")
        st.file_uploader("Upload question paper", type=["pdf", "docx", "txt"], accept_multiple_files=False)

    with tabs[2]:
        st.subheader("Approve Registrations")
        st.info("Approve/deny exam registrations")

    with tabs[3]:
        st.subheader("Create & Schedule Exams")
        st.date_input("Exam Date")
        st.time_input("Exam Time")
        st.text_input("Exam Title")
        st.button("Create Exam")

    with tabs[4]:
        st.subheader("Results & Analytics")
        st.info("View results and performance analytics")


if __name__ == "__main__":
    admin_page()


