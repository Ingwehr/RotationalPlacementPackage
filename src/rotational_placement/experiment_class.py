import os

class Experiment: 
    def __init__(self, alias: str, a: int, b: int, step_size: int, experiment_type: str): 
        import rotational_placement.load_config as load_config
        
        self.alias = str(alias)
        self.a = int(a)
        self.b = int(b)
        self.step_size = step_size
        self.experiment_type = experiment_type

        # Load configuration
        config = load_config()
        root_path = config.get("data_files_path", "data_files")  # Default to "data_files" if not set in config

        # Define name and path for saving results
        self.name = f"{self.alias}-{self.a},{self.b}-{self.step_size}-{self.experiment_type}.txt"
        self.path = os.path.join(root_path, self.experiment_type, self.alias, self.name)

        # Initialize seed_data and density_data based on experiment type
        if experiment_type in ["num", "sym"]:
            self.seed_data = []
        self.density_data = {"efficacy": [], "radius": []}

        # Ensure directories exist
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

    def run_experiment(self, max_radius: int) -> None:
        from .__rp_num__ import __rp_num__
        from .__rp_ff__ import __rp_ff__

        match self.experiment_type: 
            case "num":
                self.density_data, self.seed_data = __rp_num__(self.a, self.b, self.step_size, max_radius, self)
            case "ff":
                self.density_data = __rp_ff__(self.a, self.b, self.step_size, max_radius, self)
            case "sym": 
                pass
            case _:
                raise ValueError("invalid experiment type")
        print("Experiment done and added to instance")

    def write_to_self(self) -> None:
        with open(self.path, "w") as file:
            file.write(f"alias:{self.alias}\n")
            file.write(f"a:{self.a}\n")
            file.write(f"b:{self.b}\n")
            file.write(f"step_size:{self.step_size}\n")
            file.write(f"experiment_type:{self.experiment_type}\n")
            
            file.write("--- Seed Data ---\n")
            for seed in self.seed_data:
                file.write(f"{seed}\n")
            
            file.write("--- Density Data ---\n")
            for efficacy, radius in zip(self.density_data["efficacy"], self.density_data["radius"]):
                file.write(f"{efficacy},{radius}\n")
        
        print("Data written to file")

    def get_meta_data(self):
        return {'alias': self.alias,
                'a': self.a,
                'b': self.b,
                'experimentType': self.experiment_type,
                'stepSize': self.step_size,
                'max_radius': self.get_max_radius()}

    def get_max_radius(self): 
        try: 
            return int(self.density_data["radius"][-1])
        except IndexError:
            return None
    
    def get_density(self): 
        return [float(e) / (float(r) ** 2) for e, r in zip(self.density_data['efficacy'], self.density_data['radius'])]

    def get_seed_data(self): 
        import numpy as np
        import re
        seed_data = []
        
        # Pattern to match np.float64(x) and np.float64(y) with support for scientific notation
        np_float64_pattern = re.compile(r"np\.float64\((-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)\)")
        
        # Pattern to match plain (x, y) pairs with support for scientific notation
        plain_tuple_pattern = re.compile(r"\((-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?),\s*(-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)\)")
        
        for seed in self.seed_data:
            # First try to match the np.float64() pattern
            np_float_matches = np_float64_pattern.findall(seed)
            
            if len(np_float_matches) == 2:
                # np.float64(x), np.float64(y) case
                x, y = np.float64(np_float_matches[0]), np.float64(np_float_matches[1])
                seed_data.append((x, y))
            
            else:
                # Try to match the plain (x, y) tuple pattern
                plain_match = plain_tuple_pattern.match(seed)
                if plain_match:
                    x, y = np.float64(plain_match.group(1)), np.float64(plain_match.group(2))
                    seed_data.append((x, y))
                else:
                    print(f"...Warning: Seed data '{seed}' is malformed and was skipped....")
        
        return seed_data
        
    def get_radius(self):
        return self.density_data["radius"]

    def get_efficacy(self):
        return self.density_data["efficacy"]
        
    @staticmethod
    def read_from_file(alias: str, a: int, b: int, step_size: int, experiment_type: str):
        '''
        Reads the specified experiment from a file and returns an Experiment instance.
        '''
        import rotational_placement.load_config as load_config
        
        # Load configuration for the path
        config = load_config()
        root_path = config.get("data_files_path", "data_files")  # Default to "data_files" if not set in config

        # Create the file name and path
        name = f'{alias}-{a},{b}-{step_size}-{experiment_type}.txt'
        path = os.path.join(root_path, experiment_type, alias, name)

        seed_data = []
        density_data = {'efficacy': [], 'radius': []}
        section = None

        # Read the data from the file
        with open(path, 'r') as file:
            for line in file:
                line = line.strip()
                if line == '--- Seed Data ---':
                    section = 'seed_data'
                elif line == '--- Density Data ---':
                    section = 'density_data'
                elif section == 'seed_data':
                    seed_data.append(line)
                elif section == 'density_data':
                    if line:  # Avoid empty lines
                        efficacy, radius = map(float, line.split(','))
                        density_data['efficacy'].append(efficacy)
                        density_data['radius'].append(radius)

        # Create and return an Experiment instance
        experiment = Experiment(alias, a, b, step_size, experiment_type)
        experiment.seed_data = seed_data
        experiment.density_data = density_data
        return experiment
