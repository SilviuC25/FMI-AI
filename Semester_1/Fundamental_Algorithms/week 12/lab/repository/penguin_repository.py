import csv
import os
from typing import List, Callable, Optional, Iterable, Dict
from domain.penguin import Penguin

class RepositoryError(Exception):
    """Generic repository error."""
    pass

class PenguinRepository:
    """
    Repository for Penguin domain objects.
    Responsibilities:
    - load penguins from a CSV (using Penguin.from_csv_row)
    - give access (iterate, length, get_all)
    - add/remove/filter/find operations
    - export a cleaned CSV with the 7 columns required by the lab
    """

    def __init__(self, penguins: Optional[Iterable[Penguin]] = None):
        self._items: List[Penguin] = list(penguins) if penguins is not None else []

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def get_all(self) -> List[Penguin]:
        """Return a shallow copy of all penguins."""
        return list(self._items)

    def add(self, penguin: Penguin) -> None:
        """Add a Penguin to the repository."""
        if not isinstance(penguin, Penguin):
            raise RepositoryError("Only Penguin instances can be added")
        self._items.append(penguin)

    def extend(self, penguins: Iterable[Penguin]) -> None:
        """Extend repository with an iterable of Penguins."""
        for p in penguins:
            self.add(p)

    def remove_if(self, predicate: Callable[[Penguin], bool]) -> int:
        """
        Remove items matching predicate.
        Returns number of removed items.
        """
        old_len = len(self._items)
        self._items = [p for p in self._items if not predicate(p)]
        return old_len - len(self._items)

    def clear(self) -> None:
        """Remove all items."""
        self._items.clear()

    def filter(self, predicate: Callable[[Penguin], bool]) -> List[Penguin]:
        """Return a list of penguins matching predicate."""
        return [p for p in self._items if predicate(p)]

    def find_by_species(self, species_substring: str) -> List[Penguin]:
        """Case-insensitive substring match on species field."""
        s = species_substring.lower()
        return [p for p in self._items if p.get_species() and s in p.get_species().lower()]

    def find_by_island(self, island_substring: str) -> List[Penguin]:
        s = island_substring.lower()
        return [p for p in self._items if p.get_island() and s in p.get_island().lower()]

    def find_by_individual_id(self, individual_id: str) -> Optional[Penguin]:
        for p in self._items:
            if p.get_individual_id() == individual_id:
                return p
        return None

    def load_from_csv(self, path: str, encoding: str = "utf-8") -> int:
        """
        Load penguins from a CSV file into the repository (appends to existing items).
        Uses Penguin.from_csv_row for conversion.
        Returns number of loaded rows.
        """
        if not os.path.exists(path):
            raise RepositoryError(f"CSV file not found: {path}")

        loaded = 0
        with open(path, newline="", encoding=encoding) as f:
            reader = csv.DictReader(f)
            for row in reader:
                p = Penguin.from_csv_row(row)
                self._items.append(p)
                loaded += 1
        return loaded

    def save_to_csv(self, path: str, encoding: str = "utf-8", include_all_columns: bool = True) -> None:
        """
        Save repository items to CSV.
        - include_all_columns: if True write full set of columns (matching Penguin.to_dict keys).
          if False, writes the cleaned 7-column format (see create_cleaned_csv for headers).
        """
        if include_all_columns:
            headers = [
                "studyName", "Sample Number", "Species", "Region", "Island", "Stage",
                "Individual ID", "Clutch Completion", "Date Egg", "Culmen Length (mm)",
                "Culmen Depth (mm)", "Flipper Length (mm)", "Body Mass (g)", "Sex",
                "Delta 15 N (o/oo)", "Delta 13 C (o/oo)", "Comments"
            ]
        else:
            headers = [
                "Species", "Island", "Culmen Length (mm)", "Culmen Depth (mm)",
                "Flipper Length (mm)", "Body Mass (g)", "Sex"
            ]

        with open(path, "w", newline="", encoding=encoding) as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for p in self._items:
                if include_all_columns:
                    row = p.to_dict()
                else:
                    row = {
                        "Species": p.get_species() or "",
                        "Island": p.get_island() or "",
                        "Culmen Length (mm)": p.get_culmen_length_mm() if p.get_culmen_length_mm() is not None else "",
                        "Culmen Depth (mm)": p.get_culmen_depth_mm() if p.get_culmen_depth_mm() is not None else "",
                        "Flipper Length (mm)": p.get_flipper_length_mm() if p.get_flipper_length_mm() is not None else "",
                        "Body Mass (g)": p.get_body_mass_g() if p.get_body_mass_g() is not None else "",
                        "Sex": p.get_sex() or "",
                    }
                writer.writerow(row)

    def create_cleaned_csv(self, path: str, encoding: str = "utf-8", drop_missing: bool = True) -> int:
        """
        Create a cleaned CSV file containing exactly 7 columns:
        ['Species','Island','Culmen Length (mm)','Culmen Depth (mm)',
         'Flipper Length (mm)','Body Mass (g)','Sex']
        If drop_missing is True, rows missing any of the numeric measurement fields
        (culmen length/depth, flipper length, body mass) will be excluded.
        Returns number of rows written.
        """
        headers = [
            "Species", "Island", "Culmen Length (mm)", "Culmen Depth (mm)",
            "Flipper Length (mm)", "Body Mass (g)", "Sex"
        ]
        written = 0
        with open(path, "w", newline="", encoding=encoding) as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for p in self._items:
                culmen_l = p.get_culmen_length_mm()
                culmen_d = p.get_culmen_depth_mm()
                flipper = p.get_flipper_length_mm()
                body = p.get_body_mass_g()

                if drop_missing and (culmen_l is None or culmen_d is None or flipper is None or body is None):
                    continue

                row = {
                    "Species": p.get_species() or "",
                    "Island": p.get_island() or "",
                    "Culmen Length (mm)": culmen_l if culmen_l is not None else "",
                    "Culmen Depth (mm)": culmen_d if culmen_d is not None else "",
                    "Flipper Length (mm)": flipper if flipper is not None else "",
                    "Body Mass (g)": body if body is not None else "",
                    "Sex": p.get_sex() or "",
                }
                writer.writerow(row)
                written += 1
        return written

    @classmethod
    def load_from_csv_file(cls, path: str, encoding: str = "utf-8") -> "PenguinRepository":
        """
        Create a new repository and load items from the given CSV path.
        """
        repo = cls()
        repo.load_from_csv(path, encoding=encoding)
        return repo