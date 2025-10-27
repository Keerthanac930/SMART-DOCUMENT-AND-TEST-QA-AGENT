"""
Floating Action Buttons Component
"""
import streamlit as st

def display_floating_buttons():
    """Display floating action buttons for Voice, Quiz, and Image"""
    st.markdown(
        """
        <div class="fab-container">
            <button class="fab-button" onclick="window.dispatchEvent(new CustomEvent('fab-voice'))">🎤 Voice</button>
            <button class="fab-button" onclick="window.location.href='quiz_page'">🧩 Quiz</button>
            <button class="fab-button" onclick="window.dispatchEvent(new CustomEvent('fab-image'))">📷 Image</button>
        </div>
        """,
        unsafe_allow_html=True,
    )












