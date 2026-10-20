"""Regenerate the paper figure from the exact scalar quadrature.

Requires numpy, scipy and matplotlib. No ODE discretisation is used.
Run from this file's directory, or pass --output-dir.
"""
from pathlib import Path
import argparse
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def theta_of_s(s, m):
    # z=exp(-s): theta=integral_0^s exp((m-1)v)/(1+exp(-v)) dv.
    return quad(lambda v: np.exp((m-1)*v)/(1+np.exp(-v)),
                0., s, epsabs=1e-11, epsrel=2e-12)[0]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path,
                        default=Path(__file__).resolve().parent / "figures")
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 9,
        "axes.labelsize": 10, "axes.titlesize": 11,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.edgecolor": "#5B5660", "text.color": "#29232D",
        "axes.labelcolor": "#29232D", "xtick.color": "#5B5660",
        "ytick.color": "#5B5660", "pdf.fonttype": 42,
    })
    fig, axs = plt.subplots(1, 2, figsize=(8.2, 3.45), constrained_layout=True)
    times = np.geomspace(1e-2, 1e8, 250)
    colours = ["#7B3F7E", "#BE793B", "#417A76", "#75833A"]
    for m, colour in zip([2, 3, 4, 6], colours):
        exponent_label = "2" if m == 2 else rf"\frac{{{m}}}{{{m-1}}}"
        s = np.array([brentq(lambda v: theta_of_s(v, m)-t,
                            0., (np.log1p(2*(m-1)*t)+2)/(m-1),
                            xtol=2e-13) for t in times])
        z = np.exp(-s)
        axs[0].loglog(times, z**m, color=colour, lw=1.8,
                      label=rf"$m={m}$: $p={exponent_label}$")
        slope = m*times*(1+z)*z**(m-1)
        axs[1].semilogx(times, slope, color=colour, lw=1.8)
        axs[1].axhline(m/(m-1), color=colour, ls=":", lw=1, alpha=.8)
        # The plotted quadrature agrees with the asymptotic exponent.
        assert abs(slope[-1] - m/(m-1)) < .06
    axs[0].set(title="Exact algebraic tails", ylabel=r"Scaled activity $I/\kappa_m$",
               xlabel=r"Scaled time $\theta=\kappa_m t$")
    axs[0].legend(frameon=False, loc="lower left", fontsize=8)
    axs[1].set(title="Local decay exponent", ylabel=r"$-d\log I/d\log t$",
               xlabel=r"Scaled time $\theta=\kappa_m t$", ylim=(0, 2.12))
    for ax in axs:
        ax.grid(True, which="major", color="#DED9DE", lw=.55, alpha=.7)
        ax.set_xlim(times[0], times[-1])
    fig.savefig(args.output_dir / "decay_family.pdf")
    fig.savefig(args.output_dir / "decay_family.png", dpi=220)
    plt.close(fig)
    print("PASS: exact quadrature figure and limiting-slope sanity check")


if __name__ == "__main__":
    main()
