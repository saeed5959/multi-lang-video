from gtts import gTTS
import pyttsx3

from main import mfa
#1-align based on duration
#choose a library that you can change its speed

def tts_gtts(text_list:list, time_list:list):

    voice_list = []
    for text in text_list:
        voice_list.append(gTTS(text=text, lang="en", slow=False))

    return voice_list
        

def tts_pyttsx3(text_list:list, time_list:list):

    voice_list = []
    engine = pyttsx3.init()
    for text in text_list:
    
        engine.say("I will speak this text")
        rate = engine.getProperty('rate')
        engine.setProperty('rate', 125)
        engine.save_to_file('Hello World', 'test.mp3')

    return voice_list

def concatenate_speech(voice_list, silence_list, out_path):

    for voice in voice_list:
        mfa.mfa_audio(voice)
        mfa.silence_duration()

    return 