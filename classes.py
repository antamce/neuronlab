import pyglet
import time
from pyglet import image
from pyglet.event import EventDispatcher


class HelloWorldWindow(pyglet.window.Window):
    def __init__(self, spike_times, width, height):
        super().__init__(width, height)
        self.plot_sprite = pyglet.sprite.Sprite(image.load('png/empty.png'), -29, 60) 
        self.plot_wait = pyglet.sprite.Sprite(image.load('png/empty.png'),0, 0)
        self.window_batch = pyglet.graphics.Batch()
        self.wire_picture_exc_1 =pyglet.sprite.Sprite(image.load('png/wires/1-end.png'), 0, 0, batch=self.window_batch)
        self.wire_picture_exc_2 =pyglet.sprite.Sprite(image.load('png/empty.png'), 0, 0, batch=self.window_batch)
        self.wire_picture_exc_3 =pyglet.sprite.Sprite(image.load('png/empty.png'), 0, 0, batch=self.window_batch)
        self.wire_picture_inh_1 =pyglet.sprite.Sprite(image.load('png/wires_inh/1-end.png'), 0, 0, batch=self.window_batch)
        self.wire_picture_inh_2 =pyglet.sprite.Sprite(image.load('png/empty.png'), 0, 0, batch=self.window_batch)
        self.wire_picture_inh_3 =pyglet.sprite.Sprite(image.load('png/empty.png'), 0, 0, batch=self.window_batch)
        self.spike_times = spike_times
        self.keye = "NMDA"
        self.keyi = "GABAA"
    def on_draw(self):
        pass
    def update_pic(self, picture):
        pass
    def update_wait(self, picture):
        pass

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
    def __init__(self, e_list, i_list) -> None:
        super().__init__()
        self._e_list = e_list
        self._i_list = i_list
        self._proc = None
    def count_(self):
        pass
    @property
    def e_list(self):
        return self._e_list
    @e_list.setter
    def e_list(self,value):
        self._e_list = value
    @property
    def i_list(self):
        return self._i_list
    @i_list.setter
    def i_list(self,value):
        self._i_list = value
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
        
        

MySlider.register_event_type('on_mouse_drag')
MySlider.register_event_type('on_change')
MySlider.register_event_type('on_mouse_press')
MySlider.register_event_type('on_mouse_release')
SliderDispathcher.register_event_type('slider_activate')
SliderDispathcher.register_event_type('slider_deactivate')
HelloWorldWindow.register_event_type('update_pic')
HelloWorldWindow.register_event_type('update_wait')
MyEventDisp.register_event_type('count_d')
MyEventDisp.register_event_type('update')
Counter.register_event_type('count_')
Counter.register_event_type('drawing_plot')
