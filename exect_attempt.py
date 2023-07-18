import brian2
from brian2 import *
import matplotlib.pyplot as plt
import utils
import sys

def calculate(excite: list, inhibit: list, value):

    start_scope()

    El = -75*mV #reversal potential for Cl-, Ca2+ etc
    Esyni = -75*mV # synaptic reversal potential, -75 for inhibitory
    Esyne = 0*mV # synaptic reversal potential, 0 for excitatory

    taum = 20*ms #time constant for postsynaptic membrane
    tausyni = 25*ms #synaptic time constant (what is it)
    tausyne = 15*ms #synaptic time constant (what is it)
    vt = value*mV
    vr = -75*mV

    gmax = 0.08
    hmax = 50*Hz
    riseconste = 50*Hz
    fallconste = 50*Hz
    riseconsti = 50*Hz
    fallconsti = 50*Hz

    eqs_neurons_two = '''
    dv/dt = (gsyne * (Esyne-v) + gsyni * (Esyni-v) + El - v) / taum : volt (unless refractory)
    dgsyne/dt = -gsyne*(fallconste) + he : 1
    dhe/dt = -he*riseconste: Hz
    dgsyni/dt = -gsyni*(fallconsti) + hi : 1
    dhi/dt = -hi*riseconsti: Hz
    '''
    H = NeuronGroup(1, eqs_neurons_two, threshold='v>vt',reset='v = vr', method='euler', refractory='7*ms')
    M2 = StateMonitor(H, 'v', record=0)
    Mge = StateMonitor(H, 'gsyne', record=0)
    Mgi = StateMonitor(H, 'gsyni', record=0)
    SPi2 = SpikeMonitor(H)

    SPGGe = SpikeGeneratorGroup(1, [0]*len(excite), excite*ms)
    SPGGi = SpikeGeneratorGroup(1, [0]*len(inhibit), inhibit*ms)

    Si = Synapses(SPGGi, H,
                '''
                wh : Hz
                ''',
                on_pre='''
                hi += wh
                '''
                )

    Se = Synapses(SPGGe, H,
                '''
                wh : Hz
                ''',
                on_pre='''
                he += wh
                '''
                )
    Si.connect()
    Si.wh = hmax
    H.v = vr
    Se.connect()
    Se.wh = hmax


    run(1000*ms)

    x, y = M2.t[:]*1000, M2.v[0][:]*1000 

    fig, ax = plt.subplots(figsize=(11.28, 3.45)) 
    ax.plot(x, y, '#d2d2d2')
    
    print('success')
    return fig, ax

def save_plot(figure, axes, name='plotting'):
    axes.set_axis_off()
    extent = axes.get_window_extent().transformed(figure.dpi_scale_trans.inverted())
    figure.savefig(f'png/{name}.png', format='png', bbox_inches=extent, transparent=True) 
    plt.close(figure)



if __name__ == "__main__":    

    e_list_read_str, i_list_read_str, value_str = utils.Encoder.arg_acceptor()
    
    e_list_read = utils.Encoder.decoder(e_list_read_str)
    i_list_read = utils.Encoder.decoder(i_list_read_str)

    value = utils.Encoder.text_value_decoder(value_str)

    figure, axes = calculate(e_list_read, i_list_read, value)
    save_plot(figure, axes, 'plotting')
