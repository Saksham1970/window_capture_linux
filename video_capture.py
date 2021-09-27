import cv2
from window import Window

import time
import settings

duration = settings.duration
target_search = settings.target_search

def save_video(window,video_name,duration,fps):
    
    now = time.time()
    
    frame = window.capture_cv2im
    
    height, width, layers = frame.shape
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    
    time_taken = time.time() -now
    maximum_fps = (1/time_taken)/2
    if maximum_fps < fps:
        fps = maximum_fps
        print("video fps limiting factor:", maximum_fps)
    video = cv2.VideoWriter(video_name, fourcc, fps, (width,height))    
    video.write(frame)
    now2 = now + 1/fps 
    while True:
    
        if time.time() > now+duration:
            cv2.destroyAllWindows()
            video.release()
            break
        elif time.time() >= now2 :
            now2 = now2 + 1/fps
            frame = window.capture_cv2im
            video.write(frame)
   
if __name__ == "__main__":
    now = time.time()
    while True:
        window= Window.fromTitle(target_search)
        if window:    
            print("got window")
            window = window[0]
            break
        elif time.time() > now+duration:
            print(duration, "expired")
            raise TimeoutError
    duration = duration - (time.time() - now)
    save_video(window,"video.avi",10,20)