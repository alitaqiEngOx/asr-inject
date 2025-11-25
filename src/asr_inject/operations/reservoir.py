""" Licensed under the same terms as described in the main 
licensing script of this repository. """

from typing import Any


CELSIUS_TO_KELVIN = 273.15

class Reservoir:
    """"""

    def __init__(
            self, *, config: dict[str, Any],
            fitting: dict[str, Any], type: str
    ) -> None:
        """
        """
        self.type = type

        self.fitting = fitting

        self.length = config["reservoir_dimensions"][
            "length"
        ]

        self.width = config["reservoir_dimensions"][
            "width"
        ]

        self._height = config["reservoir_dimensions"][
            "height"
        ]

        self._volume_fraction = config["fresh_segment"][
            "volume_fraction"
        ]

        self.temperature = config["reservoir_conditions"][
            "temperature"
        ] + CELSIUS_TO_KELVIN

        self.pressure = config["reservoir_conditions"][
            "pressure"
        ]

    @property
    def volume_fraction(self) -> float:
        """
        """
        if self.type == "fresh":
            return self._volume_fraction

        elif self.type == "saline":
            return 1. - self._volume_fraction

        else:
            raise TypeError(
                f"unknown segment type {type}"
            )

    @property
    def height(self) -> float:
        """
        """
        return self._height * self.volume_fraction

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

