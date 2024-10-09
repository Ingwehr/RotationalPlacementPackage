import os
import re
import numpy as np

import rotational_placement.__ff_rp__ as __ff_rp__
import rotational_placement.__num_rp__ as __num_rp__
import rotational_placement.load_config as load_config

class Experiment: 
    def __init__(self, alias:str, a:int, b:int, step_size:int, experiment_type:str): 
        self.alias = str(alias)
        self.a = int(a)
        self.b = int(b)
        self.step_size = step_size
        self.experiment_type = experiment_type

        root_path = load_config()["plot_save_path"]

        self.name = f'{self.alias}-{self.a},{self.b}-{self.step_size}-{self.experiment_type}.txt'
        self.path = os.path.join(root_path,self.experiment_type, self.alias, self.name)

        self.seed_data = []
        self.density_data = {"efficacy":[],"radius":[]}

        os.makedirs(os.path.dirname(self.path),exist_ok=True)

    def run_experiment(self, max_radius): 
        if self.experiment_type == 'num':
            self.density_data,self.seed_data = __num_rp__(self.a,self.b,self.step_size,max_radius,self)
        elif self.experiment_type == 'ff': 
            self.density_data,self.segment_data = __ff_rp__(self.a,self.b.self.step_size,self.max_radius,self)
        elif self.experiment_type == 'sym': 
            pass
        else: 
            raise ValueError("invalid experiment type")
        
    def write_to_file(self): 
        '''
        DESCRIPTION
        -----------
        Writes the experiment metadata and data to a file.

        RETURNS 
        -------
        None 
        '''
        with open(self.path, 'w') as file:
            file.write(f'alias:{self.alias}\n')
            file.write(f'a:{self.a}\n')
            file.write(f'b:{self.b}\n')
            file.write(f'stepSize:{self.stepSize}\n')
            file.write(f'experimentType:{self.experimentType}\n')
            
            file.write('--- Seed Data ---\n')
            for seed in self.seedData:
                file.write(f'{seed}\n')
            
            file.write('--- Density Data ---\n')
            for efficacy, radius in zip(self.densityData['efficacy'], self.densityData['radius']):
                file.write(f'{efficacy},{radius}\n')
        
        print('...data written to file...')

    def get_meta_data(self): 
        return {'alias':self.alias,
                'a':self.a,
                'b':self.b,
                'experimentType':self.experimentType,
                'stepSize':self.stepSize}
    
    def get_max_radius(self): 
        return int(self.density_data["radius"][-1])
    
    def get_experiment_type(self): 
        return self.experiment_type
    
    def get_density_data(self):
        return [float(e) / (float(r) ** 2) for e, r in zip(self.densityData['efficacy'], self.densityData['radius'])]
    
    def get_seed_data(self): 
        '''
        DESCRIPTION
        -----------
        Returns the seedData as a list of (x, y) float pairs, 
        handling both np.float64() and plain (x, y) pairs, including scientific notation.

        RETURNS
        -------
        list[tuple[float, float]]
            List of seed coordinates as float pairs.
        '''
        seedData = []
        
        # Pattern to match np.float64(x) and np.float64(y) with support for scientific notation
        np_float64_pattern = re.compile(r"np\.float64\((-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)\)")
        
        # Pattern to match plain (x, y) pairs with support for scientific notation
        plain_tuple_pattern = re.compile(r"\((-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?),\s*(-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)\)")
        
        for seed in self.seedData:
            # First try to match the np.float64() pattern
            np_float_matches = np_float64_pattern.findall(seed)
            
            if len(np_float_matches) == 2:
                # np.float64(x), np.float64(y) case
                x, y = np.float64(np_float_matches[0]), np.float64(np_float_matches[1])
                seedData.append((x, y))
            
            else:
                # Try to match the plain (x, y) tuple pattern
                plain_match = plain_tuple_pattern.match(seed)
                if plain_match:
                    x, y = np.float64(plain_match.group(1)), np.float64(plain_match.group(2))
                    seedData.append((x, y))
                else:
                    print(f"...Warning: Seed data '{seed}' is malformed and was skipped....")
        
        return seedData

    def get_radii(self): 
        return self.density_data["radius"]
    
    def get_efficacies(self): 
        return self.density_data["efficacy"]
    
    @staticmethod
    def read_from_file(alias, a, b, step_size, experiment_type):
        '''
        Description
        -----------
        reads specified experiment from file 

        Parameters
        ----------
        alias: str
            name of experiment group
        a: int
            numerator of experiment
        b: int
            denominator of experiment
        step_size: int
            resolution of data
        experiment_type: str
            type of experiment
        '''

        name = f'{alias}-{a},{b}.0-{step_size}-{experiment_type}.txt'
        path = os.path.join('dataFiles', experiment_type, alias, name)

        seedData = []
        densityData = {'efficacy': [], 'radius': []}
        section = None

        with open(path, 'r') as file:
            for line in file:
                line = line.strip()
                if line == '--- Seed Data ---':
                    section = 'seedData'
                elif line == '--- Density Data ---':
                    section = 'densityData'
                elif section == 'seedData':
                    seedData.append(line)
                elif section == 'densityData':
                    if line:  # Avoid empty lines
                        efficacy, radius = map(float, line.split(','))
                        densityData['efficacy'].append(efficacy)
                        densityData['radius'].append(radius)

        # Create and return an Experiment instance
        experiment = Experiment(alias, a, b, step_size, experiment_type)
        experiment.seedData = seedData
        experiment.densityData = densityData
        return experiment