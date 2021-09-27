import os
from threading import Thread
import pathlib
import audio_capture , video_capture
import settings
from window import Window

dir = pathlib.Path(__file__).parent.resolve()


window_list = Window.fromTitle(settings.target_search)

if window_list:
    window = window_list[0]#TODO: make user selection if more than one
else:
    window = settings.target_search


t1 = Thread(target = video_capture.record_video, args=(window,settings.duration,settings.video_fps,settings.video_file_name,settings.video_ext))


sil = audio_capture.sinkInputList_by_applicationName(settings.target_search)
if sil:
    sinkinput = sil[0] #TODO: make user selection if more than one
    t2 = Thread(target=audio_capture.record_sink_to_wav,args=(sinkinput,settings.duration,settings.audio_file_name,settings.audio_fps,settings.channels,settings.depth))

else:
    t2 = Thread(target = audio_capture.record_audio_wav,args=(settings.target_search,settings.duration,settings.audio_file_name,settings.audio_fps,settings.channels,settings.depth))


t1.start()
t2.start()

t1.join()
t2.join()

  
os.system(f"ffmpeg -y -i {settings.video_file_name}.{settings.video_ext} -i {settings.audio_file_name}.wav -map 0:v -map 1:a -c:v copy -shortest {settings.final_file_name}.mp4")