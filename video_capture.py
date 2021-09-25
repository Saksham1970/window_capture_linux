import gi
import cv2
import numpy as np

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk
from gi.repository import GdkX11

gi.require_version('Wnck', '3.0')
from gi.repository import Wnck

from PIL import Image
import time
import settings

duration = settings.duration
target_search = settings.target_search



def pixbuf2pil(pix): 
    data = pix.get_pixels()
    w = pix.props.width
    h = pix.props.height
    stride = pix.props.rowstride
    mode = "RGB"
    if pix.props.has_alpha == True:
        mode = "RGBA"
    im = Image.frombytes(mode, (w, h), data, "raw", mode, stride)
    return im

def pixbuf2cv(pix):
    pil_image = pixbuf2pil(pix)
    pil_image = pil_image.convert('RGB') 
    open_cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    return open_cv_image

def get_gdk_window(target):
    def get_wnck_winlist():
        """
        Get the window list and the active workspace.
        """
        scr = Wnck.Screen.get_default()
        scr.force_update()
        windows = scr.get_windows()
        active_wspace = scr.get_active_workspace()

        return windows, active_wspace

    wlist, active_wspace = get_wnck_winlist()

    for wnck_window in wlist:
        if wnck_window.is_visible_on_workspace(active_wspace):
            if target_search in wnck_window.get_name().lower():
                break
    else:
        wnck_window = None

    if wnck_window:
        xlib_window = wnck_window.get_xid()
        gdk_display = GdkX11.X11Display.get_default()
        gdk_window = GdkX11.X11Window.foreign_new_for_display(gdk_display, xlib_window)
        return gdk_window
    else:
        return None

def gdk_window_pixbuf(gdk_window):
    x,y, w,h = gdk_window.get_geometry()
    return Gdk.pixbuf_get_from_window(gdk_window, 0,0, w,h)
    



def save_video(gdk_window,video_name,duration,fps):
    pb = gdk_window_pixbuf(gdk_window)
    frame = pixbuf2cv(pb)
    
    height, width, layers = frame.shape
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    video = cv2.VideoWriter(video_name, fourcc, fps, (width,height))
    
    video.write(frame)
    now = time.time()
    now2 = now
    while True:
        
        if time.time() > now+duration:
            cv2.destroyAllWindows()
            video.release()
            break
        elif time.time() >= now2 + 1/fps:
            now2 = now2 + 1/fps
            pb = gdk_window_pixbuf(gdk_window)
            frame = pixbuf2cv(pb)
            video.write(frame)


if __name__ == "__main__":

    now = time.time()
    while True:
        gdk_window= get_gdk_window(target_search)
        if gdk_window:    
            print("got window")
            break
        elif time.time() > now+duration:
            print(duration, "expired")
            raise TimeoutError
    duration = duration - (time.time() - now)
    save_video(gdk_window,"video.avi",10,20)