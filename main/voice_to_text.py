import speech_recognition as sr
from vosk import Model, KaldiRecognizer, SetLogLevel
import subprocess
import json

def voice_to_text_simple(voice_split_paths:str):
    
    r = sr.Recognizer()

    text_list = []
    for voice_path in voice_split_paths:

        with sr.AudioFile(voice_path) as source:
            audio = r.record(source)

        text = r.recognize_google(audio)
        text_list.append(text)

    return text_list

def voice_to_text_vosk(voice_split_paths: str, model_stt_path:str):

    SetLogLevel(0)

    model = Model(model_stt_path)

    sample_rate=16000
    rec = KaldiRecognizer(model, sample_rate)

    text_list = []

    for voice_path in voice_split_paths:
        process = subprocess.Popen(['ffmpeg', '-loglevel', 'quiet', '-i',
                                    voice_path,
                                    '-ar', str(sample_rate) , '-ac', '1', '-f', 's16le', '-'],
                                    stdout=subprocess.PIPE)

        text_all = ''
        while True:
            data = process.stdout.read(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                text = json.loads(rec.Result())
                text_all += " " + text["text"]

        text = json.loads(rec.FinalResult())
        text_all += " " + text["text"]
        text_list.append(text_all)

    return text_list