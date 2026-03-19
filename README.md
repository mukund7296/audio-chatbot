# 🤖 Audio Chatbot — Free Voice Assistant

A fully free, offline-capable audio chatbot built with Python.
Speak to it, it listens, thinks, and talks back.

Built with:
- 🎙️ faster-whisper  — Speech to Text (runs locally, free)
- 🧠 Groq + Llama 3  — AI brain (free API, no credit card)
- 🔊 gTTS            — Text to Speech (free)
- 🎮 pygame          — Audio playback

---

## 🏗️ How It Works
```
┌─────────────────────────────────────────────────────────┐
│                    AUDIO CHATBOT                        │
└─────────────────────────────────────────────────────────┘

  You speak
      │
      ▼
┌─────────────┐
│ Microphone  │  sounddevice records 5 seconds of audio
└──────┬──────┘
       │ raw audio (numpy array)
       ▼
┌─────────────┐
│   Whisper   │  faster-whisper converts speech → text
│   (local)   │  runs on your CPU, no internet needed
└──────┬──────┘
       │ "Hello, what is the weather?"
       ▼
┌─────────────┐
│  Groq API   │  Llama 3 reads your text + chat history
│  Llama 3    │  generates a smart, short reply
└──────┬──────┘
       │ "Today in Munich it is around 12°C..."
       ▼
┌─────────────┐
│    gTTS     │  converts reply text → MP3 audio
│  (Google)   │
└──────┬──────┘
       │ audio file
       ▼
┌─────────────┐
│   pygame    │  plays the audio through your speakers
│  (speaker)  │
└─────────────┘
      │
      ▼
  You hear the reply
      │
      └──────────────────────► loop back to top
```

---

## ⚙️ Requirements

- Python 3.10 or higher
- Mac / Linux / Windows
- Internet connection (for Groq API + gTTS)
- Microphone
- Free Groq API key → https://console.groq.com

---

## 🚀 Setup — Step by Step

### 1. Clone the repository
```bash
git clone https://github.com/mukund7296/audio-chatbot.git
cd audio-chatbot
```

### 2. Create a virtual environment
```bash
# Mac / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` at the start of your terminal prompt.

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

> ⚠️ Mac users: if you get a PortAudio error, run first:
> ```bash
> brew install portaudio ffmpeg
> ```

### 4. Add your Groq API key

Get your free key at https://console.groq.com → API Keys

Option A — set as environment variable (recommended):
```bash
export GROQ_API_KEY="your_key_here"       # Mac/Linux
set GROQ_API_KEY=your_key_here            # Windows
```

Option B — paste directly in `audio_chatbot.py` line 12:
```python
GROQ_API_KEY = "your_key_here"
```

### 5. Run the chatbot
```bash
python audio_chatbot.py
```

---

## 🎤 How to Use

| Action | What to do |
|---|---|
| Talk to the bot | Just speak after you see LISTENING |
| Exit | Say "bye" or "goodbye" |
| Reset memory | Say "clear" |
| Stop immediately | Press Ctrl + C |

---

## 📁 Project Structure
```
audio-chatbot/
├── audio_chatbot.py     # main application
├── requirements.txt     # all dependencies
├── .gitignore           # excludes venv, cache files
└── README.md            # this file
```

---

## 🛠️ Troubleshooting

| Error | Fix |
|---|---|
| `No module named 'sounddevice'` | `brew install portaudio` then `pip install sounddevice` |
| `ffmpeg not found` | `brew install ffmpeg` (Mac) |
| `model_decommissioned` | Change model to `llama-3.3-70b-versatile` in line 55 |
| Mic not recording | Check System Preferences → Privacy → Microphone |
| Bot speaks but no sound | Check Mac volume / pygame audio output |

---

## 🆓 Cost

This project is 100% free:

| Component | Cost |
|---|---|
| faster-whisper | Free — runs locally |
| Groq API | Free — 14,400 requests/day |
| gTTS | Free — Google TTS |
| All Python libraries | Free — open source |

---

## 🙏 Credits

Built by Mukund Biradar
GitHub: github.com/mukund7296
LinkedIn: linkedin.com/in/mukund-techlead
