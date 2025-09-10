# Tabletop Notetaker

A comprehensive audio recording and transcription tool designed for tabletop gaming sessions, meetings, and discussions. Features both GUI and command-line interfaces with speaker diarization and intelligent summarization.

## Features

- 🎙️ **Audio Recording**: High-quality audio recording with optional persistence
- 🎯 **Speaker Diarization**: Automatically identify and label different speakers
- 📝 **Transcription**: Convert speech to text with timestamps
- 📋 **Smart Summarization**: Generate structured notes and action items
- 🖥️ **Dual Interface**: Both GUI and command-line options
- 💾 **Multiple Formats**: Export in TXT, Markdown, or JSON formats
- 🔄 **Real-time Processing**: Live transcription during recording

## Installation

### Prerequisites

- Python 3.8 or higher
- Microphone access for recording
- Internet connection for speech recognition

### Setup

1. Clone the repository:
```bash
git clone https://github.com/your-username/tabletop-notetaker.git
cd tabletop-notetaker
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Audio Dependencies

For Windows users, PyAudio installation might require additional setup:

```bash
# Install PyAudio wheel
pip install pipwin
pipwin install pyaudio
```

## Usage

### Command Line Interface

Start the CLI version:
```bash
python main.py
```

Available commands:
- `record` - Start audio recording
- `stop` - Stop current recording
- `transcribe <file>` - Transcribe audio file
- `summarize <file>` - Summarize transcript
- `list` - Show available recordings
- `quit` - Exit application

### GUI Interface

Launch the graphical interface:
```bash
python main.py --gui
```

### Command Line Options

```bash
# Start GUI
python main.py --gui

# Transcribe specific file
python main.py --transcribe recording.wav --output transcript.txt

# Start recording immediately
python main.py --record
```

## File Structure

```
tabletop-notetaker/
├── main.py                 # Main entry point
├── requirements.txt        # Python dependencies
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   └── app.py         # Core application logic
│   ├── services/
│   │   ├── __init__.py
│   │   ├── recording_service.py    # Audio recording
│   │   ├── transcription_service.py # Speech-to-text
│   │   └── summarization_service.py # Note generation
│   └── ui/
│       ├── __init__.py
│       ├── cli.py         # Command-line interface
│       └── gui.py         # Graphical interface
└── README.md
```

## Features in Detail

### Audio Recording
- Records in WAV format (44.1kHz, 16-bit)
- Optional automatic file naming with timestamps
- Background recording support
- Real-time duration tracking

### Transcription
- Uses Google Speech Recognition API
- Speaker diarization (basic implementation)
- Timestamp tracking
- Confidence scoring

### Summarization
- Extracts key points and action items
- Identifies participants
- Generates structured notes
- Multiple output formats (TXT, Markdown, JSON)

### Output Formats

#### Text Format
```
MEETING SUMMARY
==================================================
Date: 2025-09-10 14:30:00
Duration: 1800 seconds

PARTICIPANTS:
  - Speaker 1
  - Speaker 2

SUMMARY:
Brief overview of the discussion...

KEY POINTS:
  1. First important point
  2. Second important point

ACTION ITEMS:
  1. Speaker 1: Task to complete
```

#### Markdown Format
```markdown
# Meeting Summary

**Date:** 2025-09-10 14:30:00
**Duration:** 1800 seconds

## Participants
- Speaker 1
- Speaker 2

## Summary
Brief overview...

## Key Points
- First important point
- Second important point

## Action Items
- Speaker 1: Task to complete
```

## Configuration

### Audio Settings
Modify recording parameters in `recording_service.py`:
```python
SAMPLE_RATE = 44100
CHANNELS = 1
CHUNK_SIZE = 1024
```

### Speech Recognition
Adjust recognition settings in `transcription_service.py`:
```python
ENERGY_THRESHOLD = 300
DYNAMIC_ENERGY = True
```

## Troubleshooting

### Common Issues

1. **"Module not found" errors**
   - Ensure virtual environment is activated
   - Run `pip install -r requirements.txt`

2. **Audio recording fails**
   - Check microphone permissions
   - Verify PyAudio installation
   - Try different audio device

3. **Transcription errors**
   - Check internet connection
   - Verify audio file format
   - Ensure clear audio quality

4. **GUI not launching**
   - Install tkinter: `pip install tk`
   - On Linux: `sudo apt-get install python3-tk`

### Performance Tips

- Use external microphone for better quality
- Record in quiet environments
- Keep recording sessions under 30 minutes for best results
- Use WAV format for highest quality

## Development

### Adding New Features

1. Create new service in `src/services/`
2. Update `core/app.py` to integrate new service
3. Add CLI commands in `ui/cli.py`
4. Add GUI elements in `ui/gui.py`

### Testing

Run basic functionality test:
```bash
python -c "from src.core.app import TabletopNotetakerApp; app = TabletopNotetakerApp(); print('Import successful')"
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Future Enhancements

- [ ] Advanced speaker diarization with ML models
- [ ] Support for additional audio formats
- [ ] Cloud storage integration
- [ ] Real-time collaboration features
- [ ] Custom summarization templates
- [ ] Multi-language support
- [ ] Integration with note-taking apps

## Support

For issues and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the code documentation

---

**Happy note-taking! 🎲📝**
