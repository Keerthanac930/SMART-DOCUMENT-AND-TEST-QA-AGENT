#!/usr/bin/env python3
"""
Enhanced Quick Start - QA Agent with Google Gemini AI
Uses your provided API key for intelligent answers
"""
import streamlit as st
import PyPDF2
import docx
import tempfile
import os
import re
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv
import speech_recognition as sr
import pyttsx3
import threading
import queue
import time
import numpy as np
from PIL import Image
import base64

# Load environment variables
load_dotenv('config.env')

# Configure Gemini AI
GEMINI_API_KEY = "AIzaSyClBuvh8RkUgaHIKssBVBwrvF9j4iv6-H0"
genai.configure(api_key=GEMINI_API_KEY)

st.set_page_config(page_title="🤖 Enhanced QA Agent", page_icon="🤖", layout="wide")

# Initialize session state
if 'documents' not in st.session_state:
    st.session_state.documents = []
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'ai_enabled' not in st.session_state:
    st.session_state.ai_enabled = True
if 'quota_mode' not in st.session_state:
    st.session_state.quota_mode = False

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
    """Search documents for relevant content"""
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
    return results[:5]

def generate_ai_answer(question, relevant_content):
    """Generate AI answer using Google Gemini with quota handling"""
    try:
        # Get available models
        models = genai.list_models()
        available_models = [m.name for m in models if 'generateContent' in m.supported_generation_methods]
        
        if not available_models:
            return "No AI models available"
        
        # Use a lightweight model to reduce quota usage
        model_name = "gemini-2.0-flash-lite"  # Use a lighter model
        if model_name not in [m.split('/')[-1] for m in available_models]:
            model_name = available_models[0].split('/')[-1]  # Fallback to first available
        
        model = genai.GenerativeModel(model_name)
        
        # Prepare context - limit content to reduce token usage
        all_documents = []
        for doc in st.session_state.documents:
            # Limit to first 500 characters per document to save tokens
            content = doc['text'][:500]
            all_documents.append(f"Document: {doc['name']}\nContent: {content}...")
        
        context = "\n\n".join(all_documents)
        
        # Shorter, more efficient prompt
        prompt = f"""Answer this question based on the documents:

Documents:
{context}

Question: {question}

Answer briefly and cite the source document:"""
        
        response = model.generate_content(prompt)
        return response.text.strip()
        
    except Exception as e:
        if "quota" in str(e).lower() or "429" in str(e):
            return "AI quota exceeded. Here's what I found using smart search:"
        else:
            st.error(f"AI Error: {str(e)}")
            return "AI temporarily unavailable. Here's what I found using simple search:"

def generate_ai_insights(question, relevant_content):
    """Generate AI insights based on document content and question"""
    try:
        models = genai.list_models()
        available_models = [m.name for m in models if 'generateContent' in m.supported_generation_methods]
        
        if not available_models:
            return None
        
        model_name = "gemini-2.0-flash-lite"
        if model_name not in [m.split('/')[-1] for m in available_models]:
            model_name = available_models[0].split('/')[-1]
        
        model = genai.GenerativeModel(model_name)
        
        # Prepare document context
        doc_context = ""
        if relevant_content:
            doc_context = "Document excerpts:\n"
            for result in relevant_content[:3]:  # Limit to top 3
                doc_context += f"From {result['document']}: {result['text'][:200]}...\n"
        
        prompt = f"""Based on the following document content and question, provide additional insights and analysis:

{doc_context}

Question: {question}

Provide:
1. Additional context or background information
2. Related concepts or implications
3. Potential follow-up questions
4. Key takeaways

Keep it concise and relevant:"""
        
        response = model.generate_content(prompt)
        return response.text.strip()
        
    except Exception as e:
        if "quota" in str(e).lower():
            return None
        return None

def generate_general_ai_answer(question):
    """Generate general AI answer when no document content is found"""
    try:
        models = genai.list_models()
        available_models = [m.name for m in models if 'generateContent' in m.supported_generation_methods]
        
        if not available_models:
            return "AI not available"
        
        model_name = "gemini-2.0-flash-lite"
        if model_name not in [m.split('/')[-1] for m in available_models]:
            model_name = available_models[0].split('/')[-1]
        
        model = genai.GenerativeModel(model_name)
        
        prompt = f"""Answer this question with general knowledge:

Question: {question}

Provide a helpful, accurate answer based on general knowledge. Keep it concise and informative:"""
        
        response = model.generate_content(prompt)
        return response.text.strip()
        
    except Exception as e:
        if "quota" in str(e).lower():
            return "AI quota exceeded - please try again later"
        return "AI temporarily unavailable"

def get_answer(question):
    """Get comprehensive answer with both document content and AI insights"""
    if not st.session_state.documents:
        return "Please upload some documents first!", []
    
    # Always search documents first
    relevant_content = search_documents(question)
    
    # Build comprehensive answer
    answer_parts = []
    
    # Part 1: Exact answers from documents
    if relevant_content:
        answer_parts.append("📄 **EXACT ANSWERS FROM YOUR DOCUMENTS:**")
        answer_parts.append("")
        for i, result in enumerate(relevant_content, 1):
            answer_parts.append(f"**{i}. From {result['document']}:**")
            answer_parts.append(f"{result['text']}")
            answer_parts.append("")
        answer_parts.append("---")
        answer_parts.append("")
    
    # Part 2: AI-generated relevant insights (if enabled and not in quota mode)
    if st.session_state.ai_enabled and not st.session_state.quota_mode:
        try:
            ai_insights = generate_ai_insights(question, relevant_content)
            if ai_insights:
                answer_parts.append("🤖 **AI-GENERATED INSIGHTS:**")
                answer_parts.append("")
                answer_parts.append(ai_insights)
                answer_parts.append("")
                answer_parts.append("💡 *This AI analysis is based on your documents and general knowledge*")
        except Exception as e:
            if "quota" not in str(e).lower():
                st.error(f"AI Error: {str(e)}")
    
    # Part 3: Fallback if no document content found
    if not relevant_content:
        if st.session_state.ai_enabled and not st.session_state.quota_mode:
            try:
                ai_general = generate_general_ai_answer(question)
                answer_parts.append("🤖 **AI GENERAL KNOWLEDGE:**")
                answer_parts.append("")
                answer_parts.append(ai_general)
                answer_parts.append("")
                answer_parts.append("⚠️ *This information is not from your documents but from general AI knowledge*")
            except Exception as e:
                answer_parts.append("❌ **No relevant information found in your documents.**")
                answer_parts.append("")
                answer_parts.append("💡 **Suggestions:**")
                answer_parts.append("• Try rephrasing your question")
                answer_parts.append("• Upload more relevant documents")
                answer_parts.append("• Use different keywords")
        else:
            answer_parts.append("❌ **No relevant information found in your documents.**")
            answer_parts.append("")
            answer_parts.append("💡 **Suggestions:**")
            answer_parts.append("• Try rephrasing your question")
            answer_parts.append("• Upload more relevant documents")
            answer_parts.append("• Enable AI mode for general knowledge insights")
    
    return "\n".join(answer_parts), relevant_content

# Voice Chat Functions
@st.cache_resource
def get_speech_recognizer():
    """Initialize speech recognizer"""
    return sr.Recognizer()

@st.cache_resource
def get_text_to_speech():
    """Initialize text-to-speech engine"""
    try:
        engine = pyttsx3.init()
        # Set properties for better voice
        voices = engine.getProperty('voices')
        if voices:
            engine.setProperty('voice', voices[0].id)  # Use first available voice
        engine.setProperty('rate', 150)  # Speed of speech
        engine.setProperty('volume', 0.9)  # Volume level
        return engine
    except Exception as e:
        st.error(f"Text-to-speech initialization failed: {str(e)}")
        return None

def listen_to_voice():
    """Listen to voice input and return transcribed text"""
    recognizer = get_speech_recognizer()
    
    with sr.Microphone() as source:
        st.info("🎤 Listening... Speak now!")
        try:
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            # Listen for audio input
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            st.info("🔄 Processing speech...")
            # Recognize speech using Google Speech Recognition
            text = recognizer.recognize_google(audio)
            return text.strip()
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            st.error("Could not understand audio. Please try again.")
            return None
        except sr.RequestError as e:
            st.error(f"Speech recognition service error: {str(e)}")
            return None
        except Exception as e:
            st.error(f"Voice recognition error: {str(e)}")
            return None

def speak_text(text):
    """Convert text to speech"""
    engine = get_text_to_speech()
    if engine:
        try:
            # Run text-to-speech in a separate thread to avoid blocking
            def speak():
                engine.say(text)
                engine.runAndWait()
            
            thread = threading.Thread(target=speak)
            thread.start()
            return True
        except Exception as e:
            st.error(f"Text-to-speech error: {str(e)}")
            return False
    return False





# Main Interface
st.title("🤖 Enhanced QA Agent")
st.markdown("Upload documents and get intelligent answers!")

# AI Status
col1, col2 = st.columns([3, 1])
with col1:
    if st.session_state.ai_enabled:
        # Test AI connection
        try:
            # List available models first
            models = genai.list_models()
            available_models = [m.name for m in models if 'generateContent' in m.supported_generation_methods]
            
        except Exception as e:
            if "quota" in str(e).lower() or "429" in str(e):
                pass
            else:
                st.error(f"🤖 AI Connection Error: {str(e)}")
    else:
        st.warning("⚠️ Simple Search Mode")
with col2:
    if st.button("🔄 Toggle AI"):
        st.session_state.ai_enabled = not st.session_state.ai_enabled
        st.rerun()

# Quota mode toggle
if st.session_state.ai_enabled:
    st.checkbox("💡 Quota-Safe Mode (Reduces API calls)", value=st.session_state.quota_mode, key="quota_toggle")

# Sidebar
st.sidebar.header("📁 Upload Documents")

uploaded_files = st.sidebar.file_uploader(
    "Choose files", 
    type=['pdf', 'txt', 'docx'], 
    accept_multiple_files=True,
    help="Upload PDF, TXT, or DOCX files"
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

# Voice Chat Controls
st.markdown("### 🎤 Voice Chat")
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    if st.button("🎤 Voice Input", help="Click to speak your question"):
        with st.spinner("Preparing voice input..."):
            voice_text = listen_to_voice()
            if voice_text:
                st.session_state.voice_question = voice_text
                st.success(f"🎤 Heard: '{voice_text}'")

with col2:
    if st.button("🔊 Read Answer", help="Click to hear the last answer"):
        if st.session_state.chat_history:
            last_answer = st.session_state.chat_history[-1].get('answer', '')
            if last_answer:
                # Clean the answer for speech (remove markdown formatting)
                clean_answer = re.sub(r'\*\*(.*?)\*\*', r'\1', last_answer)  # Remove bold
                clean_answer = re.sub(r'#{1,6}\s*', '', clean_answer)  # Remove headers
                clean_answer = re.sub(r'---+', '', clean_answer)  # Remove separators
                clean_answer = re.sub(r'\n+', '. ', clean_answer)  # Replace newlines with periods
                clean_answer = clean_answer[:500]  # Limit length for speech
                
                if speak_text(clean_answer):
                    st.success("🔊 Reading answer...")
                else:
                    st.error("Failed to read answer")
            else:
                st.warning("No answer to read")
        else:
            st.warning("No conversation history")

with col3:
    st.markdown("**Voice Features:**")
    st.markdown("• Click 'Voice Input' to speak your question")
    st.markdown("• Click 'Read Answer' to hear the response")

# Display voice question if available
if 'voice_question' in st.session_state and st.session_state.voice_question:
    st.info(f"🎤 **Voice Input:** {st.session_state.voice_question}")
    if st.button("Use This Question"):
        question = st.session_state.voice_question
        del st.session_state.voice_question
    else:
        question = None
else:
    question = None

# Chat input
if not question:
    question = st.chat_input("Ask a question about your documents...")

if question:
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
        with st.spinner("🤔 Analyzing documents and generating insights..." if st.session_state.ai_enabled else "🔍 Searching documents..."):
            answer, sources = get_answer(question)
            
            # Display the comprehensive answer with proper formatting
            st.markdown(answer)
            
            # Update history
            st.session_state.chat_history[-1].update({
                'answer': answer,
                'sources': sources
            })
            
            # Show sources in expander
            if sources:
                with st.expander("📚 Document Sources"):
                    for i, source in enumerate(sources, 1):
                        st.write(f"**{i}. {source['document']}**")
                        st.write(f"*Relevance: {source['relevance']} matches*")
                        st.write(source['text'])
                        st.write("---")

# Stats
st.sidebar.header("📊 Statistics")
st.sidebar.metric("Documents", len(st.session_state.documents))
if st.session_state.documents:
    total_words = sum(d['word_count'] for d in st.session_state.documents)
    st.sidebar.metric("Total Words", f"{total_words:,}")

# AI Info
st.sidebar.header("🤖 AI Settings")
st.sidebar.info(f"**Model:** Google Gemini Pro\n**API:** Configured\n**Status:** {'Enabled' if st.session_state.ai_enabled else 'Disabled'}")

# Clear button
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.chat_history = []
    st.rerun()

# Export chat
if st.session_state.chat_history:
    if st.sidebar.button("💾 Export Chat"):
        chat_data = {
            'timestamp': datetime.now().isoformat(),
            'chat_history': st.session_state.chat_history,
            'documents': len(st.session_state.documents)
        }
        st.sidebar.download_button(
            label="Download Chat History",
            data=str(chat_data),
            file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

st.markdown("---")
st.markdown("🚀 **Enhanced QA Agent**")
