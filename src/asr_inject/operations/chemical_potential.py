""" Licensed under the same terms as described in the main 
licensing script of this repository. """

import numpy as np


R = 8.314 # J/(mol.K)
a_0 = 1. # i.e., pure component
mu_0 = 0. # J/mol; pure at operating T & p

def compute(
        *, activity: float, temperature: float
) -> float:
    """
    """
    return (
        mu_0 +
        R * temperature * np.log(activity / a_0)
    )
