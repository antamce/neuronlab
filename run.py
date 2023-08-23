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
window = classes.HelloWorldWindow(spike_times, width=1920, height=1080)
sldisp = classes.SliderDispathcher()
calc_button = pyglet.gui.PushButton(1000, 290, pyglet.resource.image('png/start_button_pressed.png'), pyglet.resource.image('png/start_button_depressed.png'), batch=batch, group=foreground)
cache_clear_button = pyglet.gui.PushButton(1210, 290, pyglet.resource.image('png/delete_button_pressed.png'), pyglet.resource.image('png/delete_button_depressed.png'), batch=batch, group=foreground)
cache_button = pyglet.gui.PushButton(1210, 395, pyglet.resource.image('png/display_button_pressed.png'), pyglet.resource.image('png/display_button_depressed.png'), batch=batch, group=foreground)
cache_picture =  pyglet.sprite.Sprite(image.load('png/empty.png'), -37, 7, batch=undrawable, group=foreground)
background_picture = pyglet.sprite.Sprite(image.load('png/background_hd.png'), 0, 0, batch=batch_background, group=background)
icon = pyglet.resource.image("png/icon.png")
window.set_caption("Neuronlab")
window.set_icon(icon)
dropdown_list_header = classes.Dropdown(1435, 1010, image.load('png/choose_receptor/no_excitatory_input.png'), image.load('png/choose_receptor/no_excitatory_input.png'), batch=batch, group=foreground)
dropdown_list_header_inh = classes.Dropdown(1435, 720, image.load('png/choose_receptor/no_inhibitory_input.png'), image.load('png/choose_receptor/no_inhibitory_input.png'), batch=batch, group=foreground)

nmda = classes.Dropdown(1435, 965, pyglet.resource.image('png/choose_receptor/nmda.png'), pyglet.resource.image('png/choose_receptor/nmda.png'), batch=undrawable)
ampa = classes.Dropdown(1435, 912, pyglet.resource.image('png/choose_receptor/ampa.png'), pyglet.resource.image('png/choose_receptor/ampa.png'),  batch=undrawable)
gabab = classes.Dropdown(1435, 624, pyglet.resource.image('png/choose_receptor/gabab.png'), pyglet.resource.image('png/choose_receptor/gabab.png'),  batch=undrawable)
gabaa = classes.Dropdown(1435, 676, pyglet.resource.image('png/choose_receptor/gabaa.png'), pyglet.resource.image('png/choose_receptor/gabaa.png'),  batch=undrawable)


Text_input_explanation = pyglet.sprite.Sprite(image.load('png/type_in_text.png'), 0, 0, batch=batch_background, group=background)
threshold = pyglet.gui.TextEntry('-40', 1355, 239, 50, color=(30, 30, 30, 255), text_color=(211,211,211,255), caret_color=(211,211,211,255), batch=batch, group=foreground)
Esyn = pyglet.gui.TextEntry('0', 1355, 183, 50, color=(30, 30, 30, 255), text_color=(211,211,211,255), caret_color=(211,211,211,255), batch=batch, group=foreground)
Esyninh = pyglet.gui.TextEntry('-75', 1355, 127, 50, color=(30, 30, 30, 255), text_color=(211,211,211,255), caret_color=(211,211,211,255), batch=batch, group=foreground)
Membrane_potential = pyglet.gui.TextEntry('-75', 1355, 71, 50, color=(30, 30, 30, 255), text_color=(211,211,211,255), caret_color=(211,211,211,255), batch=batch, group=foreground)

slider_e_1 = classes.MySlider(1000, 1010, base=pyglet.resource.image('png/excitatory_slider.png'), knob=pyglet.resource.image('png/knob_grey.png'), edge=5, batch=batch)
slider_e_2 = classes.MySlider(1000, 912, base=pyglet.resource.image('png/excitatory_slider.png'), knob=pyglet.resource.image('png/knob_grey.png'), edge=5, batch=undrawable, enabled=False)
slider_e_3 = classes.MySlider(1000, 816, base=pyglet.resource.image('png/excitatory_slider.png'), knob=pyglet.resource.image('png/knob_grey.png'), edge=5, batch=undrawable, enabled =False)
slider_i_1 = classes.MySlider(1000, 720, base=pyglet.resource.image('png/inhibitory_slider.png'), knob=pyglet.resource.image('png/knob_grey.png'), edge=5, batch=batch)
slider_i_2 = classes.MySlider(1000, 624, base=pyglet.resource.image('png/inhibitory_slider.png'), knob=pyglet.resource.image('png/knob_grey.png'), edge=5, batch=undrawable, enabled =False)
slider_i_3 = classes.MySlider(1000, 528, base=pyglet.resource.image('png/inhibitory_slider.png'), knob=pyglet.resource.image('png/knob_grey.png'), edge=5, batch=undrawable, enabled =False)

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
@dropdown_list_header.event
def on_release():
    sldisp.dispatch_event('slider_activate', nmda, batch)
    sldisp.dispatch_event('slider_activate', ampa, batch)
    dropdown_list_header.pic_change_dep(image.load('png/choose_receptor/choose_button.png'))
    dropdown_list_header.pic_change_p(image.load('png/choose_receptor/choose_button.png'))
@dropdown_list_header_inh.event
def on_release():
    sldisp.dispatch_event('slider_activate', gabaa, batch)
    sldisp.dispatch_event('slider_activate', gabab, batch)
    dropdown_list_header_inh.pic_change_dep(image.load('png/choose_receptor/choose_button.png'))
    dropdown_list_header_inh.pic_change_p(image.load('png/choose_receptor/choose_button.png'))
@nmda.event
def on_release():
    sldisp.dispatch_event('slider_deactivate', nmda, undrawable)
    sldisp.dispatch_event('slider_deactivate', ampa, undrawable)
    window.keye = "NMDA"
@ampa.event
def on_release():
    sldisp.dispatch_event('slider_deactivate', nmda, undrawable)
    sldisp.dispatch_event('slider_deactivate', ampa, undrawable)
    window.keye = "AMPA"
@gabaa.event
def on_release():
    sldisp.dispatch_event('slider_deactivate', gabaa, undrawable)
    sldisp.dispatch_event('slider_deactivate', gabab, undrawable)
    window.keyi = "GABAA"
@gabab.event
def on_release():
    sldisp.dispatch_event('slider_deactivate', gabaa, undrawable)
    sldisp.dispatch_event('slider_deactivate', gabab, undrawable)
    window.keyi = "GABAB"
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
    window.dispatch_event('update_wait', image.load('png/please_wait.png'))
    calculator.proc = Popen(utils.Encoder.popen_generator(calculator.e_list, calculator.i_list, threshold.value, window.keye, window.keyi))
    pyglet.clock.schedule_interval(update, 1/2) 
    #temporary running block
    off_on([ slider_e_1, slider_e_2, slider_e_3, slider_i_1, slider_i_2, slider_i_3,threshold, calc_button, cache_button, cache_clear_button], False)
   
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
    window.dispatch_event('update_wait', image.load('png/empty.png'))
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
        off_on([ slider_e_1, slider_e_2, slider_e_3, slider_i_1, slider_i_2, slider_i_3,threshold, Membrane_potential, Esyn, Esyninh, calc_button, cache_button, cache_clear_button], True)
        pyglet.clock.unschedule(drawing_plot)

@slider_e_1.event
def on_change(val):
    spike_time = int(round(val*runtime_constant, 0))
    add_spike_time(1, calculator.e_list, spike_time)
    window.spike_times[0]= (pyglet.text.Label(f'excitatory: {str(spike_time)}', color=(211,211,211,255), x=830, y=675, batch=spike_time_batch))
    sldisp.dispatch_event('slider_activate', slider_e_2, batch)
    dropdown_list_header.pic_change_dep(image.load('png/choose_receptor/choose_button.png'))
    dropdown_list_header.pic_change_p(image.load('png/choose_receptor/choose_button.png'))
@slider_e_2.event
def on_change(val):
    spike_time = int(round(val*runtime_constant, 0))
    add_spike_time(2, calculator.e_list, spike_time)
    window.spike_times[1]= (pyglet.text.Label(f'excitatory: {str(spike_time)}', color=(211,211,211,255), x=830, y=595, batch=spike_time_batch))
    sldisp.dispatch_event('slider_activate', slider_e_3, batch)
    window.wire_picture_exc_1.image = image.load('png/wires/1-2.png')
    window.wire_picture_exc_2.image = image.load('png/wires/2-end.png')
    dropdown_list_header.pic_change_dep(image.load('png/choose_receptor/choose_button.png'))
    dropdown_list_header.pic_change_p(image.load('png/choose_receptor/choose_button.png'))
@slider_e_3.event
def on_change(val):
    spike_time = int(round(val*runtime_constant, 0))
    add_spike_time(3, calculator.e_list, spike_time)
    window.spike_times[2]= (pyglet.text.Label(f'excitatory: {str(spike_time)}', color=(211,211,211,255), x=830, y=515, batch=spike_time_batch))
    window.wire_picture_exc_3.image = image.load('png/wires/2-3.png')
    window.wire_picture_exc_2.image = image.load('png/wires/3-end.png')
    dropdown_list_header.pic_change_dep(image.load('png/choose_receptor/choose_button.png'))
    dropdown_list_header.pic_change_p(image.load('png/choose_receptor/choose_button.png'))
@slider_i_1.event
def on_change(val):
    spike_time = int(round(val*runtime_constant, 0))
    add_spike_time(1, calculator.i_list, spike_time)
    window.spike_times[3]= (pyglet.text.Label(f'inhibitory: {str(spike_time)}', color=(211,211,211,255), x=830, y=435, batch=spike_time_batch))
    sldisp.dispatch_event('slider_activate', slider_i_2, batch)
    dropdown_list_header_inh.pic_change_dep(image.load('png/choose_receptor/choose_button.png'))
    dropdown_list_header_inh.pic_change_p(image.load('png/choose_receptor/choose_button.png'))
@slider_i_2.event
def on_change(val):
    spike_time = int(round(val*runtime_constant, 0))
    add_spike_time(2, calculator.i_list, spike_time)
    window.spike_times[4]= (pyglet.text.Label(f'inhibitory: {str(spike_time)}', color=(211,211,211,255), x=830, y=355, batch=spike_time_batch))
    sldisp.dispatch_event('slider_activate', slider_i_3, batch)
    window.wire_picture_inh_1.image = image.load('png/wires_inh/1-2.png')
    window.wire_picture_inh_2.image = image.load('png/wires_inh/2-end.png')
    dropdown_list_header_inh.pic_change_dep(image.load('png/choose_receptor/choose_button.png'))
    dropdown_list_header_inh.pic_change_p(image.load('png/choose_receptor/choose_button.png'))
@slider_i_3.event
def on_change(val):
    spike_time = int(round(val*runtime_constant, 0))
    add_spike_time(3, calculator.i_list, spike_time)
    window.spike_times[5]= (pyglet.text.Label(f'inhibitory: {str(spike_time)}', color=(211,211,211,255), x=830, y=275, batch=spike_time_batch))
    window.wire_picture_inh_3.image = image.load('png/wires_inh/2-3.png')
    window.wire_picture_inh_2.image = image.load('png/wires_inh/3-end.png')
    dropdown_list_header_inh.pic_change_dep(image.load('png/choose_receptor/choose_button.png'))
    dropdown_list_header_inh.pic_change_p(image.load('png/choose_receptor/choose_button.png'))
@threshold.event
def on_commit(text):
    threshold.value = text
@Esyn.event
def on_commit(text):
    Esyn.value = text
@Esyninh.event
def on_commit(text):
    Esyninh.value = text
@Membrane_potential.event
def on_commit(text):
    Membrane_potential.value = text
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
    slider_i_1.dispatch_event('on_mouse_press', x, y, button, modifiers)
    slider_i_2.dispatch_event('on_mouse_press', x, y, button, modifiers)
    slider_i_3.dispatch_event('on_mouse_press', x, y, button, modifiers)
    slider_e_1.dispatch_event('on_mouse_press', x, y, button, modifiers)
    slider_e_2.dispatch_event('on_mouse_press', x, y, button, modifiers)
    slider_e_3.dispatch_event('on_mouse_press', x, y, button, modifiers)
    threshold.dispatch_event('on_mouse_press', x, y, button, modifiers)
    Esyn.dispatch_event('on_mouse_press', x, y, button, modifiers)
    Esyninh.dispatch_event('on_mouse_press', x, y, button, modifiers)
    Membrane_potential.dispatch_event('on_mouse_press', x, y, button, modifiers)
    calc_button.dispatch_event('on_mouse_press', x, y, button, modifiers)
    cache_button.dispatch_event('on_mouse_press', x, y, button, modifiers)
    cache_clear_button.dispatch_event('on_mouse_press', x, y, button, modifiers)
    dropdown_list_header.dispatch_event('on_mouse_press', x, y, button, modifiers)
    dropdown_list_header_inh.dispatch_event('on_mouse_press', x, y, button, modifiers)
    nmda.dispatch_event('on_mouse_press', x, y, button, modifiers)
    ampa.dispatch_event('on_mouse_press', x, y, button, modifiers)
    gabaa.dispatch_event('on_mouse_press', x, y, button, modifiers)
    gabab.dispatch_event('on_mouse_press', x, y, button, modifiers)
@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    slider_i_1.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    slider_i_2.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    slider_i_3.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    slider_e_1.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    slider_e_2.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    slider_e_3.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    threshold.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    Esyn.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    Esyninh.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    Membrane_potential.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    dropdown_list_header.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    dropdown_list_header_inh.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    nmda.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    ampa.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    gabaa.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    gabab.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
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
    dropdown_list_header.dispatch_event('on_mouse_release', x, y, buttons, modifiers)
    dropdown_list_header_inh.dispatch_event('on_mouse_release', x, y, buttons, modifiers)
    nmda.dispatch_event('on_mouse_release', x, y, buttons, modifiers)
    ampa.dispatch_event('on_mouse_release', x, y, buttons, modifiers)
    gabaa.dispatch_event('on_mouse_release', x, y, buttons, modifiers)
    gabab.dispatch_event('on_mouse_release', x, y, buttons, modifiers)
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
pyglet.app.run()
#interface change for a running block
#fullscreen
# надо будет cделать нормальные проверки на все running 