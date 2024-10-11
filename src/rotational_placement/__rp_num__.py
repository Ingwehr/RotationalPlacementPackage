from typing import TYPE_CHECKING

if TYPE_CHECKING: 
    from experiment_class import Experiment

def __rp_num__(a: int, b: int, step_size: int, max_radius: int, experiment: Experiment):
    import numpy as np
    
    def __distance__(point_a, point_b):
        return np.sqrt((point_a[0] - point_b[0])**2 + (point_a[1] - point_b[1])**2)
    
    def __density_dict__(seed_data: list[tuple[float,float]], max_radius: int, step_size: int) -> dict[str,list[float]]:
        data_dict = {'efficacy': [], 'radius': []}
        for radius in range(2,max_radius + 1, step_size):
            efficacy = 0

            for seed in seed_data: 
                if __distance__((0,0),seed) < radius:
                    efficacy += 1
            data_dict['efficacy'].append(efficacy)
            data_dict['radius'].append(radius)
    
        return data_dict

    SEED_RADIUS = 1
    CENTER_SEED = (np.float64(0), np.float64(0))
    PI = np.pi

    def __relevance__(seed): 

        def f(x): return np.tan(ROTATION) * x + SEED_RADIUS * 2 / np.cos(ROTATION)
        def g(x): return np.tan(ROTATION) * x - SEED_RADIUS * 2 / np.cos(ROTATION)
        def h(x): return np.tan(1 / ROTATION) * x

        x = seed[0]
        y = seed[1]

        if ROTATION == 0 and -2 < y < 2 and x > 0:
            return True
        if 0 < ROTATION < PI / 2 and g(x) < y < f(x) and h(x) < y:
            return True
        if ROTATION == PI / 2 and -2 < x < 2 and y > 0:
            return True
        if PI / 2 < ROTATION < PI and f(x) < y < g(x) and h(x) < y: 
            return True
        if ROTATION == PI and -2 < y < 2 and x < 0:
            return True
        if PI < ROTATION < 3 * PI / 2 and f(x) < y < g(x) and h(x) > y:
            return True
        if ROTATION == 3 * PI / 2 and -2 < x < 2 and y < 0: 
            return True
        if 3 * PI / 2 < ROTATION < 2 * PI and g(x) < y < f(x) and h(x) > y:
            return True
        if x == 0 and y == 0: 
            return True
        return False

    def __new_seed__(relevant_seeds: list[tuple[float|int, float|int]]):

        def __sort__(element: tuple[float|int, float|int]):
            return __distance__(CENTER_SEED, element) * -1
        
        proposed_seeds = []

        relevant_seeds.sort(key=__sort__)

        for seed in relevant_seeds:
            
            relevant_x = seed[0]
            relevant_y = seed[1]

            try: 
                sqrt = np.sqrt((relevant_x + relevant_y * TAN)**2 - (1 + TAN**2)*(relevant_x**2 + relevant_y**2 - (2 * SEED_RADIUS)**2))
                new_seed_x1 = (relevant_x + relevant_y * TAN + sqrt) / (1 + TAN**2)
                new_seed_x2 = (relevant_x - relevant_y * TAN + sqrt) / (1 + TAN**2)
            except(ZeroDivisionError):
                new_seed_x1 = (relevant_x + relevant_y * TAN) / (1 + TAN**2)
                new_seed_x2 = new_seed_x1

            proposed_seeds.append(__true_seed__(new_seed_x1,new_seed_x2))

        proposed_seeds.sort(key=__sort__)
        
        return proposed_seeds[0]
    
    def __true_seed__(new_seed_x1, new_seed_x2):
        seed_1 = (new_seed_x1, TAN * new_seed_x1)
        seed_2 = (new_seed_x2, TAN * new_seed_x2)

        if __distance__(seed_1,CENTER_SEED) > __distance__(seed_2): 
            return seed_1
        if __distance__(seed_2,CENTER_SEED) > __distance__(seed_1): 
            return seed_2
        
        if __near_center__(seed_1):
            return seed_1
        else:
            return seed_2
        
    def __near_center__(seed): 
        def h(x): return (-1 / TAN) * x

        seed_x = seed[0]
        seed_y = seed[1]

        if ROTATION == 0 and seed_x > 0:
            return True
        if ROTATION == PI / 2 and seed_y > 0: 
            return True
        if ROTATION == PI and seed_x < 0: 
            return True
        if ROTATION == 3 * PI / 2 and seed_y < 0: 
            return True
        if 0 < ROTATION < PI and h(seed_x) < seed_y: 
            return True
        if PI < ROTATION < 2 * PI and h(seed_x) > seed_y:
            return True
        return False


    #-----------------main loop-----------------
    seed_data = experiment.get_seed_data()
    if len(seed_data) != 0: 
        c = len(seed_data)
    else: 
        seed_data = [CENTER_SEED]
        c = 1
    
    while __distance__(seed_data[-1], CENTER_SEED) < max_radius and c < max_radius**2: 
        
        ROTATION = 2 * PI * (((c * a) % b) / b)
        
        TAN = np.tan(ROTATION)

        relevant_seeds = []

        for seed in seed_data:
            if __relevance__(seed): 
                relevant_seeds.append(seed)
        
        seed_data.append(__new_seed__(relevant_seeds))

        c += 1

    density_dict = __density_dict__(seed_data, max_radius, step_size)

    return(density_dict,seed_data)

    