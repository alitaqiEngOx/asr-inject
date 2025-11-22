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
        self.length = config["reservoir_dimensions"][
            "length"
        ]
        self.width = config["reservoir_dimensions"][
            "width"
        ]
        self.height = config["reservoir_dimensions"][
            "height"
        ]

        if type == "fresh":
            self.height *= config["fresh_segment"][
                "volume_fraction"
            ]

        elif type == "fresh":
            self.height *= 1. - config["fresh_segment"][
                "volume_fraction"
            ]

        else:
            raise TypeError(
                f"unknown segment type {type}"
            )
