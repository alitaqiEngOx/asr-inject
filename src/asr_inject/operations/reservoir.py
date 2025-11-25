""" Licensed under the same terms as described in the main 
licensing script of this repository. """

from typing import Any


CELSIUS_TO_KELVIN = 273.15

class Reservoir:
    """"""

    def __init__(
            self, *, config: dict[str, Any],
            fitting: dict[str, Any]
    ) -> None:
        """
        """
        self.fitting = fitting

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
        ]

        self.fresh_volume_fraction = config["fresh_segment"][
            "volume_fraction"
        ]

        self.temperature = config["reservoir_conditions"][
            "temperature"
        ] + CELSIUS_TO_KELVIN

        self.pressure = config["reservoir_conditions"][
            "pressure"
        ]

    @property
    def volume(self) -> float:
        """
        """
        return self.length * self.width * self.height

    @property
    def saline_volume_fraction(self) -> float:
        """
        """
        return 1. - self.fresh_volume_fraction

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
    def density(self) -> float:
        """
        """
        output = 0.
        for idx, coeff in enumerate(self.fitting):
            output += coeff * self.temperature**idx

        return output

    @property
    def specific_volume(self) -> float:
        """
        """
        return 1. / self.density

