from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

STT_MODEL = "whisper-large-v3"
VISION_MODEL = "llama-3.2-11b-vision-preview"
TTS_VOICE = "Aria"
