"""
Reusable Header Component
"""
import streamlit as st

def display_header(title="📚 Smart Document QA Agent", subtitle="Upload documents and ask questions to get intelligent answers based on your content"):
    """Display the main header with optional title and subtitle"""
    st.markdown(f'<h1 class="main-header">{title}</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="sub-header">{subtitle}</p>', unsafe_allow_html=True)
    
    # Quiz Mode button in top-right
    col1, col2, col3 = st.columns([2, 1, 1])
    with col3:
        if st.button("🧩 Quiz Mode", key="quiz_mode_btn", use_container_width=True):
            st.switch_page("pages/quiz_page.py")












