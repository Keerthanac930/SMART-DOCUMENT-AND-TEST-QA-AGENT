"""
Smart Document QA Agent - Streamlit Web Interface
"""
import streamlit as st
import os
import tempfile
import logging
from typing import List, Dict, Any
from datetime import datetime
import json

# Import our modules
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from qa_engine import QAEngine
from config import APP_CONFIG, GOOGLE_AI_API_KEY

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title=APP_CONFIG["title"],
    page_icon=APP_CONFIG["icon"],
    layout=APP_CONFIG["layout"],
    initial_sidebar_state=APP_CONFIG["initial_sidebar_state"]
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-message {
        padding: 1rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.25rem;
        color: #155724;
        margin: 1rem 0;
    }
    .error-message {
        padding: 1rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 0.25rem;
        color: #721c24;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 0.25rem;
        color: #0c5460;
        margin: 1rem 0;
    }
    /* Floating action buttons */
    .fab-container {
        position: fixed;
        right: 24px;
        bottom: 24px;
        display: flex;
        flex-direction: column;
        gap: 12px;
        z-index: 9999;
    }
    .fab-button {
        background: linear-gradient(45deg, #4ECDC4, #1F77B4);
        color: #fff;
        border: none;
        border-radius: 28px;
        padding: 12px 16px;
        box-shadow: 0 6px 14px rgba(0,0,0,0.2);
        cursor: pointer;
    }
    .dark .fab-button { background: linear-gradient(45deg, #444, #111); }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'qa_engine' not in st.session_state:
        try:
            st.session_state.qa_engine = QAEngine(api_key=GOOGLE_AI_API_KEY)
            st.session_state.engine_initialized = True
        except Exception as e:
            st.session_state.engine_initialized = False
            st.session_state.engine_error = str(e)
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'current_documents' not in st.session_state:
        st.session_state.current_documents = []
    if 'role' not in st.session_state:
        st.session_state.role = None
    if 'theme' not in st.session_state:
        st.session_state.theme = 'Light'

def display_header():
    """Display the main header"""
    st.markdown('<h1 class="main-header">📚 Smart Document QA Agent</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Upload documents and ask questions to get intelligent answers based on your content</p>', unsafe_allow_html=True)
    
    # Quiz Mode button in top-right
    col1, col2, col3 = st.columns([2, 1, 1])
    with col3:
        if st.button("🧩 Quiz Mode", key="quiz_mode_btn", use_container_width=True):
            st.switch_page("pages/quiz_page.py")

    # Floating action buttons (Voice / Quiz / Image)
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

def sidebar_document_management():
    """Document management in sidebar"""
    st.sidebar.header("📁 Document Management")
    
    # Document upload
    uploaded_files = st.sidebar.file_uploader(
        "Upload Documents",
        type=['pdf', 'txt', 'docx', 'doc', 'jpg', 'jpeg', 'png'],
        accept_multiple_files=True,
        help="Upload PDF, TXT, DOCX, or images (JPG/PNG). Max 200MB per file."
    )
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            if st.sidebar.button(f"Add {uploaded_file.name}", key=f"add_{uploaded_file.name}"):
                add_document_to_knowledge_base(uploaded_file)
    
    # List current documents
    st.sidebar.subheader("📋 Current Documents")
    documents = st.session_state.qa_engine.list_documents()
    
    if documents:
        for doc in documents:
            with st.sidebar.expander(f"📄 {doc['file_name']}"):
                st.write(f"**Type:** {doc['file_type']}")
                st.write(f"**Size:** {doc['file_size']} bytes")
                st.write(f"**Words:** {doc['word_count']}")
                st.write(f"**Chunks:** {doc['chunk_count']}")
                st.write(f"**Added:** {doc['added_at'][:19]}")
                
                if st.button("🗑️ Remove", key=f"remove_{doc['document_id']}"):
                    remove_document_from_knowledge_base(doc['document_id'])
    else:
        st.sidebar.info("No documents uploaded yet")
    
    # Database statistics
    st.sidebar.subheader("📊 Database Statistics")
    stats = st.session_state.qa_engine.get_database_stats()
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric("Documents", stats['document_count'])
        st.metric("Total Chunks", stats['total_chunks'])
    
    with col2:
        st.metric("Total Words", f"{stats['total_words']:,}")
        st.metric("Size (MB)", stats['total_size_mb'])

def add_document_to_knowledge_base(uploaded_file):
    """Add uploaded document to knowledge base"""
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        
        # Add to knowledge base
        result = st.session_state.qa_engine.add_document(tmp_file_path)
        
        if result['success']:
            st.sidebar.success(f"✅ {result['message']}")
            # Refresh the page to update document list
            st.rerun()
        else:
            st.sidebar.error(f"❌ {result['message']}")
        
        # Clean up temporary file
        os.unlink(tmp_file_path)
        
    except Exception as e:
        st.sidebar.error(f"❌ Error adding document: {str(e)}")

def remove_document_from_knowledge_base(document_id):
    """Remove document from knowledge base"""
    try:
        result = st.session_state.qa_engine.remove_document(document_id)
        
        if result['success']:
            st.sidebar.success(f"✅ {result['message']}")
            st.rerun()
        else:
            st.sidebar.error(f"❌ {result['message']}")
            
    except Exception as e:
        st.sidebar.error(f"❌ Error removing document: {str(e)}")

def main_chat_interface():
    """Main chat interface"""
    st.header("💬 Ask Questions About Your Documents")
    
    # Check if we have documents
    documents = st.session_state.qa_engine.list_documents()
    if not documents:
        st.info("📝 Please upload some documents first to start asking questions!")
        return
    
    # Input mode selection
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
    
    # Display chat history
    for i, chat in enumerate(st.session_state.chat_history):
        with st.chat_message("user"):
            st.write(chat['question'])
        
        with st.chat_message("assistant"):
            st.write(chat['answer'])
            
            # Show sources if available
            if chat.get('sources'):
                with st.expander("📚 Sources"):
                    for source in chat['sources']:
                        page_info = f", Page {source.get('page_number')}" if source.get('page_number') else ""
                        st.write(f"**{source['document_name']}**{page_info} (Similarity: {source['similarity']:.3f})")
                        st.write(f"*{source['chunk_preview']}*")
                        st.write("---")
    
    # Process question if provided
    if question and question.strip():
        # Add user message to chat history
        st.session_state.chat_history.append({
            'question': question,
            'answer': '',
            'sources': [],
            'timestamp': datetime.now().isoformat()
        })
        
        # Display user message
        with st.chat_message("user"):
            st.write(question)
        
        # Get answer from QA engine
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                try:
                    result = st.session_state.qa_engine.ask_question(question)
                    
                    if result['success']:
                        st.write(result['answer'])
                        
                        # Update chat history with answer
                        st.session_state.chat_history[-1].update({
                            'answer': result['answer'],
                            'sources': result.get('sources', [])
                        })
                        
                        # Show sources
                        if result.get('sources'):
                            with st.expander("📚 Sources"):
                                for source in result['sources']:
                                    page_info = f", Page {source.get('page_number')}" if source.get('page_number') else ""
                                    st.write(f"**{source['document_name']}**{page_info} (Similarity: {source['similarity']:.3f})")
                                    st.write(f"*{source['chunk_preview']}*")
                                    st.write("---")
                    else:
                        st.error(f"❌ {result.get('message', 'Failed to get answer')}")
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

def sidebar_controls():
    """Additional controls in sidebar"""
    st.sidebar.header("⚙️ Controls")
    
    # Role selection (mock auth)
    st.sidebar.subheader("👤 Role")
    st.session_state.role = st.sidebar.selectbox("Select Role", [None, "admin", "student"], index=0)
    if st.session_state.role == "admin":
        st.sidebar.markdown("[Open Admin Dashboard](pages/admin.py)")
    elif st.session_state.role == "student":
        st.sidebar.markdown("[Open Student Dashboard](pages/student.py)")

    # Theme toggle
    st.sidebar.subheader("🌓 Theme")
    st.session_state.theme = st.sidebar.selectbox("Appearance", ["Light", "Dark"], index=0)

    # Apply theme class to body
    theme_class = 'dark' if st.session_state.theme == 'Dark' else 'light'
    st.markdown(f"<script>document.body.classList.add('{theme_class}');</script>", unsafe_allow_html=True)

    # Clear conversation history
    if st.sidebar.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.session_state.qa_engine.clear_conversation_history()
        st.sidebar.success("Chat history cleared!")
        st.rerun()
    
    # Export conversation history
    if st.sidebar.button("💾 Export Chat History"):
        if st.session_state.chat_history:
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"chat_history_{timestamp}.json"
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(st.session_state.chat_history, f, indent=2, ensure_ascii=False)
                
                st.sidebar.success(f"✅ Exported to {filename}")
            except Exception as e:
                st.sidebar.error(f"❌ Export failed: {str(e)}")
        else:
            st.sidebar.warning("No chat history to export")
    
    # System information
    st.sidebar.header("ℹ️ System Info")
    system_info = st.session_state.qa_engine.get_system_info()
    
    with st.sidebar.expander("View System Information"):
        st.json(system_info)

def main():
    """Main application"""
    # Initialize session state
    initialize_session_state()
    
    # Display header
    display_header()
    
    # Check if engine is initialized
    if not st.session_state.get('engine_initialized', False):
        st.error("❌ Failed to initialize QA Engine")
        st.error(f"Error: {st.session_state.get('engine_error', 'Unknown error')}")
        st.info("Please check your Google AI API key in the configuration.")
        return
    
    # Main layout
    col1, col2 = st.columns([3, 1])
    
    with col1:
        main_chat_interface()
    
    with col2:
        sidebar_document_management()
        sidebar_controls()

if __name__ == "__main__":
    main()

