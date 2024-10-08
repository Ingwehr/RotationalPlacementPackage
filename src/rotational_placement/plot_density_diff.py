import matplotlib.pyplot as plt 
import os 
import numpy as np

def plotDensityDiff(aliass:list[str], diffDict:dict[list[list[int]]]) -> None:
    
    # Construct the name for saving the plot
    name = 'den_diff-' + '-'.join(aliass) + '.svg'
    path = f'plots/densityPlots/{name}'

    # Ensure the directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # Create the plot 
    f, ax = plt.subplots(1)
    
    # Loop through each experiment instance
    for i,data in enumerate(diffDict['densityDifferences']):
        radius = np.array(diffDict['radius'])
        efficacy = np.array(data)
        
        
        # Plot with the alias as the label
        ax.plot(radius, efficacy, label=aliass[i])
    
    # Set axis limits
    ax.set_ylim(ymin=0, ymax=1.03)
    ax.set_xlim(xmin=0, xmax=max(diffDict['radius']))
    
    # Adjust plot appearance
    for spine in ["bottom", "left", "top", "right"]:
        ax.spines[spine].set_linewidth(1.1)

    # Add legend
    ax.legend()
    
    plt.savefig(path)