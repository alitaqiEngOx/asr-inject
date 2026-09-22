""" Licensed under the same terms as described in the main 
licensing script of this repository. """

from typing import Any

import numpy as np
from numpy.typing import NDArray
from scipy.integrate import odeint

from asr_inject.operations import chemical_potential
from asr_inject.utils.log_handler import create


LOGGER = create("reservoir")

R = 8.314 # J/(mol.K)
CELSIUS_TO_KELVIN = 273.15
BAR_TO_PA = 10.**5.


class Reservoir:
    """"""

    def __init__(
            self, *, config: dict[str, Any],
            fitting: dict[str, Any]
    ) -> None:
        """
        """
        self.fitting = fitting

        self.Mr_water = fitting[
            "solution_characteristics"
        ]["Mr_water"]

        self.Mr_solute = fitting[
            "solution_characteristics"
        ]["Mr_solute"]

        self.length = config[
            "reservoir_dimensions"
        ]["length"]

        self.width = config[
            "reservoir_dimensions"
        ]["length"]

        self.height_fresh_segment = config[
            "reservoir_dimensions"
        ]["height"]["fresh_segment"]

        self.height_intermediate_segment = config[
            "reservoir_dimensions"
        ]["height"]["intermediate_segment"]

        self.height_saline_segment = config[
            "reservoir_dimensions"
        ]["height"]["saline_segment"]

        self.fresh_segment_void_fraction = config[
            "reservoir_porosity"
        ]["fresh_segment_void_fraction"]

        self.intermediate_segment_void_fraction = config[
            "reservoir_porosity"
        ]["intermediate_segment_void_fraction"]

        self.saline_segment_void_fraction = config[
            "reservoir_porosity"
        ]["saline_segment_void_fraction"]

        self.temperature = config[
            "reservoir_conditions"
        ]["temperature"] + CELSIUS_TO_KELVIN

        self.pressure = config[
            "reservoir_conditions"
        ]["pressure"] * BAR_TO_PA

        self.mass_fraction_solute_fresh_initial = config[
            "initial_solute_mass_fractions"
        ]["fresh_segment"]

        self.mass_fraction_solute_intermediate_initial = (
            config[
                "initial_solute_mass_fractions"
            ]["intermediate_segment"]
        )

        self.mass_fraction_solute_saline_initial = config[
            "initial_solute_mass_fractions"
        ]["saline_segment"]


    @property
    def mass_fraction_water_fresh_initial(self) -> float:
        """
        """
        return (
            1. - self.mass_fraction_solute_fresh_initial
        )


    @property
    def mass_fraction_water_intermediate_initial(
        self
    ) -> float:
        """
        """
        return (
            1. -
            self.mass_fraction_solute_intermediate_initial
        )


    @property
    def mass_fraction_water_saline_initial(self) -> float:
        """
        """
        return (
            1. - self.mass_fraction_solute_saline_initial
        )


    @property
    def cs_area(self) -> float:
        """
        """
        return self.length * self.width


    @property
    def numerical_separation(self) -> list[float]:
        """
        """
        return [
            (
                0.5 * self.height_fresh_segment +
                0.5 * self.height_intermediate_segment
            ),
            (
                0.5 * self.height_intermediate_segment +
                0.5 * self.height_saline_segment
            )
        ]


    @property
    def volume_fresh_segment(self) -> float:
        """
        """
        return (
            self.length * self.width *
            self.height_fresh_segment
        )


    @property
    def volume_intermediate_segment(self) -> float:
        """
        """
        return (
            self.length * self.width *
            self.height_intermediate_segment
        )


    @property
    def volume_saline_segment(self) -> float:
        """
        """
        return (
            self.length * self.width *
            self.height_saline_segment
        )


    @property
    def volume(self) -> float:
        """
        """
        return (
            self.volume_fresh_segment +
            self.volume_intermediate_segment +
            self.volume_saline_segment
        )


    @property
    def mass_water_fresh_initial(self) -> float:
        """
        """
        return (
            self.density_pure *
            self.volume_fresh_segment *
            self.fresh_segment_void_fraction *
            self.mass_fraction_water_fresh_initial
        )


    @property
    def mass_water_intermediate_initial(self) -> float:
        """
        """
        return (
            self.density_pure *
            self.volume_intermediate_segment *
            self.intermediate_segment_void_fraction *
            self.mass_fraction_water_intermediate_initial
        )


    @property
    def mass_water_saline_initial(self) -> float:
        """
        """
        return (
            self.density_pure *
            self.volume_saline_segment *
            self.saline_segment_void_fraction *
            self.mass_fraction_water_saline_initial
        )


    @property
    def mass_solute_fresh_initial(self) -> float:
        """
        """
        return (
            self.density_pure *
            self.volume_fresh_segment *
            self.fresh_segment_void_fraction *
            self.mass_fraction_solute_fresh_initial
        )


    @property
    def mass_solute_intermediate_initial(self) -> float:
        """
        """
        return (
            self.density_pure *
            self.volume_intermediate_segment *
            self.intermediate_segment_void_fraction *
            self.mass_fraction_solute_intermediate_initial
        )


    @property
    def mass_solute_saline_initial(self) -> float:
        """
        """
        return (
            self.density_pure *
            self.volume_saline_segment *
            self.saline_segment_void_fraction *
            self.mass_fraction_solute_saline_initial
        )


    @property
    def moles_water_fresh_initial(self) -> float:
        """
        """
        return (
            self.mass_water_fresh_initial /
            self.Mr_water
        )


    @property
    def moles_water_intermediate_initial(self) -> float:
        """
        """
        return (
            self.mass_water_intermediate_initial /
            self.Mr_water
        )


    @property
    def moles_water_saline_initial(self) -> float:
        """
        """
        return (
            self.mass_water_saline_initial /
            self.Mr_water
        )


    @property
    def moles_solute_fresh_initial(self) -> float:
        """
        """
        return (
            self.mass_solute_fresh_initial /
            self.Mr_solute
        )


    @property
    def moles_solute_intermediate_initial(self) -> float:
        """
        """
        return (
            self.mass_solute_intermediate_initial /
            self.Mr_solute
        )


    @property
    def moles_solute_saline_initial(self) -> float:
        """
        """
        return (
            self.mass_solute_saline_initial /
            self.Mr_solute
        )


    @property
    def diffusivity_water_fresh_segment(self) -> float:
        """
        """
        base = self.fitting[
            "diffusivity_parameters"
        ]["water_fresh_segment"][0]

        energy = self.fitting[
            "diffusivity_parameters"
        ]["water_fresh_segment"][1]

        exp_term = -energy / (R * self.temperature)

        return base * np.exp(exp_term)


    @property
    def diffusivity_water_saline_segment(self) -> float:
        """
        """
        base = self.fitting[
            "diffusivity_parameters"
        ]["water_saline_segment"][0]

        energy = self.fitting[
            "diffusivity_parameters"
        ]["water_saline_segment"][1]

        exp_term = -energy / (R * self.temperature)

        return base * np.exp(exp_term)


    @property
    def diffusivity_solute_fresh_segment(self) -> float:
        """
        """
        base = self.fitting[
            "diffusivity_parameters"
        ]["solute_fresh_segment"][0]

        energy = self.fitting[
            "diffusivity_parameters"
        ]["solute_fresh_segment"][1]

        exp_term = -energy / (R * self.temperature)

        return base * np.exp(exp_term)


    @property
    def diffusivity_solute_saline_segment(self) -> float:
        """
        """
        base = self.fitting[
            "diffusivity_parameters"
        ]["solute_saline_segment"][0]

        energy = self.fitting[
            "diffusivity_parameters"
        ]["solute_saline_segment"][1]

        exp_term = -energy / (R * self.temperature)

        return base * np.exp(exp_term)


    @property
    def density_pure(self) -> float:
        """
        """
        coefficients = self.fitting["density"][
            "temperature"
        ]

        output = 0.
        for idx, coeff in enumerate(coefficients):
            output += coeff * self.temperature**idx

        return output


    def compute_density_solution(
            self,
            mass_fraction_solute: float | NDArray
    ) -> float | NDArray:
        """
        """
        solubility = mass_fraction_solute / (
            1. - mass_fraction_solute
        )

        A0 = self.fitting["density"]["salinity"]["A0"]
        A1 = self.fitting["density"]["salinity"]["A1"]

        d_rho = solubility * (
            A0 + (self.temperature * A1)
        )

        return self.density_pure + d_rho


    def predict(
            self, *, n_steps: int, step_size: float,
            hmax: float | None=None
    ) -> dict[str, NDArray]:
        """
        """
        def differential(
                moles: NDArray, t: float
        ) -> NDArray:
            """
            """
            water_moles = moles[:3]
            solute_moles = moles[3:]

            # ----------------------------------------
            # 1. FRESH SEGMENT
            # ----------------------------------------
            water_fraction_fresh = (
                water_moles[0] / (
                    water_moles[0] + solute_moles[0]
                )
            )

            solute_fraction_fresh = (
                1. - water_fraction_fresh
            )

            water_mass_fraction_fresh = (
                (water_fraction_fresh * self.Mr_water) /
                (
                    water_fraction_fresh * self.Mr_water +
                    solute_fraction_fresh * self.Mr_solute
                )
            )

            solute_mass_fraction_fresh = (
                1. - water_mass_fraction_fresh
            )

            density_solution_fresh = (
                self.compute_density_solution(
                    solute_mass_fraction_fresh
                )
            )

            water_concentration_fresh = (
                density_solution_fresh *
                water_mass_fraction_fresh *
                (1000. / self.Mr_water)
            )

            solute_concentration_fresh = (
                density_solution_fresh *
                solute_mass_fraction_fresh *
                (1000. / self.Mr_solute)
            )

            # ----------------------------------------
            # 2. INTERMEDIATE LAYER
            # ----------------------------------------
            water_fraction_intermediate = (
                water_moles[1] / (
                    water_moles[1] + solute_moles[1]
                )
            )

            solute_fraction_intermediate = (
                1. - water_fraction_intermediate
            )

            water_mass_fraction_intermediate = (
                (
                    water_fraction_intermediate *
                    self.Mr_water
                ) /
                (
                    water_fraction_intermediate *
                    self.Mr_water +
                    solute_fraction_intermediate *
                    self.Mr_solute
                )
            )

            solute_mass_fraction_intermediate = (
                1. - water_mass_fraction_intermediate
            )

            density_solution_intermediate = (
                self.compute_density_solution(
                    solute_mass_fraction_intermediate
                )
            )

            water_concentration_intermediate = (
                density_solution_intermediate *
                water_mass_fraction_intermediate *
                (1000. / self.Mr_water)
            )

            solute_concentration_intermediate = (
                density_solution_intermediate *
                solute_mass_fraction_intermediate *
                (1000. / self.Mr_solute)
            )

            # ----------------------------------------
            # 3. SALINE SEGMENT
            # ----------------------------------------
            water_fraction_saline = (
                water_moles[2] / (
                    water_moles[2] + solute_moles[2]
                )
            )

            solute_fraction_saline = (
                1. - water_fraction_saline
            )

            water_mass_fraction_saline = (
                (water_fraction_saline * self.Mr_water) /
                (
                    water_fraction_saline * self.Mr_water +
                    solute_fraction_saline * self.Mr_solute
                )
            )

            solute_mass_fraction_saline = (
                1. - water_mass_fraction_saline
            )

            density_solution_saline = (
                self.compute_density_solution(
                    solute_mass_fraction_saline
                )
            )

            water_concentration_saline = (
                density_solution_saline *
                water_mass_fraction_saline *
                (1000. / self.Mr_water)
            )

            solute_concentration_saline = (
                density_solution_saline *
                solute_mass_fraction_saline *
                (1000. / self.Mr_solute)
            )

            # ----------------------------------------
            # 4. AVERAGE DIFFUSION COEFFICIENTS
            # ----------------------------------------
            water_concentration_fi = np.mean([
                water_concentration_fresh,
                water_concentration_intermediate
            ])

            water_concentration_is = np.mean([
                water_concentration_intermediate,
                water_concentration_saline
            ])

            solute_concentration_fi = np.mean([
                solute_concentration_fresh,
                solute_concentration_intermediate
            ])

            solute_concentration_is = np.mean([
                solute_concentration_intermediate,
                solute_concentration_saline
            ])

            water_diffusion_coeff_fi = (
                self.diffusivity_water_fresh_segment *
                water_concentration_fi  / (
                    R * self.temperature
                )
            )

            water_diffusion_coeff_is = (
                self.diffusivity_water_saline_segment *
                water_concentration_is  / (
                    R * self.temperature
                )
            )

            solute_diffusion_coeff_fi = (
                self.diffusivity_solute_fresh_segment *
                solute_concentration_fi / (
                    R * self.temperature
                )
            )

            solute_diffusion_coeff_is = (
                self.diffusivity_solute_saline_segment *
                solute_concentration_is / (
                    R * self.temperature
                )
            )

            # ----------------------------------------
            # 5. CHEMICAL POTENTIALS
            # ----------------------------------------
            water_potential_fresh = (
                chemical_potential.compute(
                    activity=water_fraction_fresh,
                    temperature=self.temperature
                )
            )

            water_potential_intermediate = (
                chemical_potential.compute(
                    activity=water_fraction_intermediate,
                    temperature=self.temperature
                )
            )

            water_potential_saline = (
                chemical_potential.compute(
                    activity=water_fraction_saline,
                    temperature=self.temperature
                )
            )

            solute_potential_fresh = (
                chemical_potential.compute(
                    activity=solute_fraction_fresh,
                    temperature=self.temperature
                )
            )

            solute_potential_intermediate = (
                chemical_potential.compute(
                    activity=solute_fraction_intermediate,
                    temperature=self.temperature
                )
            )

            solute_potential_saline = (
                chemical_potential.compute(
                    activity=solute_fraction_saline,
                    temperature=self.temperature
                )
            )

            # ----------------------------------------
            # 6. FLUXES
            # ----------------------------------------
            J_w_fi = (
                -1. *
                water_diffusion_coeff_fi *
                self.cs_area * (
                    (
                        water_potential_fresh -
                        water_potential_intermediate
                    ) / self.numerical_separation[0]
                )
            )

            J_w_is = (
                -1. *
                water_diffusion_coeff_is *
                self.cs_area * (
                    (
                        water_potential_intermediate -
                        water_potential_saline
                    ) / self.numerical_separation[1]
                ) 
            )

            J_s_fi = (
                -1. *
                solute_diffusion_coeff_fi *
                self.cs_area * (
                    (
                        solute_potential_fresh -
                        solute_potential_intermediate
                    ) / self.numerical_separation[0]
                )
            )

            J_s_is = (
                -1. *
                solute_diffusion_coeff_is *
                self.cs_area * (
                    (
                        solute_potential_intermediate -
                        solute_potential_saline
                    ) / self.numerical_separation[1]
                ) 
            )

            return np.asarray([
                J_w_fi, J_w_is - J_w_fi, -J_w_is,
                J_s_fi, J_s_is - J_s_fi, -J_s_is
            ])

        # initial condition
        initial_moles = np.asarray([
            self.moles_water_fresh_initial,
            self.moles_water_intermediate_initial,
            self.moles_water_saline_initial,
            self.moles_solute_fresh_initial,
            self.moles_solute_intermediate_initial,
            self.moles_solute_saline_initial
        ])

        # numerical solution
        t = np.arange(n_steps) * step_size

        result = odeint(
            differential, initial_moles, t,
            hmax=(
                hmax if hmax else 0
            )
        )

        # times to steady state (water)
        times_to_steady_state_water = []

        # fresh segment
        mass_fraction_water_fresh = (
            (result[:, 0] * self.Mr_water)
        ) / (
            (result[:, 0] * self.Mr_water) +
            (result[:, 3] * self.Mr_solute)
        )

        idx = 0
        while (
            mass_fraction_water_fresh[-1] -
            mass_fraction_water_fresh[idx] >= 0.0001
        ):
            idx += 1

        times_to_steady_state_water.append(t[idx])

        # intermediate segment
        mass_fraction_water_intermediate = (
            (result[:, 1] * self.Mr_water)
        ) / (
            (result[:, 1] * self.Mr_water) +
            (result[:, 4] * self.Mr_solute)
        )

        idx = 0
        while (
            mass_fraction_water_intermediate[-1] -
            mass_fraction_water_intermediate[idx] >=
            0.0001
        ):
            idx += 1

        times_to_steady_state_water.append(t[idx])

        # saline segment
        mass_fraction_water_saline = (
            (result[:, 2] * self.Mr_water)
        ) / (
            (result[:, 2] * self.Mr_water) +
            (result[:, 5] * self.Mr_solute)
        )

        idx = 0
        while (
            mass_fraction_water_saline[-1] -
            mass_fraction_water_saline[idx] >= 0.0001
        ):
            idx += 1

        times_to_steady_state_water.append(t[idx])

        # times to steady state (solute)
        times_to_steady_state_solute = []

        # fresh segment
        mass_fraction_solute_fresh = (
            (result[:, 3] * self.Mr_solute)
        ) / (
            (result[:, 0] * self.Mr_water) +
            (result[:, 3] * self.Mr_solute)
        )

        idx = 0
        while (
            mass_fraction_solute_fresh[-1] -
            mass_fraction_solute_fresh[idx] >= 0.0001
        ):
            idx += 1

        times_to_steady_state_solute.append(t[idx])

        # intermediate segment
        mass_fraction_solute_intermediate = (
            (result[:, 4] * self.Mr_solute)
        ) / (
            (result[:, 1] * self.Mr_water) +
            (result[:, 4] * self.Mr_solute)
        )

        idx = 0
        while (
            mass_fraction_solute_intermediate[-1] -
            mass_fraction_solute_intermediate[idx] >=
            0.0001
        ):
            idx += 1

        times_to_steady_state_solute.append(t[idx])

        # saline segment
        mass_fraction_solute_saline = (
            (result[:, 5] * self.Mr_solute)
        ) / (
            (result[:, 2] * self.Mr_water) +
            (result[:, 5] * self.Mr_solute)
        )

        idx = 0
        while (
            mass_fraction_solute_saline[-1] -
            mass_fraction_solute_saline[idx] >= 0.0001
        ):
            idx += 1

        times_to_steady_state_solute.append(t[idx])

        # return outcomes
        return {
            "moles": result,
            "mass_fractions": {
                "solute_fresh" : (
                    mass_fraction_solute_fresh
                ),
                "solute_intermediate": (
                    mass_fraction_solute_intermediate
                ),
                "solute_saline": (
                    mass_fraction_solute_saline
                )
            },
            "times_to_steady_state": {
                "water": times_to_steady_state_water,
                "solute": times_to_steady_state_solute
            }
        }
