""" Licensed under the same terms as described in the main 
licensing script of this repository. """

import yaml
from pathlib import Path
from typing import Any

import numpy as np

from asr_inject.operations.reservoir import Reservoir
from asr_inject.operations.visualise import plot_2d
from asr_inject.utils.fitting import (
    arrhenius_fit, density_fit
)


def read_yaml(dir: Path) -> dict[str, Any]:
    """
    """
    with open(f"{dir}", 'r') as file:
        return yaml.safe_load(file)

def run(config: Path, *, outdir: Path) -> None:
    """
    """
    # read `.yml`
    config_dict = read_yaml(config)

    # fit density
    density_data = config_dict.pop("density")

    density_coefficients = density_fit(
        density_data,
        outfile=(
            outdir / "fitting" / "density.png"
        )
    )

    # fit water diffusivity
    water_diffusivity_data = config_dict.pop(
        "water_diffusivity"
    )

    water_diffusivity_coefficients = arrhenius_fit(
        np.asarray(water_diffusivity_data),
        outfile=(
            outdir / "fitting" / "water_diffusivity.png"
        )
    )

    # fit solute diffusivity
    solute_diffusivity_data = config_dict.pop(
        "solute_diffusivity"
    )

    solute_diffusivity_coefficients = arrhenius_fit(
        np.asarray(solute_diffusivity_data),
        outfile=(
            outdir / "fitting" / "solute_diffusivity.png"
        )
    )

    # run simulation
    fitting = {
        "density": {
            "temperature": density_coefficients,
            "salinity": density_data["salinity_fitting"]
        },
        "water_diffusivity": water_diffusivity_coefficients,
        "solute_diffusivity": solute_diffusivity_coefficients
    }

    res = Reservoir(
        config=config_dict, fitting=fitting
    )

    output = res.predict(
        n_steps=config_dict["n_steps"],
        step_size=config_dict["step_size"]
    )

    plot_2d(
        output, config=config_dict,
        outdir=(outdir / "results")
    )
