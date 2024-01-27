import pyglet
from pyglet.window import key
from pyglet.window import mouse
from pyglet import image
from subprocess import Popen
import classes
import utils

t_list = []
t_1_list = []
t_2_list = []
t_3_list = []
spike_times = [0, 0, 0, 0, 0, 0]
runtime_constant = 9.99

background = pyglet.graphics.Group(order=0)
foreground = pyglet.graphics.Group(order=1)

batch = pyglet.graphics.Batch()
spike_time_batch = pyglet.graphics.Batch()
undrawable = pyglet.graphics.Batch()
batch_background = pyglet.graphics.Batch()

calculator = classes.Counter(t_list, t_1_list, t_2_list, t_3_list)
endofcalcdisp = classes.MyEventDisp()
window = classes.HelloWorldWindow(spike_times, width=1920, height=1080)
sldisp = classes.SliderDispathcher()
calc_button = pyglet.gui.PushButton(1000, 290, pyglet.resource.image('png/buttons/start_button_pressed.png'), pyglet.resource.image('png/buttons/start_button_depressed.png'), batch=batch, group=foreground)
cache_clear_button = pyglet.gui.PushButton(1210, 290, pyglet.resource.image('png/buttons/delete_button_pressed.png'), pyglet.resource.image('png/buttons/delete_button_depressed.png'), batch=batch, group=foreground)
cache_button = pyglet.gui.ToggleButton(1210, 395, pyglet.resource.image('png/buttons/display_button_pressed.png'), pyglet.resource.image('png/buttons/display_button_depressed.png'), batch=batch, group=foreground)
cache_picture =  pyglet.sprite.Sprite(image.load('png/plotting/empty.png'), -29, 60, batch=undrawable, group=foreground)
background_picture = pyglet.sprite.Sprite(image.load('png/background_hd.png'), 0, 0, batch=batch_background, group=background)
clear_button = pyglet.gui.PushButton(1435, 528, pyglet.resource.image('png/buttons/clear_button_pressed.png'), pyglet.resource.image('png/buttons/clear_button_depressed.png'), )
plus_button = classes.Dropdown(145, 58, pyglet.resource.image('png/buttons/clear_button_pressed.png'), pyglet.resource.image('png/buttons/clear_button_depressed.png'), batch=undrawable)
plus_button_1 = classes.Dropdown(1453, 70, pyglet.resource.image('png/buttons/clear_button_pressed.png'), pyglet.resource.image('png/buttons/clear_button_depressed.png'), batch=undrawable)
plus_button_2 = classes.Dropdown(1453, 88, pyglet.resource.image('png/buttons/clear_button_pressed.png'), pyglet.resource.image('png/buttons/clear_button_depressed.png'), batch=undrawable)
plus_button_3 = classes.Dropdown(1453, 98, pyglet.resource.image('png/buttons/clear_button_pressed.png'), pyglet.resource.image('png/buttons/clear_button_depressed.png'), batch=undrawable)
icon = pyglet.resource.image("png/icon.png")
window.set_caption("Neuronlab")
window.set_icon(icon)

plus_button.enabled = False
plus_button_1.enabled = False
plus_button_2.enabled = False
plus_button_3.enabled = False

nmda = pyglet.gui.ToggleButton(1453, 168, pyglet.resource.image('png/buttons/clear_button_pressed.png'), pyglet.resource.image('png/buttons/clear_button_depressed.png'), batch=batch, group=foreground)
nmda1 = pyglet.gui.ToggleButton(1453, 58, pyglet.resource.image('png/buttons/clear_button_pressed.png'), pyglet.resource.image('png/buttons/clear_button_depressed.png'), batch=batch, group=foreground)
nmda2 = pyglet.gui.ToggleButton(1453, 58, pyglet.resource.image('png/buttons/clear_button_pressed.png'), pyglet.resource.image('png/buttons/clear_button_depressed.png'), batch=batch, group=foreground)
nmda3 = pyglet.gui.ToggleButton(1453, 58, pyglet.resource.image('png/buttons/clear_button_pressed.png'), pyglet.resource.image('png/buttons/clear_button_depressed.png'), batch=batch, group=foreground)

ampa = pyglet.gui.ToggleButton(1453, 58, pyglet.resource.image('png/buttons/clear_button_pressed.png'), pyglet.resource.image('png/buttons/clear_button_depressed.png'), batch=batch, group=foreground)
ampa1 = pyglet.gui.ToggleButton(1453, 58, pyglet.resource.image('png/buttons/clear_button_pressed.png'), pyglet.resource.image('png/buttons/clear_button_depressed.png'), batch=batch, group=foreground)
ampa2 = pyglet.gui.ToggleButton(1453, 58, pyglet.resource.image('png/buttons/clear_button_pressed.png'), pyglet.resource.image('png/buttons/clear_button_depressed.png'), batch=batch, group=foreground)
ampa3 = pyglet.gui.ToggleButton(1453, 58, pyglet.resource.image('png/buttons/clear_button_pressed.png'), pyglet.resource.image('png/buttons/clear_button_depressed.png'), batch=batch, group=foreground)

gabab = pyglet.gui.ToggleButton(1453, 58, pyglet.resource.image('png/buttons/clear_button_pressed.png'), pyglet.resource.image('png/buttons/clear_button_depressed.png'), batch=batch, group=foreground)
gabab1 = pyglet.gui.ToggleButton(1453, 58, pyglet.resource.image('png/buttons/clear_button_pressed.png'), pyglet.resource.image('png/buttons/clear_button_depressed.png'), batch=batch, group=foreground)
gabab2 = pyglet.gui.ToggleButton(1453, 58, pyglet.resource.image('png/buttons/clear_button_pressed.png'), pyglet.resource.image('png/buttons/clear_button_depressed.png'), batch=batch, group=foreground)
gabab3 = pyglet.gui.ToggleButton(1453, 58, pyglet.resource.image('png/buttons/clear_button_pressed.png'), pyglet.resource.image('png/buttons/clear_button_depressed.png'), batch=batch, group=foreground)

gabaa = pyglet.gui.ToggleButton(1453, 58, pyglet.resource.image('png/buttons/clear_button_pressed.png'), pyglet.resource.image('png/buttons/clear_button_depressed.png'), batch=batch, group=foreground)
gabaa1 = pyglet.gui.ToggleButton(1453, 58, pyglet.resource.image('png/buttons/clear_button_pressed.png'), pyglet.resource.image('png/buttons/clear_button_depressed.png'), batch=batch, group=foreground)
gabaa2 = pyglet.gui.ToggleButton(1453, 58, pyglet.resource.image('png/buttons/clear_button_pressed.png'), pyglet.resource.image('png/buttons/clear_button_depressed.png'), batch=batch, group=foreground)
gabaa3 = pyglet.gui.ToggleButton(1453, 58, pyglet.resource.image('png/buttons/clear_button_pressed.png'), pyglet.resource.image('png/buttons/clear_button_depressed.png'), batch=batch, group=foreground)

Text_input_explanation = pyglet.sprite.Sprite(image.load('png/type_in_text.png'), 0, 0, batch=batch_background, group=background)
threshold = pyglet.gui.TextEntry('-40', 1355, 239, 50, color=(30, 30, 30, 255), text_color=(211,211,211,255), caret_color=(211,211,211,255), batch=batch, group=foreground)
Esyn = pyglet.gui.TextEntry('0', 1355, 183, 50, color=(30, 30, 30, 255), text_color=(211,211,211,255), caret_color=(211,211,211,255), batch=batch, group=foreground)
Esyninh = pyglet.gui.TextEntry('-75', 1355, 127, 50, color=(30, 30, 30, 255), text_color=(211,211,211,255), caret_color=(211,211,211,255), batch=batch, group=foreground)
Membrane_potential = pyglet.gui.TextEntry('-75', 1355, 71, 50, color=(30, 30, 30, 255), text_color=(211,211,211,255), caret_color=(211,211,211,255), batch=batch, group=foreground)

slider_1 = classes.MySlider(1000, 1010, base=pyglet.resource.image('png/sliders/excitatory_slider.png'), knob=pyglet.resource.image('png/sliders/knob_grey.png'), edge=5, batch=batch)
slider_2 = classes.MySlider(1000, 912, base=pyglet.resource.image('png/sliders/excitatory_slider.png'), knob=pyglet.resource.image('png/sliders/knob_grey.png'), edge=5, batch=batch)
slider_3 = classes.MySlider(1000, 816, base=pyglet.resource.image('png/sliders/excitatory_slider.png'), knob=pyglet.resource.image('png/sliders/knob_grey.png'), edge=5, batch=batch)
slider_4 = classes.MySlider(1000, 720, base=pyglet.resource.image('png/sliders/inhibitory_slider.png'), knob=pyglet.resource.image('png/sliders/knob_grey.png'), edge=5, batch=batch)


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
pyglet.gui.ToggleButton.register_event_type('on_mouse_press')
pyglet.gui.ToggleButton.register_event_type('on_mouse_release')
pyglet.gui.ToggleButton.register_event_type('on_mouse_drag')
pyglet.gui.ToggleButton.register_event_type('on_press')
pyglet.gui.ToggleButton.register_event_type('on_release')

def clear_window(slider, sldisp):
    sldisp.dispatch_event('slider_activate', slider, undrawable)
    slider.value = 0
    slider.enabled = False

def add_spike_time(n, list_, spike_time):
    if len(list_) == 0:
        list_.append(spike_time)
    elif n < 3: 
        list_[n] = spike_time
    else:
        pass
        
def null(array):
        leng = len(array)
        for n in array:
            if not isinstance(n, int):
                n.text = ''
        array =  [0]*leng

def off_on(gui_list, boolean_value):
    for elem in gui_list:
        elem.enabled = boolean_value

def time_length_counter(m):
    if calculator.n[m] <= 3:
        calculator.n[m] += 1
def receptor_choice(n, m):
    calculator.strengths[n][m] = not calculator.strengths[n][m]

@nmda.event
def on_toggle():
    receptor_choice(0,0)
@nmda1.event
def on_toggle():
     receptor_choice(1,0)
@nmda2.event
def on_toggle():
     receptor_choice(2,0)
@nmda3.event
def on_toggle():
     receptor_choice(3,0)  

@ampa.event
def on_release():
     receptor_choice(0,1)
@ampa1.event
def on_release():
     receptor_choice(1,1)
@ampa2.event
def on_release():
     receptor_choice(2,1)
@ampa3.event
def on_release():
     receptor_choice(3,1)

@gabab.event
def on_release():
     receptor_choice(0,2)
@gabab1.event
def on_release():
     receptor_choice(1,2)
@gabab2.event
def on_release():
     receptor_choice(2,2)
@gabab3.event
def on_release():
     receptor_choice(3,2)

@gabaa.event
def on_release():
     receptor_choice(0,3)
@gabaa1.event
def on_release():
     receptor_choice(1,3)
@gabaa2.event
def on_release():
     receptor_choice(2,3)
@gabaa3.event
def on_release():
     receptor_choice(3,3)

@calc_button.event
def on_release():
    calculator.dispatch_event('count_')
@cache_button.event
def on_release():
    cache_picture.image = image.load('png/plotting/plotting_c.png')
    cache_picture.batch = batch
    calculator.cache = True
@cache_clear_button.event
def on_release():
    cache_picture.batch = undrawable
    calculator.cache = False
@clear_button.event
def on_release():
    calculator.t_list =  []
    calculator.t_1_list =  []
    calculator.t_2_list =  []
    calculator.t_3_list =  []
    null(window.spike_times)
    slider_1.value = 0
    slider_2.value = 0
    slider_3.value = 0
    slider_4.value = 0
  
    spike_time_batch.invalidate()
   
    window.wire_picture_exc_1.image = image.load('png/wires/1-end.png')
    window.wire_picture_exc_2.image = image.load('png/plotting/empty.png')
    window.wire_picture_exc_3.image = image.load('png/plotting/empty.png')
    window.wire_picture_inh_1.image = image.load('png/wires_inh/1-end.png')
    window.wire_picture_inh_2.image = image.load('png/plotting/empty.png')
    window.wire_picture_inh_3.image = image.load('png/plotting/empty.png')

    window.dispatch_event('update_pic', image.load('png/plotting/empty.png'))
@calculator.event
def count_():
    window.dispatch_event('update_wait', image.load('png/please_wait.png'))
    calculator.proc = Popen(utils.CompartmentEncoder.popen_generator([calculator.t_list, calculator.t_1_list, calculator.t_2_list, calculator.t_3_list], calculator.strengths, calculator.cache))
    pyglet.clock.schedule_interval(update, 1/2) 
    #temporary running block
    off_on([ slider_1, slider_2, slider_3, slider_4,nmda, ampa, gabaa, gabab,  threshold, Membrane_potential, Esyn, Esyninh, clear_button, calc_button, cache_button, cache_clear_button], False)
   
@endofcalcdisp.event
def update(dt):
    try: 
        if calculator.proc.poll() != None:
            cache_picture.image = image.load('png/plotting/plotting_c.png')
            pyglet.clock.schedule_interval(drawing_plot, 1/30, picture=image.load('png/plotting/plotting.png'))
            
            pyglet.clock.unschedule(update)
    except BaseException:
        pass   
 

@endofcalcdisp.event
def drawing_plot(dt, picture):
    
    window.dispatch_event('update_wait', image.load('png/plotting/empty.png'))
    endofcalcdisp.count += 1
    if endofcalcdisp.count <= picture.width:
        part_plot = picture.get_region(0, 0, endofcalcdisp.count, picture.height)
        window.dispatch_event('update_pic', part_plot)
    else: 
        window.dispatch_event('update_pic', picture)
        endofcalcdisp.count = 0
        #temporary running block removal
        off_on([ slider_1, slider_2, slider_3, slider_4, nmda, ampa, gabaa, gabab, threshold, Membrane_potential, Esyn, Esyninh, calc_button, cache_button,clear_button, cache_clear_button], True)
        calculator.n = [0, 0, 0, 0]
        pyglet.clock.unschedule(drawing_plot)

@slider_1.event
def on_change(val):
    spike_time = int(round(val*runtime_constant, 0))
    add_spike_time(calculator.n[0], calculator.t_list, spike_time)
    window.spike_times[0]= (pyglet.text.Label(f'{str(spike_time)}', font_size=20, color=(105, 105, 105, 255), x=1005, y=986, batch=spike_time_batch))
    sldisp.dispatch_event('slider_activate', plus_button, batch)

@slider_2.event
def on_change(val):
    spike_time = int(round(val*runtime_constant, 0))
    add_spike_time(calculator.n[1], calculator.t_1_list, spike_time)
    window.spike_times[1]= (pyglet.text.Label(f'{str(spike_time)}', font_size=20, color=(105, 105, 105, 255), x=1005, y=888, batch=spike_time_batch))
    sldisp.dispatch_event('slider_activate', plus_button_1, batch)
    
@slider_3.event
def on_change(val):
    spike_time = int(round(val*runtime_constant, 0))
    add_spike_time(calculator.n[2], calculator.t_2_list, spike_time)
    window.spike_times[2]= (pyglet.text.Label(f'{str(spike_time)}', font_size=20, color=(105, 105, 105, 255), x=1005, y=792, batch=spike_time_batch))
    sldisp.dispatch_event('slider_activate', plus_button_2, batch)
  
@slider_4.event
def on_change(val):
    spike_time = int(round(val*runtime_constant, 0))
    add_spike_time(calculator.n[3], calculator.t_3_list, spike_time)
    window.spike_times[3]= (pyglet.text.Label(f'{str(spike_time)}', font_size=20, color=(32,32,32,255), x=1005, y=699, batch=spike_time_batch))
    sldisp.dispatch_event('slider_activate', plus_button_3, batch)

@plus_button.event
def on_release():
    time_length_counter(0)
@plus_button_1.event
def on_release():
    time_length_counter(1)
@plus_button_2.event
def on_release():
    time_length_counter(2)
@plus_button_3.event
def on_release():
    time_length_counter(3)

@window.event
def update_pic(picture):
    window.plot_sprite.image = picture
@window.event
def update_wait(picture):
    window.plot_wait.image = picture
@window.event
def on_draw():
    window.clear()
    batch_background.draw()
    window.plot_sprite.draw()
    window.plot_wait.draw()
    window.window_batch.draw()
    batch.draw()
    spike_time_batch.draw()
@window.event
def on_mouse_press(x, y, button, modifiers):
    slider_1.dispatch_event('on_mouse_press', x, y, button, modifiers)
    slider_2.dispatch_event('on_mouse_press', x, y, button, modifiers)
    slider_3.dispatch_event('on_mouse_press', x, y, button, modifiers)
    slider_4.dispatch_event('on_mouse_press', x, y, button, modifiers)
    threshold.dispatch_event('on_mouse_press', x, y, button, modifiers)
    Esyn.dispatch_event('on_mouse_press', x, y, button, modifiers)
    Esyninh.dispatch_event('on_mouse_press', x, y, button, modifiers)
    Membrane_potential.dispatch_event('on_mouse_press', x, y, button, modifiers)
    calc_button.dispatch_event('on_mouse_press', x, y, button, modifiers)
    cache_button.dispatch_event('on_mouse_press', x, y, button, modifiers)
    cache_clear_button.dispatch_event('on_mouse_press', x, y, button, modifiers)
    clear_button.dispatch_event('on_mouse_press', x, y, button, modifiers)
    
    nmda.dispatch_event('on_mouse_press', x, y, button, modifiers)
    ampa.dispatch_event('on_mouse_press', x, y, button, modifiers)
    gabaa.dispatch_event('on_mouse_press', x, y, button, modifiers)
    gabab.dispatch_event('on_mouse_press', x, y, button, modifiers)
    plus_button.dispatch_event('on_mouse_press', x, y, button, modifiers)
    plus_button_1.dispatch_event('on_mouse_press', x, y, button, modifiers)
    plus_button_2.dispatch_event('on_mouse_press', x, y, button, modifiers)
    plus_button_3.dispatch_event('on_mouse_press', x, y, button, modifiers)
@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    slider_1.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    slider_2.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    slider_3.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    slider_4.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    threshold.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    Esyn.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    Esyninh.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    Membrane_potential.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    
    nmda.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    ampa.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    gabaa.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    gabab.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    plus_button.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    plus_button_1.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    plus_button_2.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    plus_button_3.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
@window.event
def on_mouse_release(x, y, buttons, modifiers):
    slider_1.dispatch_event('on_mouse_release', x, y, buttons, modifiers)
    slider_2.dispatch_event('on_mouse_release', x, y, buttons, modifiers)
    slider_3.dispatch_event('on_mouse_release', x, y, buttons, modifiers)
    slider_4.dispatch_event('on_mouse_release', x, y, buttons, modifiers)
    calc_button.dispatch_event('on_mouse_release', x, y, buttons, modifiers)
    cache_button.dispatch_event('on_mouse_release', x, y, buttons, modifiers)
    cache_clear_button.dispatch_event('on_mouse_release', x, y, buttons, modifiers)
    clear_button.dispatch_event('on_mouse_release', x, y, buttons, modifiers)
    
    nmda.dispatch_event('on_mouse_release', x, y, buttons, modifiers)
    ampa.dispatch_event('on_mouse_release', x, y, buttons, modifiers)
    gabaa.dispatch_event('on_mouse_release', x, y, buttons, modifiers)
    gabab.dispatch_event('on_mouse_release', x, y, buttons, modifiers)
    plus_button.dispatch_event('on_mouse_release', x, y, buttons, modifiers)
    plus_button_1.dispatch_event('on_mouse_release', x, y, buttons, modifiers)
    plus_button_2.dispatch_event('on_mouse_release', x, y, buttons, modifiers)
    plus_button_3.dispatch_event('on_mouse_release', x, y, buttons, modifiers)
@window.event
def on_text(text):
    threshold.dispatch_event('on_text', text)
    Esyn.dispatch_event('on_text', text)
    Esyninh.dispatch_event('on_text', text)
    Membrane_potential.dispatch_event('on_text', text)
@window.event
def on_text_motion(motion):
    threshold.dispatch_event('on_text_motion', motion)
    Esyn.dispatch_event('on_text_motion', motion)
    Esyninh.dispatch_event('on_text_motion', motion)
    Membrane_potential.dispatch_event('on_text_motion', motion)
@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.E:
        calculator.dispatch_event('count_')
window.set_fullscreen()
pyglet.app.run()
