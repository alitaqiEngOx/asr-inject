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

    # water moles
    water_mass = results["moles"][:, :3] * (
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

    plt.plot(
        (
            np.arange(config["n_steps"]) *
            config["step_size"] / DAY_TO_SEC
        ),
        water_mass[:, 2],
        label="recovered"
    )

    if results["time_to_recovery_limit"]:
        plt.plot(
            np.asarray([
                (
                    results["time_to_recovery_limit"] /
                    DAY_TO_SEC
                ),
                (
                    results["time_to_recovery_limit"] /
                    DAY_TO_SEC
                )
            ]),
            np.asarray([
                np.min(water_mass), np.max(water_mass)
            ]),
            "k--",
            label="recovery limit"
        )

    filename = "water_mass"
    plt.legend(loc="best")
    plt.title(filename)
    plt.xlabel("time (days)")
    plt.ylabel("mass (kg)")
    plt.savefig(f"{outdir / f"{filename}.png"}")
    plt.close()

    # solute moles
    solute_mass = results["moles"][:, 3:] * (
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

    plt.plot(
        (
            np.arange(config["n_steps"]) *
            config["step_size"] / DAY_TO_SEC
        ),
        solute_mass[:, 2],
        label="recovered"
    )

    if results["time_to_recovery_limit"]:
        plt.plot(
            np.asarray([
                (
                    results["time_to_recovery_limit"] /
                    DAY_TO_SEC
                ),
                (
                    results["time_to_recovery_limit"] /
                    DAY_TO_SEC
                )
            ]),
            np.asarray([
                np.min(solute_mass), np.max(solute_mass)
            ]),
            "k--",
            label="recovery limit"
        )

    filename = "solute_mass"
    plt.legend(loc="best")
    plt.title(filename)
    plt.xlabel("time (days)")
    plt.ylabel("mass (kg)")
    plt.savefig(f"{outdir / f"{filename}.png"}")
    plt.close()

    # mass fraction of fresh segment
    mass_fraction = results["mass_fraction_solute_fresh"]
    plt.plot(
        (
            np.arange(config["n_steps"]) *
            config["step_size"] / DAY_TO_SEC
        ),
        mass_fraction
    )

    if results["time_to_recovery_limit"]:
        plt.plot(
            (
                np.arange(config["n_steps"]) *
                config["step_size"] / DAY_TO_SEC
            ),
            (
                np.zeros(config["n_steps"]) +
                config["recovery"][
                    "threshold_solute_mass_fraction"
                ]
            ),
            "k--"
        )

        plt.plot(
            np.asarray([
                (
                    results["time_to_recovery_limit"] /
                    DAY_TO_SEC
                ),
                (
                    results["time_to_recovery_limit"] /
                    DAY_TO_SEC
                )
            ]),
            np.asarray([
                mass_fraction[0], mass_fraction[-1]
            ]),
            "k--",
            label="recovery limit"
        )

    filename = "recovery_purity"
    plt.legend(loc="best")
    plt.title(filename)
    plt.xlabel("time (days)")
    plt.ylabel("solute mass fraction in fresh segment")
    plt.savefig(f"{outdir / f"{filename}.png"}")
    plt.close()
    
    
    
    
    
    
    # asr efficiency
    #efficiency = results["asr-efficiency"] * 100.

    #plt.plot(
    #    (
    #        np.arange(config["n_steps"]) *
    #        config["step_size"] / DAY_TO_SEC
    #    ),
    #    efficiency
    #)

    #filename = "asr_efficiency"
    #plt.title(filename)
    #plt.xlabel("time (days)")
    #plt.ylabel("efficiency (%)")
    #plt.savefig(f"{outdir / f"{filename}.png"}")
    #plt.close()
