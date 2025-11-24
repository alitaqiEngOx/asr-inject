""" Licensed under the same terms as described in the main 
licensing script of this repository. """

from typing import Any


class Segment:
    """"""

    def __init__(
            self, config: dict[str, Any], *,
            type: str
    ) -> None:
        """
        """
        self.type = type

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
