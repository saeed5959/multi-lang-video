import argparse
import os

from core import configs,settings
from main import translate, voice_to_text, text_to_voice, silence_detection, utils

default_path = settings.DEFAULT_PATH


def convert_multi_lang(lang:str, video_path:str, audio_out_path:str, video_out_path:str):

    model_stt_path = configs.model_trans_path_dic[lang]
    
    voice_path = os.path.join(default_path, os.path.basename(video_path)[:-3] + "wav")
    
    print("1")
    #extract audio from video
    utils.voice_from_video(video_path, voice_path,sr=16000)

    print("1_denoise")
    #denoiser
    utils.denoiser(voice_path, voice_path)

    print("2")
    #split audio in silence part
    voice_split_paths, time_list, silence_list, first_silence = silence_detection.split(voice_path, default_path)
    print(first_silence)
    print(silence_list)
    print("3")
    #convert audio to text
    text_list = voice_to_text.voice_to_text_vosk(voice_split_paths, model_stt_path)
    print(text_list)
    #voice_to_text.voice_to_text_vosk(voice_path, text_path, model_trans_path)

    print("4")
    #convert every split text to translate-text
    #text_trans_list = translate.translate_text_func(text_list, lang)

    print("5")
    #convert every split translate-text to audio
    voice_list = text_to_voice.tts_gtts(text_list, time_list)

    print("6")
    #concatenate all split audio genrated with silence duration to each other
    text_to_voice.concatenate_speech(voice_list, time_list, silence_list, first_silence, audio_out_path)

    print("7")
    #replace generated audio in video
    utils.replace_audio_in_movie(video_path, audio_out_path, video_out_path)

    return 





if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", type=str, required=True)
    parser.add_argument("--video_path", type=str, required=True)
    parser.add_argument("--out_path", type=str, required=True)
    args = parser.parse_args()
    convert_multi_lang(parser.lang, parser.video_path, parser.out_path)