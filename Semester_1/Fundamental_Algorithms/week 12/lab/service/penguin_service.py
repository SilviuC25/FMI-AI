from __future__ import annotations

from typing import List, Dict, Callable, Optional, Any, Tuple
from statistics import mean, median, pstdev
import os
import time
import random
import copy

from repository.penguin_repository import PenguinRepository
from domain.penguin import Penguin
from utils import sorting


_NUMERIC_FIELD_GETTERS: Dict[str, Callable[[Penguin], Optional[float]]] = {
    "culmen_length_mm": lambda p: p.get_culmen_length_mm(),
    "culmen length": lambda p: p.get_culmen_length_mm(),
    "culmenlength": lambda p: p.get_culmen_length_mm(),
    "culmen_length": lambda p: p.get_culmen_length_mm(),
    "culmen_depth_mm": lambda p: p.get_culmen_depth_mm(),
    "culmen depth mm": lambda p: p.get_culmen_depth_mm(),
    "culmendepth": lambda p: p.get_culmen_depth_mm(),
    "culmen_depth": lambda p: p.get_culmen_depth_mm(),
    "flipper_length_mm": lambda p: p.get_flipper_length_mm(),
    "flipper length": lambda p: p.get_flipper_length_mm(),
    "flipperlength": lambda p: p.get_flipper_length_mm(),
    "flipper_length": lambda p: p.get_flipper_length_mm(),
    "body_mass_g": lambda p: p.get_body_mass_g(),
    "body mass": lambda p: p.get_body_mass_g(),
    "bodymass": lambda p: p.get_body_mass_g(),
    "body_mass": lambda p: p.get_body_mass_g(),
}

_TEXT_FIELD_GETTERS: Dict[str, Callable[[Penguin], Optional[str]]] = {
    "species": lambda p: p.get_species(),
    "island": lambda p: p.get_island(),
    "sex": lambda p: p.get_sex(),
    "individual_id": lambda p: p.get_individual_id(),
    "study_name": lambda p: p.get_study_name(),
}

_SORTING_ALGORITHMS: Dict[str, Callable[..., List[Penguin]]] = {
    "bubble": sorting.bubble_sort,
    "selection": sorting.selection_sort,
    "insertion": sorting.insertion_sort,
    "merge": sorting.merge_sort,
    "quick": sorting.quick_sort,
    "heap": sorting.heap_sort,
}


class ServiceError(Exception):
    """Generic service-level error."""
    pass


class PenguinService:
    """
    High-level operations on Penguin data (independent from UI).
    """

    def __init__(self, repository: PenguinRepository, data_dir: str = "data"):
        """
        Initializes the service with a repository instance and a predefined data directory.

        Args:
            repository (PenguinRepository): The underlying repository.
            data_dir (str): Directory used by `print available_data` and for saving generated CSVs.

        Time Complexity:
            O(1)

        Space Complexity:
            O(1)
        """
        self._repo = repository
        self._data_dir = data_dir

    def set_data_dir(self, data_dir: str) -> None:
        """
        Sets the predefined data directory.

        Args:
            data_dir (str): New directory path.

        Raises:
            ServiceError: If the directory does not exist.

        Time Complexity:
            O(1)

        Space Complexity:
            O(1)
        """
        if not os.path.isdir(data_dir):
            raise ServiceError(f"Directory does not exist: {data_dir}")
        self._data_dir = data_dir

    def load_from_csv(self, path: str, encoding: str = "utf-8") -> int:
        """
        Loads penguins from a CSV file into the underlying repository.

        Args:
            path (str): Path to the CSV file.
            encoding (str): Text encoding (default 'utf-8').

        Returns:
            int: Number of rows loaded.

        Raises:
            ServiceError: If the repository fails to load.

        Time Complexity:
            O(n), where n is the number of rows in the file.

        Space Complexity:
            O(n), for storing the loaded penguins in memory.
        """
        try:
            return self._repo.load_from_csv(path, encoding=encoding)
        except Exception as exc:
            raise ServiceError(str(exc)) from exc

    def get_all(self) -> List[Penguin]:
        """
        Returns all penguins from the repository.

        Returns:
            list[Penguin]: List of all penguins.

        Time Complexity:
            O(n) – returns a shallow copy.

        Space Complexity:
            O(n).
        """
        return self._repo.get_all()

    def filter(self, predicate: Callable[[Penguin], bool]) -> List[Penguin]:
        """
        Returns a list of penguins matching the given predicate.

        Args:
            predicate (Callable[[Penguin], bool]): Predicate applied to each penguin.

        Returns:
            list[Penguin]: Penguins for which predicate returns True.

        Time Complexity:
            O(n).

        Space Complexity:
            O(k).
        """
        return self._repo.filter(predicate)

    def filter_by_species(self, species_substring: str) -> List[Penguin]:
        """
        Filters penguins whose species contains the given substring (case-insensitive).

        Time Complexity:
            O(n)

        Space Complexity:
            O(k)
        """
        return self._repo.find_by_species(species_substring)

    def filter_by_island(self, island_substring: str) -> List[Penguin]:
        """
        Filters penguins whose island contains the given substring (case-insensitive).

        Time Complexity:
            O(n)

        Space Complexity:
            O(k)
        """
        return self._repo.find_by_island(island_substring)

    def filter_by_sex(self, sex_value: str) -> List[Penguin]:
        """
        Filters penguins by sex (exact match after normalization).

        Time Complexity:
            O(n)

        Space Complexity:
            O(k)
        """
        s = sex_value.strip().lower()
        return [p for p in self._repo if p.get_sex() and p.get_sex().strip().lower() == s]

    def filter_by_range(self, field: str, low: Optional[float], high: Optional[float]) -> List[Penguin]:
        """
        Filters penguins where low <= field_value <= high for a numeric field.

        Time Complexity:
            O(n)

        Space Complexity:
            O(k)
        """
        getter = self._normalize_numeric_getter(field)
        out: List[Penguin] = []
        for p in self._repo:
            v = getter(p)
            if v is None:
                continue
            if low is not None and v < low:
                continue
            if high is not None and v > high:
                continue
            out.append(p)
        return out

    def filter_attribute(self, attribute: str, value_str: str) -> List[Penguin]:
        """
        Implements: filter <attribute> <value>

        Rules:
            - numeric attribute: keep rows where attribute_value > value
            - text attribute: keep rows where attribute_value == value

        Time Complexity:
            O(n)

        Space Complexity:
            O(k)
        """
        attribute = attribute.strip()
        try:
            g = self._normalize_numeric_getter(attribute)
            try:
                t = float(value_str)
            except ValueError as exc:
                raise ServiceError("Numeric attribute requires a numeric value.") from exc
            return [p for p in self._repo if (v := g(p)) is not None and v > t]
        except ServiceError:
            gt = self._get_text_getter(attribute)
            return [p for p in self._repo if (v := gt(p)) is not None and v == value_str]

    def sort_by(self, field: str, reverse: bool = False) -> List[Penguin]:
        """
        Sort using Python built-in sorted().

        Time Complexity:
            O(n log n)

        Space Complexity:
            O(n)
        """
        return sorted(self._repo.get_all(), key=self._get_sort_key(field), reverse=reverse)

    def sort_by_algorithm(self, field: str, algorithm: str = "quick", reverse: bool = False) -> List[Penguin]:
        """
        Sort using a specified algorithm.

        Time Complexity:
            bubble/selection/insertion: O(n^2)
            merge/heap: O(n log n)
            quick: avg O(n log n), worst O(n^2)

        Space Complexity:
            Depends on algorithm.
        """
        if algorithm not in _SORTING_ALGORITHMS:
            raise ServiceError(f"Unknown algorithm: {algorithm!r}.")
        items = self._repo.get_all()
        key_func = self._get_sort_key(field)
        return _SORTING_ALGORITHMS[algorithm](items, key=key_func, reverse=reverse)

    def unique_values(self, attribute: str) -> Dict[str, int]:
        """
        Implements: unique <attribute>

        Time Complexity:
            O(n)

        Space Complexity:
            O(k)
        """
        attribute = attribute.strip()
        out: Dict[str, int] = {}
        try:
            g = self._normalize_numeric_getter(attribute)
            for p in self._repo:
                v = g(p)
                if v is None:
                    continue
                k = str(v)
                out[k] = out.get(k, 0) + 1
            return out
        except ServiceError:
            gt = self._get_text_getter(attribute)
            for p in self._repo:
                v = gt(p)
                if v is None:
                    continue
                k = str(v)
                out[k] = out.get(k, 0) + 1
            return out

    def describe_attribute(self, attribute: str) -> Tuple[float, float, float]:
        """
        Implements: describe <attribute> (numeric only).

        Time Complexity:
            O(n)

        Space Complexity:
            O(m)
        """
        g = self._normalize_numeric_getter(attribute)
        vals = [float(v) for p in self._repo if (v := g(p)) is not None]
        if not vals:
            raise ServiceError(f"No numeric data found for attribute {attribute!r}.")
        return min(vals), max(vals), float(mean(vals))

    def stats_for_field(self, field: str, species: Optional[str] = None) -> Dict[str, Optional[float]]:
        """
        Stats for numeric field: count, mean, median, min, max, std(population).

        Time Complexity:
            O(n)

        Space Complexity:
            O(m)
        """
        g = self._normalize_numeric_getter(field)
        vals: List[float] = []
        for p in self._repo:
            if species and p.get_species() != species:
                continue
            v = g(p)
            if v is not None:
                vals.append(float(v))
        if not vals:
            return {"count": 0, "mean": None, "median": None, "min": None, "max": None, "std": None}
        return {
            "count": len(vals),
            "mean": float(mean(vals)),
            "median": float(median(vals)),
            "min": float(min(vals)),
            "max": float(max(vals)),
            "std": float(pstdev(vals)) if len(vals) > 1 else 0.0,
        }

    def average_measurements_by_species(self) -> Dict[str, Dict[str, Optional[float]]]:
        """
        Per-species averages for the 4 numeric measurement fields.

        Time Complexity:
            O(n)

        Space Complexity:
            O(s)
        """
        acc: Dict[str, Dict[str, List[float]]] = {}
        for p in self._repo:
            sp = p.get_species() or "UNKNOWN"
            if sp not in acc:
                acc[sp] = {k: [] for k in ("culmen_length_mm", "culmen_depth_mm", "flipper_length_mm", "body_mass_g")}
            for name, getter in (
                ("culmen_length_mm", lambda x: x.get_culmen_length_mm()),
                ("culmen_depth_mm", lambda x: x.get_culmen_depth_mm()),
                ("flipper_length_mm", lambda x: x.get_flipper_length_mm()),
                ("body_mass_g", lambda x: x.get_body_mass_g()),
            ):
                v = getter(p)
                if v is not None:
                    acc[sp][name].append(float(v))
        return {sp: {f: (float(mean(vs)) if vs else None) for f, vs in fields.items()} for sp, fields in acc.items()}

    def group_by(self, field: str) -> Dict[Any, List[Penguin]]:
        """
        Groups penguins by a text field.

        Time Complexity:
            O(n)

        Space Complexity:
            O(n)
        """
        gt = self._get_text_getter(field)
        groups: Dict[Any, List[Penguin]] = {}
        for p in self._repo:
            k = gt(p) or "UNKNOWN"
            groups.setdefault(k, []).append(p)
        return groups

    def measurement_pairs_for_scatter(self, x_field: str, y_field: str, species: Optional[str] = None) -> Tuple[List[float], List[float]]:
        """
        Returns x,y numeric pairs for plotting.

        Time Complexity:
            O(n)

        Space Complexity:
            O(m)
        """
        gx = self._normalize_numeric_getter(x_field)
        gy = self._normalize_numeric_getter(y_field)
        xs: List[float] = []
        ys: List[float] = []
        for p in self._repo:
            if species and p.get_species() != species:
                continue
            xv, yv = gx(p), gy(p)
            if xv is None or yv is None:
                continue
            xs.append(float(xv))
            ys.append(float(yv))
        return xs, ys

    @staticmethod
    def random_fact() -> str:
        """
        Returns a random penguin fact (at least 15 choices).

        Time Complexity:
            O(1)

        Space Complexity:
            O(1)
        """
        facts = [
            "Penguins are flightless birds but are excellent swimmers.",
            "Most penguin species live in the Southern Hemisphere.",
            "Gentoo penguins are among the fastest underwater swimming birds.",
            "Penguins have dense feathers and a fat layer for insulation.",
            "Emperor penguins can dive deeper than 500 meters when hunting.",
            "Penguins can drink seawater thanks to a salt-filtering gland.",
            "Adelie penguins often build nests using small stones.",
            "Penguin chicks have soft down feathers before waterproof plumage.",
            "Many species form colonies with thousands of individuals.",
            "Penguins use their wings as flippers underwater.",
            "Each penguin has a unique call to recognize mates and chicks.",
            "Some penguins can hold their breath underwater for over 15 minutes.",
            "Penguins preen to keep feathers clean and waterproof.",
            "Their black-and-white coloring helps camouflage in water.",
            "Penguins mainly eat krill, fish, and squid.",
            "Penguins molt once a year and replace all feathers.",
        ]
        return random.choice(facts)

    @staticmethod
    def ascii_penguin() -> str:
        """
        Returns an ASCII-art drawing of a penguin.

        Time Complexity:
            O(1)

        Space Complexity:
            O(1)
        """
        return (
            """

            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡄⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⢇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠃⠸⠀⠀⠀⣀⣠⡄⠀⠀⠀⠁⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠘⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣤⣶⡶⠛⠛⠛⠟⢂⣶⣆⡀⠀⠇⠀⠀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠆⠀⠀⠀⠀⠀⢀⣴⣿⠛⠛⢩⠇⠀⠀⠀⠀⠾⡇⠈⠻⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⢰⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⣠⠞⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠈⠀⠈⢷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠘⡄⡆⠀⠀
⠀⠀⠀⠀⠀⠀⠀⡉⠁⠀⣰⡟⣣⠶⠛⠙⢻⣦⠀⠀⠀⠀⠀⢀⣴⠶⠚⠳⣾⣿⡀⢠⠒⠲⡄⢀⣀⠀⠀⠇⢰⠀⠀
⠀⠀⠀⠀⠀⠀⠄⢡⠀⢠⡿⣿⠋⠀⠀⠀⠀⠹⣧⠀⠀⠀⠀⢸⠃⠀⠀⠀⠈⣿⣇⢸⡀⠀⠙⠉⠀⢹⠀⠰⠈⠀⠀
⠀⠀⠀⠀⠀⠀⢠⠀⠀⣼⣼⠇⠀⣰⣾⣶⠀⢀⣿⢂⣠⣄⣀⣼⡄⢰⣿⣶⡄⠸⣿⡀⢣⡀⠀⢀⣠⠎⠀⠒⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⡆⢠⣿⡿⠀⠀⢿⣿⠟⠀⢸⣿⡏⠁⠀⢙⣿⡇⠈⢿⣿⠇⠀⢻⣧⠀⠳⠖⠋⠀⠀⠀⠀⠀⠰⠀
⡴⠉⠉⠓⠒⠒⠤⣄⡸⣿⣧⠀⠀⠀⣤⡄⠀⠀⠙⠿⠿⠿⠿⠋⠁⠀⠀⣤⡀⠀⣸⣿⣀⡤⠔⠒⠚⠉⠉⠳⡀⠀⠃
⢧⠀⠀⠀⠀⠀⠀⠀⠉⣻⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⠋⠁⠀⠀⠀⠀⠀⠀⢰⠃⠀⠀
⠘⢆⠀⠀⠀⠀⠀⠀⠈⣟⠙⠛⠷⣦⣄⣀⡀⠀⠀⢀⣀⠴⣲⢤⣀⣀⣠⣴⠾⠻⣿⠀⠀⠀⠀⠀⠀⠀⢠⠏⠀⠀⠀
⠀⠈⢦⡀⠀⠀⠀⠀⠀⠈⢧⠀⠀⠈⠉⠋⠉⠉⠉⠉⠀⠀⠀⠀⣿⠉⠀⠀⠀⣸⢿⠀⠀⠀⠀⠀⠀⣠⠏⠀⠀⠀⠀
⠀⠀⠀⠳⣄⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠈⢧⠀⠀⠀⢀⡼⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠈⠙⣲⠒⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⡒⠊⠉⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢠⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣳⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⡀⠀⡴⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠨⡇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⡜⢀⡇⠀⠀⠀⠀⢠⠴⢤⣠⠴⠶⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠖⢻⣀⣀⣒⡇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⡜⠀⠀⡇⠀⠀⠀⢠⠃⠀⡆⠀⠀⠀⠉⠉⣷⠀⠀⠀⠀⠀⠀⠀⢀⡎⠀⢀⠀⠀⠀⠿⣧⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⣧⠀⠀⠹⡄⠀⠀⢸⠀⠀⡇⠀⠀⠀⠀⢀⠇⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⢸⠀⠀⠀⣰⠃⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠘⠳⠤⠤⣹⣦⡀⠸⡄⠀⠹⡄⠀⠀⠀⡞⠀⠀⠀⠀⠀⠀⠀⠀⠸⡆⠀⠸⠀⢀⠼⠁⠀⢱⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠦⣄⣁⣀⣤⠾⠓⠒⠉⠉⠀⠀⠀⠉⠉⠑⠛⠢⠤⠴⠋⠀⠀⠠⠘⠀⠀⠀⠀⠀⠀⠀
        
"""
        )

    def list_available_data(self) -> List[str]:
        """
        Implements: print available_data

        Returns:
            list[str]: Names of all .csv files in the predefined directory.

        Time Complexity:
            O(f)

        Space Complexity:
            O(f)
        """
        try:
            return sorted([fn for fn in os.listdir(self._data_dir) if fn.lower().endswith(".csv")])
        except Exception as exc:
            raise ServiceError(str(exc)) from exc

    def augment(self, percent: int, mode: str, encoding: str = "utf-8") -> str:
        """
        Implements: augument <percent> <duplicate|create>

        It creates a new CSV file in the predefined directory (auto name).
        duplicate: randomly duplicates existing rows.
        create: creates new rows with random values based on existing data:
            - text fields: choose an existing value
            - numeric fields: random value between min and max

        Returns:
            str: full path to the generated CSV file.

        Time Complexity:
            duplicate: O(n + a)
            create: O(n + a)

        Space Complexity:
            O(n)
        """
        if percent < 0:
            raise ServiceError("Percent must be non-negative.")
        mode = mode.strip().lower()
        if mode not in ("duplicate", "create"):
            raise ServiceError("Mode must be 'duplicate' or 'create'.")
        base = self._repo.get_all()
        n = len(base)
        if n == 0:
            raise ServiceError("No data loaded.")
        add_count = int(n * (percent / 100.0))
        augmented: List[Penguin] = base.copy()
        if add_count <= 0:
            return self._save_generated_csv(augmented, mode, percent, encoding=encoding)

        if mode == "duplicate":
            for _ in range(add_count):
                augmented.append(copy.deepcopy(random.choice(base)))
            return self._save_generated_csv(augmented, mode, percent, encoding=encoding)

        str_pool: Dict[str, List[str]] = {}
        for k, getter in _TEXT_FIELD_GETTERS.items():
            vals = [v for p in base if (v := getter(p)) not in (None, "")]
            if vals:
                str_pool[k] = list({str(v) for v in vals})

        num_minmax: Dict[str, Tuple[float, float]] = {}
        for k, getter in _NUMERIC_FIELD_GETTERS.items():
            if "_" not in k:
                continue
            vals = [float(v) for p in base if (v := getter(p)) is not None]
            if vals:
                num_minmax[k] = (min(vals), max(vals))

        template_row = base[0].to_dict()
        for _ in range(add_count):
            row = dict(template_row)
            if "species" in str_pool:
                row["Species"] = random.choice(str_pool["species"])
            if "island" in str_pool:
                row["Island"] = random.choice(str_pool["island"])
            if "sex" in str_pool:
                row["Sex"] = random.choice(str_pool["sex"])
            if "study_name" in str_pool:
                row["studyName"] = random.choice(str_pool["study_name"])

            if "culmen_length_mm" in num_minmax:
                a, b = num_minmax["culmen_length_mm"]
                row["Culmen Length (mm)"] = f"{random.uniform(a, b):.1f}"
            if "culmen_depth_mm" in num_minmax:
                a, b = num_minmax["culmen_depth_mm"]
                row["Culmen Depth (mm)"] = f"{random.uniform(a, b):.1f}"
            if "flipper_length_mm" in num_minmax:
                a, b = num_minmax["flipper_length_mm"]
                row["Flipper Length (mm)"] = str(int(round(random.uniform(a, b))))
            if "body_mass_g" in num_minmax:
                a, b = num_minmax["body_mass_g"]
                row["Body Mass (g)"] = str(int(round(random.uniform(a, b))))

            row["Individual ID"] = f"GEN_{int(time.time() * 1000)}_{random.randint(0, 99999)}"
            augmented.append(Penguin.from_csv_row(row))

        return self._save_generated_csv(augmented, mode, percent, encoding=encoding)

    def help_text(self) -> str:
        """
        Implements: help

        Returns:
            str: Help text listing commands and short usage indications.

        Time Complexity:
            O(1)

        Space Complexity:
            O(1)
        """
        return (
            "GUI Tabs (what each one does):\n"
            "  Load & Info\n"
            "    Load a CSV from anywhere. Then you can show counts by Species/Island,\n"
            "    display a random penguin fact, or draw the ASCII penguin.\n"
            "  Available Data\n"
            "    Shows all .csv files found in the predefined data directory (DATA_DIR).\n"
            "    You can refresh the list and load a selected file directly from there.\n"
            "  Augment\n"
            "    Runs: augument <percent> <duplicate|create>.\n"
            "    'duplicate' randomly duplicates existing penguins.\n"
            "    'create' generates new penguins using existing string values and\n"
            "    numeric values between min and max. Saves to an auto-named CSV in DATA_DIR.\n"
            "  Plots\n"
            "    Create plots from the loaded data: scatter (x vs y), histogram (one field),\n"
            "    and boxplot (numeric field grouped by a text field).\n"
            "  Sorting\n"
            "    Sort the dataset by a chosen field using one of 6 algorithms and show the\n"
            "    top results in a table.\n"
            "  Filter\n"
            "    Simple filter by species/island/sex, plus the PDF command:\n"
            "    filter <attribute> <value> (numeric: attribute > value, text: attribute == value).\n"
            "  Statistics\n"
            "    Show statistics for numeric fields, average by species, describe <attribute>,\n"
            "    and unique <attribute>.\n"
            "  Help\n"
            "    Shows this message. You can also copy it to clipboard.\n"
        )


    def _save_generated_csv(self, penguins: List[Penguin], mode: str, percent: int, encoding: str = "utf-8") -> str:
        """
        Saves a list of penguins to a new file inside the predefined directory.

        Time Complexity:
            O(n)

        Space Complexity:
            O(1)
        """
        os.makedirs(self._data_dir, exist_ok=True)
        fname = f"augmented_{mode}_{percent}_{int(time.time())}.csv"
        out_path = os.path.join(self._data_dir, fname)
        tmp_repo = PenguinRepository(penguins)
        try:
            tmp_repo.save_to_csv(out_path, encoding=encoding, include_all_columns=True)
        except Exception as exc:
            raise ServiceError(str(exc)) from exc
        return out_path

    def _normalize_numeric_getter(self, field: str) -> Callable[[Penguin], Optional[float]]:
        """
        Normalizes a numeric field name and returns the corresponding getter.

        Time Complexity:
            O(m) where m is number of supported numeric aliases (small constant).

        Space Complexity:
            O(1)
        """
        raw = field.strip().lower()
        key = raw.replace("-", " ").replace(".", " ").replace("_", " ")
        if raw in _NUMERIC_FIELD_GETTERS:
            return _NUMERIC_FIELD_GETTERS[raw]
        for k in _NUMERIC_FIELD_GETTERS:
            if k == key or k.replace("_", " ") == key or k.replace(" ", "") == key:
                return _NUMERIC_FIELD_GETTERS[k]
        raise ServiceError(f"Unknown numeric field: {field!r}.")

    def _get_text_getter(self, field: str) -> Callable[[Penguin], Optional[str]]:
        """
        Returns a getter for a text attribute.

        Time Complexity:
            O(1)

        Space Complexity:
            O(1)
        """
        k = field.strip().lower()
        if k in _TEXT_FIELD_GETTERS:
            return _TEXT_FIELD_GETTERS[k]
        raise ServiceError(f"The specified column '{field}' does not exist.")

    def _get_sort_key(self, field: str) -> Callable[[Penguin], Any]:
        """
        Returns a key function that produces sortable values, placing missing values last.

        Time Complexity:
            O(1)

        Space Complexity:
            O(1)
        """
        try:
            g = self._normalize_numeric_getter(field)
            return lambda p: (1, 0.0) if (v := g(p)) is None else (0, float(v))
        except ServiceError:
            gt = self._get_text_getter(field)
            return lambda p: (1, "") if (v := gt(p)) is None else (0, str(v).lower())


    
    def save_random_penguins(self, k: int, path: str) -> None:
        """
        Choose k random penguins from the currently loaded dataset
        and save them to a CSV file.

        Time Complexity:
            O(n) – sampling + saving
        Space Complexity:
            O(k)
        """
        if k <= 0:
            raise ServiceError("Number of penguins must be positive.")

        all_penguins = self._repo.get_all()
        if not all_penguins:
            raise ServiceError("No penguins available to save.")

        if k > len(all_penguins):
            raise ServiceError(
                f"Requested {k} penguins, but only {len(all_penguins)} available."
            )

        selected = random.sample(all_penguins, k)

        temp_repo = PenguinRepository(selected)

        try:
            temp_repo.save_to_csv(path)
        except Exception as e:
            raise ServiceError(f"Could not save random penguins: {e}")
        

    def generate_research_groups(self, k: int) -> List[List]:
        """
        Generate and return all possible research groups of size k (k >= 3),
        where each group contains at least one penguin from each species
        present in the currently loaded dataset. Penguins must be distinct.

        Constraints:
        - the loaded dataset must contain at most 10 penguins
        - solve using backtracking

        Returns:
            List of groups; each group is a list of Penguin objects.
        """
        if k < 3:
            raise ServiceError("k must be >= 3.")

        penguins = self._repo.get_all()
        n = len(penguins)

        if n == 0:
            raise ServiceError("No penguins loaded.")
        if n > 10:
            raise ServiceError("Research groups can only be generated when the loaded dataset has at most 10 penguins.")
        if k > n:
            raise ServiceError(f"k={k} is larger than the number of loaded penguins ({n}).")

        required_species = {p.get_species() for p in penguins if p.get_species() is not None}
        if len(required_species) == 0:
            raise ServiceError("No species information available in the loaded dataset.")
        if len(required_species) > k:
            raise ServiceError("k is too small to include at least one penguin from each species.")

        results: List[List] = []
        current: List = []

        def backtrack(start_index: int):
            if len(current) == k:
                group_species = {p.get_species() for p in current if p.get_species() is not None}
                if required_species.issubset(group_species):
                    results.append(current.copy())
                return

            remaining_slots = k - len(current)
            remaining_penguins = n - start_index
            if remaining_penguins < remaining_slots:
                return

            for i in range(start_index, n):
                current.append(penguins[i])
                backtrack(i + 1)
                current.pop()

        backtrack(0)

        if not results:
            raise ServiceError("No research group can be generated for the given k and the currently loaded dataset.")

        return results
    
    def split_into_groups(self, threshold: float) -> List[Tuple[List, List, float, float]]:
        """
        Generate all possible ways to split ALL loaded penguins into two groups
        (different sizes allowed) such that:
        - each group has at least 2 penguins
        - sum(body_mass_g) in each group <= threshold
        Constraints:
        - loaded dataset must contain at most 10 penguins
        Solve using backtracking (no itertools/combinations).

        Returns:
        A list of tuples: (group1, group2, sum1, sum2)
        """
        if threshold <= 0:
            raise ServiceError("Threshold must be > 0.")

        penguins = self._repo.get_all()
        n = len(penguins)

        if n == 0:
            raise ServiceError("No penguins loaded.")
        if n > 10:
            raise ServiceError("Splitting into groups is allowed only when the loaded dataset has at most 10 penguins.")
        if n < 4:
            raise ServiceError("At least 4 penguins are required (each group must have at least 2 penguins).")

        masses: List[float] = []
        for p in penguins:
            m = p.get_body_mass_g()
            if m is None:
                raise ServiceError("All penguins must have body_mass_g in order to split into groups.")
            masses.append(float(m))

        results: List[Tuple[List, List, float, float]] = []
        g1: List = []
        g2: List = []
        s1 = 0.0
        s2 = 0.0

        g1.append(penguins[0])
        s1 += masses[0]

        def backtrack(i: int, sum1: float, sum2: float):
            if sum1 > threshold or sum2 > threshold:
                return

            if i == n:
                if len(g1) >= 2 and len(g2) >= 2:
                    results.append((g1.copy(), g2.copy(), sum1, sum2))
                return

            remaining = n - i

            need1 = 0 if len(g1) >= 2 else (2 - len(g1))
            need2 = 0 if len(g2) >= 2 else (2 - len(g2))
            if remaining < (need1 + need2):
                return

            p = penguins[i]
            m = masses[i]

            g1.append(p)
            backtrack(i + 1, sum1 + m, sum2)
            g1.pop()

            g2.append(p)
            backtrack(i + 1, sum1, sum2 + m)
            g2.pop()

        backtrack(1, s1, s2)

        if not results:
            raise ServiceError("No valid split could be identified for the given threshold.")

        return results

