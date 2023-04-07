from gtts import gTTS
import pyttsx3
import numpy as np
import soundfile as sf
import librosa
import os

from core import settings

default_path = settings.DEFAULT_PATH

def tts_gtts(text_list:list, time_list:list):

    voice_list = []
    for count, text in enumerate(text_list):
        voice = gTTS(text=text, lang="en", slow=False)
        voice_path = os.path.join(default_path,f"{count}.mp3")
        voice.save(voice_path)
        voice_load, sr = librosa.load(voice_path)
        voice_list.append(voice_load)
        
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


def concatenate_speech(voice_list, time_list, silence_list, first_silence, out_path):

    voice_all = np.zeros(int(first_silence*22050/1000))

    for voice, time, silence in zip(voice_list, time_list, silence_list):

        voice_time_silence = np.zeros(int((time+silence)*22050/1000))

        if len(voice)>int((time+silence)*22050/1000):
            voice_time_silence = voice[:int((time+silence)*22050/1000)]

        else:
            voice_time_silence[:len(voice)] = voice

        voice_all = np.concatenate((voice_all, voice_time_silence))

    sf.write(out_path, voice_all , 22050)
    return 