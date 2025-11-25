""" Licensed under the same terms as described in the main 
licensing script of this repository. """

import yaml
from pathlib import Path
from typing import Any

import numpy as np

from asr_inject.utils.fitting import fit_density


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

    # fit water density
    density_input = config_dict.pop("water_density")

    solution_characteristics = config_dict.pop(
        "solution_characteristics"
    )

    density_coefficients = fit_density(
        np.asarray(density_input["data"]),
        density_input["fitting_degree"],
        solution_characteristics=solution_characteristics,
        outdir=outdir
    )
