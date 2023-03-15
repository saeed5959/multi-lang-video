


def len_text_no_punc(text:str):

    all_punc = [",",":","\.","\?","!",";","@", "\*", "\/", "\+","\(","\)","\[","\]"]
    for punc in all_punc:
        text = re.sub(punc,"",text)

    return len(text.split())

def split_text_max_word(text:str):

    text_list = text.split() 
    words = ""
    text_split = []
    for i, word in enumerate(text_list):
        words += word + " "
        if (i+1) % settings.MAX_NUM_WORDS==0 or i==len(text_list)-1:
            text_split.append(words)
            words = ""

    return text_split

def split_text(text:str):

    text_list = [sent+" ." for sent in text.split(".")[:-1]]


    text_split = []
    for sent in text_list:

        if len(sent.split()) < settings.MAX_NUM_WORDS:
            text_split.append(sent)
        else:
            sents_split = split_text_max_word(sent)
            for sent_split in sents_split:
                text_split.append(sent_split)

    # determin min number of words 
    for i, text_ in reversed(list(enumerate(text_split))):
        if len_text_no_punc(text_) <= settings.MIN_NUM_WORDS:       
            text_split[i-1] = text_split[i-1] + text_split[i] 
            del text_split[i]

    break_indexs = []
    count = 0
    for sent in text_split:
        count += len_text_no_punc(sent)
        break_indexs.append(count)

    return text_split,break_indexs

def mfa(voice_path:str,text:str):

    lexicon_path = settings.LEXICAN_PATH
    acoustic_path = settings.ACOUSTIC_PATH
    out_folder = tempfile.TemporaryDirectory()
    input_folder = tempfile.TemporaryDirectory()

    shutil.copy(voice_path,input_folder.name)
    text_path = os.path.join(input_folder.name,os.path.basename(voice_path)[:-3]+"txt")
    with open(text_path,"w") as file:
        file.write(text)

    cmd = f'. {settings.CONDA_PATH} && conda activate aligner && mfa align --clean {input_folder.name} {lexicon_path} {acoustic_path} {out_folder.name}'
    p = subprocess.Popen(cmd, shell=True, executable='/bin/bash')
    p.communicate()
    tg_path = os.path.join(out_folder.name,os.listdir(out_folder.name)[0])
    tg = textgrid.TextGrid.fromFile(tg_path)[0]

    return tg

def detect_split_times_sub(voice_path:str, text:str):
    tg = mfa(voice_path, text)

    last_break_time = 0
    split_times = []
    sent = ""
    text_list = []

    for i in range(len(tg)):
        sent += tg[i].mark
        break_time = tg[i].maxTime
        if (tg[i]== "" and (break_time-last_break_time)>8) or  i==(len(tg)-1):
            split_times.append(break_time)
            last_break_time = break_time

            text_list.append(sent)
            sent = ""

    return split_times, text_list


def detect_split_times(voice_path:str, text:str):
    tg = mfa(voice_path, text)
    text_list, break_indexs = split_text(text)

    tg_list = [tg[i].maxTime for i in range(len(tg)) if tg[i].mark != ""]

    split_times = [tg_list[break_index-1] for break_index in break_indexs]
    return split_times, text_list


def split_voice(voice_path:str,text:str,output_folder:str):

    split_times, text_list = detect_split_times(voice_path,text)

    wav, sr = librosa.load(voice_path)
    voice_list = []

    for count in range(len(split_times)):
        if count==0:
            voice_name = tempfile.NamedTemporaryFile(suffix=".wav")
            voice_name.close()
            out_path = os.path.join(output_folder, os.path.basename(voice_name.name))
            sf.write(out_path,wav[:int(split_times[count]*sr)], sr)
            voice_list.append({"file":out_path,"text":text_list[count]})

        else: 
            voice_name = tempfile.NamedTemporaryFile(suffix=".wav")
            voice_name.close()
            out_path = os.path.join(output_folder,os.path.basename(voice_name.name))
            sf.write(out_path,wav[int(split_times[count-1]*sr):int(split_times[count]*sr)], sr)
            voice_list.append({"file":out_path,"text":text_list[count]})

    return voice_list    
