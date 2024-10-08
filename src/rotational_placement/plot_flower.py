import matplotlib.pyplot as plt
from experiment_class import Experiment
def plot_flower(experiment: Experiment):
    """
    Description
    -----------
    plots the flower of an experiment, a circle with seeds within 

    Parameters
    ---------
    experiment: Experiment 
        Experiment class instance with seed_data 
    """

    name = f'{experiment.alias}-{experiment.a},{experiment.b}-{experiment.stepSize}-{experiment.experimentType}.svg'
    path = f'plots/flowerPlots/{name}'

    fig,ax = plt.subplots()

    ax.set_ylim(-experiment.getMaxRadius() * 1.1, experiment.getMaxRadius() * 1.1)
    ax.set_xlim(-experiment.getMaxRadius() * 1.1, experiment.getMaxRadius() * 1.1)

    ax.set_aspect('equal',adjustable='box')
    ax.set_axis_off()

    ax.add_patch(plt.Circle((0,0),experiment.getMaxRadius(),fill=False,color='k'))
    for seed in experiment.getSeedData(): 
        ax.add_patch(plt.Circle(seed,1,fill=True,color='k'))


    plt.savefig(path)
