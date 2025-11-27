""" Licensed under the same terms as described in the main 
licensing script of this repository. """

from typing import Any


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

        self.fresh_volume_fraction = config["fresh_segment"][
            "volume_fraction"
        ]

        self.fresh_mole_fraction = config["fresh_segment"][
            "solute_mole_fraction"
        ]

        self.saline_mole_fraction = config["saline_segment"][
            "solute_mole_fraction"
        ]

    @property
    def saline_volume_fraction(self) -> float:
        """
        """
        return 1. - self.fresh_volume_fraction

    @property
    def volume(self) -> float:
        """
        """
        return self.length * self.width * self.height

    @property
    def fresh_volume(self) -> float:
        """
        """
        return self.volume * self.fresh_volume_fraction

    @property
    def saline_volume(self) -> float:
        """
        """
        return self.volume * self.saline_volume_fraction

    @property
    def pure_water_density(self) -> float:
        """
        """
        output = 0.
        for idx, coeff in enumerate(self.fitting):
            output += coeff * self.temperature**idx

        return output

    @property
    def fresh_density(self) -> float:
        """
        """
        solubility = self.fresh_mole_fraction / (
            1. - self.fresh_mole_fraction
        )

        solubility *= (self.Mr_solute / self.Mr_water)

        A0 = self.fitting["density"][
            "salinity_fitting"
        ]["A0"]
        A1 = self.fitting["density"][
            "salinity_fitting"
        ]["A1"]

        d_rho = solubility * (A0 + (self.temperature * A1))

        return self.pure_water_density + d_rho

    @property
    def saline_density(self) -> float:
        """
        """
        solubility = self.saline_mole_fraction / (
            1. - self.saline_mole_fraction
        )

        solubility *= (self.Mr_solute / self.Mr_water)

        A0 = self.fitting["density"][
            "salinity_fitting"
        ]["A0"]
        A1 = self.fitting["density"][
            "salinity_fitting"
        ]["A1"]

        d_rho = solubility * (A0 + (self.temperature * A1))

        return self.pure_water_density + d_rho
