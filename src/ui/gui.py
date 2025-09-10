"""
Graphical User Interface for Tabletop Notetaker
"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import threading
import time
from pathlib import Path

from core.app import TabletopNotetakerApp


class GUIInterface:
    """Graphical user interface for Tabletop Notetaker"""

    def __init__(self, app: TabletopNotetakerApp):
        self.app = app
        self.root = None
        self.recording = False
        self.current_file = None

    def run(self):
        """Start the GUI application"""
        self.root = tk.Tk()
        self.root.title("Tabletop Notetaker")
        self.root.geometry("800x600")

        self._create_widgets()
        self._setup_layout()

        self.root.mainloop()

    def _create_widgets(self):
        """Create GUI widgets"""
        # Main frame
        self.main_frame = tk.Frame(self.root, padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = tk.Label(self.main_frame, text="Tabletop Notetaker",
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))

        # Recording section
        recording_frame = tk.LabelFrame(self.main_frame, text="Recording", padx=10, pady=10)
        recording_frame.pack(fill=tk.X, pady=(0, 20))

        self.record_button = tk.Button(recording_frame, text="Start Recording",
                                      command=self._toggle_recording, bg="green", fg="white",
                                      font=("Arial", 12, "bold"))
        self.record_button.pack(side=tk.LEFT, padx=(0, 10))

        self.status_label = tk.Label(recording_frame, text="Ready", font=("Arial", 10))
        self.status_label.pack(side=tk.LEFT, padx=(0, 20))

        self.timer_label = tk.Label(recording_frame, text="00:00:00", font=("Arial", 12, "bold"))
        self.timer_label.pack(side=tk.RIGHT)

        # File operations section
        file_frame = tk.LabelFrame(self.main_frame, text="File Operations", padx=10, pady=10)
        file_frame.pack(fill=tk.X, pady=(0, 20))

        # Buttons frame
        buttons_frame = tk.Frame(file_frame)
        buttons_frame.pack(fill=tk.X)

        tk.Button(buttons_frame, text="Transcribe Audio",
                 command=self._transcribe_audio).pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(buttons_frame, text="Summarize Transcript",
                 command=self._summarize_transcript).pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(buttons_frame, text="Load Transcript",
                 command=self._load_transcript).pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(buttons_frame, text="Save Output",
                 command=self._save_output).pack(side=tk.LEFT)

        # Output section
        output_frame = tk.LabelFrame(self.main_frame, text="Output", padx=10, pady=10)
        output_frame.pack(fill=tk.BOTH, expand=True)

        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD,
                                                   font=("Arial", 10))
        self.output_text.pack(fill=tk.BOTH, expand=True)

        # Progress bar (simple label for now)
        self.progress_label = tk.Label(self.main_frame, text="", font=("Arial", 9))
        self.progress_label.pack(pady=(10, 0))

    def _setup_layout(self):
        """Setup the layout and event handlers"""
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _toggle_recording(self):
        """Toggle recording on/off"""
        if not self.recording:
            self._start_recording()
        else:
            self._stop_recording()

    def _start_recording(self):
        """Start audio recording"""
        try:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"recording_{timestamp}.wav"

            success = self.app.start_recording(filename)
            if success:
                self.recording = True
                self.current_file = filename
                self.record_button.config(text="Stop Recording", bg="red")
                self.status_label.config(text=f"Recording to: {filename}")
                self._start_timer()
            else:
                messagebox.showerror("Error", "Failed to start recording")
        except Exception as e:
            messagebox.showerror("Error", f"Recording error: {e}")

    def _stop_recording(self):
        """Stop audio recording"""
        try:
            result = self.app.stop_recording()
            if result:
                self.recording = False
                self.record_button.config(text="Start Recording", bg="green")
                self.status_label.config(text=f"Recording saved: {result}")
                self._stop_timer()
                messagebox.showinfo("Success", f"Recording saved to: {result}")
            else:
                messagebox.showwarning("Warning", "No active recording to stop")
        except Exception as e:
            messagebox.showerror("Error", f"Stop recording error: {e}")

    def _start_timer(self):
        """Start the recording timer"""
        self.start_time = time.time()
        self._update_timer()

    def _stop_timer(self):
        """Stop the recording timer"""
        if hasattr(self, 'timer_job'):
            self.root.after_cancel(self.timer_job)

    def _update_timer(self):
        """Update the timer display"""
        if self.recording:
            elapsed = time.time() - self.start_time
            hours, remainder = divmod(int(elapsed), 3600)
            minutes, seconds = divmod(remainder, 60)
            time_str = "02d"
            self.timer_label.config(text=time_str)
            self.timer_job = self.root.after(1000, self._update_timer)

    def _transcribe_audio(self):
        """Transcribe selected audio file"""
        file_path = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[("Audio files", "*.wav *.mp3 *.m4a"), ("All files", "*.*")]
        )

        if not file_path:
            return

        self.progress_label.config(text="Transcribing audio...")
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Starting transcription...\n")

        # Run transcription in background thread
        def transcribe_thread():
            try:
                transcript = self.app.transcribe_audio(file_path)
                if transcript:
                    self._display_transcript(transcript)
                    self.current_transcript = transcript
                else:
                    self.output_text.insert(tk.END, "Transcription failed.\n")
            except Exception as e:
                self.output_text.insert(tk.END, f"Error: {e}\n")
            finally:
                self.progress_label.config(text="")

        threading.Thread(target=transcribe_thread, daemon=True).start()

    def _summarize_transcript(self):
        """Summarize current transcript"""
        if not hasattr(self, 'current_transcript'):
            messagebox.showwarning("Warning", "No transcript loaded. Please transcribe audio first.")
            return

        self.progress_label.config(text="Generating summary...")

        def summarize_thread():
            try:
                summary = self.app.summarize_transcript(self.current_transcript, "md")
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(tk.END, summary)
            except Exception as e:
                self.output_text.insert(tk.END, f"Error: {e}\n")
            finally:
                self.progress_label.config(text="")

        threading.Thread(target=summarize_thread, daemon=True).start()

    def _load_transcript(self):
        """Load transcript from file"""
        file_path = filedialog.askopenfilename(
            title="Select Transcript File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )

        if not file_path:
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, content)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")

    def _save_output(self):
        """Save current output to file"""
        content = self.output_text.get(1.0, tk.END).strip()
        if not content:
            messagebox.showwarning("Warning", "No content to save.")
            return

        file_path = filedialog.asksaveasfilename(
            title="Save Output",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("Markdown files", "*.md"), ("All files", "*.*")]
        )

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("Success", f"File saved to: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")

    def _display_transcript(self, transcript: dict):
        """Display transcript in the output area"""
        self.output_text.delete(1.0, tk.END)

        segments = transcript.get('segments', [])
        if not segments:
            self.output_text.insert(tk.END, "No transcript content.\n")
            return

        for segment in segments:
            speaker = segment.get('speaker', 'Unknown')
            text = segment.get('text', '').strip()
            if text:
                self.output_text.insert(tk.END, f"[{speaker}]: {text}\n")

    def _on_closing(self):
        """Handle window closing"""
        if self.recording:
            if messagebox.askyesno("Recording in Progress",
                                 "Recording is in progress. Stop and exit?"):
                self._stop_recording()
            else:
                return

        self.root.destroy()
