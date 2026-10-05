# 🎙️ Jarvis - Python Voice Assistant

Jarvis is a voice-activated virtual assistant built in Python using SpeechRecognition, Google Text-to-Speech (gTTS), Pygame audio engine, NewsAPI, and OpenAI GPT.

---

## ✨ Features

- **Wake Word Detection**: Responds to `"hello"` or `"jarvis"`.
- **Speech-to-Text & Text-to-Speech**: Seamless voice recognition and gTTS audio playback with pyttsx3 fallback.
- **Web Navigation**: Quickly opens Google, YouTube, LinkedIn, Facebook, etc.
- **Custom Music Library**: Plays songs from YouTube bookmarks.
- **Live News Headlines**: Fetches real-time headlines using NewsAPI.
- **AI Intelligence**: Answers general queries using OpenAI GPT models.

---

## 🚀 Getting Started

### 1. Clone or Open the Repository
```bash
git clone <repository_url>
cd jarvis_project
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Environment Variables
Copy `.env.example` to `.env` and insert your API keys:
```bash
copy .env.example .env
```
Edit `.env`:
```ini
OPENAI_API_KEY=your_openai_api_key_here
NEWS_API_KEY=your_news_api_key_here
```

### 4. Run Jarvis
```bash
python main.py
```

---

## 📂 Project Structure

```
jarvis_project/
├── .env.example       # Template for environment variables
├── .gitignore          # Excludes secrets, temporary files and caches
├── client.py          # Standalone test client for OpenAI API
├── main.py            # Main Jarvis voice assistant application
├── musicLibrary.py    # Dictionary mapping song names to URLs
├── requirements.txt   # Python package dependencies
└── README.md          # Project documentation
```
