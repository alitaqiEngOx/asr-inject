""" Licensed under the same terms as described in the main 
licensing script of this repository. """

from pathlib import Path
from typing import Any, Optional

import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial.polynomial import polyfit
from numpy.typing import NDArray


CELSIUS_TO_KELVIN = 273.15

def fit_density(
        data: NDArray, degree: int, *,
        solution_characteristics:
        Optional[dict[str, Any]]=None,
        outdir: Optional[Path]=None
) -> NDArray:
    """
    """
    coefficients, stats = polyfit(
        data[:, 0] + CELSIUS_TO_KELVIN, data[:, 1],
        degree, full=True
    )

    if outdir:
        saving_dir = outdir / "fitting"
        saving_dir.mkdir(parents=True, exist_ok=True)

        temp = np.arange(data[0, 0], data[-1, 0], 0.01)
        dens = np.zeros(len(temp))
        for idx in range(degree + 1):
            dens += (
                coefficients[idx] *
                (temp + CELSIUS_TO_KELVIN)**idx
            )

        # imported data
        plt.scatter(
            data[:, 0], data[:, 1],
            marker='x', c="red", label="real data"
        )

        # pure water fit
        plt.plot(temp, dens, label="polynomial fit")

        # impure water
        if solution_characteristics:
            Mr_water = solution_characteristics["Mr_water"]
            Mr_solute = solution_characteristics["Mr_solute"]

            A0 = solution_characteristics[
                "salinity_density_fitting"
            ]["A0"]
            A1 = solution_characteristics[
                "salinity_density_fitting"
            ]["A1"]

            for mole_fraction in [0.0025, 0.005]:
                molar_solubility = (
                    mole_fraction / (1. - mole_fraction)
                )

                solubility = molar_solubility * (
                    Mr_solute / Mr_water
                )

                d_rho = solubility * (
                    A0 + 
                    (temp + CELSIUS_TO_KELVIN) * A1
                )

                dens_impure = dens + d_rho

                plt.plot(
                    temp, dens_impure,
                    label=f"mol%={mole_fraction*100.}"
                )

        filename = f"water_density_fitting.png"
        plt.legend(loc="best")
        plt.title("density-temperature data fit")
        plt.xlabel("T (degC)")
        plt.ylabel("dens (kg/m^3)")
        plt.savefig(str(saving_dir / filename))
        plt.close()

    return np.asarray(coefficients)
