import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
from groq import Groq
from config import GROQ_API_KEY, STT_MODEL

logging.basicConfig(level=logging.INFO)

def record_audio(file_path, timeout=20, phrase_time_limit=None):
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            logging.info("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)

        wav_data = audio_data.get_wav_data()
        audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
        audio_segment.export(file_path, format="mp3", bitrate="128k")
        return file_path
   
    except Exception as e:
        logging.error(f"Recording error: {e}")
        return None

def transcribe_with_groq(audio_filepath):
    try:
        client = Groq(api_key=GROQ_API_KEY)
        with open(audio_filepath, "rb") as f:
            transcription = client.audio.transcriptions.create(
                model=STT_MODEL,
                file=f,
                language="en"
            )
        return transcription.text
    
    except Exception as e:
        logging.error(f"Transcription failed: {e}")
        return None
