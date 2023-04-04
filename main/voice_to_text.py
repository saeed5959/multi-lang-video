import speech_recognition as sr
from vosk import Model, KaldiRecognizer, SetLogLevel
import subprocess
import json

def voice_to_text_simple(voice_path:str, text_path:str, model_trans_path:str):
    
    r = sr.Recognizer()

    with sr.AudioFile(voice_path) as source:
        audio = r.record(source)

    text = r.recognize_google(audio)

    with open(text_path,"w") as file:
        file.write(text)

    return 

def voice_to_text_vosk(voice_path: str, text_path:str, model_trans_path:str):

    SetLogLevel(0)

    model = Model(model_trans_path)

    sample_rate=16000
    rec = KaldiRecognizer(model, sample_rate)
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

    with open(text_path) as file:
        file.write(text)

    return