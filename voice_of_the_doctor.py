from gtts import gTTS
from langdetect import detect
import os
import uuid


def text_to_speech_with_gtts(text):
    try:
        # Detect language
        lang = detect(text)

        # gTTS supported mapping
        if lang.startswith("ur"):
            tts_lang = "ur"
        elif lang.startswith("ar"):
            tts_lang = "ar"
        elif lang.startswith("ta"):
            tts_lang = "ta"
        elif lang.startswith("ml"):
            tts_lang = "ml"
        elif lang.startswith("hi"):
            tts_lang = "hi"
        else:
            tts_lang = "en"

        filename = f"/tmp/doctor_{uuid.uuid4()}.mp3"
        tts = gTTS(text=text, lang=tts_lang)
        tts.save(filename)

        return filename

    except Exception as e:
        print("TTS error:", e)
        return None
