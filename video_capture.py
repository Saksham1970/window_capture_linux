import cv2
import numpy as np
from window import Window

import time
import settings
from threading import Thread

duration = settings.duration
target_search = settings.target_search

image_list = []

def blank_cv2_image(height,width):
    ar = np.array([0]*(height*width*3))
    ar.resize(height,width,3)
    ar = ar.astype(np.uint8)
    return ar

def video_write_image_list(video_writer):
    global image_list
    while True:
        if image_list:
            image = image_list.pop(0)
            if type(image) == type(None):
                cv2.destroyAllWindows()
                video_writer.release()
                break
            video_writer.write(image)

def record_video(window,duration,fps,filename = "video",extension = "avi", fourcc = cv2.VideoWriter_fourcc(*'XVID')):

    global image_list
    now = now2 = time.time()
    now3 = None
    maximum_fps = None
    h = w = None
    blank  = None
    thread =None
    while True:
        if time.time() >= now+duration:

            if now3:
                if maximum_fps:
                    image_list += [blank]*int(fps*(time.time() - now3))
                else:
                    # Didnt get window after the whole duration
                    h,w = 50,50 #setting manually
                    blank = blank_cv2_image(h,w)
                    image_list += [blank]*int(fps*(duration))
                    video_writer = cv2.VideoWriter(filename +"."+extension, fourcc, fps, (w,h))
                    thread = Thread(target = video_write_image_list, args = (video_writer,))
                    thread.start()
            image_list += [None]
            thread.join()
            break
        elif time.time() >= now2:
            frame = None
            now2 = time.time()
            if isinstance(window,Window):
                try:
                    frame = window.capture_cv2im
                except:
                    pass
            elif isinstance(window,str):
                window2 = Window.fromTitle(window)
                if window2:
                    print("got the window")
                    window = window2[0]    
                    frame = window.capture_cv2im
            else:
                raise "Window arg takes either Window() or application name (str())"
            if type(frame) != type(None):
                if not maximum_fps:
                    time_taken = time.time() -now2
                    h,w,c = frame.shape
                    blank = blank_cv2_image(h,w)
                    maximum_fps = (1/time_taken)/2
                    if maximum_fps < fps:
                        fps = maximum_fps
                        print("Hardware limiting factor, FPS set:", maximum_fps)
                    video_writer = cv2.VideoWriter(filename +"."+extension, fourcc, fps, (w,h))
                    thread = Thread(target = video_write_image_list, args = (video_writer,))
                    thread.start()

                if now3:
                    image_list += [blank]*int(fps*(time.time() - now3))
                    now3 = None
                image_list += [blank]*int(fps*(time.time() - now2 - 1/fps))
                image_list.append(frame)
                now2 += 1/fps

            else:
                if not now3: now3 = time.time()
    
if __name__ == "__main__":
    record_video("youtube",10,10)