#
# Copyright © 2023 University of Strasbourg. All Rights Reserved.
# See AUTHORS.md for the list of authors.
#

from pkg_resources import resource_filename
from tabulate import tabulate
from matplotlib import pyplot as plt
from IPython.display import display, HTML, set_matplotlib_formats
#from cycler import cycler

# define colors for plots
qp_color1 = "#0c7e8f"
qp_color2 = "#EC7016"
qp_color3 = "#A4598D"
qp_color4 = "#006E51"
qp_color5 = "#96694A"
qp_color6 = "#7E6A98"

#mpl.rcParams['axes.prop_cycle'] = cycler('color', [qp_color1, 
#    qp_color2, qp_color3, qp_color4, qp_color5, qp_color6]) 

# improve quality of plots
set_matplotlib_formats('svg','pdf')

# modify jupyter css
css = resource_filename(__name__, 'assets/custom.css')
with open( css, 'r' ) as f: style = f.read()
display(HTML( style ))

def ptime(time):
    """ 
        print `time` with appropriate units
    """
    if time<1e-6: print(f"{time*1e9:.3g} ns"); return
    if time<1e-3: print(f"{time*1e6:.3g} µs"); return
    if time<1e-0: print(f"{time*1e3:.3g} ms"); return
    print(f"{time:.3g} s"); return
    
def printreport(res, max_outcomes=8):
    """
    Print a report on the MIMIQ simulation results `res`

    Args
    max_outcomes (int): the maximum number of unique measurement outcomes to display (default 8)
    
    Raises:
    TypeError: if res is not a valid MIMIQ Result object
    """  
    if not hasattr(res, 'results'):
            raise TypeError(
                f"First argument is not a valid MIMIQ {Result} object")

    print("===========================")
    print("Simulation report")
    print("===========================")
    print(f"Algorithm: \t {res.results['algorithm']}")
    
    print(f"Execution time \t ", end=""); ptime(res.results['time']['apply'])
    print(f"Sampling time \t ", end=""); ptime(res.results['time']['sampling'])
    print(f"Fidelity est. \t {res.results['fidelity']:.2f} (avg. gate error {res.results['averageGateError']:.4f})")
    
    if len(res.samples) > 0:
        outcomes = sorted(res.samples, key=res.samples.get, reverse=True)[0:max_outcomes]

        print("")
        print("Measurement results")
        table = [[o.to01(), res.samples[o]] for o in outcomes]
        print(tabulate(table, headers=["state", "samples"], tablefmt='rst'))
        if len(outcomes) >= max_outcomes: print(f"results limited to {max_outcomes} items, see `res.samples` for a full list")

    if len(res.amplitudes) > 0:    
        print("")
        print("Statevector amplitudes")
        table = [[o.to01(), f"{res.amplitudes[o]:.3f}"] for o in res.amplitudes]
        print(tabulate(table, headers=["state", "amplitude"], tablefmt='rst'))

def hist(res, n_outcomes=15):
    """
    Plot a histogram of the MIMIQ simulation results `res`

    Args
    max_outcomes (int): the maximum number of unique measurement outcomes to display (default 15)

    Raises:
    TypeError: if res is not a valid MIMIQ Result object
    """  
    if not hasattr(res, 'samples'):
            raise TypeError(
                f"First argument is not a valid MIMIQ {Result} object")
    n_samples = sum(res.samples.values())


    outcomes = sorted(res.samples, key=res.samples.get, reverse=True)[0:n_outcomes]
    counts = [res.samples[x] for x in outcomes]
    labels = [x.to01() for x in outcomes]
    n_bars = len(outcomes)
    
    # calculate automatic scaling of the plot size
    w = 1+n_bars**0.5
    h = 2+6.5*len(labels[0])/100

    fig = plt.figure(figsize=(w,h))
    plt.bar(labels, counts, color=qp_color1)
    plt.xticks(rotation = 90, fontsize=8)
    plt.xlim(-1,n_bars)
    plt.ylabel(f"counts / {n_samples}")
    plt.tight_layout()

    return fig

