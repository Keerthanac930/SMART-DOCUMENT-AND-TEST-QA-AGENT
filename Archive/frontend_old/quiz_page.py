"""
Quiz Mode Page with Camera and Microphone Access
"""
import streamlit as st
import streamlit.components.v1 as components
import json
from datetime import datetime

def quiz_page():
    """Quiz Mode page with anti-malpractice detection"""
    st.set_page_config(
        page_title="Quiz Mode - Smart Document QA Agent",
        page_icon="🧩",
        layout="wide"
    )
    
    st.markdown("""
    <style>
    .quiz-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .start-exam-btn {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        color: white;
        padding: 15px 30px;
        border: none;
        border-radius: 25px;
        font-size: 1.2rem;
        cursor: pointer;
        margin: 20px auto;
        display: block;
    }
    .malpractice-warning {
        background-color: #ff4444;
        color: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-size: 1.1rem;
        margin: 20px 0;
    }
    .camera-container {
        border: 2px solid #ddd;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="quiz-header">🧩 Quiz Mode</h1>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'exam_started' not in st.session_state:
        st.session_state.exam_started = False
    if 'malpractice_detected' not in st.session_state:
        st.session_state.malpractice_detected = False
    if 'malpractice_type' not in st.session_state:
        st.session_state.malpractice_type = ""
    
    if not st.session_state.exam_started:
        st.markdown("""
        ### 📋 Exam Instructions
        
        - Click "Start Exam" to begin
        - Camera and microphone access will be requested
        - Keep your face visible to the camera
        - Do not turn away or have multiple people in view
        - Speak clearly into the microphone
        - Any suspicious activity will be flagged
        """)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Start Exam", key="start_exam", use_container_width=True):
                st.session_state.exam_started = True
                st.rerun()
    
    else:
        # Show malpractice warning if detected
        if st.session_state.malpractice_detected:
            st.markdown(f"""
            <div class="malpractice-warning">
                🚨 Malpractice detected: {st.session_state.malpractice_type}
            </div>
            """, unsafe_allow_html=True)
        
        # Camera and microphone access
        st.markdown("### 📹 Camera & Microphone Access")
        
        # JavaScript for camera/mic access and detection
        camera_js = """
        <script>
        let video = null;
        let canvas = null;
        let ctx = null;
        let stream = null;
        let isMonitoring = false;
        
        async function startCamera() {
            try {
                stream = await navigator.mediaDevices.getUserMedia({ 
                    video: { width: 640, height: 480 },
                    audio: true 
                });
                
                video = document.getElementById('video');
                video.srcObject = stream;
                video.play();
                
                canvas = document.getElementById('canvas');
                ctx = canvas.getContext('2d');
                
                isMonitoring = true;
                monitorActivity();
                
            } catch (err) {
                console.error('Error accessing camera/microphone:', err);
                alert('Could not access camera or microphone. Please check permissions.');
            }
        }
        
        function monitorActivity() {
            if (!isMonitoring) return;
            
            // Check for movement (simplified)
            if (video && video.videoWidth > 0) {
                ctx.drawImage(video, 0, 0, 640, 480);
                // Here you would implement actual movement detection
                // For now, we'll simulate random detection
                if (Math.random() < 0.01) { // 1% chance per check
                    window.parent.postMessage({
                        type: 'malpractice',
                        reason: 'movement detected'
                    }, '*');
                }
            }
            
            // Check for multiple people (simplified)
            if (Math.random() < 0.005) { // 0.5% chance per check
                window.parent.postMessage({
                    type: 'malpractice',
                    reason: 'background voice detected'
                }, '*');
            }
            
            setTimeout(monitorActivity, 1000); // Check every second
        }
        
        function stopCamera() {
            isMonitoring = false;
            if (stream) {
                stream.getTracks().forEach(track => track.stop());
            }
        }
        
        // Listen for messages from parent
        window.addEventListener('message', function(event) {
            if (event.data.type === 'malpractice') {
                alert('🚨 Malpractice detected: ' + event.data.reason);
            }
        });
        
        // Start camera when page loads
        window.addEventListener('load', startCamera);
        </script>
        """
        
        st.markdown("""
        <div class="camera-container">
            <video id="video" width="640" height="480" autoplay muted></video>
            <canvas id="canvas" width="640" height="480" style="display: none;"></canvas>
            <br>
            <p>Camera and microphone are active. Keep your face visible and speak clearly.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Include the JavaScript
        components.html(camera_js, height=0)
        
        # Exam controls
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("⏹️ End Exam", key="end_exam"):
                st.session_state.exam_started = False
                st.session_state.malpractice_detected = False
                st.rerun()
        
        with col2:
            if st.button("🔄 Reset Detection", key="reset_detection"):
                st.session_state.malpractice_detected = False
                st.session_state.malpractice_type = ""
                st.rerun()
        
        with col3:
            if st.button("📊 View Results", key="view_results"):
                st.info("Results will be displayed here after exam completion.")
        
        # Simulate malpractice detection for demo
        if st.button("🔍 Test Malpractice Detection", key="test_detection"):
            st.session_state.malpractice_detected = True
            st.session_state.malpractice_type = "movement detected"
            st.rerun()

if __name__ == "__main__":
    quiz_page()
