"""
Audio recording service for Tabletop Notetaker
"""

import pyaudio
import wave
import threading
import time
from pathlib import Path
from typing import Optional, Callable


class RecordingService:
    """Handles audio recording with optional persistence"""

    def __init__(self, sample_rate: int = 44100, channels: int = 1, chunk_size: int = 1024):
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.audio = None
        self.stream = None
        self.frames = []
        self.is_recording = False
        self.recording_thread = None
        self.output_path = None

    def start_recording(self, output_path: Optional[str] = None, callback: Optional[Callable] = None):
        """Start audio recording"""
        if self.is_recording:
            print("Already recording!")
            return

        self.output_path = output_path
        self.frames = []
        self.is_recording = True

        # Initialize PyAudio
        self.audio = pyaudio.PyAudio()

        # Open audio stream
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )

        # Start recording in a separate thread
        self.recording_thread = threading.Thread(target=self._record_loop, args=(callback,))
        self.recording_thread.daemon = True
        self.recording_thread.start()

        print("Recording started...")

    def _record_loop(self, callback: Optional[Callable]):
        """Main recording loop"""
        while self.is_recording:
            try:
                data = self.stream.read(self.chunk_size)
                self.frames.append(data)

                if callback:
                    callback(data)
            except Exception as e:
                print(f"Recording error: {e}")
                break

    def stop_recording(self) -> Optional[str]:
        """Stop recording and save to file if path provided"""
        if not self.is_recording:
            return None

        self.is_recording = False

        # Wait for recording thread to finish
        if self.recording_thread and self.recording_thread.is_alive():
            self.recording_thread.join(timeout=2.0)

        # Close stream
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()

        # Close PyAudio
        if self.audio:
            self.audio.terminate()

        # Save recording if path provided
        if self.output_path and self.frames:
            try:
                self._save_recording(self.output_path)
                print(f"Recording saved to: {self.output_path}")
                return self.output_path
            except Exception as e:
                print(f"Error saving recording: {e}")

        return None

    def _save_recording(self, output_path: str):
        """Save recorded frames to WAV file"""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        with wave.open(output_path, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(self.frames))

    def get_recording_duration(self) -> float:
        """Get current recording duration in seconds"""
        if not self.frames:
            return 0.0
        return len(self.frames) * self.chunk_size / self.sample_rate

    def is_currently_recording(self) -> bool:
        """Check if currently recording"""
        return self.is_recording
