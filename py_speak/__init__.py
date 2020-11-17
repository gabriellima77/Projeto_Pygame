import pyttsx3


def speak_text(text):
    engine = pyttsx3.init()
    engine.setProperty('voice', "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_PT-BR_MARIA_11.0")
    engine.say(text)
    engine.runAndWait()