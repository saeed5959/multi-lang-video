import argparse
import moviepy.editor
import speech_recognition as sr

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
    audio_path = video_path[:-3] + "wav"
    text_path = video_path[:-3] + "txt"

    #extract audio from video
    audio_from_video(video_path, audio_path)

    #convert audio to text
    audio_to_text_simple(audio_path, text_path)

    

    return 

















if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", type=str, required=True)
    parser.add_argument("--video_path", type=str, required=True)
    parser.add_argument("--out_path", type=str, required=True)
    args = parser.parse_args()
    convert_multi_lang(parser.lang, parser.video_path, parser.out_path)