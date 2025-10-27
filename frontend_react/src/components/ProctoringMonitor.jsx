import { useEffect, useRef, useState } from 'react';
import { API_BASE_URL } from '../config/api';

const ProctoringMonitor = ({ onViolation, maxViolations = 10, isActive = true, testId, resultId }) => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [violations, setViolations] = useState(0);
  const [cameraActive, setCameraActive] = useState(false);
  const [audioContext, setAudioContext] = useState(null);
  const [lastViolationType, setLastViolationType] = useState('');
  const violationCheckInterval = useRef(null);
  const audioAnalyserRef = useRef(null);

  // Log violation to backend
  const logViolation = async (violationType) => {
    if (!testId || !resultId) return;

    try {
      const token = localStorage.getItem('token');
      await fetch(`${API_BASE_URL}/api/proctor/log`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          test_id: testId,
          result_id: resultId,
          violation_type: violationType
        })
      });
    } catch (error) {
      console.error('Failed to log violation:', error);
    }
  };

  // Simple face detection using canvas
  const detectFace = () => {
    if (!videoRef.current || !canvasRef.current) return false;
    
    const video = videoRef.current;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const data = imageData.data;
    
    // Simple skin tone detection as a proxy for face detection
    let skinPixels = 0;
    for (let i = 0; i < data.length; i += 4) {
      const r = data[i];
      const g = data[i + 1];
      const b = data[i + 2];
      
      // Skin tone detection (simplified)
      if (r > 95 && g > 40 && b > 20 && 
          Math.max(r, g, b) - Math.min(r, g, b) > 15 &&
          Math.abs(r - g) > 15 && r > g && r > b) {
        skinPixels++;
      }
    }
    
    // If skin pixels are between 5-50% of frame, assume face is visible
    const skinRatio = skinPixels / (canvas.width * canvas.height);
    return skinRatio > 0.05 && skinRatio < 0.50;
  };

  // Start camera and audio monitoring
  useEffect(() => {
    if (!isActive) return;

    const startMonitoring = async () => {
      try {
        // Request camera and microphone access
        const stream = await navigator.mediaDevices.getUserMedia({
          video: true,
          audio: true
        });

        if (videoRef.current) {
          videoRef.current.srcObject = stream;
          setCameraActive(true);
        }

        // Setup audio monitoring
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const analyser = audioCtx.createAnalyser();
        const microphone = audioCtx.createMediaStreamSource(stream);
        
        analyser.smoothingTimeConstant = 0.3; // More responsive
        analyser.fftSize = 2048; // Higher resolution
        
        microphone.connect(analyser);
        setAudioContext(audioCtx);
        audioAnalyserRef.current = analyser;

        console.log('✅ Camera and microphone active');
      } catch (error) {
        console.error('Error accessing media devices:', error);
        alert('Please enable camera and microphone access to continue the test.');
      }
    };

    startMonitoring();

    return () => {
      // Cleanup
      if (videoRef.current && videoRef.current.srcObject) {
        const tracks = videoRef.current.srcObject.getTracks();
        tracks.forEach(track => track.stop());
      }
      if (audioContext) {
        audioContext.close();
      }
    };
  }, [isActive]);

  // Face detection and violation checking
  useEffect(() => {
    if (!isActive || !cameraActive) return;

    const checkForViolations = async () => {
      if (!videoRef.current) return;

      try {
        let violationType = null;

        // Check for face violations using simple detection
        const hasFace = detectFace();
        if (!hasFace) {
          violationType = 'no_face';
          console.log('⚠️ No face detected');
        }

        // Check for loud audio
        if (audioAnalyserRef.current) {
          const dataArray = new Uint8Array(audioAnalyserRef.current.frequencyBinCount);
          audioAnalyserRef.current.getByteFrequencyData(dataArray);
          
          const average = dataArray.reduce((a, b) => a + b) / dataArray.length;
          const max = Math.max(...dataArray);
          
          // Lower threshold for better sensitivity (30 for normal voice, 60 for loud)
          // Log to console for debugging
          console.log('🔊 Audio level - Average:', Math.round(average), 'Max:', Math.round(max));
          
          // If average volume is above threshold (speaking loudly)
          if (average > 40) { // Lowered threshold for better detection
            violationType = 'loud_audio';
            console.log('⚠️ LOUD AUDIO VIOLATION detected! Average:', Math.round(average), 'Max:', Math.round(max));
          }
        }

        // Log violation
        if (violationType) {
          setViolations(prev => {
            const newCount = prev + 1;
            setLastViolationType(violationType);
            
            // Log to backend
            logViolation(violationType);
            
            // Notify parent component
            if (onViolation) {
              onViolation(newCount);
            }

            // Terminate test if max violations reached
            if (newCount >= maxViolations) {
              alert('Test terminated due to excessive violations!');
            }

            return newCount;
          });
        }
      } catch (error) {
        console.error('Error during violation check:', error);
      }
    };

    // Check for violations every 1.5 seconds for more real-time detection
    violationCheckInterval.current = setInterval(checkForViolations, 1500);

    return () => {
      if (violationCheckInterval.current) {
        clearInterval(violationCheckInterval.current);
      }
    };
  }, [isActive, cameraActive, onViolation, maxViolations, testId, resultId]);

  if (!isActive) return null;

  return (
    <div className="proctoring-monitor fixed top-4 right-4 z-50">
      <div className="bg-white rounded-lg shadow-lg p-4 w-80">
        <h3 className="text-lg font-semibold mb-2">AI Proctoring</h3>
        
        {/* Camera Feed */}
        <div className="relative mb-3">
          <video
            ref={videoRef}
            autoPlay
            muted
            className="w-full h-48 bg-black rounded"
          />
          <canvas ref={canvasRef} className="hidden" />
          <div className="absolute top-2 left-2">
            <span className={`inline-flex items-center px-2 py-1 rounded text-xs font-medium ${
              cameraActive ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
            }`}>
              <span className={`w-2 h-2 rounded-full mr-1 ${
                cameraActive ? 'bg-green-500' : 'bg-red-500'
              }`}></span>
              {cameraActive ? 'Recording' : 'Inactive'}
            </span>
          </div>
        </div>

        {/* Violation Counter */}
        <div className="space-y-2">
          <div className="flex justify-between items-center">
            <span className="text-sm font-medium">Violations:</span>
            <span className={`text-lg font-bold ${
              violations >= maxViolations - 2 ? 'text-red-600' : 
              violations >= maxViolations / 2 ? 'text-yellow-600' : 'text-green-600'
            }`}>
              {violations} / {maxViolations}
            </span>
          </div>

          {/* Progress bar */}
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className={`h-2 rounded-full transition-all ${
                violations >= maxViolations - 2 ? 'bg-red-500' : 
                violations >= maxViolations / 2 ? 'bg-yellow-500' : 'bg-green-500'
              }`}
              style={{ width: `${(violations / maxViolations) * 100}%` }}
            />
          </div>

          {/* Last violation */}
          {lastViolationType && (
            <div className="text-xs text-gray-600">
              Last: {lastViolationType.replace('_', ' ')}
            </div>
          )}

          {/* Warning message */}
          {violations >= maxViolations - 2 && (
            <div className="bg-red-50 border border-red-200 rounded p-2 text-xs text-red-700">
              ⚠️ Warning: Test will terminate at {maxViolations} violations!
            </div>
          )}
        </div>

        {/* Instructions */}
        <div className="mt-3 text-xs text-gray-500 border-t pt-2">
          <p className="font-medium mb-1">Rules:</p>
          <ul className="list-disc list-inside space-y-1">
            <li>Keep your face visible</li>
            <li>No multiple people</li>
            <li>Keep noise to minimum</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default ProctoringMonitor;
