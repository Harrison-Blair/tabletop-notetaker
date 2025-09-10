"""
Command Line Interface for Tabletop Notetaker
"""

import os
import time
from pathlib import Path
from typing import Optional

from core.app import TabletopNotetakerApp


class CLIInterface:
    """Command line interface for the Tabletop Notetaker application"""

    def __init__(self, app: TabletopNotetakerApp):
        self.app = app

    def run(self):
        """Run the CLI interface"""
        print("=== Tabletop Notetaker CLI ===")
        print("Commands:")
        print("  record - Start recording")
        print("  stop   - Stop recording")
        print("  transcribe <file> - Transcribe audio file")
        print("  summarize <file> - Summarize transcript")
        print("  list   - List recordings")
        print("  quit   - Exit")
        print()

        while True:
            try:
                command = input("notetaker> ").strip().lower()

                if command == "quit" or command == "q":
                    break
                elif command == "record" or command == "r":
                    self.start_recording()
                elif command == "stop" or command == "s":
                    self.stop_recording()
                elif command.startswith("transcribe"):
                    parts = command.split()
                    if len(parts) > 1:
                        self.transcribe_file(parts[1])
                    else:
                        print("Usage: transcribe <audio_file>")
                elif command.startswith("summarize"):
                    parts = command.split()
                    if len(parts) > 1:
                        self.summarize_file(parts[1])
                    else:
                        print("Usage: summarize <transcript_file>")
                elif command == "list" or command == "l":
                    self.list_recordings()
                elif command == "help" or command == "h":
                    self.show_help()
                else:
                    print("Unknown command. Type 'help' for available commands.")

            except KeyboardInterrupt:
                print("\nUse 'quit' to exit.")
            except Exception as e:
                print(f"Error: {e}")

    def start_recording(self):
        """Start audio recording"""
        output_path = input("Enter output filename (or press Enter for auto-generated): ").strip()
        if not output_path:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_path = f"recording_{timestamp}.wav"

        print(f"Starting recording to: {output_path}")
        print("Press Ctrl+C to stop recording...")

        success = self.app.start_recording(output_path)
        if success:
            print("Recording started. Press Enter to stop...")
            try:
                input()
            except KeyboardInterrupt:
                pass
            finally:
                self.stop_recording()
        else:
            print("Failed to start recording.")

    def stop_recording(self):
        """Stop audio recording"""
        result = self.app.stop_recording()
        if result:
            print(f"Recording saved to: {result}")
        else:
            print("No active recording to stop.")

    def transcribe_file(self, audio_path: str):
        """Transcribe an audio file"""
        if not Path(audio_path).exists():
            print(f"File not found: {audio_path}")
            return

        print(f"Transcribing: {audio_path}")
        transcript = self.app.transcribe_audio(audio_path)

        if transcript:
            # Save transcript
            base_name = Path(audio_path).stem
            transcript_path = f"{base_name}_transcript.txt"
            self.app.save_transcript(transcript, transcript_path)

            print(f"Transcript saved to: {transcript_path}")

            # Ask if user wants to summarize
            response = input("Would you like to generate a summary? (y/n): ").strip().lower()
            if response in ['y', 'yes']:
                self.summarize_transcript(transcript)
        else:
            print("Transcription failed.")

    def summarize_file(self, transcript_path: str):
        """Summarize a transcript file"""
        if not Path(transcript_path).exists():
            print(f"File not found: {transcript_path}")
            return

        # Load transcript from file
        try:
            with open(transcript_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse basic transcript format
            transcript = self._parse_transcript_file(content)
            self.summarize_transcript(transcript)

        except Exception as e:
            print(f"Error reading transcript: {e}")

    def summarize_transcript(self, transcript: dict):
        """Generate summary from transcript data"""
        print("Generating summary...")

        format_choice = input("Choose format (txt/md/json) [txt]: ").strip().lower()
        if format_choice not in ['txt', 'md', 'json']:
            format_choice = 'txt'

        summary = self.app.summarize_transcript(transcript, format_choice)

        if summary:
            base_name = "meeting_summary"
            output_path = f"{base_name}.{format_choice}"
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(summary)
            print(f"Summary saved to: {output_path}")
        else:
            print("Summary generation failed.")

    def list_recordings(self):
        """List available recordings"""
        recordings_dir = Path(".")
        recordings = list(recordings_dir.glob("*.wav")) + list(recordings_dir.glob("*.mp3"))

        if not recordings:
            print("No recordings found.")
            return

        print("Available recordings:")
        for i, recording in enumerate(recordings, 1):
            size_mb = recording.stat().st_size / (1024 * 1024)
            print(f"  {i}. {recording.name} ({size_mb:.1f} MB)")

    def show_help(self):
        """Show help information"""
        print("\nAvailable commands:")
        print("  record (r)     - Start audio recording")
        print("  stop (s)       - Stop current recording")
        print("  transcribe <file> - Transcribe audio file")
        print("  summarize <file> - Summarize transcript file")
        print("  list (l)       - List available recordings")
        print("  help (h)       - Show this help")
        print("  quit (q)       - Exit the application")
        print()

    def _parse_transcript_file(self, content: str) -> dict:
        """Parse a basic transcript file into structured format"""
        segments = []
        lines = content.split('\n')

        for line in lines:
            line = line.strip()
            if line and '[' in line and ']:' in line:
                # Parse format: [Speaker]: text
                try:
                    speaker_end = line.find(']:')
                    speaker = line[1:speaker_end].strip()
                    text = line[speaker_end + 2:].strip()

                    segments.append({
                        'speaker': speaker,
                        'text': text,
                        'start': 0.0,  # Placeholder
                        'end': 0.0    # Placeholder
                    })
                except:
                    continue

        return {
            'segments': segments,
            'duration': len(segments) * 10  # Estimate duration
        }
