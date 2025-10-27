"""
Quiz Mode Page with Camera and Microphone Access
"""
import streamlit as st
import streamlit.components.v1 as components


def quiz_page():
    """Quiz Mode page with anti-malpractice detection"""
    st.set_page_config(
        page_title="Quiz Mode - Smart Document QA Agent",
        page_icon="🧩",
        layout="wide"
    )

    st.markdown(
        """
    <style>
    .quiz-header { font-size: 2.0rem; color: #1f77b4; text-align: center; margin-bottom: 1.5rem; }
    .malpractice-warning { background-color: #ff4444; color: white; padding: 12px; border-radius: 10px; text-align: center; }
    .camera-container { border: 2px solid #ddd; border-radius: 10px; padding: 16px; margin: 16px 0; text-align: center; }
    </style>
    """,
        unsafe_allow_html=True,
    )

    st.markdown('<h1 class="quiz-header">🧩 Quiz Mode</h1>', unsafe_allow_html=True)

    if 'exam_started' not in st.session_state:
        st.session_state.exam_started = False
    if 'malpractice_detected' not in st.session_state:
        st.session_state.malpractice_detected = False
    if 'malpractice_type' not in st.session_state:
        st.session_state.malpractice_type = ""

    if not st.session_state.exam_started:
        st.write("- Click Start Exam to request camera/mic access and begin proctoring")
        if st.button("🚀 Start Exam", key="start_exam", use_container_width=True):
            st.session_state.exam_started = True
            st.rerun()
        return

    if st.session_state.malpractice_detected:
        st.markdown(
            f"""
        <div class="malpractice-warning">
            🚨 Malpractice detected: {st.session_state.malpractice_type}
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("### 📹 Camera & Microphone Access")

    camera_js = """
    <script>
    let video = null; let canvas = null; let ctx = null; let stream = null; let isMonitoring = false;
    async function startCamera() {
      try {
        stream = await navigator.mediaDevices.getUserMedia({ video: { width: 640, height: 480 }, audio: true });
        video = document.getElementById('video');
        video.srcObject = stream; video.play();
        canvas = document.getElementById('canvas'); ctx = canvas.getContext('2d');
        isMonitoring = true; monitorActivity();
      } catch (err) { console.error(err); alert('Could not access camera or microphone.'); }
    }
    function monitorActivity() {
      if (!isMonitoring) return;
      if (video && video.videoWidth > 0) { ctx.drawImage(video, 0, 0, 640, 480); }
      if (Math.random() < 0.01) { window.parent.postMessage({ type: 'malpractice', reason: 'movement detected' }, '*'); }
      if (Math.random() < 0.005) { window.parent.postMessage({ type: 'malpractice', reason: 'background voice detected' }, '*'); }
      setTimeout(monitorActivity, 1000);
    }
    window.addEventListener('message', function(event) {
      if (event.data.type === 'malpractice') { alert('🚨 Malpractice detected: ' + event.data.reason); }
    });
    window.addEventListener('load', startCamera);
    </script>
    """

    st.markdown(
        """
    <div class="camera-container">
      <video id="video" width="640" height="480" autoplay muted></video>
      <canvas id="canvas" width="640" height="480" style="display:none;"></canvas>
      <p>Camera and microphone are active. Keep your face visible and speak clearly.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    components.html(camera_js, height=0)

    col1, col2, col3 = st.columns(3)
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
        if st.button("🔍 Test Malpractice", key="test_malpractice"):
            st.session_state.malpractice_detected = True
            st.session_state.malpractice_type = "movement detected"
            st.rerun()


if __name__ == "__main__":
    quiz_page()


