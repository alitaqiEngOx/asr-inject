""" Licensed under the same terms as described in the main 
licensing script of this repository. """

from pathlib import Path
from typing import Optional

import numpy as np
from numpy.polynomial.polynomial import polyfit
from numpy.typing import NDArray


def fit_density(
        data: NDArray, degree: int, *,
        outdir: Optional[Path]=None
) -> NDArray:
    """
    """
    coefficients, stats = polyfit(
        data[:, 0] + 273.15, data[:, 1],
        degree, full=True
    )

    return np.asarray(coefficients)