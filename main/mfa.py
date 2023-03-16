import subprocess
import os
import textgrid

from core import settings

def mfa_audio(input_folder:str, out_folder:str):

    lexicon_path = settings.LEXICAN_PATH
    acoustic_path = settings.ACOUSTIC_PATH

    cmd = f'. {settings.CONDA_PATH} && conda activate aligner && mfa align --clean {input_folder} {lexicon_path} {acoustic_path} {out_folder}'
    p = subprocess.Popen(cmd, shell=True, executable='/bin/bash')
    p.communicate()
    tg_path = os.path.join(out_folder,os.listdir(out_folder)[0])
    tg = textgrid.TextGrid.fromFile(tg_path)[0]

    return tg


def silence_duration(tg:object):

    last_break_time = 0
    time_list = []
    sent = ""
    text_list = []
    silence_list = []
    silence_thresh = 2

    for i in range(len(tg)):

        sent += tg[i].mark
        max_time = tg[i].maxTime
        min_time = tg[i].minTime

        if (tg[i]== "" and (max_time - min_time > silence_thresh)) or  i==(len(tg)-1):

            time_list.append(max_time - last_break_time)
            silence_list.append(max_time - min_time)
            text_list.append(sent)

            last_break_time = max_time
            sent = ""

    return text_list, time_list, silence_list
