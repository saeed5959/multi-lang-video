from pydub import AudioSegment, silence
import os

def split(voice_path:str, default_path:str):

    voice = AudioSegment.from_wav(voice_path)

    silence_time = silence.detect_silence(voice, min_silence_len=500, silence_thresh=-45)
    print(silence_time)
    voice_split_paths = []
    time_list = []
    silence_list = []

    if silence_time[0][0]>1000:
        silence_time = [[0,0]] + silence_time

    first_silence = silence_time[0][1]
        

    for count in range(len(silence_time)-1):

        voice_split_path = os.path.join(default_path, f"{count}.wav")
        voice[silence_time[count][1]:silence_time[count+1][0]].export(voice_split_path,format="wav")
        
        voice_split_paths.append(voice_split_path)
        time_list.append(silence_time[count+1][0] - silence_time[count][1])
        silence_list.append(silence_time[count+1][1] - silence_time[count+1][0])

    return voice_split_paths, time_list, silence_list, first_silence