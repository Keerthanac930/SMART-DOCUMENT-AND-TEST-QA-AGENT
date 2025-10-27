#!/usr/bin/env python3
"""
Quick Start - Simple QA Agent
Works immediately without complex setup
"""
import streamlit as st
import PyPDF2
import docx
import tempfile
import os
from datetime import datetime

st.set_page_config(page_title="🤖 Quick QA Agent", page_icon="🤖", layout="wide")

# Initialize session state
if 'documents' not in st.session_state:
    st.session_state.documents = []
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def extract_text(file):
    """Extract text from file"""
    file_ext = os.path.splitext(file.name)[1].lower()
    
    if file_ext == '.pdf':
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            return f"PDF Error: {str(e)}"
    
    elif file_ext == '.txt':
        try:
            return file.read().decode('utf-8')
        except:
            return "Text file error"
    
    elif file_ext in ['.docx', '.doc']:
        try:
            doc = docx.Document(file)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            return f"DOCX Error: {str(e)}"
    
    else:
        return "Unsupported file type"

def search_documents(question):
    """Simple search in documents"""
    results = []
    for doc in st.session_state.documents:
        if question.lower() in doc['text'].lower():
            sentences = doc['text'].split('.')
            for sentence in sentences:
                if question.lower() in sentence.lower():
                    results.append({
                        'document': doc['name'],
                        'text': sentence.strip(),
                        'relevance': sentence.lower().count(question.lower())
                    })
    
    results.sort(key=lambda x: x['relevance'], reverse=True)
    return results[:3]

# Main Interface
st.title("🤖 Quick QA Agent")
st.markdown("Upload documents and ask questions - **Works immediately!**")

# Sidebar
st.sidebar.header("📁 Upload Documents")

uploaded_files = st.sidebar.file_uploader(
    "Choose files", 
    type=['pdf', 'txt', 'docx'], 
    accept_multiple_files=True
)

# Process uploads
if uploaded_files:
    for file in uploaded_files:
        if file.name not in [d['name'] for d in st.session_state.documents]:
            with st.spinner(f"Processing {file.name}..."):
                text = extract_text(file)
                doc = {
                    'name': file.name,
                    'text': text,
                    'word_count': len(text.split()),
                    'uploaded_at': datetime.now().strftime("%H:%M:%S")
                }
                st.session_state.documents.append(doc)
                st.sidebar.success(f"✅ Added {file.name}")

# Show documents
st.sidebar.header("📚 Documents")
if st.session_state.documents:
    for i, doc in enumerate(st.session_state.documents):
        with st.sidebar.expander(f"📄 {doc['name']}"):
            st.write(f"**Words:** {doc['word_count']:,}")
            st.write(f"**Time:** {doc['uploaded_at']}")
            if st.button("🗑️ Remove", key=f"rm_{i}"):
                st.session_state.documents.pop(i)
                st.rerun()
else:
    st.sidebar.info("No documents yet")

# Chat Interface
st.header("💬 Ask Questions")

# Show chat history
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
        st.error("Please upload documents first!")
        st.stop()
    
    # Add to history
    st.session_state.chat_history.append({
        'question': question,
        'answer': '',
        'sources': []
    })
    
    # Show user message
    with st.chat_message("user"):
        st.write(question)
    
    # Get answer
    with st.chat_message("assistant"):
        with st.spinner("Searching..."):
            results = search_documents(question)
            
            if results:
                answer = f"Found {len(results)} relevant sections about '{question}':\n\n"
                for i, result in enumerate(results, 1):
                    answer += f"{i}. From {result['document']}:\n{result['text']}\n\n"
            else:
                answer = f"Couldn't find information about '{question}'. Try different keywords."
            
            st.write(answer)
            
            # Update history
            st.session_state.chat_history[-1].update({
                'answer': answer,
                'sources': results
            })
            
            # Show sources
            if results:
                with st.expander("📚 Sources"):
                    for result in results:
                        st.write(f"**{result['document']}**")
                        st.write(result['text'])

# Stats
st.sidebar.header("📊 Stats")
st.sidebar.metric("Documents", len(st.session_state.documents))
if st.session_state.documents:
    total_words = sum(d['word_count'] for d in st.session_state.documents)
    st.sidebar.metric("Total Words", f"{total_words:,}")

# Clear button
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.chat_history = []
    st.rerun()

st.markdown("---")
st.markdown("🚀 **Quick QA Agent** - Upload documents and ask questions instantly!")
