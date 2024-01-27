from brian2 import *
import utils
import matplotlib.pyplot as plt
import classes
import matplotlib.transforms as trn

def calculate(timing, strength, caching):
    
    defaultclock.dt = 0.01*ms

    morpho = Soma(30*um)
    morpho.axon = Cylinder(diameter=1*um, length=1000*um, n=200)
    morpho.dendrite1 = Cylinder(diameter=1*um, length=200*um, n=50)
    morpho.dendrite2 = Cylinder(diameter=1*um, length=200*um, n=50)
   
    timing_aug = [i+1 for i in timing]
    El = -67*mV
    ENa = 50*mV
    EK = -100*mV
    gl = 0.1*msiemens/cm**2
    gNa0 = 100*msiemens/cm**2
    gK = 80*msiemens/cm**2
    gsynmnmda = 20*msiemens/cm**2
    Esynmda = 0*mV
    Rb = 5*10**6 *Hz
    Ru = 12.9*Hz
    Rd = 8.4*Hz
    Rr = 6.8*Hz
    Ro = 46.5*Hz
    Rc = 73.8*Hz

    gsynmamp = 700*msiemens/cm**2
    Esynamp = 0*mV
    Rba = 13*10**6 *Hz
    Ru1 = 5.9*Hz
    Ru2 = 8.6*10**4*Hz
    Rda = 900*Hz
    Rra = 64*Hz
    Roa = 2.7*10**3*Hz
    Rca = 200*Hz

    gsynmga = 500*msiemens/cm**2
    Esynga = -70*mV
    Rb1ga = 20*10**6 *Hz
    Rb2ga = 10*10**6 *Hz
    Ru1ga = 4.6*10**3*Hz
    Ru2ga = 9.2*10**3*Hz
    Ro1ga = 3.3*10**3*Hz
    Ro2ga = 10.6*10**3*Hz
    Rc1ga = 9.8*10**3*Hz
    Rc2ga = 410*Hz

    gsynmgb = 120*msiemens/cm**2
    Kd = 10**-22
    K1 = 6.6*10**5*Hz
    K2 = 20*Hz
    K3 = 5.3*Hz
    K4 = 17*Hz
    K5 = 8.3*10**-5*Hz
    K6 = 7.9*Hz

    eqs = '''
    Im = gl * (El-v) + gNa * m**3 * h * (ENa-v) + gK * n**4 * (EK-v) + Isnmda + Isamp + Isga - Isgb : amp/meter**2
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

    gsynmda = gsynmnmda * O : siemens/meter**2
    dCo/dt = -Co*Rb*tr + Ru*C1 : 1
    dC1/dt = -Rb*tr*C1+C2*Ru+Co*Rb*tr-C1*Ru : 1
    dC2/dt = C1*Rb*tr + D*Rd+O*Rc-C2*(Ro+Ru+Rr) : 1
    dO/dt = C2*Ro-O*Rc : 1
    dD/dt = C2*Rr-Rd*D : 1
    Isnmda = gsynmda * (Esynmda-v) * block : amp/meter**2
    block = 1/(1+(exp(-0.062*v/volt)*2*10**-3)/3.57) : 1
    tr : 1

    gsynamp = gsynmamp * Oa : siemens/meter**2
    dCoa/dt = -Coa*Rba*tra + Ru1*C1a : 1
    dC1a/dt = -C1a*(Ru1+Rda+Rba*tra) + Coa*Rba*tra + D1*Rra+C2a*Ru2 : 1
    dC2a/dt = -C2a*(Ru2+Rda+Roa)+ C1a*Rba*tra + D2*Rra + Oa*Rca : 1
    dOa/dt = C2a*Roa-Oa*Rca : 1
    dD1/dt = C1a*Rda-Rda*D1 : 1
    dD2/dt = C2a*Rda-Rda*D2 : 1
    Isamp = gsynamp * (Esynamp-v) : amp/meter**2
    tra : 1

    gsynga = gsynmga * (O1ga +O2ga) : siemens/meter**2
    dCoga/dt = -Coga*Rb1ga*trga + Ru1ga*C1ga : 1
    dC1ga/dt = -C1ga*(Ru1ga+Ro1ga+Rb2ga*trga) + Coga*Rb1ga*trga + O1ga*Rc1ga +C2ga*Ru2ga : 1
    dC2ga/dt = -C2ga*(Ru2ga+Ro2ga)+ C1ga*Rb2ga*trga + O2ga*Rc2ga : 1
    dO1ga/dt = C1ga*Ro1ga-O1ga*Rc1ga : 1
    dO2ga/dt = C2ga*Ro2ga-O2ga*Rc2ga : 1
    Isga = gsynga * (Esynga-v) : amp/meter**2
    trga : 1

    # 0.001
    dRgb/dt = K1*trgb*(1-Rgb-Dgb)-K2*Rgb + K3*Dgb : 1
    dDgb/dt = K4*Rgb-K3*Dgb : 1
    dGgb/dt = K5*Rgb-K6*Ggb : 1
    Isgb = gsynmgb *((Ggb**4)/((Ggb**4)+Kd))*(v+95*mV) : amp/meter**2
    trgb : 1
    '''

    neuron = SpatialNeuron(morphology=morpho, model=eqs, method="euler",
                        refractory="m > 0.2", threshold="m > 0.4",threshold_location=morpho.axon[1],
                        Cm=1*uF/cm**2, Ri=31.4*ohm*cm)
    neuron.v = -66.5911055*mV
    neuron.m = "alpham / (alpham + betam)"
    neuron.h = "alphah / (alphah + betah)"
    neuron.n = "alphan / (alphan + betan)"
    neuron.gNa = gNa0
    neuron.O = 0
    neuron.Co = 1
    neuron.C1 = 0
    neuron.C2 = 0
    neuron.D = 0

    neuron.Oa = 0
    neuron.Coa = 1
    neuron.C1a = 0
    neuron.C2a = 0
    neuron.D1 = 0
    neuron.D2 = 0

    neuron.O1ga = 0
    neuron.O2ga = 0
    neuron.Coga = 1
    neuron.C1ga = 0
    neuron.C2ga = 0

    neuron.Rgb = 0
    neuron.Dgb = 0
    neuron.Ggb = 0

    spikes = SpikeMonitor(neuron)
    st_mon = StateMonitor(neuron.axon, ['v'], record=True)
    den_mon = StateMonitor(neuron.dendrite1, ['v'], record=True)
    den2_mon = StateMonitor(neuron.dendrite2, ['v'], record=True)
    network = Network()

    def synaptic_tr(lengths, timings, strengths):
        SPGG = SpikeGeneratorGroup(1, [0]*len(timings[0]), timings[0]*ms)
        S = Synapses(SPGG, neuron,
                    '''
                    w : 1
                    wa : 1
                    wga : 1
                    wgb : 1
                    ''',
                    on_pre='''
                    tr += w 
                    tra += wa
                    trga += wga
                    trgb += wgb
                    '''
                    )
        S.connect(i=0, j=morpho.dendrite1[lengths[0]*um])
        S.connect(i=0, j=morpho.dendrite2[lengths[0]*um])
        S.w = strengths[0][0]
        S.wa = strengths[0][1]
        S.wgb = strengths[0][2]
        S.wga = strengths[0][3]
        SPGGoff = SpikeGeneratorGroup(1, [0]*len(timings[0]), [i+1 for i in timings[0]]*ms)
        Soff = Synapses(SPGGoff, neuron,
                    '''
                    ''',
                    on_pre='''
                    tr *=0 
                    tra *=0 
                    trgb *=0 
                    trga *=0 
                    '''
                    )
        Soff.connect(i=0, j=morpho.dendrite1[lengths[0]*um])
        Soff.connect(i=0, j=morpho.dendrite2[lengths[0]*um])
        SPGG2 = SpikeGeneratorGroup(1, [0]*len(timings[1]), timings[1]*ms)
        S2 = Synapses(SPGG2, neuron,
                    '''
                    w : 1
                    wa : 1
                    wga : 1
                    wgb : 1
                    ''',
                    on_pre='''
                    tr += w 
                    tra += wa
                    trga += wga
                    trgb += wgb
                    '''
                    )
        S2.connect(i=0, j=morpho.dendrite1[lengths[1]*um])
        S2.connect(i=0, j=morpho.dendrite2[lengths[1]*um])
        S2.w = strengths[1][0]
        S2.wa = strengths[1][1]
        S2.wgb = strengths[1][2]
        S2.wga = strengths[1][3]
        SPGGoff2 = SpikeGeneratorGroup(1, [0]*len(timings[1]), [i+1 for i in timings[1]]*ms)
        Soff2 = Synapses(SPGGoff2, neuron,
                    '''
                    ''',
                    on_pre='''
                    tr *=0 
                    tra *=0 
                    trgb *=0 
                    trga *=0 
                    '''
                    )
        Soff2.connect(i=0, j=morpho.dendrite1[lengths[1]*um])
        Soff2.connect(i=0, j=morpho.dendrite2[lengths[1]*um])
        network.add(neuron, den_mon, den2_mon,SPGG, S, SPGG2, S2,SPGGoff, Soff,SPGGoff2, Soff2,st_mon, spikes)

    
    lengtharr = [197, 15] 
    synaptic_tr(lengtharr, timing, strength)
    

    network.run(1000*ms, report='text')
    def cache(x, y, does_cache):
            '''
            Accepts a list of x coordinates, y coordinates of plot points and a true/false caching variable
            #x = st_mon.t[:]*1000
            #y = st_mon.v[0][:]*1000 
            does_cache = False
            '''
            if does_cache:
                classes.Cacheholder.list_of_plots.append(y)
                fig, ax = plt.subplots(figsize=(13.13, 5.67)) 
                for plots in classes.Cacheholder.list_of_plots[:len(classes.Cacheholder.list_of_plots)-1]:
                    ax.plot(x, plots, '#d2d2d2', alpha = 0)
                ax.plot(x, classes.Cacheholder.list_of_plots[-1],'#d2d2d2') 
                fig_c, ax_c = plt.subplots(figsize=(13.1, 5.67)) 
                for plots in classes.Cacheholder.list_of_plots[:len(classes.Cacheholder.list_of_plots)-1]:
                    ax_c.plot(x, plots, '#404040')
                ax_c.plot(x, classes.Cacheholder.list_of_plots[-1],'#d2d2d2', alpha=0)
                print('success cache')
                return fig, ax, fig_c, ax_c, [min(y)/volt, max(y)/volt]
            else: 
                classes.Cacheholder.list_of_plots = []
                classes.Cacheholder.list_of_plots.append(y)
                fig, ax = plt.subplots(figsize=(13.13, 5.67)) 
                ax.plot(x, y, '#d2d2d2')
                fig_c, ax_c = plt.subplots(figsize=(13.1, 5.67)) 
                #это ось
                ax_c.plot(x, y, '#404040', alpha = 0)
                print('success no cache')
                return fig, ax, fig_c, ax_c, [min(y)/volt, max(y)/volt]
            
    figure, axes, figure_c, axes_c, list_of_max_min = cache(st_mon.t[:]*1000, st_mon.v[0][:]*1000, caching)
    return figure, axes, figure_c, axes_c, list_of_max_min



def save_plot(figure, axes, y, name='plotting'):
    axes.set_yticks(np.arange(y[0],y[1]+1, step=1))
    axes.spines['top'].set_visible(False)
    axes.spines['right'].set_visible(False)
    axes.spines['bottom'].set_visible(False)
    axes.spines['left'].set_visible(False)
    axes.get_xaxis().set_visible(False)
    extent = axes.get_window_extent().transformed(figure.dpi_scale_trans.inverted())
    extent_array = np.array([[0, 0.5], [extent.get_points()[1][0], extent.get_points()[1][1]+0.1]])
    extent1 = trn.Bbox(extent_array)
    figure.savefig(f'png/plotting/{name}.png', format='png', bbox_inches=extent1, transparent=True)

# we have a list of timings that is just 4 listls of timings that go like this: [[1 distal], [1 proximal], [2 distal], [2 proximal]], a list of strengths that goes like this 
#[[nmda, ampa, gabab, gaba], [nmda, ampa, gabab, gaba], [nmda, ampa, gabab, gaba], [nmda, ampa, gabab, gaba]] that is true/false and that gets accepted as a list where for every true
#nmda ampa gabab gabaa becomes
#0.0001 0.0001 0.001 0.0001 
#and for every false its 0
#caching is just a true/false 


if __name__ == "__main__":    
    #здесь я ничего не трогала
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
