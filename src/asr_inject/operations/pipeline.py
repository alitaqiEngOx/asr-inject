""" Licensed under the same terms as described in the main 
licensing script of this repository. """

from pathlib import Path

import numpy as np

from asr_inject.operations.reservoir import Reservoir
from asr_inject.operations.visualise import plot_2d
from asr_inject.utils.fitting import (
    arrhenius_fit, density_fit
)
from asr_inject.utils.log_handler import create
from asr_inject.utils.outtree import make_global_outdir
from asr_inject.utils.txt import dump
from asr_inject.utils._yaml import read


LOGGER = create("pipeline")

DAY_TO_SEC = 86400.
k_TO_SI = 1000.


def run(config: Path) -> None:
    """
    """
    LOGGER.info("pipeline running")

    # ----------------------------------------
    # 1. GENERATE OUTPUTS' DIRECTORY
    # ----------------------------------------
    outdir = make_global_outdir(
        config.parent, return_path=True
    )

    # ----------------------------------------
    # 2. READ `.yml` AND LOOP THROUGH ENTRIES
    # ----------------------------------------
    config_dict = read(
        config, global_outdir_name=outdir.name
    )

    # ----------------------------------------
    # 3. DEFINE/FIT PARAMETERS/COORDINATES
    # ----------------------------------------
    LOGGER.info("defining/fitting parameters")

    # solution characteristics
    solution_characteristics = config_dict.pop(
        "solution_characteristics"
    )

    # fit density
    density_data = config_dict.pop("density")
    density_coefficients = density_fit(
        density_data,
        outname=(outdir / "fitting" / "density.png")
    )

    # fit water diffusivity
    water_diffusivity_data = config_dict.pop(
        "water_diffusivity"
    )

    water_diff_params_fresh_segment = arrhenius_fit(
        water_diffusivity_data["fresh_segment"],
        outname=(
            outdir / "fitting" /
            "water_diffusivity_fresh.png"
        )
    )

    water_diff_params_saline_segment = arrhenius_fit(
        water_diffusivity_data["saline_segment"],
        outname=(
            outdir / "fitting" /
            "water_diffusivity_saline.png"
        )
    )

    # fit solute diffusivity
    solute_diffusivity_data = config_dict.pop(
        "solute_diffusivity"
    )

    solute_diff_params_fresh_segment = arrhenius_fit(
        solute_diffusivity_data["fresh_segment"],
        outname=(
            outdir / "fitting" /
            "solute_diffusivity_fresh.png"
        )
    )

    solute_diff_params_saline_segment = arrhenius_fit(
        solute_diffusivity_data["saline_segment"],
        outname=(
            outdir / "fitting" /
            "solute_diffusivity_saline.png"
        )
    )

    # fitting dictionary
    fitting = {
        "solution_characteristics": (
            solution_characteristics
        ),
        "density": {
            "temperature": density_coefficients,
            "salinity": density_data["salinity_fitting"]
        },
        "diffusivity_parameters": {
            "water_fresh_segment": (
                water_diff_params_fresh_segment
            ),
            "water_saline_segment": (
                water_diff_params_saline_segment
            ),
            "solute_fresh_segment": (
                solute_diff_params_fresh_segment
            ),
            "solute_saline_segment": (
                solute_diff_params_saline_segment
            ),
        }
    }

    for key, value in config_dict.items():
        # ----------------------------------------
        # 3. LOOP THROUGH ENTRIES
        # ----------------------------------------
        LOGGER.info(f"working on `{key}`")

        # define/load reservoir data in memory
        res = Reservoir(
            config=value, fitting=fitting
        )

        # compute outputs
        output = res.predict(
            n_steps=value["n_steps"],
            step_size=value["step_size"],
            hmax=(
                value["hmax"] if "hmax" in value.keys()
                else None
            )
        )

        # show outputs in 2D plots
        LOGGER.info(
            "preparing results for visualisation"
        )

        x_domain = (
            np.arange(value["n_steps"]) *
            value["step_size"] / DAY_TO_SEC
        )

        y_domain_labels = [
            "fresh_segment", "transition_layer",
            "saline_segment"
        ]

        axis_labels = [
            "time (days)", "mass (kg)"
        ]

        for species in ["water", "solute"]:
            if species == "water":
                moles = output["moles"][:, :3]

            else:
                moles = output["moles"][:, 3:]

            y_domains = (
                moles *
                fitting[
                    "solution_characteristics"
                ][f"Mr_{species}"] / k_TO_SI
            )

            plot_2d(
                x_domain, y_domains,
                outname=(
                    outdir / f"{key}" /
                    f"{species}_mass.png"
                ),
                y_domain_labels=y_domain_labels,
                axis_labels=axis_labels,
                times_to_steady_state=(
                    output[
                        "times_to_steady_state"
                    ][f"{species}"] / DAY_TO_SEC
                )
            )

        # generate written outcomes
        LOGGER.info(
            "preparing written results for exportation"
        )

        txt_data = {
            "final water moles fresh segment" : str(
                output["moles"][-1, 0] * fitting[
                    "solution_characteristics"
                ]["Mr_water"] / k_TO_SI
            ) + " kg",

            "time to steady state - water fresh segment" : str(
                output[
                    "times_to_steady_state"
                ]["water"][0] / DAY_TO_SEC
            ) + " days",

            "final water moles transition zone" : str(
                output["moles"][-1, 1] * fitting[
                    "solution_characteristics"
                ]["Mr_water"] / k_TO_SI
            ) + " kg",

            "time to steady state - water transition zone" : str(
                output[
                    "times_to_steady_state"
                ]["water"][1] / DAY_TO_SEC
            ) + " days",

            "final water moles saline segment" : str(
                output["moles"][-1, 2] * fitting[
                    "solution_characteristics"
                ]["Mr_water"] / k_TO_SI
            ) + " kg",

            "time to steady state - water saline segment" : str(
                output[
                    "times_to_steady_state"
                ]["water"][2] / DAY_TO_SEC
            ) + " days",

            "final solute moles fresh segment" : str(
                output["moles"][-1, 3] * fitting[
                    "solution_characteristics"
                ]["Mr_solute"] / k_TO_SI
            ) + " kg",

            "time to steady state - solute fresh segment" : str(
                output[
                    "times_to_steady_state"
                ]["solute"][0] / DAY_TO_SEC
            ) + " days",

            "final solute moles transition zone" : str(
                output["moles"][-1, 4] * fitting[
                    "solution_characteristics"
                ]["Mr_solute"] / k_TO_SI
            ) + " kg",

            "time to steady state - solute transition zone" : str(
                output[
                    "times_to_steady_state"
                ]["solute"][1] / DAY_TO_SEC
            ) + " days",

            "final solute moles saline segment" : str(
                output["moles"][-1, 5] * fitting[
                    "solution_characteristics"
                ]["Mr_solute"] / k_TO_SI
            ) + " kg",

            "time to steady state - solute saline segment" : str(
                output[
                    "times_to_steady_state"
                ]["solute"][2] / DAY_TO_SEC
            ) + " days",
        }

        dump(
            txt_data, outname=(
                outdir / f"{key}" / "outputs.txt"
            )
        )

        LOGGER.info(f"completed tasks for `{key}`")

    LOGGER.info("completed all tasks\n")

    # temporary prints
    #print(
    #    "final efficiency: "
    #    f"{output['asr_efficiency'][-1]}"
    #)

    #if output['time_to_recovery_limit']:
    #    print(
    #        "time to recovery limit: "
    #        f"{output['time_to_recovery_limit'] / 86400.} "
    #        "days"
    #    )

    #else:
    #    print(
    #        "time to full recovery: "
    #        f"{output['time_to_full_recovery'] / 86400.} "
    #        "days"
    #    )
