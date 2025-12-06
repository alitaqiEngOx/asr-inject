""" Licensed under the same terms as described in the main 
licensing script of this repository. """

from typing import Any, Optional, Union

import numpy as np
from numpy.typing import NDArray
from scipy.integrate import odeint

from asr_inject.operations import chemical_potential


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

        self.Mr_water = config[
            "solution_characteristics"
        ]["Mr_water"]

        self.Mr_solute = config[
            "solution_characteristics"
        ]["Mr_solute"]

        self.length = config["reservoir_dimensions"][
            "length"
        ]

        self.width = config["reservoir_dimensions"][
            "width"
        ]

        self.height = config["reservoir_dimensions"][
            "height"
        ]

        self.temperature = config["reservoir_conditions"][
            "temperature"
        ] + CELSIUS_TO_KELVIN

        self.pressure = config["reservoir_conditions"][
            "pressure"
        ] * BAR_TO_PA

        self.volume_fraction_fresh = config["fresh_segment"][
            "volume_fraction"
        ]

        self.mass_fraction_solute_fresh_initial = config[
            "fresh_segment"
        ]["solute_mass_fraction"]

        self.mass_fraction_solute_saline_initial = config[
            "saline_segment"
        ]["solute_mass_fraction"]

    @property
    def mass_fraction_water_fresh_initial(self) -> float:
        """
        """
        return 1. - self.mass_fraction_solute_fresh_initial

    @property
    def mass_fraction_water_saline_initial(self) -> float:
        """
        """
        return 1. - self.mass_fraction_solute_saline_initial

    @property
    def cs_area(self) -> float:
        """
        """
        return self.length * self.width

    @property
    def numerical_separation(self) -> float:
        """
        """
        height_fresh = (
            self.height * self.volume_fraction_fresh
        )

        height_saline = (
            self.height * self.volume_fraction_saline
        )

        return 0.5 * (height_fresh + height_saline)

    @property
    def volume_fraction_saline(self) -> float:
        """
        """
        return 1. - self.volume_fraction_fresh

    @property
    def volume(self) -> float:
        """
        """
        return self.length * self.width * self.height

    @property
    def volume_fresh(self) -> float:
        """
        """
        return self.volume * self.volume_fraction_fresh

    @property
    def volume_saline(self) -> float:
        """
        """
        return self.volume * self.volume_fraction_saline

    @property
    def mass_water_fresh_initial(self) -> float:
        """
        """
        return (
            self.density_pure * self.volume_fresh *
            self.mass_fraction_water_fresh_initial
        )

    @property
    def mass_water_saline_initial(self) -> float:
        """
        """
        return (
            self.density_pure * self.volume_saline *
            self.mass_fraction_water_saline_initial
        )

    @property
    def mass_solute_fresh_initial(self) -> float:
        """
        """
        return (
            self.density_pure * self.volume_fresh *
            self.mass_fraction_solute_fresh_initial
        )

    @property
    def mass_solute_saline_initial(self) -> float:
        """
        """
        return (
            self.density_pure * self.volume_saline *
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
    def moles_solute_saline_initial(self) -> float:
        """
        """
        return (
            self.mass_solute_saline_initial /
            self.Mr_solute
        )

    @property
    def diffusivity_water(self) -> float:
        """
        """
        base = self.fitting["water_diffusivity"][0]
        energy = self.fitting["water_diffusivity"][1]

        exp_term = -energy / (R * self.temperature)

        return base * np.exp(exp_term)

    @property
    def diffusivity_solute(self) -> float:
        """
        """
        base = self.fitting["solute_diffusivity"][0]
        energy = self.fitting["solute_diffusivity"][1]

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
            mass_fraction_solute: Union[float, NDArray]
    ) -> Union[float, NDArray]:
        """
        """
        solubility = mass_fraction_solute / (
            1. - mass_fraction_solute
        )

        A0 = self.fitting["density"]["salinity"]["A0"]
        A1 = self.fitting["density"]["salinity"]["A1"]

        d_rho = solubility * (A0 + (self.temperature * A1))

        return self.density_pure + d_rho

    def predict(
            self, *, n_steps: int, step_size: float,
            hmax: Optional[float]=None
    ) -> dict[str, NDArray]:
        """
        """
        def differential(
                moles: NDArray, t: float
        ) -> NDArray:
            """
            """
            water_moles = moles[:2]
            solute_moles = moles[2:]

            # fresh segment
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

            water_concentration_fresh = (
                self.density_pure *
                water_mass_fraction_fresh *
                (1000. / self.Mr_water)
            )

            solute_concentration_fresh = (
                self.density_pure *
                solute_mass_fraction_fresh *
                (1000. / self.Mr_solute)
            )

            # saline segment
            water_fraction_saline = (
                water_moles[1] / (
                    water_moles[1] + solute_moles[1]
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

            water_concentration_saline = (
                self.density_pure *
                water_mass_fraction_saline *
                (1000. / self.Mr_water)
            )

            solute_concentration_saline = (
                self.density_pure *
                solute_mass_fraction_saline *
                (1000. / self.Mr_solute)
            )

            # average diffusion coefficients
            water_concentration_mean = np.mean([
                water_concentration_fresh,
                water_concentration_saline
            ])

            solute_concentration_mean = np.mean([
                solute_concentration_fresh,
                solute_concentration_saline
            ])

            water_diffusion_coefficient_average = (
                self.diffusivity_water *
                water_concentration_mean / (
                    R * self.temperature
                )
            )

            solute_diffusion_coefficient_average = (
                self.diffusivity_solute *
                solute_concentration_mean / (
                    R * self.temperature
                )
            )

            # chemical potentials
            water_potential_fresh = (
                chemical_potential.compute(
                    activity=water_fraction_fresh,
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

            solute_potential_saline = (
                chemical_potential.compute(
                    activity=solute_fraction_saline,
                    temperature=self.temperature
                )
            )

            # fluxes
            J_w_sf = (
                -1. *
                water_diffusion_coefficient_average *
                self.cs_area * (
                    (
                        water_potential_saline -
                        water_potential_fresh
                    ) / self.numerical_separation
                )
            )

            J_s_sf = (
                -1. *
                solute_diffusion_coefficient_average *
                self.cs_area * (
                    (
                        solute_potential_saline -
                        solute_potential_fresh
                    ) / self.numerical_separation
                )
            )

            return np.asarray([
                -J_w_sf, J_w_sf, -J_s_sf, J_s_sf
            ])

        # initial condition
        initial_moles = np.asarray([
            self.moles_water_fresh_initial,
            self.moles_water_saline_initial,
            self.moles_solute_fresh_initial,
            self.moles_solute_saline_initial
        ])

        # numerical solution
        result = odeint(
            differential, initial_moles,
            np.arange(n_steps) * step_size,
            hmax=(
                hmax if hmax else 0
            )
        )

        mass_fraction_solute_fresh = result[:, 2] / (
            result[:, 0] + result[:, 2]
        )

        density_fresh = self.compute_density_solution(
            mass_fraction_solute_fresh
        )

        return {
            "moles": result,
            "mass_fraction_solute_fresh": (
                mass_fraction_solute_fresh
            ),
            "density_fresh": density_fresh
        }
