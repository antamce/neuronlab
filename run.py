import pyglet
from pyglet.window import key
from pyglet.window import mouse
from pyglet import image
from subprocess import Popen
from subprocess import PIPE
import classes
import utils

t_list = []
t_1_list = []
t_2_list = []
t_3_list = []
spike_times = [[], [], [], []]
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
calc_button = pyglet.gui.PushButton(1259, 404, pyglet.resource.image('png/buttons/start_button_pressed.png'), pyglet.resource.image('png/buttons/start_button_unpressed.png'), batch=batch, group=foreground)
cache_clear_button = pyglet.gui.PushButton(1259, 159, pyglet.resource.image('png/buttons/delete_button_pressed.png'), pyglet.resource.image('png/buttons/delete_button_unpressed.png'), batch=batch, group=foreground)
cache_button = pyglet.gui.ToggleButton(1259, 281, pyglet.resource.image('png/buttons/display_button_pressed.png'), pyglet.resource.image('png/buttons/display_button_unpressed.png'), batch=batch, group=foreground)

background_plate_1 = [classes.Dropdown(1477, 970, image.load('png/sliders/text_plate.png'), image.load('png/sliders/text_plate.png'), batch=batch), classes.Dropdown(1537, 970, image.load('png/sliders/text_plate.png'), image.load('png/sliders/text_plate.png'), batch=undrawable), classes.Dropdown(1597, 970, image.load('png/sliders/text_plate.png'), image.load('png/sliders/text_plate.png'), batch=undrawable)]
background_plate_2 = [classes.Dropdown(1477, 849, image.load('png/sliders/text_plate.png'), image.load('png/sliders/text_plate.png'), batch=batch), classes.Dropdown(1537, 849, image.load('png/sliders/text_plate.png'), image.load('png/sliders/text_plate.png'), batch=undrawable), classes.Dropdown(1597, 849, image.load('png/sliders/text_plate.png'), image.load('png/sliders/text_plate.png'), batch=undrawable)]
background_plate_3 = [classes.Dropdown(1477, 728, image.load('png/sliders/text_plate.png'), image.load('png/sliders/text_plate.png'), batch=batch), classes.Dropdown(1537, 728, image.load('png/sliders/text_plate.png'), image.load('png/sliders/text_plate.png'), batch=undrawable), classes.Dropdown(1597, 708, image.load('png/sliders/text_plate.png'), image.load('png/sliders/text_plate.png'), batch=undrawable)]
background_plate_4 = [classes.Dropdown(1477, 607, image.load('png/sliders/text_plate.png'), image.load('png/sliders/text_plate.png'), batch=batch), classes.Dropdown(1537, 607, image.load('png/sliders/text_plate.png'), image.load('png/sliders/text_plate.png'), batch=undrawable), classes.Dropdown(1597, 607, image.load('png/sliders/text_plate.png'), image.load('png/sliders/text_plate.png'), batch=undrawable)]

background_picture = pyglet.sprite.Sprite(image.load('png/background.png'), 0, 0, batch=batch_background, group=background)
clear_button = pyglet.gui.PushButton(1259, 34, pyglet.resource.image('png/buttons/clear_button_pressed.png'), pyglet.resource.image('png/buttons/clear_button_unpressed.png'),batch=batch)
plus_button = classes.Dropdown(1859, 973, pyglet.resource.image('png/buttons/cross_pressed.png'), pyglet.resource.image('png/buttons/cross_unpressed.png'), batch=undrawable)
plus_button_1 = classes.Dropdown(1859, 852, pyglet.resource.image('png/buttons/cross_pressed.png'), pyglet.resource.image('png/buttons/cross_unpressed.png'), batch=undrawable)
plus_button_2 = classes.Dropdown(1859, 731, pyglet.resource.image('png/buttons/cross_pressed.png'), pyglet.resource.image('png/buttons/cross_unpressed.png'), batch=undrawable)
plus_button_3 = classes.Dropdown(1859, 610, pyglet.resource.image('png/buttons/cross_pressed.png'), pyglet.resource.image('png/buttons/cross_unpressed.png'), batch=undrawable)
icon = pyglet.resource.image("png/icon.png")
window.set_caption("Neuronlab")
window.set_icon(icon)

plus_button.enabled = False
plus_button_1.enabled = False
plus_button_2.enabled = False
plus_button_3.enabled = False

nmda = pyglet.gui.ToggleButton(1719, 205, pyglet.resource.image('png/choose_receptor/n_pressed.png'), pyglet.resource.image('png/choose_receptor/n_unpressed.png'), batch=batch, group=foreground)
nmda1 = pyglet.gui.ToggleButton(1719, 285, pyglet.resource.image('png/choose_receptor/n_pressed.png'), pyglet.resource.image('png/choose_receptor/n_unpressed.png'), batch=batch, group=foreground)
nmda2 = pyglet.gui.ToggleButton(1799, 285, pyglet.resource.image('png/choose_receptor/n_pressed.png'), pyglet.resource.image('png/choose_receptor/n_unpressed.png'), batch=batch, group=foreground)
nmda3 = pyglet.gui.ToggleButton(1799, 205, pyglet.resource.image('png/choose_receptor/n_pressed.png'), pyglet.resource.image('png/choose_receptor/n_unpressed.png'), batch=batch, group=foreground)

ampa = pyglet.gui.ToggleButton(1759, 205, pyglet.resource.image('png/choose_receptor/p_pressed.png'), pyglet.resource.image('png/choose_receptor/p_unpressed.png'), batch=batch, group=foreground)
ampa1 = pyglet.gui.ToggleButton(1759, 285, pyglet.resource.image('png/choose_receptor/p_pressed.png'), pyglet.resource.image('png/choose_receptor/p_unpressed.png'), batch=batch, group=foreground)
ampa2 = pyglet.gui.ToggleButton(1839, 205, pyglet.resource.image('png/choose_receptor/p_pressed.png'), pyglet.resource.image('png/choose_receptor/p_unpressed.png'), batch=batch, group=foreground)
ampa3 = pyglet.gui.ToggleButton(1839, 285, pyglet.resource.image('png/choose_receptor/p_pressed.png'), pyglet.resource.image('png/choose_receptor/p_unpressed.png'), batch=batch, group=foreground)

gabab = pyglet.gui.ToggleButton(1759, 165, pyglet.resource.image('png/choose_receptor/b_pressed.png'), pyglet.resource.image('png/choose_receptor/b_unpressed.png'), batch=batch, group=foreground)
gabab1 = pyglet.gui.ToggleButton(1759, 245, pyglet.resource.image('png/choose_receptor/b_pressed.png'), pyglet.resource.image('png/choose_receptor/b_unpressed.png'), batch=batch, group=foreground)
gabab2 = pyglet.gui.ToggleButton(1839, 165, pyglet.resource.image('png/choose_receptor/b_pressed.png'), pyglet.resource.image('png/choose_receptor/b_unpressed.png'), batch=batch, group=foreground)
gabab3 = pyglet.gui.ToggleButton(1839, 245, pyglet.resource.image('png/choose_receptor/b_pressed.png'), pyglet.resource.image('png/choose_receptor/b_unpressed.png'), batch=batch, group=foreground)

gabaa = pyglet.gui.ToggleButton(1719, 165, pyglet.resource.image('png/choose_receptor/a_pressed.png'), pyglet.resource.image('png/choose_receptor/a_unpressed.png'), batch=batch, group=foreground)
gabaa1 = pyglet.gui.ToggleButton(1719, 245, pyglet.resource.image('png/choose_receptor/a_pressed.png'), pyglet.resource.image('png/choose_receptor/a_unpressed.png'), batch=batch, group=foreground)
gabaa2 = pyglet.gui.ToggleButton(1799, 165, pyglet.resource.image('png/choose_receptor/a_pressed.png'), pyglet.resource.image('png/choose_receptor/a_unpressed.png'), batch=batch, group=foreground)
gabaa3 = pyglet.gui.ToggleButton(1799, 245, pyglet.resource.image('png/choose_receptor/a_pressed.png'), pyglet.resource.image('png/choose_receptor/a_unpressed.png'), batch=batch, group=foreground)

slider_1 = classes.MySlider(1474, 997, base=pyglet.resource.image('png/sliders/slider.png'), knob=pyglet.resource.image('png/sliders/knob.png'), edge=5, batch=batch)
slider_2 = classes.MySlider(1474, 876, base=pyglet.resource.image('png/sliders/slider.png'), knob=pyglet.resource.image('png/sliders/knob.png'), edge=5, batch=batch)
slider_3 = classes.MySlider(1474, 755, base=pyglet.resource.image('png/sliders/slider.png'), knob=pyglet.resource.image('png/sliders/knob.png'), edge=5, batch=batch)
slider_4 = classes.MySlider(1474, 634, base=pyglet.resource.image('png/sliders/slider.png'), knob=pyglet.resource.image('png/sliders/knob.png'), edge=5, batch=batch)


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

def add_spike_time(n, list_, spike_time, button):
    if n>2:
        pass
    elif len(list_) < n+1:
        list_.append(spike_time)
        if n == 2:
            sldisp.dispatch_event('slider_deactivate', button, undrawable)
        else:
            sldisp.dispatch_event('slider_activate', button, batch)
            
    elif len(list_) >= n+1: 
        list_[n] = spike_time
        if n == 2:
            sldisp.dispatch_event('slider_deactivate', button, undrawable)
        else:
            sldisp.dispatch_event('slider_activate', button, batch)
            
    else:
        pass
        
def null(array):
        leng = len(array)
        for n in array:
            for m in n:
                if not isinstance(m, int):
                    m.text = ''
        array =  [0]*leng

def off_on(gui_list, boolean_value):
    for elem in gui_list:
        elem.enabled = boolean_value

def time_length_counter(m):
    if calculator.n[m] <= 3:
        calculator.n[m] += 1
    
def receptor_choice(n, m, boolean):
    if(boolean):
        calculator.strengths[n][m] = not calculator.strengths[n][m]
    

@nmda.event
def on_toggle(boole):
    receptor_choice(0,0, boole)
@nmda1.event
def on_toggle(boole):
     receptor_choice(1,0, boole)
@nmda2.event
def on_toggle(boole):
     receptor_choice(2,0, boole)
@nmda3.event
def on_toggle(boole):
     receptor_choice(3,0, boole)  
@ampa.event
def on_toggle(boole):
     receptor_choice(0,1, boole)
@ampa1.event
def on_toggle(boole):
     receptor_choice(1,1, boole)
@ampa2.event
def on_toggle(boole):
     receptor_choice(2,1, boole)
@ampa3.event
def on_toggle(boole):
     receptor_choice(3,1, boole)

@gabab.event
def on_toggle(boole):
     receptor_choice(0,2, boole)
@gabab1.event
def on_toggle(boole):
     receptor_choice(1,2, boole)
@gabab2.event
def on_toggle(boole):
     receptor_choice(2,2, boole)
@gabab3.event
def on_toggle(boole):
     receptor_choice(3,2, boole)

@gabaa.event
def on_toggle(boole):
     receptor_choice(0,3, boole)
@gabaa1.event
def on_toggle(boole):
     receptor_choice(1,3, boole)
@gabaa2.event
def on_toggle(boole):
     receptor_choice(2,3, boole)
@gabaa3.event
def on_toggle(boole):
     receptor_choice(3,3, boole)

@calc_button.event
def on_release():
    calculator.dispatch_event('count_')
@cache_button.event
def on_toggle(arg):
    window.dispatch_event('update_cache', image.load('png/plotting/plotting_c.png'))
    calculator.cache = True
@cache_clear_button.event
def on_release():
    window.dispatch_event('update_cache', image.load('png/plotting/empty.png'))
    calculator.cache = False
@clear_button.event
def on_release():
    calculator.t_list =  []
    calculator.t_1_list =  []
    calculator.t_2_list =  []
    calculator.t_3_list =  []
    calculator.n = [0, 0, 0, 0]
    slider_1.value = 0
    slider_2.value = 0
    slider_3.value = 0
    slider_4.value = 0
    window.spike_times = spike_times
    null(window.spike_times)
    
    spike_time_batch.invalidate()
   
    window.dispatch_event('update_pic', image.load('png/plotting/empty.png'))
@calculator.event
def count_():
    window.dispatch_event('update_wait', image.load('png/please_wait.png'))
    calculator.proc = Popen(utils.CompartmentEncoder.popen_generator([calculator.t_1_list, calculator.t_list, calculator.t_3_list, calculator.t_2_list], calculator.strengths, calculator.cache), stdout=PIPE, shell=True)
    pyglet.clock.schedule_interval(update, 1/2) 
    #temporary running block
    off_on([ slider_2, slider_1, slider_4, slider_3,nmda, ampa, gabaa, gabab, clear_button, calc_button, cache_button, cache_clear_button], False)
   
@endofcalcdisp.event
def update(dt):
    try: 
        if calculator.proc.poll() != None:
            a = calculator.proc.communicate()
            #here we get the filename in the a variable (in what i believe are bytes). Regular strings do not work as paths, so i use the r'<string_path>' but idk abt bytes
            print(a)
            window.dispatch_event('update_cache', image.load('png/plotting/plotting_c.png'))
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
        off_on([ slider_1, slider_2, slider_3, slider_4, nmda, ampa, gabaa, gabab, calc_button, cache_button,clear_button, cache_clear_button], True)
        calculator.n = [0, 0, 0, 0]
        pyglet.clock.unschedule(drawing_plot)

@slider_1.event
def on_change(val):
    spike_time = int(round(val*runtime_constant, 0))
    add_spike_time(calculator.n[0], calculator.t_list, spike_time, plus_button)
    add_spike_time(calculator.n[0], window.spike_times[0],pyglet.text.Label(f'{str(spike_time)}', font_size=17, font_name = 'calibri', color=(20, 20, 20, 255), x=(1480+calculator.n[0]*60), y=975, batch=spike_time_batch), plus_button)

@slider_2.event
def on_change(val):
    spike_time = int(round(val*runtime_constant, 0))
    add_spike_time(calculator.n[1], calculator.t_1_list, spike_time, plus_button_1)
    add_spike_time(calculator.n[1], window.spike_times[1],pyglet.text.Label(f'{str(spike_time)}', font_size=17, font_name = 'calibri', color=(20, 20, 20, 255), x=(1480+calculator.n[1]*60), y=854, batch=spike_time_batch), plus_button_1)
    
    
@slider_3.event 
def on_change(val):
    spike_time = int(round(val*runtime_constant, 0))
    add_spike_time(calculator.n[2], calculator.t_2_list, spike_time, plus_button_2, )
    add_spike_time(calculator.n[2], window.spike_times[2], pyglet.text.Label(f'{str(spike_time)}', font_size=17, font_name = 'calibri', color=(20, 20, 20, 255), x=(1480+calculator.n[2]*60), y=733, batch=spike_time_batch), plus_button_2)
    
  
@slider_4.event
def on_change(val):
    spike_time = int(round(val*runtime_constant, 0))
    add_spike_time(calculator.n[3], calculator.t_3_list, spike_time, plus_button_3)
    add_spike_time(calculator.n[3], window.spike_times[3],pyglet.text.Label(f'{str(spike_time)}', font_size=17, font_name = 'calibri', color=(20, 20, 20, 255), x=(1480+calculator.n[3]*60), y=612, batch=spike_time_batch), plus_button_3)
    

@plus_button.event
def on_release():
    time_length_counter(0)
    plus_button.enabled = False
    sldisp.dispatch_event('slider_deactivate', plus_button, undrawable)
    if calculator.n[0]<=2:
        sldisp.dispatch_event('slider_activate', background_plate_1[(calculator.n[0])], batch)
@plus_button_1.event
def on_release():
    time_length_counter(1)
    if calculator.n[1]<=2:
        sldisp.dispatch_event('slider_activate', background_plate_2[(calculator.n[1])], batch)
    sldisp.dispatch_event('slider_deactivate', plus_button_1, undrawable)
@plus_button_2.event
def on_release():
    time_length_counter(2)
    if calculator.n[2]<=2:
        sldisp.dispatch_event('slider_activate', background_plate_3[(calculator.n[2])], batch)
    sldisp.dispatch_event('slider_deactivate', plus_button_2, undrawable)
@plus_button_3.event
def on_release():
    time_length_counter(3)
    sldisp.dispatch_event('slider_deactivate', plus_button_3, undrawable)
    if calculator.n[3]<=2:
        sldisp.dispatch_event('slider_activate', background_plate_4[(calculator.n[3])], batch)
@window.event
def update_pic(picture):
    window.plot_sprite.image = picture
@window.event
def update_cache(picture):
    window.plot_cache.image = picture
@window.event
def update_wait(picture):
    window.plot_wait.image = picture
@window.event
def on_draw():
    window.clear()
    batch_background.draw()
    window.plot_sprite.draw()
    window.plot_wait.draw()
    window.plot_cache.draw()
    window.window_batch.draw()
    batch.draw()
    spike_time_batch.draw()
@window.event
def on_mouse_press(x, y, button, modifiers):
    slider_1.dispatch_event('on_mouse_press', x, y, button, modifiers)
    slider_2.dispatch_event('on_mouse_press', x, y, button, modifiers)
    slider_3.dispatch_event('on_mouse_press', x, y, button, modifiers)
    slider_4.dispatch_event('on_mouse_press', x, y, button, modifiers)
    calc_button.dispatch_event('on_mouse_press', x, y, button, modifiers)
    cache_button.dispatch_event('on_mouse_press', x, y, button, modifiers)
    cache_clear_button.dispatch_event('on_mouse_press', x, y, button, modifiers)
    clear_button.dispatch_event('on_mouse_press', x, y, button, modifiers)
    nmda.dispatch_event('on_mouse_press', x, y, button, modifiers)
    ampa.dispatch_event('on_mouse_press', x, y, button, modifiers)
    gabaa.dispatch_event('on_mouse_press', x, y, button, modifiers)
    gabab.dispatch_event('on_mouse_press', x, y, button, modifiers)
    nmda1.dispatch_event('on_mouse_press', x, y, button, modifiers)
    ampa1.dispatch_event('on_mouse_press', x, y, button, modifiers)
    gabaa1.dispatch_event('on_mouse_press', x, y, button, modifiers)
    gabab1.dispatch_event('on_mouse_press', x, y, button, modifiers)
    nmda2.dispatch_event('on_mouse_press', x, y, button, modifiers)
    ampa2.dispatch_event('on_mouse_press', x, y, button, modifiers)
    gabaa2.dispatch_event('on_mouse_press', x, y, button, modifiers)
    gabab2.dispatch_event('on_mouse_press', x, y, button, modifiers)
    nmda3.dispatch_event('on_mouse_press', x, y, button, modifiers)
    ampa3.dispatch_event('on_mouse_press', x, y, button, modifiers)
    gabaa3.dispatch_event('on_mouse_press', x, y, button, modifiers)
    gabab3.dispatch_event('on_mouse_press', x, y, button, modifiers)
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
    
    nmda.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    ampa.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    gabaa.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    gabab.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    nmda1.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    ampa1.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    gabaa1.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    gabab1.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    nmda2.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    ampa2.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    gabaa2.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    gabab2.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    nmda3.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    ampa3.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    gabaa3.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    gabab3.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
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
    nmda1.dispatch_event('on_mouse_release', x, y, buttons, modifiers)
    ampa1.dispatch_event('on_mouse_release', x, y, buttons, modifiers)
    gabaa1.dispatch_event('on_mouse_release', x, y, buttons, modifiers)
    gabab1.dispatch_event('on_mouse_release', x, y, buttons, modifiers)
    nmda2.dispatch_event('on_mouse_release', x, y, buttons, modifiers)
    ampa2.dispatch_event('on_mouse_release', x, y, buttons, modifiers)
    gabaa2.dispatch_event('on_mouse_release', x, y, buttons, modifiers)
    gabab2.dispatch_event('on_mouse_release', x, y, buttons, modifiers)
    nmda3.dispatch_event('on_mouse_release', x, y, buttons, modifiers)
    ampa3.dispatch_event('on_mouse_release', x, y, buttons, modifiers)
    gabaa3.dispatch_event('on_mouse_release', x, y, buttons, modifiers)
    gabab3.dispatch_event('on_mouse_release', x, y, buttons, modifiers)
    plus_button.dispatch_event('on_mouse_release', x, y, buttons, modifiers)
    plus_button_1.dispatch_event('on_mouse_release', x, y, buttons, modifiers)
    plus_button_2.dispatch_event('on_mouse_release', x, y, buttons, modifiers)
    plus_button_3.dispatch_event('on_mouse_release', x, y, buttons, modifiers)

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.E:
        calculator.dispatch_event('count_')
window.set_fullscreen()
pyglet.app.run()
