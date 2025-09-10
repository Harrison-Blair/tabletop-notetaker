"""
Core application logic for Tabletop Notetaker
"""

import json
import threading
import time
from pathlib import Path
from typing import Optional, Dict, List, Any
from datetime import datetime

from services.recording_service import RecordingService
from services.transcription_service import TranscriptionService
from services.summarization_service import SummarizationService


class TabletopNotetakerApp:
    """Main application class for Tabletop Notetaker"""

    def __init__(self):
        self.recording_service = RecordingService()
        self.transcription_service = TranscriptionService()
        self.summarization_service = SummarizationService()
        self.is_recording = False
        self.current_recording_path = None
        self.recordings = []

    def start_recording(self, output_path: Optional[str] = None) -> bool:
        """Start audio recording"""
        try:
            if output_path:
                self.current_recording_path = Path(output_path)
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                self.current_recording_path = Path(f"recording_{timestamp}.wav")

            self.recording_service.start_recording(str(self.current_recording_path))
            self.is_recording = True
            return True
        except Exception as e:
            print(f"Error starting recording: {e}")
            return False

    def stop_recording(self) -> Optional[str]:
        """Stop audio recording and return the file path"""
        try:
            if self.is_recording:
                self.recording_service.stop_recording()
                self.is_recording = False
                if self.current_recording_path:
                    self.recordings.append(str(self.current_recording_path))
                return str(self.current_recording_path)
        except Exception as e:
            print(f"Error stopping recording: {e}")
        return None

    def transcribe_audio(self, audio_path: str) -> Optional[Dict[str, Any]]:
        """Transcribe audio file with speaker diarization"""
        try:
            if not Path(audio_path).exists():
                print(f"Audio file not found: {audio_path}")
                return None

            print("Starting transcription...")
            transcript = self.transcription_service.transcribe_with_diarization(audio_path)
            return transcript
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            return None

    def summarize_transcript(self, transcript: Dict[str, Any], format_type: str = "txt") -> str:
        """Summarize transcript into notes"""
        try:
            summary = self.summarization_service.summarize(transcript, format_type)
            return summary
        except Exception as e:
            print(f"Error summarizing transcript: {e}")
            return ""

    def save_transcript(self, transcript: Dict[str, Any], output_path: str, format_type: str = "txt"):
        """Save transcript to file in specified format"""
        try:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)

            if format_type == "json":
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(transcript, f, indent=2, ensure_ascii=False)
            elif format_type == "md":
                self._save_as_markdown(transcript, output_path)
            else:  # txt
                self._save_as_text(transcript, output_path)

            print(f"Transcript saved to: {output_path}")
        except Exception as e:
            print(f"Error saving transcript: {e}")

    def _save_as_text(self, transcript: Dict[str, Any], output_path: str):
        """Save transcript as plain text"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"Meeting Transcript\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            for segment in transcript.get('segments', []):
                speaker = segment.get('speaker', 'Unknown')
                text = segment.get('text', '').strip()
                if text:
                    f.write(f"[{speaker}]: {text}\n")

    def _save_as_markdown(self, transcript: Dict[str, Any], output_path: str):
        """Save transcript as markdown"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"# Meeting Transcript\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            current_speaker = None
            for segment in transcript.get('segments', []):
                speaker = segment.get('speaker', 'Unknown')
                text = segment.get('text', '').strip()

                if text:
                    if speaker != current_speaker:
                        f.write(f"\n## {speaker}\n\n")
                        current_speaker = speaker
                    f.write(f"{text}\n")

    def get_recording_status(self) -> Dict[str, Any]:
        """Get current recording status"""
        return {
            'is_recording': self.is_recording,
            'current_file': str(self.current_recording_path) if self.current_recording_path else None,
            'recordings': self.recordings.copy()
        }
