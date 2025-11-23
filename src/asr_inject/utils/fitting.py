""" Licensed under the same terms as described in the main 
licensing script of this repository. """

from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
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

    if outdir:
        saving_dir = outdir / "fitting"
        saving_dir.mkdir(parents=True, exist_ok=True)

        temp = np.arange(data[0, 0], data[-1, 0], 0.01)
        dens = np.zeros(len(temp))
        for idx in range(degree + 1):
            dens += coefficients[idx] * (temp + 273.15)**idx

        plt.scatter(
            data[:, 0], data[:, 1],
            marker='x', c="red", label="real data"
        )

        plt.plot(temp, dens, label="polynomial fit")

        filename = f"water_density_fitting.png"
        plt.legend(loc="best")
        plt.title("density-temperature data fit")
        plt.xlabel("T (degC)")
        plt.ylabel("dens (kg/m^3)")
        plt.savefig(str(saving_dir / filename))
        plt.close()

    return np.asarray(coefficients)