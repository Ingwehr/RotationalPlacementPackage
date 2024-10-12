def __rp_num__(a: int, b: int, step_size: int, max_radius: int, experiment) -> tuple[dict[str, float], list[dict[str, float | int]]]:
    import numpy as np
    
    def __distance(point_a, point_b):
        return np.sqrt((point_a['x'] - point_b['x'])**2 + (point_a['y'] - point_b['y'])**2)
    
    def __density_dict(seed_data: list[dict[str, float]], max_radius: int, step_size: int) -> dict[str, list[float]]:
        data_dict = {'efficacy': [], 'radius': []}
        for radius in range(2, max_radius + 1, step_size):
            efficacy = sum(1 for seed in seed_data if seed['distance'] < radius)
            data_dict['efficacy'].append(efficacy)
            data_dict['radius'].append(radius)
    
        return data_dict

    SEED_RADIUS = 1
    CENTER_SEED = {'x': 0, 'y': 0, 'distance': 0}
    PI = np.pi
    ROTATION = 2 * PI * a / b

    def __relevance(seed): 
        def f(x): return np.tan(rotation) * x + SEED_RADIUS * 2 / np.cos(rotation)
        def g(x): return np.tan(rotation) * x - SEED_RADIUS * 2 / np.cos(rotation)
        def h(x): return np.tan(1 / rotation) * x

        x = seed['x']
        y = seed['y']

        if rotation == 0 and -2 < y < 2 and x > 0:
            return True
        if 0 < rotation < PI / 2 and g(x) < y < f(x) and h(x) < y:
            return True
        if rotation == PI / 2 and -2 < x < 2 and y > 0:
            return True
        if PI / 2 < rotation < PI and f(x) < y < g(x) and h(x) < y: 
            return True
        if rotation == PI and -2 < y < 2 and x < 0:
            return True
        if PI < rotation < 3 * PI / 2 and f(x) < y < g(x) and h(x) > y:
            return True
        if rotation == 3 * PI / 2 and -2 < x < 2 and y < 0: 
            return True
        if 3 * PI / 2 < rotation < 2 * PI and g(x) < y < f(x) and h(x) > y:
            return True
        if x == 0 and y == 0: 
            return True
        return False

    def __new_seed(relevant_seeds: list[dict[str, float | int]]):
        def __sort(element: dict[str, float | int]) -> float:
            return element['distance'] * -1
        
        proposed_seeds = []
        relevant_seeds.sort(key=__sort)

        for seed in relevant_seeds:
            relevant_x = seed['x']
            relevant_y = seed['y']

            try: 
                sqrt = np.sqrt((relevant_x + relevant_y * tan)**2 - (1 + tan**2)*(relevant_x**2 + relevant_y**2 - (2 * SEED_RADIUS)**2))
                new_seed_x1 = (relevant_x + relevant_y * tan + sqrt) / (1 + tan**2)
                new_seed_x2 = (relevant_x - relevant_y * tan + sqrt) / (1 + tan**2)
            except(ZeroDivisionError):
                new_seed_x1 = (relevant_x + relevant_y * tan) / (1 + tan**2)
                new_seed_x2 = new_seed_x1

            proposed_seeds.append(__true_seed(new_seed_x1, new_seed_x2))

        return max(proposed_seeds, key=lambda seed: seed["distance"])
    
    def __true_seed(new_seed_x1, new_seed_x2):
        seed_1 = {'x': new_seed_x1, 'y': tan * new_seed_x1, 'distance': __distance({'x': new_seed_x1, 'y': tan * new_seed_x1}, CENTER_SEED)}
        seed_2 = {'x': new_seed_x2, 'y': tan * new_seed_x2, 'distance': __distance({'x': new_seed_x2, 'y': tan * new_seed_x2}, CENTER_SEED)}

        if seed_1['distance'] > seed_2['distance']: 
            del seed_2
            return seed_1
        if seed_2['distance'] > seed_1['distance']: 
            del seed_1
            return seed_2
        
        if __near_center(seed_1):
            del seed_2
            return seed_1
        else:
            del seed_1
            return seed_2
        
    def __near_center(seed): 
        def h(x): return (-1 / tan) * x

        seed_x = seed['x']
        seed_y = seed['y']

        if rotation == 0 and seed_x > 0:
            return True
        if rotation == PI / 2 and seed_y > 0: 
            return True
        if rotation == PI and seed_x < 0: 
            return True
        if rotation == 3 * PI / 2 and seed_y < 0: 
            return True
        if 0 < rotation < PI and h(seed_x) < seed_y: 
            return True
        if PI < rotation < 2 * PI and h(seed_x) > seed_y:
            return True
        return False

    #-----------------main loop-----------------
    seed_data = experiment.get_seed_data()
    if len(seed_data) != 0: 
        seed_data = [{'x': s[0], 'y': s[1], 'distance': __distance({'x': s[0], 'y': s[1]}, CENTER_SEED)} for s in seed_data]
        c = len(seed_data)
    else: 
        seed_data = [CENTER_SEED]
        c = 1
    
    while seed_data[-1]['distance'] < max_radius and c < max_radius**2: 
        rotation = (ROTATION * c) % (2 * PI)
        tan = np.tan(rotation)

        relevant_seeds = [seed for seed in seed_data if __relevance(seed)]
        new_seed = __new_seed(relevant_seeds)
        new_seed['distance'] = __distance(new_seed, CENTER_SEED)
        seed_data.append(new_seed)

        c += 1

    density_dict = __density_dict(seed_data, max_radius, step_size)
    return density_dict, seed_data
