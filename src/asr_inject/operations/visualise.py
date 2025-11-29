""" Licensed under the same terms as described in the main 
licensing script of this repository. """

from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray


DAY_TO_SEC = 86400.
k_TO_SI = 1000.

def plot_2d(
        results: dict[str, NDArray], *,
        config: dict[str, Any], outdir: Path
) -> None:
    """
    """
    # make outdir
    outdir.mkdir(parents=True, exist_ok=True)

    # water
    water_mass = results["moles"][:, :2] * (
        config["solution_characteristics"]["Mr_water"] /
        k_TO_SI
    )

    plt.plot(
        (
            np.arange(config["n_steps"]) *
            config["step_size"] / DAY_TO_SEC
        ),
        water_mass[:, 0],
        label="fresh segment"
    )

    plt.plot(
        (
            np.arange(config["n_steps"]) *
            config["step_size"] / DAY_TO_SEC
        ),
        water_mass[:, 1],
        label="saline segment"
    )

    filename = "water_moles"
    plt.legend(loc="best")
    plt.title(filename)
    plt.xlabel("time (days)")
    plt.ylabel("mass (kg)")
    plt.savefig(f"{outdir / f"{filename}.png"}")
    plt.close()

    # solute
    solute_mass = results["moles"][:, 2:] * (
        config["solution_characteristics"]["Mr_solute"] /
        k_TO_SI
    )

    plt.plot(
        (
            np.arange(config["n_steps"]) *
            config["step_size"] / DAY_TO_SEC
        ),
        solute_mass[:, 0],
        label="fresh segment"
    )

    plt.plot(
        (
            np.arange(config["n_steps"]) *
            config["step_size"] / DAY_TO_SEC
        ),
        solute_mass[:, 1],
        label="saline segment"
    )

    filename = "solute_moles"
    plt.legend(loc="best")
    plt.title(filename)
    plt.xlabel("time (days)")
    plt.ylabel("mass (kg)")
    plt.savefig(f"{outdir / f"{filename}.png"}")
    plt.close()
