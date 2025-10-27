"""
Simple Standalone QA Agent - Works without backend
For testing and demonstration purposes
"""
import streamlit as st
import os
import tempfile
import PyPDF2
import docx
from datetime import datetime
import json

# Configure page
st.set_page_config(
    page_title="🤖 Simple QA Agent",
    page_icon="🤖",
    layout="wide"
)

def extract_text_from_file(file):
    """Extract text from uploaded file"""
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.name)[1]) as tmp_file:
            tmp_file.write(file.getvalue())
            tmp_file_path = tmp_file.name
        
        # Extract text based on file type
        file_ext = os.path.splitext(file.name)[1].lower()
        
        if file_ext == '.pdf':
            text = extract_pdf_text(tmp_file_path)
        elif file_ext == '.txt':
            with open(tmp_file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        elif file_ext in ['.docx', '.doc']:
            text = extract_docx_text(tmp_file_path)
        else:
            text = "Unsupported file type"
        
        # Clean up
        os.unlink(tmp_file_path)
        return text
        
    except Exception as e:
        return f"Error processing file: {str(e)}"

def extract_pdf_text(file_path):
    """Extract text from PDF"""
    try:
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"PDF extraction error: {str(e)}"

def extract_docx_text(file_path):
    """Extract text from DOCX"""
    try:
        doc = docx.Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        return f"DOCX extraction error: {str(e)}"

def simple_search(text, query):
    """Simple text search"""
    if not text or not query:
        return []
    
    text_lower = text.lower()
    query_lower = query.lower()
    
    # Split text into sentences
    sentences = text.split('.')
    results = []
    
    for i, sentence in enumerate(sentences):
        if query_lower in sentence.lower():
            results.append({
                'sentence': sentence.strip(),
                'position': i,
                'relevance': sentence.lower().count(query_lower)
            })
    
    # Sort by relevance
    results.sort(key=lambda x: x['relevance'], reverse=True)
    return results[:5]  # Top 5 results

def main():
    """Main application"""
    st.title("🤖 Simple QA Agent")
    st.markdown("Upload documents and ask questions (Standalone version)")
    
    # Initialize session state
    if 'documents' not in st.session_state:
        st.session_state.documents = []
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Sidebar for file upload
    st.sidebar.header("📁 Upload Documents")
    
    uploaded_files = st.sidebar.file_uploader(
        "Choose files",
        type=['pdf', 'txt', 'docx'],
        accept_multiple_files=True,
        help="Upload PDF, TXT, or DOCX files"
    )
    
    # Process uploaded files
    if uploaded_files:
        for uploaded_file in uploaded_files:
            if uploaded_file.name not in [doc['name'] for doc in st.session_state.documents]:
                with st.spinner(f"Processing {uploaded_file.name}..."):
                    text = extract_text_from_file(uploaded_file)
                    
                    document = {
                        'name': uploaded_file.name,
                        'text': text,
                        'word_count': len(text.split()),
                        'uploaded_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    st.session_state.documents.append(document)
                    st.sidebar.success(f"✅ Added {uploaded_file.name}")
    
    # Display documents
    st.sidebar.header("📚 Your Documents")
    if st.session_state.documents:
        for i, doc in enumerate(st.session_state.documents):
            with st.sidebar.expander(f"📄 {doc['name']}"):
                st.write(f"**Words:** {doc['word_count']:,}")
                st.write(f"**Uploaded:** {doc['uploaded_at']}")
                if st.button("🗑️ Remove", key=f"remove_{i}"):
                    st.session_state.documents.pop(i)
                    st.rerun()
    else:
        st.sidebar.info("No documents uploaded yet")
    
    # Main chat interface
    st.header("💬 Ask Questions")
    
    # Display chat history
    for chat in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(chat['question'])
        
        with st.chat_message("assistant"):
            st.write(chat['answer'])
            if chat.get('sources'):
                with st.expander("📚 Sources"):
                    for source in chat['sources']:
                        st.write(f"**{source['document']}**")
                        st.write(source['text'])
    
    # Chat input
    question = st.chat_input("Ask a question about your documents...")
    
    if question:
        if not st.session_state.documents:
            st.error("Please upload some documents first!")
            return
        
        # Add to chat history
        st.session_state.chat_history.append({
            'question': question,
            'answer': '',
            'sources': []
        })
        
        # Display user message
        with st.chat_message("user"):
            st.write(question)
        
        # Process question
        with st.chat_message("assistant"):
            with st.spinner("Searching documents..."):
                # Simple search across all documents
                all_sources = []
                for doc in st.session_state.documents:
                    results = simple_search(doc['text'], question)
                    for result in results:
                        all_sources.append({
                            'document': doc['name'],
                            'text': result['sentence'],
                            'relevance': result['relevance']
                        })
                
                # Sort by relevance
                all_sources.sort(key=lambda x: x['relevance'], reverse=True)
                top_sources = all_sources[:3]
                
                if top_sources:
                    # Generate simple answer
                    answer_parts = []
                    answer_parts.append(f"Based on your documents, here's what I found about '{question}':")
                    answer_parts.append("")
                    
                    for i, source in enumerate(top_sources, 1):
                        answer_parts.append(f"{i}. From {source['document']}:")
                        answer_parts.append(f"   {source['text']}")
                        answer_parts.append("")
                    
                    answer = "\n".join(answer_parts)
                    
                    # Update chat history
                    st.session_state.chat_history[-1].update({
                        'answer': answer,
                        'sources': top_sources
                    })
                    
                    st.write(answer)
                    
                    # Show sources
                    with st.expander("📚 Sources"):
                        for source in top_sources:
                            st.write(f"**{source['document']}** (Relevance: {source['relevance']})")
                            st.write(source['text'])
                            st.write("---")
                else:
                    answer = f"I couldn't find specific information about '{question}' in your documents. Try rephrasing your question or upload more relevant documents."
                    st.session_state.chat_history[-1]['answer'] = answer
                    st.write(answer)
    
    # Statistics
    st.sidebar.header("📊 Statistics")
    st.sidebar.metric("Documents", len(st.session_state.documents))
    if st.session_state.documents:
        total_words = sum(doc['word_count'] for doc in st.session_state.documents)
        st.sidebar.metric("Total Words", f"{total_words:,}")
    
    # Clear chat button
    if st.sidebar.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

if __name__ == "__main__":
    main()