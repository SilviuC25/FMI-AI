"""
Plotting utilities for the Penguins lab.

Provides functions that produce matplotlib Figure objects and save PNG files.
Functions are GUI-agnostic: a GUI can embed the returned Figure (e.g. with
FigureCanvasTkAgg for Tkinter) or simply use the saved PNG files.

Dependencies:
  - matplotlib (required)
  - seaborn (optional, used when available for nicer styling)

All functions will create the output directory if necessary.
"""

from typing import List, Dict, Optional, Tuple
import os

try:
    import matplotlib.pyplot as plt
    from matplotlib.figure import Figure
except Exception as e:
    raise ImportError("matplotlib is required for utils.plotting: pip install matplotlib") from e

try:
    import seaborn as sns
    _HAS_SEABORN = True
except Exception:
    _HAS_SEABORN = False


def _ensure_dir_for_file(path: str) -> None:
    d = os.path.dirname(path)
    if d and not os.path.exists(d):
        os.makedirs(d, exist_ok=True)


def _apply_style():
    if _HAS_SEABORN:
        sns.set(style="whitegrid")
    else:
        plt.style.use("seaborn-v0_8") if "seaborn-v0_8" in plt.style.available else plt.style.use("ggplot")


def save_scatter(
    xs: List[float],
    ys: List[float],
    out_path: str,
    title: str = "",
    x_label: str = "x",
    y_label: str = "y",
    figsize: Tuple[float, float] = (7, 5),
    dpi: int = 150,
    marker: str = "o",
    color: str = None,
    alpha: float = 0.8,
) -> Figure:
    """
    Create and save a scatter plot from parallel lists xs, ys.
    Returns the matplotlib Figure (useful for embedding in GUIs).
    """
    if len(xs) != len(ys):
        raise ValueError("xs and ys must have the same length")
    if not xs:
        raise ValueError("No data provided to save_scatter")

    _apply_style()
    fig = plt.Figure(figsize=figsize, dpi=dpi)
    ax = fig.subplots()
    ax.scatter(xs, ys, marker=marker, c=color, alpha=alpha)
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.grid(True)

    _ensure_dir_for_file(out_path)
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)
    return fig


def save_histogram(
    values: List[float],
    out_path: str,
    title: str = "",
    x_label: str = "",
    bins: int = 20,
    figsize: Tuple[float, float] = (7, 5),
    dpi: int = 150,
    color: str = None,
    alpha: float = 0.8,
) -> Figure:
    """
    Create and save a histogram of `values`.
    """
    if not values:
        raise ValueError("No data provided to save_histogram")

    _apply_style()
    fig = plt.Figure(figsize=figsize, dpi=dpi)
    ax = fig.subplots()
    ax.hist(values, bins=bins, color=color, alpha=alpha)
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel("Frequency")
    ax.grid(True)

    _ensure_dir_for_file(out_path)
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)
    return fig


def save_boxplot(
    groups: Dict[str, List[float]],
    out_path: str,
    title: str = "",
    y_label: str = "",
    figsize: Tuple[float, float] = (8, 5),
    dpi: int = 150,
    showfliers: bool = True,
) -> Figure:
    """
    Create and save a boxplot. `groups` is a dict label -> list of numeric values.
    """
    if not groups:
        raise ValueError("No groups provided to save_boxplot")

    _apply_style()
    fig = plt.Figure(figsize=figsize, dpi=dpi)
    ax = fig.subplots()
    labels = []
    data = []
    for label, vals in groups.items():
        non_empty = [v for v in vals if v is not None]
        if non_empty:
            labels.append(label)
            data.append(non_empty)

    if not data:
        raise ValueError("All groups are empty or contain only None")

    ax.boxplot(data, labels=labels, patch_artist=True, showfliers=showfliers)
    ax.set_title(title)
    ax.set_ylabel(y_label)
    ax.grid(axis="y")

    _ensure_dir_for_file(out_path)
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)
    return fig


def save_scatter_from_service(
    svc,
    x_field: str,
    y_field: str,
    out_path: str,
    title: str = "",
    x_label: Optional[str] = None,
    y_label: Optional[str] = None,
    species: Optional[str] = None,
    **kwargs,
) -> Figure:
    xs, ys = svc.measurement_pairs_for_scatter(x_field, y_field, species=species)
    if x_label is None:
        x_label = x_field
    if y_label is None:
        y_label = y_field
    return save_scatter(xs, ys, out_path, title=title, x_label=x_label, y_label=y_label, **kwargs)


def save_histogram_from_service(
    svc,
    field: str,
    out_path: str,
    title: str = "",
    x_label: Optional[str] = None,
    species: Optional[str] = None,
    bins: int = 20,
    **kwargs,
) -> Figure:
    """
    Convenience wrapper that collects values for `field` from svc and saves a histogram.
    svc must implement iteration over Penguin objects or provide a suitable getter.
    """
    getter = None
    values = []
    for p in svc.get_all():
        if hasattr(p, "get_" + field):
            v = getattr(p, "get_" + field)()
        else:
            method_name = "get_" + field.strip().lower()
            v = getattr(p, method_name)() if hasattr(p, method_name) else None
        if v is not None:
            values.append(float(v))

    if x_label is None:
        x_label = field
    return save_histogram(values, out_path, title=title, x_label=x_label, bins=bins, **kwargs)