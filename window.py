import gi

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk
from gi.repository import GdkX11

gi.require_version('Wnck', '3.0')
from gi.repository import Wnck

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from PIL import Image
import numpy as np
import cv2

class Window():
    def __init__(self,x_id):
        self._x_id = x_id
        gdk_display = GdkX11.X11Display.get_default()
        self._gdk_window = GdkX11.X11Window.foreign_new_for_display(gdk_display, x_id)
        
        self._wnck_window = Wnck.Window.get(x_id)

    @classmethod
    def fromTitle(cls,title:str):
        title = title.lower()
        scr = Wnck.Screen.get_default()
        scr.force_update()
        while Gtk.events_pending():
            Gtk.main_iteration()
        windows = scr.get_windows()
        active_wspace = scr.get_active_workspace()
        x_ids = []
        for wnck_window in windows:
            if wnck_window.is_visible_on_workspace(active_wspace):
                if title in wnck_window.get_name().lower():
                    x_ids.append(wnck_window.get_xid())

        return [cls(x_id) for x_id in x_ids]

    # Properties
    @property
    def x_id(self):
        return self._x_id
    
    @property
    def title(self):
        return self._wnck_window.get_name()
    
    @property
    def process_id(self):
        return self._wnck_window.get_pid()

    @property
    def icon_name(self):
        return self._wnck_window.get_icon_name()

    @property
    def icon_pixbuf(self):
        return self._wnck_window.get_icon()

    @property
    def icon_pixels(self):
        return self.icon_pixbuf.get_pixels()
    
    @property
    def icon_PIL(self):
        return self.pixbuf_to_PIL(self.icon_pixbuf)
    
    @property
    def icon_pixels_array(self):
        return self.pixbuff_to_numpy(self.icon_pixbuf)
    
    @property
    def icon_cv2im(self):
        return self.array_to_cv2(self.icon_pixels_array)

    @property
    def height(self):
        return self._gdk_window.get_height()

    @property
    def width(self):
        return self._gdk_window.get_width()

    @property
    def position(self):
        return self._gdk_window.get_position()

    @property
    def capture_pixbuf(self):
        return Gdk.pixbuf_get_from_window(self._gdk_window, 0,0, self.width,self.height)

    @property
    def capture_pixels(self):
        return self.capture_pixbuf.get_pixels()
    
    @property
    def capture_PIL(self):
        return self.pixbuf_to_PIL(self.capture_pixbuf)
    
    @property
    def capture_pixels_array(self):
        return self.pixbuff_to_numpy(self.capture_pixbuf)
    
    @property
    def capture_cv2im(self):
        return self.array_to_cv2(self.capture_pixels_array)
    
    def pixbuf_to_PIL(self, pixbuff):
        data = pixbuff.get_pixels()
        w = pixbuff.props.width
        h = pixbuff.props.height
        stride = pixbuff.props.rowstride
        mode = "RGB"
        if pixbuff.props.has_alpha == True:
            mode = "RGBA"
        pil_image = Image.frombytes(mode, (w, h), data, "raw", mode, stride)
        return pil_image
    
    def pixbuff_to_numpy(self, pixbuff):
        p = pixbuff
        a = np.frombuffer(p.get_pixels(),dtype=np.uint8)
        w,h,c,r=(p.get_width(), p.get_height(), p.get_n_channels(), p.get_rowstride())
        if a.shape[0] == w*c*h:
            return a.reshape( (h, w, c) )
        else:
            b=np.zeros((h,w*c),'uint8')
            for j in range(h):
                b[j,:]=a[r*j:r*j+w*c]
            return b.reshape( (h, w, c) )
    
    def array_to_cv2(self, array):
        array = array[:,:,:3] #remove alpha
        open_cv_image = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
        return open_cv_image

if __name__ == "__main__":
    
    while True:
        chrome = Window.fromTitle("chrome")
        chrome =chrome[0]
        print(chrome.title)
    
