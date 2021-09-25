from moviepy.editor import *
import os
from threading import Thread
def vc():
    os.system("python3 /home/lakshay/PycharmProjects/SakshamTestProject/video_capture.py")
def ac():
    os.system("python3 /home/lakshay/PycharmProjects/SakshamTestProject/audio_capture.py")
t1 = Thread(target = vc) 
t2 = Thread(target = ac)


t1.start()
t2.start()

t1.join()
t2.join()

clip = VideoFileClip("video.avi")
audioclip = AudioFileClip("sound.wav")
  
# adding audio to the video clip
videoclip = clip.set_audio(audioclip)

videoclip.write_videofile("final.mp4")