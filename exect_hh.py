from brian2 import *
import utils
import sys
import matplotlib.pyplot as plt

def calculate(e_timing: list, i_timing: list, e_lengths: list, i_lengths: list, e_syn_str: list, i_syn_str: list, esyn_value: int, keye, keyi):
    
    #repush attempt
    defaultclock.dt = 0.01*ms
    morpho = Soma(30*um)
    morpho.axon = Cylinder(diameter=1*um, length=1000*um, n=200)
    morpho.dendrite1 = Cylinder(diameter=1*um, length=200*um, n=50)
    morpho.dendrite2 = Cylinder(diameter=1*um, length=200*um, n=50)
    morpho.dendrite3 = Cylinder(diameter=1*um, length=200*um, n=50)
    El = -67*mV
    ENa = 50*mV
    EK = -100*mV
    gl = 0.1*msiemens/cm**2
    gNa0 = 100*msiemens/cm**2
    gK = 80*msiemens/cm**2
    gsynm = 500*msiemens/cm**2
    beta = 100*Hz
    Esyn = esyn_value*mV #0
    eqs = '''
    Im = gl * (El-v) + gNa * m**3 * h * (ENa-v) + gK * n**4 * (EK-v) + Is : amp/meter**2
    dm/dt = alpham * (1-m) - betam * m : 1
    dn/dt = alphan * (1-n) - betan * n : 1
    dh/dt = alphah * (1-h) - betah * h : 1
    alphah = 0.128 * exp(-(v + 50.0*mV) / (18.0*mV))/ms :Hz
    alpham = 0.32/mV * (v + 54*mV) / (1.0 - exp(-(v + 54.0*mV) / (4.0*mV)))/ms:Hz
    alphan = 0.032/mV * (v + 52*mV) / (1.0 - exp(-(v + 52.0*mV) / (5.0*mV)))/ms:Hz
    betah  = 4.0 / (1.0 + exp(-(v + 27.0*mV) / (5.0*mV)))/ms:Hz
    betam  = 0.28/mV * (v + 27.0*mV) / (exp((v + 27.0*mV) / (5.0*mV)) - 1.0)/ms:Hz
    betan  = 0.5 * exp(-(v + 57.0*mV) / (40.0*mV))/ms:Hz
    gNa : siemens/meter**2
    gsyn = gsynm * o : siemens/meter**2
    do/dt = alpha*(1-o)-beta*o : 1
    Is = gsyn * (Esyn-v) : amp/meter**2
    alpha : Hz
    '''

    neuron = SpatialNeuron(morphology=morpho, model=eqs, method="exponential_euler",
                        refractory="m > 0.2", threshold="m > 0.4",threshold_location=morpho.axon[1],
                        Cm=1*uF/cm**2, Ri=31.4*ohm*cm)
    neuron.v = -74.99891667*mV
    neuron.m = "alpham / (alpham + betam)"
    neuron.h = "alphah / (alphah + betah)"
    neuron.n = "alphan / (alphan + betan)"
    neuron.gNa = gNa0
    neuron.o = 0
    neuron.alpha = 0

    spikes = SpikeMonitor(neuron)
    st_mon = StateMonitor(neuron.axon, ["n", "m", "h", "v"], record=True)
    den_mon = StateMonitor(neuron.dendrite1, ["gsyn", "o", 'alpha', 'v', 'Im'], record=True)
    den2_mon = StateMonitor(neuron.dendrite2, ["gsyn", "o", 'alpha'], record=True)
    den3_mon = StateMonitor(neuron.dendrite3, ["gsyn", "o", 'alpha'], record=True)
    SPGG = SpikeGeneratorGroup(1, [0], [timing[0]]*ms)
    S = Synapses(SPGG, neuron,
                '''
                w : Hz
                ''',
                on_pre='''
                alpha += w 
                '''
                )

    S.connect(i=0, j=morpho.dendrite1[lengths[0]*um])
    S.connect(i=0, j=morpho.dendrite3[lengths[0]*um])
    S.connect(i=0, j=morpho.dendrite2[lengths[0]*um])
    S.w = syn_str[0]*Hz
    SPGGoff = SpikeGeneratorGroup(1, [0], [timing[0]+1]*ms)
    Soff = Synapses(SPGGoff, neuron,
                '''
                ''',
                on_pre='''
                alpha *= 0 
                '''
                )

    Soff.connect(i=0, j=morpho.dendrite1[lengths[0]*um])
    Soff.connect(i=0, j=morpho.dendrite2[lengths[0]*um])
    Soff.connect(i=0, j=morpho.dendrite3[lengths[0]*um])
    SPGG2 = SpikeGeneratorGroup(1, [0], [timing[1]]*ms)
    S2 = Synapses(SPGG2, neuron,
                '''
                w : Hz
                ''',
                on_pre='''
                alpha += w 
                '''
                )

    S2.connect(i=0, j=morpho.dendrite1[lengths[1]*um])
    S2.connect(i=0, j=morpho.dendrite2[lengths[1]*um])
    S2.connect(i=0, j=morpho.dendrite3[lengths[1]*um])
    S2.w = syn_str[1]*Hz


    SPGGoff2 = SpikeGeneratorGroup(1, [0], [timing[1]+1]*ms)
    Soff2 = Synapses(SPGGoff2, neuron,
                '''
                ''',
                on_pre='''
                alpha *= 0 
                '''
                )

    Soff2.connect(i=0, j=morpho.dendrite1[lengths[1]*um])
    Soff2.connect(i=0, j=morpho.dendrite2[lengths[1]*um])
    Soff2.connect(i=0, j=morpho.dendrite3[lengths[1]*um])
    SPGG3 = SpikeGeneratorGroup(1, [0], [timing[2]]*ms)
    S3 = Synapses(SPGG3, neuron,
                '''
                w : Hz
                ''',
                on_pre='''
                alpha += w 
                '''
                )

    S3.connect(i=0, j=morpho.dendrite1[lengths[2]*um])
    S3.connect(i=0, j=morpho.dendrite2[lengths[2]*um])
    S3.connect(i=0, j=morpho.dendrite3[lengths[2]*um])
    S3.w = syn_str[2]*Hz


    SPGGoff3 = SpikeGeneratorGroup(1, [0], [timing[2]+1]*ms)
    Soff3 = Synapses(SPGGoff3, neuron,
                '''
                ''',
                on_pre='''
                alpha *= 0 
                '''
                )

    Soff3.connect(i=0, j=morpho.dendrite1[lengths[2]*um])
    Soff3.connect(i=0, j=morpho.dendrite2[lengths[2]*um])
    Soff3.connect(i=0, j=morpho.dendrite3[lengths[2]*um])

    network = Network()
    network.add(neuron, den_mon, den2_mon,SPGG, S, SPGG2, S2,SPGGoff, Soff, SPGG3, S3,SPGGoff3, Soff3,SPGGoff2, Soff2, st_mon, spikes)

    network.run(1000*ms)

    x, y = st_mon.t[:]*1000, st_mon.v[0][:]*1000 

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
    #accept written?
    e_list_read_str, i_list_read_str, e_lengths_read_str, i_lengths_read_str, e_sys_str_read_str, i_syn_str_read_str, esyn_value_str, keye, keyi = utils.CompartmentEncoder.arg_acceptor()
    
    e_list_read = utils.CompartmentEncoder.decoder(e_list_read_str)
    i_list_read = utils.CompartmentEncoder.decoder(i_list_read_str)

    e_lengths_read = utils.CompartmentEncoder.decoder(e_lengths_read_str)
    i_lengths_read = utils.CompartmentEncoder.decoder(i_lengths_read_str)

    e_sys_str_read = utils.CompartmentEncoder.decoder(e_sys_str_read_str)
    i_sys_str_read = utils.CompartmentEncoder.decoder(i_syn_str_read_str)

    esyn_value = utils.CompartmentEncoder.text_value_decoder(esyn_value_str)

    plots = calculate(e_list_read, i_list_read, e_lengths_read, i_lengths_read, esyn_value, e_sys_str_read, i_sys_str_read, esyn_value, keye, keyi)
    figure, axes = plots[0], plots[1]
    figure_c, axes_c = plots[2], plots[3]
    save_plot(figure, axes, 'plotting')
    save_plot(figure_c, axes_c, 'plotting_c')
