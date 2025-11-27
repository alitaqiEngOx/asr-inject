""" Licensed under the same terms as described in the main 
licensing script of this repository. """

from pathlib import Path
from typing import Any, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial.polynomial import polyfit
from numpy.typing import NDArray


R = 8.314462618  # J/(molK)
CELSIUS_TO_KELVIN = 273.15

def density_fit(
        *, density_data: dict[str, Any],
        solution_characteristics: dict[str, Any],
        outdir: Optional[Path]=None,
        filename: Optional[str]=None
) -> NDArray:
    """
    """
    data = np.asarray(density_data["data"])
    degree = density_data["temperature_fitting_degree"]
    A0 = density_data["salinity_fitting"]["A0"]
    A1 = density_data["salinity_fitting"]["A1"]

    Mr_water = solution_characteristics["Mr_water"]
    Mr_solute = solution_characteristics["Mr_solute"]

    # temperature fitting
    coefficients, stats = polyfit(
        data[:, 0] + CELSIUS_TO_KELVIN, data[:, 1],
        degree, full=True
    )

    # plots
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

        if not filename:
            filename = f"density_fit"

        plt.legend(loc="best")
        plt.title("density-temperature data fit")
        plt.xlabel("T (degC)")
        plt.ylabel("dens (kg/m^3)")
        plt.savefig(str(saving_dir / f"{filename}.png"))
        plt.close()

    return np.asarray(coefficients)

def arrhenius_fit(
        data: NDArray, *, outdir: Optional[Path]=None,
        filename: Optional[str]=None
) -> Tuple[float, float]:
    """
    """
    x_axis = 1. / (data[:, 0] + CELSIUS_TO_KELVIN)
    y_axis = np.log(data[:, 1])

    # least-squares' fitting
    slope, intercept = np.polyfit(x_axis, y_axis, 1)

    # plots
    if outdir:
        saving_dir = outdir / "fitting"
        saving_dir.mkdir(parents=True, exist_ok=True)

        plt.scatter(
            x_axis, y_axis,
            marker='x', c="red", label="real data"
        )

        plt.plot(
            np.asarray([x_axis[0], x_axis[-1]]),
            np.asarray([
                intercept + slope * x_axis[0],
                intercept + slope * x_axis[-1]
            ]),
            label="linear fit"
        )

        if not filename:
            filename="arrhenius_fit"

        plt.legend(loc="best")
        plt.title("permeability-temperature data fit")
        plt.xlabel("1/T (K^-1)")
        plt.ylabel("ln(diff)")
        plt.savefig(str(saving_dir / f"{filename}.png"))
        plt.close()

    return np.exp(intercept), -R * slope
