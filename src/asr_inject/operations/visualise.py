""" Licensed under the same terms as described in the main 
licensing script of this repository. """

from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray


DAY_TO_SEC = 86400.

def plot_2d(
        results: dict[str, NDArray], *,
        config: dict[str, Any], outfile: Path
) -> None:
    """
    """
    # make outdir
    outfile.parent.mkdir(parents=True, exist_ok=True)

    # water
    water_moles = results["moles"][:, :2]

    plt.plot(
        (
            np.arange(config["n_steps"]) *
            config["step_size"] / DAY_TO_SEC
        ),
        water_moles[:, 0],
        label="fresh segment"
    )

    plt.plot(
        (
            np.arange(config["n_steps"]) *
            config["step_size"] / DAY_TO_SEC
        ),
        water_moles[:, 1],
        label="saline segment"
    )

    plt.legend(loc="best")
    plt.title(str(outfile.stem))
    plt.xlabel("time (days)")
    plt.ylabel("moles (mol)")
    plt.savefig(str(outfile))
    plt.close()   
