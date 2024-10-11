from typing import TYPE_CHECKING

if TYPE_CHECKING: 
    from .experiment_class import Experiment

def __rp_ff__(a: int, b: int, step_size: int, max_radius: int, experiment: Experiment):
    import numpy as np

    