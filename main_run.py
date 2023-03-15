import argparse
import moviepy.editor
import speech_recognition as sr
import os

from core import configs



def audio_from_video(video_path:str, audio_path:str):

    video = moviepy.editor.VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_path)

    return

def audio_to_text_simple(audio_path:str, text_path:str):
    
    r = sr.Recognizer()

    with sr.AudioFile(audio_path) as source:
        audio = r.record(source)

    text = r.recognize_google(audio)

    with open(text_path) as file:
        file.write(text)

    return 


    
def convert_multi_lang(lang:str, video_path:str, out_path:str):

    model_trans_path = configs.model_trans_path_dic[lang]
    mfa_in_folder = "/home/saeed/software/python/multi-lang-video/test_data/in"
    mfa_out_folder = "/home/saeed/software/python/multi-lang-video/test_data/out"
    audio_path = os.path.join(mfa_in_folder, os.path.basename(video_path)[:-3] + "wav")
    text_path = os.path.join(mfa_in_folder, os.path.basename(video_path)[:-3] + "txt")
    

    #extract audio from video
    audio_from_video(video_path, audio_path)

    #convert audio to text
    audio_to_text_simple(audio_path, text_path)

    #give audio and text to MFA to get time of any words in audio
    mfa_audio()

    #detect silence speech for splitting audio : time and duration
    silence_duration()

    #convert every split text to translate-text
    translate_text_func()

    #convert every split translate-text to audio
    text_to_audio.tts()

    #concatenate all split audio genrated with silence duration to each other
    concatenate_speech()

    return 

















if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", type=str, required=True)
    parser.add_argument("--video_path", type=str, required=True)
    parser.add_argument("--out_path", type=str, required=True)
    args = parser.parse_args()
    convert_multi_lang(parser.lang, parser.video_path, parser.out_path)