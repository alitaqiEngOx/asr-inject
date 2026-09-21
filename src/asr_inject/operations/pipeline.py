""" Licensed under the same terms as described in the main 
licensing script of this repository. """

from pathlib import Path

from asr_inject.operations.reservoir import Reservoir
from asr_inject.operations.visualise import plot_2d
from asr_inject.utils.fitting import (
    arrhenius_fit, density_fit
)
from asr_inject.utils.log_handler import create
from asr_inject.utils.outtree import make_global_outdir
from asr_inject.utils._yaml import read


LOGGER = create("pipeline")


def run(config: Path) -> None:
    """
    """
    LOGGER.info("pipeline running")

    # ----------------------------------------
    # 1. GENERATE OUTPUTS' DIRECTORY
    # ----------------------------------------
    outdir = make_global_outdir(
        config.parent, return_name=True
    )

    # ----------------------------------------
    # 2. READ `.yml` AND LOOP THROUGH ENTRIES
    # ----------------------------------------
    config_dict = read(
        config, global_outdir_name=outdir
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
    density_coefficients = density_fit(density_data)

    # fit water diffusivity
    water_diffusivity_data = config_dict.pop(
        "water_diffusivity"
    )

    water_diff_coeff_fresh_segment = arrhenius_fit(
        water_diffusivity_data["fresh_segment"]
    )

    water_diff_coeff_saline_segment = arrhenius_fit(
        water_diffusivity_data["saline_segment"]
    )

    # fit solute diffusivity
    solute_diffusivity_data = config_dict.pop(
        "solute_diffusivity"
    )

    solute_diff_coeff_fresh_segment = arrhenius_fit(
        solute_diffusivity_data["fresh_segment"]
    )

    solute_diff_coeff_saline_segment = arrhenius_fit(
        solute_diffusivity_data["saline_segment"]
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
        "diffusion_coefficients": {
            "water_fresh_segment": (
                water_diff_coeff_fresh_segment
            ),
            "water_saline_segment": (
                water_diff_coeff_saline_segment
            ),
            "solute_fresh_segment": (
                solute_diff_coeff_fresh_segment
            ),
            "solute_saline_segment": (
                solute_diff_coeff_saline_segment
            ),
        }
    }

    for key, value in config_dict.items():
        # ----------------------------------------
        # 3. LOOP THROUGH ENTRIES
        # ----------------------------------------
        LOGGER.info(f"working on `{key}`")

        res = Reservoir(
            config=value, fitting=fitting
        )



    
    
    
    
    
    
    
    
    
    
    
    
    

    #res = Reservoir(
    #    config=config_dict, fitting=fitting
    #)

    output = res.predict(
        n_steps=config_dict["n_steps"],
        step_size=config_dict["step_size"],
        hmax=(
            config_dict["hmax"]
            if "hmax" in config_dict.keys()
            else None
        )
    )

    plot_2d(
        output, config=config_dict,
        outdir=(outdir / "results")
    )

    # temporary prints
    print(
        "final efficiency: "
        f"{output['asr_efficiency'][-1]}"
    )

    if output['time_to_recovery_limit']:
        print(
            "time to recovery limit: "
            f"{output['time_to_recovery_limit'] / 86400.} "
            "days"
        )

    else:
        print(
            "time to full recovery: "
            f"{output['time_to_full_recovery'] / 86400.} "
            "days"
        )
