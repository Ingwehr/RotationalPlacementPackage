import numpy as np

def num_rp(a:int, b:int, step_size:int, max_radius:int, exp) -> tuple[list[np.float64,np.float64],dict[str,list[int,float]]]: 
    """
    Description
    -----------
    with numerical precision generates seeds within a given boundry and returns them as a list of coord-pairs
    
    Parameters
    ----------
    a: int
        numerator of input
    b: int
        denominator of input
    step_size: int
        frequency of data collection, resolution of data
    max_radius: int
        termination point for experiment
    exp: type
        class instance of experiment with these parameters

    Returns
    -------
    seed_data: list[np.float64,np.float64]
        list containing all seed-pairs
    density_data: dict[string,list[int,float]]
        dict of radii and corresponding density within that radius
    """

    def __distance__(a:np.float64, b:np.float64): 
        return(np.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2))
    
    def __density_dict__(seed_data: list[tuple[np.float64,np.float64]]): 
        dataDict = {'efficacy': [], 'radius': []}
        for radius in range(2,max_radius + 1, step_size):
            efficacy = 0

            for seed in seed_data: 
                if __distance__((0,0),seed) < radius:
                    efficacy += 1
            dataDict['efficacy'].append(efficacy)
            dataDict['radius'].append(radius)
        
        return dataDict

    seed_radius = 1
    center_seed = (np.float64(0),np.float64(0))

    def __relevance__(seed):
        def f(x):
            return(np.tan(rotation) * x + ((seed_radius*2) / np.cos(rotation)))
        def g(x):
            return(np.tan(rotation) * x - ((seed_radius*2) / np.cos(rotation)))
        def h(x):
            return((-1 / np.tan(rotation) * x))
    
        x = seed[0]
        y = seed[1]

        #Åtta fall utefter om rotationen är längs med axlarna eller i 1a 2a 3e 4e kvadranten (alla har varsitt fall) 
        if (rotation == 0) and (-2 < y and y < 2) and (x > 0):
            return(True)
        elif (0 < rotation and rotation < (np.pi / 2)) and (g(x) < y < f(x)) and h(x) < y:
            return(True)
        elif (rotation == np.pi/2) and (-2 < x and x < 2) and (y > 0):
            return True
        elif ((np.pi / 2) < rotation and rotation < np.pi) and (f(x) < y and y < g(x)) and h(x) < y:
            return(True)
        elif (rotation == np.pi) and -2 < y < 2 and x < 0:
            return(True)
        elif (np.pi < rotation and rotation < (3 * np.pi) / 2) and (f(x) < y and y < g(x)) and h(x) > y:
            return(True)
        elif (rotation == (3 * np.pi) / 2) and (-2 < x < 2) and (y < 0):
            return(True)
        elif ((3 * np.pi) / 2 < rotation and rotation < 2 * np.pi) and (g(x) < y and y < f(x)) and h(x) > y:
            return(True)
        elif x == 0 and y == 0:
            return(True) 
        else:
            return(False)

    def __new_seed__(relevantSeeds): 
        #Kallas för att sortera utefter avståndet mellan mitten och punkten som skickats med
        def Sort(element):
            return(__distance__(center_seed,element))
        #Proposed seeds håller alla förslag på nya frön 
        proposedSeeds = []
    
        #abc-formeln för att bestämma två lösningar på vart det nya fröet ska ligga utifrån alla relevanta frön
        relevantSeeds.sort(key=Sort,reverse=True)
        for seed in relevantSeeds[:4] or relevantSeeds:
            relevantSeedX = seed[0]
            relevantSeedY = seed[1]
    
            af = (1 + np.tan(rotation)**2)
            bf = (relevantSeedX + relevantSeedY*np.tan(rotation))
            cf = (relevantSeedX**2 + relevantSeedY**2 - (2*seed_radius)**2)
            
            try:
                newSeed_x1 = (bf + np.sqrt(bf**2 - af*cf))/af
                newSeed_x2 = (bf - np.sqrt(bf**2 - af*cf))/af
            except(ZeroDivisionError):
                newSeed_x1 = (bf / af)
                newSeed_x2 = (bf / af)
        
            #True seed bestämmer vilken av lösningarna som är den relevanta och lägger in i proposed seeds
            proposedSeeds.append(__true_seed__(newSeed_x1,newSeed_x2))
        
        #proposed seeds sorteras och det största värdet är det nya fröet
        proposedSeeds.sort(key=Sort,reverse=True)

        return(proposedSeeds[0])

    def __true_seed__(newSeed_x1,newSeed_x2):
        if __distance__((newSeed_x1, newSeed_x1 * np.tan(rotation)),center_seed) > __distance__((newSeed_x2, newSeed_x2 * np.tan(rotation)),center_seed):
            newSeed = (newSeed_x1, newSeed_x1 * np.tan(rotation))
            
        elif __distance__((newSeed_x1, newSeed_x1 * np.tan(rotation)),center_seed) < __distance__((newSeed_x2, newSeed_x2 * np.tan(rotation)),center_seed):
            newSeed = (newSeed_x2, newSeed_x2 * np.tan(rotation))
        else:
            if __near_center_seeds__((newSeed_x1, newSeed_x1 * np.tan(rotation))):
                newSeed = (newSeed_x1, newSeed_x1 * np.tan(rotation))
            if not __near_center_seeds__((newSeed_x1, newSeed_x1 * np.tan(rotation))):
                newSeed = (newSeed_x2, newSeed_x2 * np.tan(rotation))
        return(newSeed)

    def __near_center_seeds__(seed):
        def h(x):
            return(-1/np.tan(rotation)*x)

        x = seed[0]
        y = seed[1]

        if rotation == 0:
            if x > 0:
                return(True)
            else:
                return(False)
        elif rotation == (np.pi/2):
            if y > 0:
                return(True)
            else:
                return(False)
        elif rotation == np.pi:
            if x < 0:
                return(True)
            else:
                return(False)
        elif rotation == (3 * np.pi) / 2:
            if y < 0:
                return(True)
            else:
                return(False)
        elif 0 < rotation and rotation < np.pi:
            if h(x) < y:
                return(True)
            else:
                return(False)
        elif np.pi < rotation and rotation < 2 * np.pi:
            if h(x) > y:
                return(True)
            else:
                return(False)
    #if there is existing data, continue from there, othw start from beginning
    if exp.getSeedData in locals():
        c = len(exp.getSeedData)
        seedData = exp.getSeedData
    else: 
        c = 1
        seedData = [(0,0)]
    
    while __distance__(seedData[-1], center_seed) < max_radius  and c < max_radius * max_radius:

        rotation = 2 * np.pi * (((c * a) % b) / b)

        relevantSeeds = []
         
        for seed in seedData:
            if __relevance__(seed):
                relevantSeeds.append(seed)

        newSeed = __new_seed__(relevantSeeds)

        seedData.append(newSeed)
        c += 1
    
    densityData = __density_dict__(seedData,max_radius,step_size)

    return(densityData,seedData)
