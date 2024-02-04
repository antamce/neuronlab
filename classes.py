import pyglet
import time
from pyglet import image
from pyglet.event import EventDispatcher
import os

class HelloWorldWindow(pyglet.window.Window):
    def __init__(self, spike_times, width, height, cachefilepath=''):
        super().__init__(width, height)
        self.plot_sprite = pyglet.sprite.Sprite(image.load('png/plotting/empty.png'), -110, 75) 
        self.plot_wait = pyglet.sprite.Sprite(image.load('png/plotting/empty.png'),0, 0)
        self.plot_cache = pyglet.sprite.Sprite(image.load('png/plotting/empty.png'),-110, 75)
        self.window_batch = pyglet.graphics.Batch()
        self._spike_times = spike_times
        self.cachefilepath = cachefilepath
    def on_draw(self):
        pass
    def update_pic(self, picture):
        pass
    def update_wait(self, picture):
        pass
    def update_cache(self, picture):
        pass
    def close(self):
        """Close the window.

        After closing the window, the GL context will be invalid.  The
        window instance cannot be reused once closed (see also `set_visible`).

        The `pyglet.app.EventLoop.on_window_close` event is dispatched on
        `pyglet.app.event_loop` when this method is called.
        """
        if os.path.isfile(self.cachefilepath):
                    os.remove(self.cachefilepath)
        from pyglet import app
        if not self._context:
            return
        app.windows.remove(self)
        self._context.destroy()
        self._config = None
        self._context = None
        if app.event_loop:
            app.event_loop.dispatch_event('on_window_close', self)
        self._event_queue = []
        
    @property
    def spike_times(self):
        return self._spike_times
    @spike_times.setter
    def spike_times(self,value):
        self._spike_times = value


class MyEventDisp(EventDispatcher):
    
    def __init__(self) -> None:
        super().__init__()
        self.count = 0
    def count_d(self):
        pass
    def update(self, dt):
        pass
    def drawing_plot(self, dt, picture):
        pass

class Counter(EventDispatcher):
    def __init__(self, t_list, t_1_list, t_2_list, t_3_list, n=[0, 0, 0, 0], strengths=[[False, False, False, False],[False, False, False, False],[False, False, False, False],[False, False, False, False]], cache=False) -> None:
        super().__init__()
        self.n = n
        self.cache = cache
        self.strengths = strengths
        self._t_list = t_list
        self.t_1_list = t_1_list
        self.t_2_list = t_2_list
        self.t_3_list = t_3_list
        self._proc = None
    def count_(self):
        pass
    @property
    def t_list(self):
        return self._t_list
    @t_list.setter
    def t_list(self,value):
        self._t_list = value
    @property
    def t_1_list(self):
        return self._t_1_list
    @t_1_list.setter
    def t_1_list(self,value):
        self._t_1_list = value
    @property
    def t_2_list(self):
        return self._t_2_list
    @t_2_list.setter
    def t_2_list(self,value):
        self._t_2_list = value
    @property
    def t_3_list(self):
        return self._t_3_list
    @t_3_list.setter
    def t_3_list(self,value):
        self._t_3_list = value
    @property
    def proc(self):
        return self._proc
    @proc.setter
    def proc(self,value):
        self._proc = value

class MySlider(pyglet.gui.Slider):
    def __init__(self, x, y, base, knob, edge=0, batch=None, group=None, runconstant = 9.99, enabled=True):
        super().__init__(x, y, base, knob, edge, batch, group)
        self._runconstant = runconstant
        self.enabled = enabled
    def on_mouse_release(self, x, y, buttons, modifiers):
        if not self.enabled:
            return
        if self._check_hit(x, y):
            self.dispatch_event('on_change', self._value)
        self._in_update = False

    def change_pos_of_knob(self, x):
        self._knob_spr.x = max(self._min_knob_x, min(x - self._half_knob_width, self._max_knob_x))
        self._value = abs(((self._knob_spr.x - self._min_knob_x) * 100) / (self._min_knob_x - self._max_knob_x))

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if not self.enabled:
            return
        if self._in_update:
            self.change_pos_of_knob(x)

    def on_mouse_press(self, x, y, buttons, modifiers):
        if not self.enabled:
            return
        if self._check_hit(x, y):
            self._in_update = True
            self.change_pos_of_knob(x)

    def batch_change(self, new_batch):
        self._base_spr.batch = new_batch
        self._knob_spr.batch = new_batch

    def on_change(self, value):
        pass

    @property
    def _min_y(self):
        return self._y + self._edge


class SliderDispathcher(EventDispatcher):
    def __init__(self) -> None:
        super().__init__()
    def slider_activate(self, slider, new_batch):
        slider.batch_change(new_batch)
        slider.enabled = True
    def slider_deactivate(self, slider, new_batch):
        slider.batch_change(new_batch)
        slider.enabled = False
    
class Dropdown(pyglet.gui.PushButton):
    def __init__(self, x, y, pressed, depressed, hover=None, batch=None, group=None):
        super().__init__(x, y, pressed, depressed, hover, batch, group)
        self.openstate = True
    def batch_change(self, new_batch):
        self._sprite.batch = new_batch
    def pic_change_dep(self, new_picture):
        self._depressed_img = new_picture
        self._sprite.image = new_picture
    def pic_change_p(self, new_picture):
        self._pressed_img = new_picture

class Cacheholder():
    list_of_plots = []
    first_plot = []
    def __init__(self) -> None:
        pass
    @classmethod
    def add_plot(cls, plot):
        Cacheholder.list_of_plots.append(plot)
    @classmethod
    def set_first_plot(cls, plot):
        Cacheholder.first_plot.append(plot)

        

MySlider.register_event_type('on_mouse_drag')
MySlider.register_event_type('on_change')
MySlider.register_event_type('on_mouse_press')
MySlider.register_event_type('on_mouse_release')
SliderDispathcher.register_event_type('slider_activate')
SliderDispathcher.register_event_type('slider_deactivate')
HelloWorldWindow.register_event_type('update_pic')
HelloWorldWindow.register_event_type('update_wait')
HelloWorldWindow.register_event_type('update_cache')
MyEventDisp.register_event_type('count_d')
MyEventDisp.register_event_type('update')
Counter.register_event_type('count_')
Counter.register_event_type('drawing_plot')
