"""
Working Document QA Agent - Simple and Reliable
"""
import streamlit as st
import os
import tempfile
from datetime import datetime
import json
import sys

# Page configuration
st.set_page_config(
    page_title="Working Document QA Agent",
    page_icon="📚",
    layout="wide"
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
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.25rem;
        color: #155724;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 0.25rem;
        color: #721c24;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'documents' not in st.session_state:
    st.session_state.documents = {}
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def extract_text_from_file(uploaded_file):
    """Extract text from uploaded file"""
    try:
        if uploaded_file.name.lower().endswith('.txt'):
            return str(uploaded_file.read(), "utf-8")
        
        elif uploaded_file.name.lower().endswith('.pdf'):
            try:
                import PyPDF2
                uploaded_file.seek(0)
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
            except Exception as e:
                return f"Error reading PDF: {str(e)}"
        
        elif uploaded_file.name.lower().endswith(('.docx', '.doc')):
            try:
                import docx
                uploaded_file.seek(0)
                doc = docx.Document(uploaded_file)
                text = ""
                for paragraph in doc.paragraphs:
                    text += paragraph.text + "\n"
                return text
            except Exception as e:
                return f"Error reading DOCX: {str(e)}"
        
        else:
            return f"Unsupported file type: {uploaded_file.name}"
            
    except Exception as e:
        return f"Error processing file: {str(e)}"

def search_in_documents(query, documents):
    """Search for query in documents"""
    results = []
    query_lower = query.lower()
    
    for doc_id, doc in documents.items():
        content_lower = doc['content'].lower()
        
        # Check if query is in content
        if query_lower in content_lower:
            # Find the position
            start = content_lower.find(query_lower)
            # Get context around the match
            context_start = max(0, start - 100)
            context_end = min(len(doc['content']), start + len(query) + 100)
            context = doc['content'][context_start:context_end]
            
            results.append({
                'document': doc['name'],
                'context': context,
                'relevance': 1.0
            })
    
    return results

def main():
    # Header
    st.markdown('<h1 class="main-header">📚 Working Document QA Agent</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Upload documents and search through their content</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("📁 Document Management")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Upload Document",
            type=['pdf', 'txt', 'docx', 'doc'],
            help="Upload a document to search through"
        )
        
        if uploaded_file is not None:
            if st.button("Add Document", key="add_doc"):
                # Extract text
                content = extract_text_from_file(uploaded_file)
                
                # Add to documents
                doc_id = f"doc_{len(st.session_state.documents)}"
                st.session_state.documents[doc_id] = {
                    'name': uploaded_file.name,
                    'content': content,
                    'word_count': len(content.split()),
                    'added_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                st.success(f"✅ Added {uploaded_file.name}")
                st.info(f"📊 Extracted {len(content.split())} words")
        
        # Show documents
        st.header("📋 Current Documents")
        if st.session_state.documents:
            for doc_id, doc in st.session_state.documents.items():
                with st.expander(f"📄 {doc['name']}"):
                    st.write(f"**Words:** {doc['word_count']}")
                    st.write(f"**Added:** {doc['added_at']}")
                    
                    if st.button("🗑️ Remove", key=f"remove_{doc_id}"):
                        del st.session_state.documents[doc_id]
                        st.rerun()
        else:
            st.info("No documents uploaded")
        
        # Statistics
        st.header("📊 Statistics")
        total_docs = len(st.session_state.documents)
        total_words = sum(doc['word_count'] for doc in st.session_state.documents.values())
        st.metric("Documents", total_docs)
        st.metric("Total Words", total_words)
    
    # Main content
    st.header("💬 Search Your Documents")
    
    if not st.session_state.documents:
        st.info("📝 Please upload a document first to start searching!")
        return
    
    # Show chat history
    for i, chat in enumerate(st.session_state.chat_history):
        with st.chat_message("user"):
            st.write(chat['question'])
        
        with st.chat_message("assistant"):
            st.write(chat['answer'])
            
            if chat.get('sources'):
                with st.expander("📚 Sources"):
                    for source in chat['sources']:
                        st.write(f"**{source['document']}**")
                        st.write(f"*{source['context']}*")
                        st.write("---")
    
    # Search input
    if query := st.chat_input("Search for something in your documents..."):
        # Add to chat history
        st.session_state.chat_history.append({
            'question': query,
            'answer': '',
            'sources': [],
            'timestamp': datetime.now().isoformat()
        })
        
        # Display user message
        with st.chat_message("user"):
            st.write(query)
        
        # Search for results
        with st.chat_message("assistant"):
            with st.spinner("🔍 Searching..."):
                results = search_in_documents(query, st.session_state.documents)
                
                if results:
                    answer = f"Found {len(results)} result(s) for '{query}':"
                    st.write(answer)
                    
                    # Update chat history
                    st.session_state.chat_history[-1].update({
                        'answer': answer,
                        'sources': results
                    })
                    
                    # Show sources
                    with st.expander("📚 Sources"):
                        for source in results:
                            st.write(f"**{source['document']}**")
                            st.write(f"*{source['context']}*")
                            st.write("---")
                else:
                    answer = f"No results found for '{query}'. Try different keywords."
                    st.write(answer)
                    
                    # Update chat history
                    st.session_state.chat_history[-1].update({
                        'answer': answer,
                        'sources': []
                    })
    
    # Controls
    with st.sidebar:
        st.header("⚙️ Controls")
        
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.success("Chat history cleared!")
            st.rerun()
        
        if st.button("💾 Export Chat History"):
            if st.session_state.chat_history:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"chat_history_{timestamp}.json"
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(st.session_state.chat_history, f, indent=2, ensure_ascii=False)
                
                st.success(f"✅ Exported to {filename}")
            else:
                st.warning("No chat history to export")

if __name__ == "__main__":
    main()

