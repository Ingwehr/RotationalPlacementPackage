import matplotlib.pyplot as plt
import os 
import numpy as np
from .experiment_class import Experiment


def plot_heatmap(data:list[list[float]], experiment: Experiment):
    from load_config import load_config
    root_path = load_config()["plot_save_path"]

    #save dir
    name = f'{len(data[0])}-{experiment.get_experiment_type()}.svg'
    path = f'{root_path}/heatmaps/{name}'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    #heatmap
    plt.imshow(data, cmap='inferno', interpolation='none', origin='lower')

    #ticks 
    num_ticks = len(data[0])
    ticks = list(range(1, num_ticks + 1))    
    plt.xticks(ticks=np.arange(num_ticks), labels=ticks, rotation=-90,fontsize=4)
    plt.yticks(ticks=np.arange(num_ticks), labels=ticks, rotation=0,fontsize=4)

    #title
    plt.title(f'{experiment.get_experiment_type()}, {len(data[0])}x{len(data[0])}')

    plt.savefig(path)