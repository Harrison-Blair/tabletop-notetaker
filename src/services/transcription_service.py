"""
Transcription service with speaker diarization for Tabletop Notetaker
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
import speech_recognition as sr
from datetime import datetime, timedelta


class TranscriptionService:
    """Handles audio transcription with speaker diarization"""

    def __init__(self):
        self.recognizer = sr.Recognizer()
        # Adjust for ambient noise
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True

    def transcribe_with_diarization(self, audio_path: str) -> Dict[str, Any]:
        """
        Transcribe audio file with basic speaker diarization
        Note: For production use, consider using more advanced diarization libraries
        like pyannote.audio or similar
        """
        try:
            print(f"Loading audio file: {audio_path}")

            # Load audio file
            with sr.AudioFile(audio_path) as source:
                # Record the entire audio file
                audio = self.recognizer.record(source)

                # Get duration for segmentation
                duration = source.DURATION if hasattr(source, 'DURATION') else 30

            # Perform transcription with basic segmentation
            transcript = self._transcribe_segmented(audio, duration)

            return {
                'file_path': audio_path,
                'duration': duration,
                'timestamp': datetime.now().isoformat(),
                'segments': transcript
            }

        except Exception as e:
            print(f"Transcription error: {e}")
            return {
                'error': str(e),
                'file_path': audio_path,
                'segments': []
            }

    def _transcribe_segmented(self, audio: sr.AudioData, duration: float) -> List[Dict[str, Any]]:
        """
        Transcribe audio in segments with simulated speaker diarization
        In a real implementation, you'd use proper diarization models
        """
        segments = []
        segment_length = 10  # seconds per segment

        try:
            # For basic transcription without advanced diarization
            text = self.recognizer.recognize_google(audio)

            # Create a single segment for the entire audio
            # In production, you'd split this into speaker segments
            segments.append({
                'start': 0.0,
                'end': duration,
                'speaker': 'Speaker 1',  # Default speaker
                'text': text,
                'confidence': 0.8  # Estimated confidence
            })

        except sr.UnknownValueError:
            print("Could not understand audio")
            segments.append({
                'start': 0.0,
                'end': duration,
                'speaker': 'Unknown',
                'text': '[Inaudible]',
                'confidence': 0.0
            })
        except sr.RequestError as e:
            print(f"Could not request results from speech recognition service: {e}")
            segments.append({
                'start': 0.0,
                'end': duration,
                'speaker': 'Error',
                'text': f'[Transcription service error: {e}]',
                'confidence': 0.0
            })

        return segments

    def transcribe_realtime(self, audio_data: bytes) -> Optional[str]:
        """Transcribe audio data in real-time (for live transcription)"""
        try:
            # Convert bytes to AudioData
            audio = sr.AudioData(audio_data, 44100, 2)  # Assuming 44.1kHz, 16-bit

            # Quick transcription for real-time use
            text = self.recognizer.recognize_google(audio, show_all=False)
            return text
        except (sr.UnknownValueError, sr.RequestError):
            return None

    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages for transcription"""
        return ['en-US', 'en-GB', 'es-ES', 'fr-FR', 'de-DE', 'it-IT', 'pt-BR', 'ja-JP', 'ko-KR', 'zh-CN']

    def set_language(self, language: str):
        """Set transcription language"""
        # This would be used with more advanced speech recognition services
        self.language = language
