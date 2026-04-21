"""
prepare_data.py

Generate `data/penguins_data.csv` containing only the seven required fields:
- species (Adelie / Chinstrap / Gentoo)
- flipper_length_mm
- culmen_length_mm
- culmen_depth_mm
- body_mass_g
- island
- sex

Only rows that have all seven fields present (non-empty / non-null) are written.

Time Complexity:
    O(n)
"""

import csv
from pathlib import Path
from typing import Optional


def _normalize_species(raw: Optional[str]) -> Optional[str]:
    """
    Normalize raw species name to one of:
        'Adelie', 'Chinstrap', 'Gentoo'.

    Returns:
        str | None: normalized species or None if it cannot be recognized.

    Time Complexity:
        O(1)

    Space Complexity:
        O(1).
    """
    if not raw:
        return None
    s = raw.lower()
    if "adelie" in s:
        return "Adelie"
    if "chinstrap" in s:
        return "Chinstrap"
    if "gentoo" in s or "papua" in s:
        return "Gentoo"
    return None


def _parse_float(raw: Optional[str]) -> Optional[float]:
    """
    Parse a string to float, returning None if it is empty or invalid.

    Time Complexity:
        O(1)

    Space Complexity:
        O(1)
    """
    if raw is None:
        return None
    raw = raw.strip()
    if raw == "":
        return None
    try:
        return float(raw)
    except ValueError:
        return None


def generate_penguins_data(
    src_path: str = "data/penguins.csv",
    out_path: str = "data/penguins_data.csv",
) -> int:
    """
    Reads the original penguins.csv and writes penguins_data.csv
    with only the 7 required columns and only rows where all of them
    are present.

    Args:
        src_path (str): path to the original CSV file.
        out_path (str): path for the generated CSV file.

    Returns:
        int: number of rows written to the output file (excluding header).

    Raises:
        FileNotFoundError: if the source CSV does not exist.

    Time Complexity:
        O(n)
    """
    src = Path(src_path)
    if not src.exists():
        raise FileNotFoundError(f"Source CSV not found: {src}")

    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "species",
        "flipper_length_mm",
        "culmen_length_mm",
        "culmen_depth_mm",
        "body_mass_g",
        "island",
        "sex",
    ]

    written = 0

    with src.open("r", newline="", encoding="utf-8") as fin, \
            out.open("w", newline="", encoding="utf-8") as fout:

        reader = csv.DictReader(fin)
        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            species = _normalize_species(row.get("Species"))
            flipper = _parse_float(row.get("Flipper Length (mm)"))
            culmen_l = _parse_float(row.get("Culmen Length (mm)"))
            culmen_d = _parse_float(row.get("Culmen Depth (mm)"))
            body = _parse_float(row.get("Body Mass (g)"))
            island = (row.get("Island") or "").strip()
            sex = (row.get("Sex") or "").strip()

            if (
                species is None
                or flipper is None
                or culmen_l is None
                or culmen_d is None
                or body is None
                or not island
                or not sex
            ):
                continue

            writer.writerow(
                {
                    "species": species,
                    "flipper_length_mm": flipper,
                    "culmen_length_mm": culmen_l,
                    "culmen_depth_mm": culmen_d,
                    "body_mass_g": body,
                    "island": island,
                    "sex": sex,
                }
            )
            written += 1

    return written


if __name__ == "__main__":
    count = generate_penguins_data()
    print(f"Wrote {count} rows to data/penguins_data.csv")
