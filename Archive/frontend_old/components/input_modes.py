"""
Input Modes Component (Manual, Voice, Image)
"""
import streamlit as st

def display_input_modes():
    """Display input mode selection and handling"""
    st.subheader("📝 Choose Input Method")
    input_mode = st.radio(
        "How would you like to ask your question?",
        ["🖋️ Manual Typing", "🎤 Voice Input", "📷 Image Scanner"],
        horizontal=True
    )
    
    question = ""
    
    if input_mode == "🖋️ Manual Typing":
        question = st.text_input("Type your question here:", placeholder="Ask a question about your documents...")
    
    elif input_mode == "🎤 Voice Input":
        st.markdown("**Voice Input** (Click to start recording)")
        if st.button("🎤 Start Recording", key="voice_record"):
            st.info("Voice recording would be implemented here using Web Speech API")
            # For demo purposes, show a text input
            question = st.text_input("Voice input (simulated):", placeholder="Your voice input will appear here...")
    
    elif input_mode == "📷 Image Scanner":
        st.markdown("**Image Scanner** (Upload an image with your question)")
        uploaded_image = st.file_uploader("Upload image with question", type=['jpg', 'jpeg', 'png'])
        if uploaded_image:
            st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
            st.info("OCR processing would extract text from this image")
            # For demo purposes, show a text input
            question = st.text_input("Extracted text (simulated):", placeholder="Text extracted from image will appear here...")
    
    return question












