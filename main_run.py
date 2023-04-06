import argparse
import moviepy.editor
import os

from core import configs
from main import mfa, translate, voice_to_text, text_to_voice, silence_detection


def voice_from_video(video_path:str, voice_path:str):

    video = moviepy.editor.VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(voice_path,22050)

    return

def trim_video(video_path:str, first_time:int, last_time:int, out_path:str):

    video = moviepy.editor.VideoFileClip(video_path)

    clip1 = video.subclip(first_time, last_time)
    clip1.write_videofile(out_path)


def convert_multi_lang(lang:str, video_path:str, out_path:str):

    model_trans_path = configs.model_trans_path_dic[lang]
    mfa_in_folder = "/home/saeed/software/python/multi-lang-video/test_data/in"
    mfa_out_folder = "/home/saeed/software/python/multi-lang-video/test_data/out"
    voice_path = os.path.join(mfa_in_folder, os.path.basename(video_path)[:-3] + "wav")
    text_path = os.path.join(mfa_in_folder, os.path.basename(video_path)[:-3] + "txt")
    
    print("1")
    #extract audio from video
    voice_from_video(video_path, voice_path)
    print("2")
    #convert audio to text
    voice_to_text.voice_to_text_simple(voice_path, text_path, model_trans_path)
    #voice_to_text.voice_to_text_vosk(voice_path, text_path, model_trans_path)
    print("3")
    #give audio and text to MFA to get time of any words in audio
    tg = mfa.mfa_audio(mfa_in_folder, mfa_out_folder)
    print("4")
    #detect silence speech for splitting audio : time and duration
    text_list, time_list, silence_list = mfa.silence_duration(tg)
    print("5")
    #convert every split text to translate-text
    text_trans_list = translate.translate_text_func(text_list, lang)
    print("6")
    #convert every split translate-text to audio
    voice_list = text_to_voice.tts_gtts(text_trans_list, time_list)
    print("7")
    #concatenate all split audio genrated with silence duration to each other
    text_to_voice.concatenate_speech(voice_list, time_list, silence_list, out_path)

    return 


def convert_multi_lang_direct(lang:str, video_path:str, out_path:str):

    model_stt_path = configs.model_trans_path_dic[lang]
    default_path = "/home/saeed/software/python/multi-lang-video/test_data"
    voice_path = os.path.join(default_path, os.path.basename(video_path)[:-3] + "wav")
    
    print("1")
    #extract audio from video
    voice_from_video(video_path, voice_path)
    print("2")
    #split audio in silence part
    voice_split_paths, time_list, silence_list, first_silence = silence_detection.split(voice_path, default_path)
    #convert audio to text
    text_list = voice_to_text.voice_to_text_simple(voice_split_paths, model_stt_path)
    #voice_to_text.voice_to_text_vosk(voice_path, text_path, model_trans_path)
    print("3")
    #convert every split text to translate-text
    #text_trans_list = translate.translate_text_func(text_list, lang)
    print("4")
    #convert every split translate-text to audio
    voice_list = text_to_voice.tts_gtts(text_list, time_list)
    print("5")
    #concatenate all split audio genrated with silence duration to each other
    text_to_voice.concatenate_speech(voice_list, time_list, silence_list, first_silence, out_path)

    return 





if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", type=str, required=True)
    parser.add_argument("--video_path", type=str, required=True)
    parser.add_argument("--out_path", type=str, required=True)
    args = parser.parse_args()
    convert_multi_lang(parser.lang, parser.video_path, parser.out_path)