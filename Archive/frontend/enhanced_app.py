"""
Enhanced Smart Document QA Agent - Streamlit Web Interface
Supports images, voice, Google Drive, and mobile
"""
import streamlit as st
import requests
import json
import io
import base64
from datetime import datetime
import time

# Configure page
st.set_page_config(
    page_title="🤖 Enhanced QA Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API base URL - try different ports and add fallback
API_BASE = "http://localhost:5000/api"
FALLBACK_API_BASE = "http://127.0.0.1:5000/api"

def get_api_base():
    """Get working API base URL"""
    import requests
    try:
        response = requests.get(f"{API_BASE}/health", timeout=2)
        if response.status_code == 200:
            return API_BASE
    except:
        pass
    
    try:
        response = requests.get(f"{FALLBACK_API_BASE}/health", timeout=2)
        if response.status_code == 200:
            return FALLBACK_API_BASE
    except:
        pass
    
    return None

# Custom CSS for mobile support
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .feature-card {
        padding: 1rem;
        border: 1px solid #ddd;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        background: #f9f9f9;
    }
    .mobile-friendly {
        font-size: 1.1rem;
        line-height: 1.5;
    }
    @media (max-width: 768px) {
        .main-header { font-size: 1.5rem; }
        .mobile-friendly { font-size: 1rem; }
    }
</style>
""", unsafe_allow_html=True)

def init_session_state():
    """Initialize session state"""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'documents' not in st.session_state:
        st.session_state.documents = []
    if 'voice_enabled' not in st.session_state:
        st.session_state.voice_enabled = False

def make_api_request(endpoint, method='GET', data=None, files=None):
    """Make API request with proper error handling"""
    api_base = get_api_base()
    if not api_base:
        return {
            'success': False, 
            'error': 'Backend API not available. Please start the backend server.',
            'message': 'Run: python backend/enhanced_api.py'
        }
    
    try:
        url = f"{api_base}{endpoint}"
        headers = {'Content-Type': 'application/json'} if data and not files else {}
        
        if method == 'GET':
            response = requests.get(url, headers=headers, timeout=10)
        elif method == 'POST':
            if files:
                response = requests.post(url, data=data, files=files, timeout=30)
            else:
                response = requests.post(url, json=data, headers=headers, timeout=10)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers, timeout=10)
        
        # Handle response
        if response.status_code == 200:
            return response.json() if response.headers.get('content-type', '').startswith('application/json') else {'success': True, 'data': response.text}
        else:
            return {
                'success': False, 
                'error': f'HTTP {response.status_code}',
                'message': response.text if response.text else 'Unknown error'
            }
            
    except requests.exceptions.ConnectionError:
        return {
            'success': False, 
            'error': 'Connection failed',
            'message': 'Cannot connect to backend API. Please ensure the backend server is running.'
        }
    except requests.exceptions.Timeout:
        return {
            'success': False, 
            'error': 'Request timeout',
            'message': 'The request took too long. Please try again.'
        }
    except Exception as e:
        return {
            'success': False, 
            'error': str(e),
            'message': f'Unexpected error: {str(e)}'
        }

def display_header():
    """Display header with connection status"""
    st.markdown('<h1 class="main-header">🤖 Enhanced QA Agent</h1>', unsafe_allow_html=True)
    st.markdown('<p class="mobile-friendly">Upload documents, images, voice notes, or connect Google Drive</p>', unsafe_allow_html=True)
    
    # Show connection status
    api_base = get_api_base()
    if api_base:
        st.success(f"✅ Connected to backend at {api_base}")
    else:
        st.error("❌ Backend not connected. Please start the backend server.")
        st.info("To start backend: `python backend/enhanced_api.py`")
        st.stop()

def sidebar_upload():
    """File upload sidebar"""
    st.sidebar.header("📁 Upload Files")
    
    # File uploader
    uploaded_files = st.sidebar.file_uploader(
        "Choose files",
        type=['pdf', 'txt', 'docx', 'doc', 'xlsx', 'xls', 'pptx', 'ppt', 'csv',
              'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp',
              'mp3', 'wav', 'm4a', 'aac', 'ogg', 'flac'],
        accept_multiple_files=True,
        help="Upload documents, images, or audio files"
    )
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            if st.sidebar.button(f"Add {uploaded_file.name}", key=f"add_{uploaded_file.name}"):
                add_document(uploaded_file)
    
    # Voice note recording
    st.sidebar.subheader("🎤 Voice Note")
    if st.sidebar.button("Record Voice Note"):
        st.sidebar.info("Voice recording feature - use mobile device for best experience")

def add_document(uploaded_file):
    """Add document to knowledge base"""
    with st.spinner(f"Adding {uploaded_file.name}..."):
        files = {'file': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        result = make_api_request('/documents', 'POST', files=files)
        
        if result.get('success'):
            st.sidebar.success(f"✅ Added {uploaded_file.name}")
            st.rerun()
        else:
            st.sidebar.error(f"❌ {result.get('error', 'Failed to add document')}")

def google_drive_section():
    """Google Drive integration section"""
    st.sidebar.header("☁️ Google Drive")
    
    if st.sidebar.button("Connect Google Drive"):
        result = make_api_request('/google-drive/authenticate', 'POST')
        if result.get('success'):
            st.sidebar.success("✅ Connected to Google Drive")
        else:
            st.sidebar.error("❌ Failed to connect")
    
    if st.sidebar.button("List Drive Files"):
        result = make_api_request('/google-drive/files')
        if result.get('success'):
            files = result.get('files', [])
            st.sidebar.write(f"Found {len(files)} files")
            for file_info in files[:5]:  # Show first 5
                if st.sidebar.button(f"📄 {file_info['name']}", key=f"drive_{file_info['id']}"):
                    add_drive_file(file_info['id'])

def add_drive_file(file_id):
    """Add Google Drive file to knowledge base"""
    with st.spinner("Adding Drive file..."):
        result = make_api_request(f'/google-drive/download/{file_id}')
        if result.get('success'):
            st.sidebar.success("✅ Added Drive file")
        else:
            st.sidebar.error("❌ Failed to add Drive file")

def chat_interface():
    """Main chat interface"""
    st.header("💬 Chat with Your Documents")
    
    # Display chat history
    for i, chat in enumerate(st.session_state.chat_history):
        with st.chat_message("user"):
            st.write(chat['question'])
        
        with st.chat_message("assistant"):
            st.write(chat['answer'])
            if chat.get('sources'):
                with st.expander("📚 Sources"):
                    for source in chat['sources']:
                        st.write(f"**{source['document_name']}**")
    
    # Chat input
    col1, col2 = st.columns([4, 1])
    with col1:
        question = st.chat_input("Ask a question about your documents...")
    with col2:
        voice_response = st.checkbox("🎤 Voice Response", help="Include voice response")
    
    if question:
        # Add to chat history
        st.session_state.chat_history.append({
            'question': question,
            'answer': '',
            'sources': []
        })
        
        # Display user message
        with st.chat_message("user"):
            st.write(question)
        
        # Get answer
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                data = {
                    'question': question,
                    'include_voice_response': voice_response
                }
                result = make_api_request('/ask', 'POST', data=data)
                
                if result.get('success'):
                    answer = result.get('answer', '')
                    st.write(answer)
                    
                    # Update chat history
                    st.session_state.chat_history[-1].update({
                        'answer': answer,
                        'sources': result.get('sources', [])
                    })
                    
                    # Show sources
                    if result.get('sources'):
                        with st.expander("📚 Sources"):
                            for source in result['sources']:
                                st.write(f"**{source['document_name']}**")
                                st.write(source['chunk_preview'])
                else:
                    st.error(f"❌ {result.get('error', 'Failed to get answer')}")

def documents_section():
    """Documents management section"""
    st.header("📚 Your Documents")
    
    # Get documents
    result = make_api_request('/documents')
    if result.get('success'):
        documents = result.get('documents', [])
        
        if documents:
            for doc in documents:
                with st.expander(f"📄 {doc['file_name']}"):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**Type:** {doc['file_type']}")
                        st.write(f"**Size:** {doc.get('file_size', 0):,} bytes")
                        st.write(f"**Words:** {doc.get('word_count', 0):,}")
                    with col2:
                        if st.button("🗑️ Remove", key=f"remove_{doc['document_id']}"):
                            remove_document(doc['document_id'])
        else:
            st.info("No documents uploaded yet")
    else:
        st.error("Failed to load documents")

def remove_document(doc_id):
    """Remove document"""
    result = make_api_request(f'/documents/{doc_id}', 'DELETE')
    if result.get('success'):
        st.success("✅ Document removed")
        st.rerun()
    else:
        st.error("❌ Failed to remove document")

def stats_section():
    """Statistics section"""
    st.sidebar.header("📊 Statistics")
    
    result = make_api_request('/stats')
    if result.get('success'):
        stats = result.get('stats', {})
        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.metric("Documents", stats.get('document_count', 0))
            st.metric("Chunks", stats.get('total_chunks', 0))
        with col2:
            st.metric("Words", f"{stats.get('total_words', 0):,}")
            st.metric("Size (MB)", stats.get('total_size_mb', 0))

def capabilities_section():
    """System capabilities section"""
    st.sidebar.header("🔧 Capabilities")
    
    result = make_api_request('/capabilities')
    if result.get('success'):
        caps = result.get('capabilities', {})
        
        with st.sidebar.expander("System Info"):
            st.write(f"**Image Processing:** {'✅' if caps.get('document_processing', {}).get('image_processing') else '❌'}")
            st.write(f"**Voice Chat:** {'✅' if caps.get('voice_processing', {}).get('voice_chat_enabled') else '❌'}")
            st.write(f"**Google Drive:** {'✅' if caps.get('google_drive', {}).get('authenticated') else '❌'}")
            st.write(f"**Mobile Support:** {'✅' if caps.get('features', {}).get('mobile_support') else '❌'}")

def main():
    """Main application"""
    init_session_state()
    display_header()
    
    # Sidebar
    sidebar_upload()
    google_drive_section()
    stats_section()
    capabilities_section()
    
    # Main content
    tab1, tab2 = st.tabs(["💬 Chat", "📚 Documents"])
    
    with tab1:
        chat_interface()
    
    with tab2:
        documents_section()
    
    # Footer
    st.markdown("---")
    st.markdown("🤖 Enhanced QA Agent - Supports images, voice, Google Drive, and mobile devices")

if __name__ == "__main__":
    main()
