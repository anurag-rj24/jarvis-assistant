import os
import webbrowser
import requests
import speech_recognition as sr
import pyttsx3
import pygame
from gtts import gTTS
from dotenv import load_dotenv
from openai import OpenAI
import musicLibrary

# Load environment variables
load_dotenv()

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = os.getenv("NEWS_API_KEY", "")
openai_api_key = os.getenv("OPENAI_API_KEY", "")

def speak_old(text):
    """Fallback offline TTS engine using pyttsx3."""
    engine.say(text)
    engine.runAndWait()

def speak(text):
    """Speaks given text using gTTS and pygame audio playback."""
    try:
        tts = gTTS(text)
        temp_audio = 'temp.mp3'
        tts.save(temp_audio)

        # Initialize Pygame mixer
        pygame.mixer.init()

        # Load and play the MP3 file
        pygame.mixer.music.load(temp_audio)
        pygame.mixer.music.play()

        # Keep running until playback finishes
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.music.unload()
        if os.path.exists(temp_audio):
            os.remove(temp_audio)
    except Exception as e:
        print(f"gTTS error: {e}, falling back to pyttsx3...")
        speak_old(text)

def aiProcess(command):
    """Sends prompt to OpenAI and returns response."""
    try:
        client = OpenAI(api_key=openai_api_key)
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
                {"role": "user", "content": command}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"OpenAI error: {e}")
        return "I encountered an issue connecting to my AI service."

def processCommand(c):
    """Processes user voice commands."""
    cmd = c.lower()
    if "open google" in cmd:
        webbrowser.open("https://google.com")
    elif "open facebook" in cmd:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in cmd:
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in cmd:
        webbrowser.open("https://linkedin.com")
    elif cmd.startswith("play"):
        parts = cmd.split(" ")
        if len(parts) > 1:
            song = parts[1]
            if song in musicLibrary.music:
                link = musicLibrary.music[song]
                webbrowser.open(link)
            else:
                speak(f"Sorry, song {song} is not in my library.")
    elif "headlines" in cmd or "news" in cmd:
        if not newsapi:
            speak("News API key is not configured.")
            return
        url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}"
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                data = r.json()
                articles = data.get('articles', [])
                if not articles:
                    speak("No headlines found.")
                else:
                    for article in articles[:5]:  # Read top 5 headlines
                        title = article.get("title")
                        if title:
                            speak(title)
            else:
                speak("Failed to fetch news from server.")
        except Exception as e:
            print(f"News fetch error: {e}")
            speak("Could not fetch the latest news.")
    else:
        # Fallback to OpenAI AI response
        output = aiProcess(c)
        speak(output)

if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        r = sr.Recognizer()
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening for wake word 'hello' or 'jarvis'...")
                audio = r.listen(source, timeout=2, phrase_time_limit=2)
            word = r.recognize_google(audio)
            if word.lower() in ["hello", "jarvis"]:
                speak("Yes?")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    r.adjust_for_ambient_noise(source, duration=0.3)
                    audio = r.listen(source, timeout=5, phrase_time_limit=5)
                    command = r.recognize_google(audio)
                    print(f"Command received: {command}")
                    processCommand(command)

        except Exception as e:
            # Silence recognition timeouts during continuous loop
            pass