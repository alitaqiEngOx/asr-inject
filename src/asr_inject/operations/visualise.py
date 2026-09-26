""" Licensed under the same terms as described in the main 
licensing script of this repository. """

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray

from asr_inject.utils.log_handler import create


LOGGER = create("visualise")


def plot_2d(
        x_domain: NDArray, y_domains: NDArray,
        *, outname: Path,
        y_domain_labels: list[str] | None=None, 
        axis_labels: list[str] | None=None,
        times_to_steady_state: NDArray | None=None
) -> None:
    """
    """
    # make outdir
    outname.parent.mkdir(parents=True, exist_ok=True)

    for idx in range(y_domains.shape[1]):
        plt.plot(
            x_domain, y_domains[:, idx],
            label=(
                y_domain_labels[idx]
                if y_domain_labels else ''
            )
        )

    if times_to_steady_state is not None:
        time = np.max(times_to_steady_state)

    plt.plot(
        np.asarray([time, time]),
        np.asarray([
            np.min(y_domains), np.max(y_domains)
        ]),
        "k--", label="time to steady state"
    )

    plt.title(outname.stem)

    if y_domain_labels is not None:
        plt.legend(loc="best")

    if axis_labels is not None:
        plt.xlabel(axis_labels[0])
        plt.ylabel(axis_labels[1])

    plt.savefig(outname)
    plt.close()
