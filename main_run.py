import argparse
import moviepy.editor
import os

from core import configs
from main import mfa, translate


def voice_from_video(video_path:str, voice_path:str):

    video = moviepy.editor.VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(voice_path)

    return


def convert_multi_lang(lang:str, video_path:str, out_path:str):

    model_trans_path = configs.model_trans_path_dic[lang]
    mfa_in_folder = "/home/saeed/software/python/multi-lang-video/test_data/in"
    mfa_out_folder = "/home/saeed/software/python/multi-lang-video/test_data/out"
    voice_path = os.path.join(mfa_in_folder, os.path.basename(video_path)[:-3] + "wav")
    text_path = os.path.join(mfa_in_folder, os.path.basename(video_path)[:-3] + "txt")
    

    #extract audio from video
    voice_from_video(video_path, voice_path)

    #convert audio to text
    translate.voice_to_text_simple(voice_path, text_path, model_trans_path)

    #give audio and text to MFA to get time of any words in audio
    tg = mfa.mfa_audio(mfa_in_folder, mfa_out_folder)

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