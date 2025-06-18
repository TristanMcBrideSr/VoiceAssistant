
import pyttsx4
import os
import speech_recognition as sr
import re
from Utils.Config import ASSISTANT_NAME, ASSISTANT_GENDER, SPEAKING_RATE, SPEAKING_PITCH, SPEAKING_VOLUME

# Initialize the text-to-speech engine
engine = pyttsx4.init()

# Initialize the speech recognizer
recognizer = sr.Recognizer()

def listen():
    with sr.Microphone() as source:
        print(f"{ASSISTANT_NAME.title()} is listening...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print(f"You said:\n{text}")
        text = text.lower()
        if ASSISTANT_NAME in text:
            # Remove assistant name (and possible comma after it) from beginning of phrase
            cleaned = text.replace(ASSISTANT_NAME, "", 1).lstrip(",. ").strip()
            return cleaned
        return None
    except Exception as e:
        print(f"Sorry, I didn't catch that. {e}")
        return None


def keyboard():
    text = input("Enter your input: ")
    return text.lower()


def cleanForSpeech(text):
    # Remove *, [, ], (, ), {, }, <, > and any other symbols you want
    return re.sub(r'[\*\[\]\(\)\{\}\<\>]', '', text)

def speak(text):
    print(f"{ASSISTANT_NAME.title()}:\n{text}")
    cleaned = cleanForSpeech(text)
    voices = engine.getProperty('voices')
    # If ASSISTANT_GENDER is 'male', use 0, else use 1
    voice = 0 if ASSISTANT_GENDER == "male" else 1
    if len(voices) > voice:
        engine.setProperty('voice', voices[voice].id)
    else:
        engine.setProperty('voice', voices[0].id)  # fallback if only 1 voice
    engine.setProperty('rate', SPEAKING_RATE)  # Set speech rate
    engine.setProperty('pitch', SPEAKING_PITCH) # Set pitch (not supported in pyttsx3, but is supported in pyttsx4)
    engine.setProperty('volume', SPEAKING_VOLUME)  # Set volume to maximum
    engine.say(cleaned)
    engine.runAndWait()

