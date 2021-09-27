from moviepy.editor import *
import os
from threading import Thread
import pathlib
import audio_capture
import settings
dir = pathlib.Path(__file__).parent.resolve()

def vc():
    os.system(f'python3 {os.path.join(dir,"video_capture.py")}')

t1 = Thread(target = vc) 
t2 = Thread(target = audio_capture.record_audio_wav,args=(settings.target_search,settings.duration,"sound"))


t1.start()
t2.start()

t1.join()
t2.join()

clip = VideoFileClip("video.avi")
audioclip = AudioFileClip("sound.wav")
  
# adding audio to the video clip
videoclip = clip.set_audio(audioclip)

videoclip.write_videofile("final.mp4")