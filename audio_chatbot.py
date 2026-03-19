import os
import tempfile
import sounddevice as sd
import soundfile as sf
import numpy as np
from faster_whisper import WhisperModel
import pygame
from gtts import gTTS
from groq import Groq
from datetime import datetime

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "your-key")  #your key paste here

SAMPLE_RATE    = 16000
RECORD_SECONDS = 5

# ── Console colors (works on Mac/Linux terminal) ───────
RESET  = "\033[0m"
BOLD   = "\033[1m"
CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
GRAY   = "\033[90m"
RED    = "\033[91m"
BLUE   = "\033[94m"

def print_divider():
    print(f"{GRAY}{'─' * 60}{RESET}")

def print_you(text):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"\n{CYAN}{BOLD}🎤 YOU  [{timestamp}]{RESET}")
    print(f"{CYAN}   {text}{RESET}")
    print_divider()

def print_bot(text):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"\n{GREEN}{BOLD}🤖 BOT  [{timestamp}]{RESET}")
    print(f"{GREEN}   {text}{RESET}")
    print_divider()

def print_status(text):
    print(f"\n{YELLOW}⏳ {text}{RESET}")

def print_listening():
    print(f"\n{BLUE}{BOLD}🎙️  LISTENING...  speak now!{RESET}")
    print(f"{BLUE}{'▶' * 30}{RESET}")

def print_header():
    print(f"\n{BOLD}{'═' * 60}{RESET}")
    print(f"{BOLD}{'  🤖  AUDIO CHATBOT  —  Powered by Groq + Whisper':^60}{RESET}")
    print(f"{BOLD}{'═' * 60}{RESET}")
    print(f"{GRAY}  Say 'bye' or 'goodbye' to exit{RESET}")
    print(f"{GRAY}  Say 'clear' to reset conversation{RESET}")
    print(f"{BOLD}{'─' * 60}{RESET}\n")

def print_goodbye():
    print(f"\n{YELLOW}{BOLD}{'═' * 60}{RESET}")
    print(f"{YELLOW}{BOLD}{'  👋  GOODBYE! See you next time!':^60}{RESET}")
    print(f"{YELLOW}{BOLD}{'═' * 60}{RESET}\n")

# ── Load models ────────────────────────────────────────
print_status("Loading Whisper model... (downloads ~150MB on first run)")
stt_model = WhisperModel("base", device="cpu", compute_type="int8")
print(f"{GREEN}✅ Whisper loaded{RESET}")

client = Groq(api_key=GROQ_API_KEY)
print(f"{GREEN}✅ Groq connected{RESET}")

pygame.mixer.init()
print(f"{GREEN}✅ Audio ready{RESET}")

history = [
    {
        "role": "system",
        "content": (
            "You are a friendly voice assistant called Claudi. "
            "Give short, clear answers — you are speaking out loud. "
            "Be warm, helpful and conversational."
        )
    }
]

turn_count = 0


# ── 1. Record audio ────────────────────────────────────
def record_audio():
    print_listening()
    audio = sd.rec(
        int(RECORD_SECONDS * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32"
    )
    sd.wait()
    print(f"{BLUE}✔  Got it!{RESET}")
    return audio.flatten()


# ── 2. Transcribe ──────────────────────────────────────
def transcribe(audio):
    print_status("Transcribing...")
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        sf.write(f.name, audio, SAMPLE_RATE)
        segments, _ = stt_model.transcribe(f.name)
        text = " ".join([s.text for s in segments]).strip()
    return text


# ── 3. Ask LLM ─────────────────────────────────────────
def ask_llm(user_text):
    print_status("Thinking...")
    history.append({"role": "user", "content": user_text})
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=history,
        max_tokens=150,
        temperature=0.7,
    )
    reply = response.choices[0].message.content.strip()
    history.append({"role": "assistant", "content": reply})
    return reply


# ── 4. Speak ───────────────────────────────────────────
def speak(text):
    print_status("Speaking...")
    tts = gTTS(text=text, lang="en", slow=False)
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        tts.save(f.name)
        pygame.mixer.music.load(f.name)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)


# ── Main loop ──────────────────────────────────────────
def main():
    global turn_count, history

    print_header()
    speak("Hello! I am Claudi, your free voice assistant. How can I help you?")
    print_bot("Hello! I am Claudi, your free voice assistant. How can I help you?")

    while True:
        try:
            turn_count += 1
            print(f"\n{GRAY}  Turn {turn_count}{RESET}")

            audio = record_audio()
            text  = transcribe(audio)

            if not text or len(text) < 2:
                msg = "I did not catch that. Please try again."
                print_bot(msg)
                speak(msg)
                turn_count -= 1
                continue

            print_you(text)

            # Exit commands
            if any(w in text.lower() for w in ["quit", "bye", "exit", "goodbye"]):
                msg = "Goodbye! It was great talking with you. See you next time!"
                print_bot(msg)
                speak(msg)
                print_goodbye()
                break

            # Clear conversation memory
            if "clear" in text.lower():
                history = history[:1]   # keep system prompt only
                msg = "Conversation cleared! Starting fresh. How can I help?"
                print_bot(msg)
                speak(msg)
                turn_count = 0
                continue

            reply = ask_llm(text)
            print_bot(reply)
            speak(reply)

        except KeyboardInterrupt:
            print(f"\n\n{RED}  Interrupted. Goodbye!{RESET}\n")
            break


if __name__ == "__main__":
    main()
