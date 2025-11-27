""" Licensed under the same terms as described in the main 
licensing script of this repository. """

import numpy as np


mu_0 = 0. # J/mol; pure at operating T & p

def compute(
        *, activity: float, diffusivity: float,
        concentration: float
) -> float:
    """
    """
    return (
        diffusivity * concentration * np.log(activity) +
        mu_0
    )
