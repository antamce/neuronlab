import pyglet
from pyglet.window import key
from pyglet.window import mouse
from pyglet import image
from subprocess import Popen
import classes
import utils

e_list = []
i_list = []
spike_times = [0, 0, 0, 0, 0, 0]
runtime_constant = 9.99

background = pyglet.graphics.Group(order=0)
foreground = pyglet.graphics.Group(order=1)

batch = pyglet.graphics.Batch()
spike_time_batch = pyglet.graphics.Batch()
undrawable = pyglet.graphics.Batch()
batch_background = pyglet.graphics.Batch()


calculator = classes.Counter(e_list, i_list)
endofcalcdisp = classes.MyEventDisp()
window = classes.HelloWorldWindow(spike_times, width=1100, height=750)
sldisp = classes.SliderDispathcher()
calc_button = pyglet.gui.PushButton(825, 10, pyglet.resource.image('png/excitatory_slider.png'), pyglet.resource.image('png/inhibitory_slider.png'), batch=batch, group=foreground)
cache_clear_button = pyglet.gui.PushButton(825, 48, pyglet.resource.image('png/excitatory_small.png'), pyglet.resource.image('png/inhibitory_small.png'), batch=batch, group=foreground)
cache_button = pyglet.gui.PushButton(954, 48, pyglet.resource.image('png/excitatory_small.png'), pyglet.resource.image('png/inhibitory_small.png'), batch=batch, group=foreground)
cache_picture =  pyglet.sprite.Sprite(image.load('png/empty.png'), -37, 7, batch=undrawable, group=foreground)
side_panel = pyglet.sprite.Sprite(image.load('png/side_panel.png'), 800, 0, batch=batch_background, group=background)
scope = pyglet.sprite.Sprite(image.load('png/scope.png'), 0, 0, batch=batch_background, group=background)
neuron_pic = pyglet.sprite.Sprite(image.load('png/mirror.png'), 0, 270, batch=batch_background, group=background)

Text_input_explanation = pyglet.text.Label('Threshold:', color=(30, 30, 30, 255), x=825, y=100, batch=batch_background, group=background)
text_entry = pyglet.gui.TextEntry('-40', 1000, 100, 50, color=(30, 30, 30, 255), text_color=(211,211,211,255), caret_color=(211,211,211,255), batch=batch, group=foreground)

slider_e_1 = classes.MySlider(825, 692, base=pyglet.resource.image('png/excitatory_slider.png'), knob=pyglet.resource.image('png/knob_grey.png'), edge=5, batch=batch)
slider_e_2 = classes.MySlider(825, 612, base=pyglet.resource.image('png/excitatory_slider.png'), knob=pyglet.resource.image('png/knob_grey.png'), edge=5, batch=undrawable, enabled=False)
slider_e_3 = classes.MySlider(825, 532, base=pyglet.resource.image('png/excitatory_slider.png'), knob=pyglet.resource.image('png/knob_grey.png'), edge=5, batch=undrawable, enabled =False)
slider_i_1 = classes.MySlider(825, 452, base=pyglet.resource.image('png/inhibitory_slider.png'), knob=pyglet.resource.image('png/knob_grey.png'), edge=5, batch=batch)
slider_i_2 = classes.MySlider(825, 372, base=pyglet.resource.image('png/inhibitory_slider.png'), knob=pyglet.resource.image('png/knob_grey.png'), edge=5, batch=undrawable, enabled =False)
slider_i_3 = classes.MySlider(825, 292, base=pyglet.resource.image('png/inhibitory_slider.png'), knob=pyglet.resource.image('png/knob_grey.png'), edge=5, batch=undrawable, enabled =False)

pyglet.gui.TextEntry.register_event_type('on_text_motion_select')
pyglet.gui.TextEntry.register_event_type('on_text_motion')
pyglet.gui.TextEntry.register_event_type('on_mouse_drag')
pyglet.gui.TextEntry.register_event_type('on_text')
pyglet.gui.TextEntry.register_event_type('on_mouse_press')
pyglet.gui.TextEntry.register_event_type('on_commit')
pyglet.gui.PushButton.register_event_type('on_mouse_press')
pyglet.gui.PushButton.register_event_type('on_mouse_release')
pyglet.gui.PushButton.register_event_type('on_mouse_drag')
pyglet.gui.PushButton.register_event_type('on_press')
pyglet.gui.PushButton.register_event_type('on_release')

def clear_window(slider, sldisp):
    sldisp.dispatch_event('slider_activate', slider, undrawable)
    slider.value = 0
    slider.enabled = False

def add_spike_time(n, list_, spike_time):
    if len(list_) >= n:
            list_[n-1] = spike_time
    else: 
        list_.append(spike_time) 

def null(array):
        leng = len(array)
        for n in array:
            if not isinstance(n, int):
                n.text = ''
        array =  [0]*leng
def off_on(gui_list, boolean_value):
    for elem in gui_list:
        elem.enabled = boolean_value

@calc_button.event
def on_release():
    calculator.dispatch_event('count_')
@cache_button.event
def on_release():
    cache_picture.image = image.load('png/plotting_c.png')
    window.dispatch_event('update_pic', image.load('png/empty.png'))
    cache_picture.batch = batch
@cache_clear_button.event
def on_release():
    cache_picture.batch = undrawable
    
@calculator.event
def count_():
    window.dispatch_event('update_pic', image.load('png/wait.png'))
    calculator.proc = Popen(utils.Encoder.popen_generator(calculator.e_list, calculator.i_list, text_entry.value))
    pyglet.clock.schedule_interval(update, 1/2) 
    #temporary running block
    off_on([ slider_e_1, slider_e_2, slider_e_3, slider_i_1, slider_i_2, slider_i_3,text_entry, calc_button, cache_button, cache_clear_button], False)
   
@endofcalcdisp.event
def update(dt):
    try: 
        if calculator.proc.poll() != None:
            pyglet.clock.schedule_interval(drawing_plot, 1/30, picture=image.load('png/plotting.png'))
            
            pyglet.clock.unschedule(update)
    except BaseException:
        pass   


@endofcalcdisp.event
def drawing_plot(dt, picture):
    endofcalcdisp.count += 1
    if endofcalcdisp.count <= picture.width:
        part_plot = picture.get_region(0, 0, endofcalcdisp.count, picture.height)
        window.dispatch_event('update_pic', part_plot)
    else: 
        window.dispatch_event('update_pic', picture)
        endofcalcdisp.count = 0
        calculator.e_list =  []
        calculator.i_list =  []
        null(window.spike_times)
        slider_e_1.value = 0
        slider_i_1.value = 0
        clear_window(slider_e_2, sldisp)
        clear_window(slider_e_3, sldisp)
        clear_window(slider_i_2, sldisp)
        clear_window(slider_i_3, sldisp)
        spike_time_batch.invalidate()
        window.wire_picture_exc_1.image = image.load('png/wires/1-end.png')
        window.wire_picture_exc_2.image = image.load('png/empty.png')
        window.wire_picture_exc_3.image = image.load('png/empty.png')
        window.wire_picture_inh_1.image = image.load('png/wires_inh/1-end.png')
        window.wire_picture_inh_2.image = image.load('png/empty.png')
        window.wire_picture_inh_3.image = image.load('png/empty.png')
        #temporary running block removal
        off_on([ slider_e_1, slider_e_2, slider_e_3, slider_i_1, slider_i_2, slider_i_3,text_entry, calc_button, cache_button, cache_clear_button], True)
        pyglet.clock.unschedule(drawing_plot)

@slider_e_1.event
def on_change(val):
    spike_time = int(round(val*runtime_constant, 0))
    add_spike_time(1, calculator.e_list, spike_time)
    window.spike_times[0]= (pyglet.text.Label(f'excitatory: {str(spike_time)}', color=(211,211,211,255), x=830, y=675, batch=spike_time_batch))
    sldisp.dispatch_event('slider_activate', slider_e_2, batch)

@slider_e_2.event
def on_change(val):
    spike_time = int(round(val*runtime_constant, 0))
    add_spike_time(2, calculator.e_list, spike_time)
    window.spike_times[1]= (pyglet.text.Label(f'excitatory: {str(spike_time)}', color=(211,211,211,255), x=830, y=595, batch=spike_time_batch))
    sldisp.dispatch_event('slider_activate', slider_e_3, batch)
    window.wire_picture_exc_1.image = image.load('png/wires/1-2.png')
    window.wire_picture_exc_2.image = image.load('png/wires/2-end.png')
@slider_e_3.event
def on_change(val):
    spike_time = int(round(val*runtime_constant, 0))
    add_spike_time(3, calculator.e_list, spike_time)
    window.spike_times[2]= (pyglet.text.Label(f'excitatory: {str(spike_time)}', color=(211,211,211,255), x=830, y=515, batch=spike_time_batch))
    window.wire_picture_exc_3.image = image.load('png/wires/2-3.png')
    window.wire_picture_exc_2.image = image.load('png/wires/3-end.png')
@slider_i_1.event
def on_change(val):
    spike_time = int(round(val*runtime_constant, 0))
    add_spike_time(1, calculator.i_list, spike_time)
    window.spike_times[3]= (pyglet.text.Label(f'inhibitory: {str(spike_time)}', color=(211,211,211,255), x=830, y=435, batch=spike_time_batch))
    sldisp.dispatch_event('slider_activate', slider_i_2, batch)

@slider_i_2.event
def on_change(val):
    spike_time = int(round(val*runtime_constant, 0))
    add_spike_time(2, calculator.i_list, spike_time)
    window.spike_times[4]= (pyglet.text.Label(f'inhibitory: {str(spike_time)}', color=(211,211,211,255), x=830, y=355, batch=spike_time_batch))
    sldisp.dispatch_event('slider_activate', slider_i_3, batch)
    window.wire_picture_inh_1.image = image.load('png/wires_inh/1-2.png')
    window.wire_picture_inh_2.image = image.load('png/wires_inh/2-end.png')
@slider_i_3.event
def on_change(val):
    spike_time = int(round(val*runtime_constant, 0))
    add_spike_time(3, calculator.i_list, spike_time)
    window.spike_times[5]= (pyglet.text.Label(f'inhibitory: {str(spike_time)}', color=(211,211,211,255), x=830, y=275, batch=spike_time_batch))
    window.wire_picture_inh_3.image = image.load('png/wires_inh/2-3.png')
    window.wire_picture_inh_2.image = image.load('png/wires_inh/3-end.png')
@text_entry.event
def on_commit(text):
    text_entry.value = text

@window.event
def update_pic(picture):
    window.plot_sprite.image = picture
@window.event
def on_draw():
    window.clear()
    batch_background.draw()
    window.plot_sprite.draw()
    window.window_batch.draw()
    batch.draw()
    spike_time_batch.draw()
@window.event
def on_mouse_press(x, y, button, modifiers):
    slider_i_1.dispatch_event('on_mouse_press', x, y, button, modifiers)
    slider_i_2.dispatch_event('on_mouse_press', x, y, button, modifiers)
    slider_i_3.dispatch_event('on_mouse_press', x, y, button, modifiers)
    slider_e_1.dispatch_event('on_mouse_press', x, y, button, modifiers)
    slider_e_2.dispatch_event('on_mouse_press', x, y, button, modifiers)
    slider_e_3.dispatch_event('on_mouse_press', x, y, button, modifiers)
    text_entry.dispatch_event('on_mouse_press', x, y, button, modifiers)
    calc_button.dispatch_event('on_mouse_press', x, y, button, modifiers)
    cache_button.dispatch_event('on_mouse_press', x, y, button, modifiers)
    cache_clear_button.dispatch_event('on_mouse_press', x, y, button, modifiers)
@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    slider_i_1.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    slider_i_2.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    slider_i_3.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    slider_e_1.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    slider_e_2.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    slider_e_3.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    text_entry.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
@window.event
def on_mouse_release(x, y, buttons, modifiers):
    slider_i_1.dispatch_event('on_mouse_release', x, y, buttons, modifiers)
    slider_i_2.dispatch_event('on_mouse_release', x, y, buttons, modifiers)
    slider_i_3.dispatch_event('on_mouse_release', x, y, buttons, modifiers)
    slider_e_1.dispatch_event('on_mouse_release', x, y, buttons, modifiers)
    slider_e_2.dispatch_event('on_mouse_release', x, y, buttons, modifiers)
    slider_e_3.dispatch_event('on_mouse_release', x, y, buttons, modifiers)
    calc_button.dispatch_event('on_mouse_release', x, y, buttons, modifiers)
    cache_button.dispatch_event('on_mouse_release', x, y, buttons, modifiers)
    cache_clear_button.dispatch_event('on_mouse_release', x, y, buttons, modifiers)
@window.event
def on_text(text):
    text_entry.dispatch_event('on_text', text)
@window.event
def on_text_motion(motion):
    text_entry.dispatch_event('on_text_motion', motion)

pyglet.app.run()

# надо будет cделать нормальные проверки на все running 