import brian2
from brian2 import *
import matplotlib.pyplot as plt
import utils
import sys

def calculate(excite: list, inhibit: list, threshold_value, esyn_value, esyninh_value, membrpot_value, keye, keyi):

    start_scope()
    El = membrpot_value*mV #reversal potential for Cl-, Ca2+ etc
    Esyni = esyninh_value*mV # synaptic reversal potential, -75 for inhibitory
    Esyne = esyn_value*mV # synaptic reversal potential, 0 for excitatory
    taum = 20*ms #time constant for postsynaptic membrane
    vt = threshold_value*mV
    vr = -75*mV

    ereceptors = {"AMPA": [1100*Hz,1000*Hz,300*Hz], "NMDA" : [100*Hz,100*Hz,20*Hz]}
    ireceptors = {"GABAA": [2500*Hz, 1100*Hz, 110*Hz], "GABAB": [50*Hz, 10*Hz, 10*Hz]}

    hmaxe = ereceptors[keye][0]
    riseconste = ereceptors[keye][1]
    fallconste = ereceptors[keye][2]
    hmaxi = ireceptors[keyi][0]
    riseconsti = ireceptors[keyi][1]
    fallconsti = ireceptors[keyi][2]


    eqs_neurons_two = '''
    Ise = gsyne * (Esyne-v) : volt
    Isi = gsyni * (Esyni-v) : volt
    dv/dt = (Ise + Isi + El - v) / taum : volt (unless refractory)
    dgsyne/dt = -gsyne*(fallconste) + he : 1
    dhe/dt = -he*riseconste: Hz
    dgsyni/dt = -gsyni*(fallconsti) + hi : 1
    dhi/dt = -hi*riseconsti: Hz
    '''
    H = NeuronGroup(1, eqs_neurons_two, threshold='v>vt',reset='v = vr', method='euler', refractory='7*ms')
    M2 = StateMonitor(H, 'v', record=0)

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
    Se.connect()

    Si.wh = hmaxi
    Se.wh = hmaxe

    H.v = El

    run(1000*ms)

    x, y = M2.t[:]*1000, M2.v[0][:]*1000 

    fig, ax = plt.subplots(figsize=(13.13, 5.67)) 
    ax.plot(x, y, '#d2d2d2')
    fig_c, ax_c = plt.subplots(figsize=(13.1, 5.67)) 
    ax_c.plot(x, y, '#404040')
    print('success')
    return fig, ax, fig_c, ax_c



def save_plot(figure, axes, name='plotting'):
    axes.set_axis_off()
    extent = axes.get_window_extent().transformed(figure.dpi_scale_trans.inverted())
    figure.savefig(f'png/plotting/{name}.png', format='png', bbox_inches=extent, transparent=True) 
    plt.close(figure)



if __name__ == "__main__":    

    e_list_read_str, i_list_read_str, threshold_value_str, esyn_value_str, esyninh_value_str, membrpot_value_str, keye, keyi = utils.Encoder.arg_acceptor()
    
    e_list_read = utils.Encoder.decoder(e_list_read_str)
    i_list_read = utils.Encoder.decoder(i_list_read_str)

    threshold_value = utils.Encoder.text_value_decoder(threshold_value_str)
    esyn_value = utils.Encoder.text_value_decoder(esyn_value_str)
    esyninh_value = utils.Encoder.text_value_decoder(esyninh_value_str)
    membrpot_value = utils.Encoder.text_value_decoder(membrpot_value_str)

    plots = calculate(e_list_read, i_list_read, threshold_value, esyn_value, esyninh_value, membrpot_value, keye, keyi)
    figure, axes = plots[0], plots[1]
    figure_c, axes_c = plots[2], plots[3]
    save_plot(figure, axes, 'plotting')
    save_plot(figure_c, axes_c, 'plotting_c')
