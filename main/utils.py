import moviepy.editor
import os
import subprocess
import shutil
import librosa
import soundfile as sf

from core import settings

default_path = settings.DEFAULT_PATH

def voice_from_video(video_path:str, voice_path:str, sr=22050):

    video = moviepy.editor.VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(voice_path,sr)
    wav,sr = librosa.load(voice_path,sr=sr)
    sf.write(voice_path,wav,sr)
    
    return

def trim_video(video_path:str, first_time:int, last_time:int, out_path:str):

    video = moviepy.editor.VideoFileClip(video_path)

    clip1 = video.subclip(first_time, last_time)
    clip1.write_videofile(out_path)

def replace_audio_in_movie(video_path:str, audio_path:str, video_path_out:str):

    audio = moviepy.editor.AudioFileClip(audio_path)
    video = moviepy.editor.VideoFileClip(video_path)

    final_video = video.set_audio(audio)
    final_video.write_videofile(video_path_out)

def denoiser(voice_path:str, out_path:str):

    denoise_in_folder = os.path.join(default_path,"in")
    os.mkdir(denoise_in_folder)
    denoise_out_folder = os.path.join(default_path,"out")
    os.mkdir(denoise_out_folder)

    shutil.copy(voice_path,denoise_in_folder)

    cmd = f'python3 -m denoiser.enhance --dns64 --noisy_dir {denoise_in_folder} --out_dir {denoise_out_folder}'
    p = subprocess.Popen(cmd, shell=True, executable='/bin/bash')
    p.communicate()

    shutil.copy(os.path.join(denoise_out_folder, os.path.basename(voice_path)[:-4] + "_enhanced.wav"), out_path)
    
    shutil.rmtree(denoise_in_folder)
    shutil.rmtree(denoise_out_folder)