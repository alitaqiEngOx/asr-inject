""" Licensed under the same terms as described in the main 
licensing script of this repository. """

from typing import Any

import numpy as np


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

        self.initial_solute_mole_fraction_fresh = config[
            "fresh_segment"
        ]["solute_mole_fraction"]

        self.initial_solute_mole_fraction_saline = config[
            "saline_segment"
        ]["solute_mole_fraction"]

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
    def water_diffusivity(self) -> float:
        """
        """
        base = self.fitting["water_diffusivity"][0]
        energy = self.fitting["water_diffusivity"][1]

        exp_term = -energy / (R * self.temperature)

        return base * np.exp(exp_term)

    @property
    def solute_diffusivity(self) -> float:
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
        output = 0.
        for idx, coeff in enumerate(self.fitting):
            output += coeff * self.temperature**idx

        return output

    def density_solution(
            self, mole_fraction: float
    ) -> float:
        """
        """
        solubility = mole_fraction / (1. - mole_fraction)

        solubility *= (self.Mr_solute / self.Mr_water)

        A0 = self.fitting["density"][
            "salinity_fitting"
        ]["A0"]
        A1 = self.fitting["density"][
            "salinity_fitting"
        ]["A1"]

        d_rho = solubility * (A0 + (self.temperature * A1))

        return self.density_pure + d_rho
