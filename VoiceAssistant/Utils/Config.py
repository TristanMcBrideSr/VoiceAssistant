import os
from dotenv import load_dotenv

load_dotenv()

ASSISTANT_NAME = os.getenv("ASSISTANT_NAME", "Assistant").lower()

ASSISTANT_GENDER = os.getenv("ASSISTANT_GENDER", "female").lower()

SPEAKING_RATE = int(os.getenv("SPEAKING_RATE", 150))
SPEAKING_PITCH = int(os.getenv("SPEAKING_PITCH", 100))  # Set pitch (not supported in pyttsx3, but is supported in pyttsx4)
SPEAKING_VOLUME = float(os.getenv("SPEAKING_VOLUME", 1.0))

VERBOSE = os.getenv("VERBOSE", "False")