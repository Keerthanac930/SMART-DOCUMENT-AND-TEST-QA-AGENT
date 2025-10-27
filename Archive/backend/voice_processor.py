"""
Voice processing module for speech-to-text and text-to-speech functionality
"""
import io
import tempfile
import logging
from typing import Dict, Any, Optional, Union
import os
from datetime import datetime

# Audio processing
import speech_recognition as sr
from pydub import AudioSegment
import librosa
import soundfile as sf
import numpy as np

# Text-to-speech
try:
    import pyttsx3
    TTS_ENGINE_AVAILABLE = True
except ImportError:
    TTS_ENGINE_AVAILABLE = False
    pyttsx3 = None

# Configuration
from config import (
    VOICE_CHAT_ENABLED, SPEECH_RECOGNITION_TIMEOUT, SPEECH_RECOGNITION_PHRASE_TIMEOUT,
    TEXT_TO_SPEECH_ENABLED, TEXT_TO_SPEECH_VOICE, AUDIO_SAMPLE_RATE, AUDIO_CHUNK_SIZE,
    AUDIO_MAX_DURATION_SECONDS, FEATURES
)

logger = logging.getLogger(__name__)

class VoiceProcessor:
    """
    Handles voice input and output processing
    """
    
    def __init__(self):
        self.speech_recognizer = sr.Recognizer()
        self.tts_engine = None
        
        # Configure speech recognition
        self.speech_recognizer.energy_threshold = 300
        self.speech_recognizer.dynamic_energy_threshold = True
        self.speech_recognizer.pause_threshold = 0.8
        self.speech_recognizer.operation_timeout = SPEECH_RECOGNITION_TIMEOUT
        self.speech_recognizer.phrase_timeout = SPEECH_RECOGNITION_PHRASE_TIMEOUT
        
        # Initialize text-to-speech engine
        if FEATURES.get('voice_chat', False) and TEXT_TO_SPEECH_ENABLED and TTS_ENGINE_AVAILABLE:
            try:
                self.tts_engine = pyttsx3.init()
                self._configure_tts_engine()
                logger.info("Text-to-speech engine initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize text-to-speech engine: {e}")
                self.tts_engine = None
    
    def _configure_tts_engine(self):
        """Configure text-to-speech engine settings"""
        if not self.tts_engine:
            return
        
        try:
            # Set voice
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Try to find the preferred voice
                for voice in voices:
                    if TEXT_TO_SPEECH_VOICE.lower() in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
                else:
                    # Use first available voice
                    self.tts_engine.setProperty('voice', voices[0].id)
            
            # Set speech rate (words per minute)
            self.tts_engine.setProperty('rate', 150)
            
            # Set volume (0.0 to 1.0)
            self.tts_engine.setProperty('volume', 0.8)
            
        except Exception as e:
            logger.warning(f"Error configuring TTS engine: {e}")
    
    def process_voice_input(self, audio_data: Union[bytes, str], 
                           audio_format: str = 'wav') -> Dict[str, Any]:
        """
        Process voice input and convert to text
        
        Args:
            audio_data: Audio data as bytes or file path
            audio_format: Audio format (wav, mp3, etc.)
            
        Returns:
            Dict containing transcription result and metadata
        """
        if not FEATURES.get('voice_chat', False):
            return {
                'success': False,
                'error': 'Voice chat is disabled',
                'text': '',
                'confidence': 0.0
            }
        
        try:
            # Handle different input types
            if isinstance(audio_data, str):
                # File path
                audio_file = audio_data
            else:
                # Bytes data - save to temporary file
                with tempfile.NamedTemporaryFile(suffix=f'.{audio_format}', delete=False) as tmp_file:
                    tmp_file.write(audio_data)
                    audio_file = tmp_file.name
            
            try:
                # Process audio file
                return self._transcribe_audio_file(audio_file)
            finally:
                # Clean up temporary file if we created one
                if isinstance(audio_data, bytes) and os.path.exists(audio_file):
                    os.unlink(audio_file)
                    
        except Exception as e:
            logger.error(f"Error processing voice input: {e}")
            return {
                'success': False,
                'error': str(e),
                'text': '',
                'confidence': 0.0
            }
    
    def _transcribe_audio_file(self, audio_file_path: str) -> Dict[str, Any]:
        """Transcribe audio file to text"""
        try:
            # Preprocess audio for better recognition
            processed_audio_file = self._preprocess_audio(audio_file_path)
            
            # Perform speech recognition
            with sr.AudioFile(processed_audio_file) as source:
                # Adjust for ambient noise
                self.speech_recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio_data = self.speech_recognizer.record(source)
            
            # Try multiple recognition engines
            transcription_result = self._recognize_speech_multiple_engines(audio_data)
            
            # Clean up processed audio file
            if processed_audio_file != audio_file_path and os.path.exists(processed_audio_file):
                os.unlink(processed_audio_file)
            
            return transcription_result
            
        except Exception as e:
            logger.error(f"Error transcribing audio file {audio_file_path}: {e}")
            return {
                'success': False,
                'error': str(e),
                'text': '',
                'confidence': 0.0
            }
    
    def _preprocess_audio(self, audio_file_path: str) -> str:
        """Preprocess audio for better speech recognition"""
        try:
            # Load audio
            audio = AudioSegment.from_file(audio_file_path)
            
            # Check duration
            duration_seconds = len(audio) / 1000
            if duration_seconds > AUDIO_MAX_DURATION_SECONDS:
                logger.warning(f"Audio file is too long ({duration_seconds:.1f}s), truncating")
                audio = audio[:AUDIO_MAX_DURATION_SECONDS * 1000]
            
            # Convert to mono if stereo
            if audio.channels > 1:
                audio = audio.set_channels(1)
            
            # Set sample rate
            if audio.frame_rate != AUDIO_SAMPLE_RATE:
                audio = audio.set_frame_rate(AUDIO_SAMPLE_RATE)
            
            # Normalize audio
            audio = audio.normalize()
            
            # Apply noise reduction (simple high-pass filter)
            audio = audio.high_pass_filter(200)
            
            # Save processed audio
            processed_file_path = audio_file_path.replace('.', '_processed.')
            audio.export(processed_file_path, format='wav')
            
            return processed_file_path
            
        except Exception as e:
            logger.warning(f"Error preprocessing audio: {e}")
            return audio_file_path  # Return original if preprocessing fails
    
    def _recognize_speech_multiple_engines(self, audio_data) -> Dict[str, Any]:
        """Try multiple speech recognition engines"""
        engines = [
            ('google', 'Google Speech Recognition'),
            ('sphinx', 'Sphinx (offline)')
        ]
        
        best_result = {
            'success': False,
            'text': '',
            'confidence': 0.0,
            'engine': '',
            'error': ''
        }
        
        for engine, name in engines:
            try:
                if engine == 'google':
                    text = self.speech_recognizer.recognize_google(audio_data)
                elif engine == 'sphinx':
                    text = self.speech_recognizer.recognize_sphinx(audio_data)
                
                if text and text.strip():
                    # Calculate confidence based on text length and content
                    confidence = min(0.9, len(text.strip()) / 50.0)
                    
                    result = {
                        'success': True,
                        'text': text.strip(),
                        'confidence': confidence,
                        'engine': name,
                        'error': ''
                    }
                    
                    # Use the first successful result
                    if not best_result['success'] or confidence > best_result['confidence']:
                        best_result = result
                    
                    logger.info(f"Speech recognition successful using {name}")
                    
            except sr.UnknownValueError:
                logger.warning(f"Could not understand audio with {name}")
                continue
            except sr.RequestError as e:
                logger.warning(f"Error with {name}: {e}")
                if not best_result['error']:
                    best_result['error'] = str(e)
                continue
        
        return best_result
    
    def text_to_speech(self, text: str, output_format: str = 'wav') -> Optional[bytes]:
        """
        Convert text to speech
        
        Args:
            text: Text to convert to speech
            output_format: Output audio format (wav, mp3)
            
        Returns:
            Audio data as bytes or None if failed
        """
        if not FEATURES.get('voice_chat', False) or not self.tts_engine:
            logger.warning("Text-to-speech is not available")
            return None
        
        try:
            # Create temporary file for audio output
            with tempfile.NamedTemporaryFile(suffix=f'.{output_format}', delete=False) as tmp_file:
                tmp_file_path = tmp_file.name
            
            try:
                # Generate speech
                self.tts_engine.save_to_file(text, tmp_file_path)
                self.tts_engine.runAndWait()
                
                # Read the generated audio file
                with open(tmp_file_path, 'rb') as audio_file:
                    audio_data = audio_file.read()
                
                return audio_data
                
            finally:
                # Clean up temporary file
                if os.path.exists(tmp_file_path):
                    os.unlink(tmp_file_path)
                    
        except Exception as e:
            logger.error(f"Error in text-to-speech: {e}")
            return None
    
    def get_voice_capabilities(self) -> Dict[str, Any]:
        """Get information about voice processing capabilities"""
        return {
            'voice_chat_enabled': FEATURES.get('voice_chat', False),
            'speech_recognition_available': True,
            'text_to_speech_available': self.tts_engine is not None,
            'tts_engine_available': TTS_ENGINE_AVAILABLE,
            'supported_audio_formats': ['wav', 'mp3', 'm4a', 'aac', 'ogg', 'flac'],
            'max_audio_duration_seconds': AUDIO_MAX_DURATION_SECONDS,
            'default_sample_rate': AUDIO_SAMPLE_RATE,
            'speech_recognition_timeout': SPEECH_RECOGNITION_TIMEOUT,
            'speech_recognition_phrase_timeout': SPEECH_RECOGNITION_PHRASE_TIMEOUT
        }
    
    def test_microphone(self) -> Dict[str, Any]:
        """Test microphone availability and audio levels"""
        try:
            with sr.Microphone() as source:
                # Test ambient noise
                self.speech_recognizer.adjust_for_ambient_noise(source, duration=1)
                
                # Get audio level
                audio_level = source.get_ambient_noise()
                
                return {
                    'success': True,
                    'microphone_available': True,
                    'audio_level': audio_level,
                    'message': 'Microphone test successful'
                }
                
        except Exception as e:
            logger.error(f"Microphone test failed: {e}")
            return {
                'success': False,
                'microphone_available': False,
                'audio_level': 0,
                'error': str(e),
                'message': 'Microphone test failed'
            }
    
    def get_available_voices(self) -> List[Dict[str, Any]]:
        """Get list of available text-to-speech voices"""
        if not self.tts_engine:
            return []
        
        try:
            voices = self.tts_engine.getProperty('voices')
            voice_list = []
            
            for voice in voices:
                voice_list.append({
                    'id': voice.id,
                    'name': voice.name,
                    'languages': voice.languages,
                    'gender': getattr(voice, 'gender', 'unknown'),
                    'age': getattr(voice, 'age', 'unknown')
                })
            
            return voice_list
            
        except Exception as e:
            logger.error(f"Error getting available voices: {e}")
            return []
    
    def set_voice(self, voice_id: str) -> bool:
        """Set the text-to-speech voice"""
        if not self.tts_engine:
            return False
        
        try:
            self.tts_engine.setProperty('voice', voice_id)
            return True
        except Exception as e:
            logger.error(f"Error setting voice {voice_id}: {e}")
            return False
    
    def set_speech_rate(self, rate: int) -> bool:
        """Set the speech rate (words per minute)"""
        if not self.tts_engine:
            return False
        
        try:
            self.tts_engine.setProperty('rate', rate)
            return True
        except Exception as e:
            logger.error(f"Error setting speech rate {rate}: {e}")
            return False
    
    def set_volume(self, volume: float) -> bool:
        """Set the volume (0.0 to 1.0)"""
        if not self.tts_engine:
            return False
        
        try:
            volume = max(0.0, min(1.0, volume))  # Clamp between 0 and 1
            self.tts_engine.setProperty('volume', volume)
            return True
        except Exception as e:
            logger.error(f"Error setting volume {volume}: {e}")
            return False
