import os
import platform
import subprocess
from gtts import gTTS
from elevenlabs.client import ElevenLabs
from config import ELEVENLABS_API_KEY, TTS_VOICE

def text_to_speech_with_elevenlabs(input_text, output_filepath):
    try:
        client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        audio = client.generate(
            text=input_text,
            voice=TTS_VOICE,
            output_format="mp3_22050_32",
            model="eleven_turbo_v2"
        )
        from elevenlabs import save
        save(audio, output_filepath)
        play_audio(output_filepath)
        return output_filepath
   
    except Exception as e:
        print(f"ElevenLabs TTS error: {e}")
        return None

def play_audio(filepath):
    os_name = platform.system()
    try:
        if os_name == "Darwin":
            subprocess.run(['afplay', filepath])
        elif os_name == "Windows":
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{filepath}").PlaySync();'])
        elif os_name == "Linux":
            subprocess.run(['aplay', filepath])
    
    except Exception as e:
        print(f"Audio play error: {e}")
