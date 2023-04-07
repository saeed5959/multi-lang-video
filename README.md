# Multi Language Video
## Convert your native language video to English language video 

### Let your video be an international video without need to a subtitle
# 


### Pipleline

    1-extract audio from video
    2-convert audio to text
    3-give audio and text to MFA to get time of any words in audio
    4-detect silence speech for splitting audio : time and duration
    5-convert every split text to translate-text
    6-convert every split translate-text to audio
    7-concatenate all split audio genrated with silence duration to each other

### Problems

    1-MFA result is not good for silence parts : using a silence detector library 
    2-background song : using a denoiser
    3-online speech to text is not accurate : using VOSK that is offline and more accurate
     