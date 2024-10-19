from .experiment_class import Experiment
def plot_flower(experiment: Experiment, max_radius=0):
    

    if max_radius == 0: 
        max_radius = experiment.get_max_radius()
    
    from .load_config import load_config
    root_path = load_config().get("plot_save_path","plots")

    name = f"flower-{experiment.get_meta_data['alias']}-{max_radius}.png"
    path = f'{root_path}/densityPlots/{name}'

    import matplotlib.pyplot as plt
    _,ax = plt.subplots()

    ax.set_ylim(-experiment.getMaxRadius() * 1.1, experiment.getMaxRadius() * 1.1)
    ax.set_xlim(-experiment.getMaxRadius() * 1.1, experiment.getMaxRadius() * 1.1)

    ax.set_aspect('equal',adjustable='box')
    ax.set_axis_off()

    ax.add_patch(plt.Circle((0,0),experiment.getMaxRadius(),fill=False,color='k'))

    print('...creating plot...')

    for seed in experiment.getSeedData(): 
        ax.add_patch(plt.Circle(seed,1,fill=True,color='k'))


    plt.savefig(path)    
    print(f"flower saved at {path}")

    