"""
Domain model for a Penguin.

Attributes:
  • species: the penguin species (Chinstrap, Adelie, Gentoo) 
  • flipper_length_mm: flipper length (mm) 
  • culmen_length_mm*: culmen length (mm) 
  • culmen_depth_mm*: culmen depth (mm) 
  • body_mass_g: body mass (g) 
  • island: island name in the Palmer Archipelago
  • sex: penguin sex
"""

from typing import Optional, Dict, Any

class Penguin:
    def __init__(
        self,
        study_name: Optional[str] = None,
        sample_number: Optional[int] = None,
        species: Optional[str] = None,
        region: Optional[str] = None,
        island: Optional[str] = None,
        stage: Optional[str] = None,
        individual_id: Optional[str] = None,
        clutch_completion: Optional[str] = None,
        date_egg: Optional[str] = None,
        culmen_length_mm: Optional[float] = None,
        culmen_depth_mm: Optional[float] = None,
        flipper_length_mm: Optional[float] = None,
        body_mass_g: Optional[float] = None,
        sex: Optional[str] = None,
        delta_15_n: Optional[float] = None,
        delta_13_c: Optional[float] = None,
        comments: Optional[str] = None,
    ):
        self.__study_name = study_name
        self.__sample_number = sample_number
        self.__species = species
        self.__region = region
        self.__island = island
        self.__stage = stage
        self.__individual_id = individual_id
        self.__clutch_completion = clutch_completion
        self.__date_egg = date_egg
        self.__culmen_length_mm = culmen_length_mm
        self.__culmen_depth_mm = culmen_depth_mm
        self.__flipper_length_mm = flipper_length_mm
        self.__body_mass_g = body_mass_g
        self.__sex = sex
        self.__delta_15_n = delta_15_n
        self.__delta_13_c = delta_13_c
        self.__comments = comments

    def get_study_name(self) -> Optional[str]:
        return self.__study_name

    def get_sample_number(self) -> Optional[int]:
        return self.__sample_number

    def get_species(self) -> Optional[str]:
        return self.__species

    def get_region(self) -> Optional[str]:
        return self.__region

    def get_island(self) -> Optional[str]:
        return self.__island

    def get_stage(self) -> Optional[str]:
        return self.__stage

    def get_individual_id(self) -> Optional[str]:
        return self.__individual_id

    def get_clutch_completion(self) -> Optional[str]:
        return self.__clutch_completion

    def get_date_egg(self) -> Optional[str]:
        return self.__date_egg

    def get_culmen_length_mm(self) -> Optional[float]:
        return self.__culmen_length_mm

    def get_culmen_depth_mm(self) -> Optional[float]:
        return self.__culmen_depth_mm

    def get_flipper_length_mm(self) -> Optional[float]:
        return self.__flipper_length_mm

    def get_body_mass_g(self) -> Optional[float]:
        return self.__body_mass_g

    def get_sex(self) -> Optional[str]:
        return self.__sex

    def get_delta_15_n(self) -> Optional[float]:
        return self.__delta_15_n

    def get_delta_13_c(self) -> Optional[float]:
        return self.__delta_13_c

    def get_comments(self) -> Optional[str]:
        return self.__comments

    def set_study_name(self, value: Optional[str]) -> None:
        self.__study_name = value

    def set_sample_number(self, value: Optional[int]) -> None:
        self.__sample_number = value

    def set_species(self, value: Optional[str]) -> None:
        self.__species = value

    def set_region(self, value: Optional[str]) -> None:
        self.__region = value

    def set_island(self, value: Optional[str]) -> None:
        self.__island = value

    def set_stage(self, value: Optional[str]) -> None:
        self.__stage = value

    def set_individual_id(self, value: Optional[str]) -> None:
        self.__individual_id = value

    def set_clutch_completion(self, value: Optional[str]) -> None:
        self.__clutch_completion = value

    def set_date_egg(self, value: Optional[str]) -> None:
        self.__date_egg = value

    def set_culmen_length_mm(self, value: Optional[float]) -> None:
        self.__culmen_length_mm = value

    def set_culmen_depth_mm(self, value: Optional[float]) -> None:
        self.__culmen_depth_mm = value

    def set_flipper_length_mm(self, value: Optional[float]) -> None:
        self.__flipper_length_mm = value

    def set_body_mass_g(self, value: Optional[float]) -> None:
        self.__body_mass_g = value

    def set_sex(self, value: Optional[str]) -> None:
        self.__sex = value

    def set_delta_15_n(self, value: Optional[float]) -> None:
        self.__delta_15_n = value

    def set_delta_13_c(self, value: Optional[float]) -> None:
        self.__delta_13_c = value

    def set_comments(self, value: Optional[str]) -> None:
        self.__comments = value

    def to_dict(self) -> Dict[str, Any]:
        return {
            "studyName": self.__study_name,
            "Sample Number": self.__sample_number,
            "Species": self.__species,
            "Region": self.__region,
            "Island": self.__island,
            "Stage": self.__stage,
            "Individual ID": self.__individual_id,
            "Clutch Completion": self.__clutch_completion,
            "Date Egg": self.__date_egg,
            "Culmen Length (mm)": self.__culmen_length_mm,
            "Culmen Depth (mm)": self.__culmen_depth_mm,
            "Flipper Length (mm)": self.__flipper_length_mm,
            "Body Mass (g)": self.__body_mass_g,
            "Sex": self.__sex,
            "Delta 15 N (o/oo)": self.__delta_15_n,
            "Delta 13 C (o/oo)": self.__delta_13_c,
            "Comments": self.__comments,
        }

    @classmethod
    def from_csv_row(cls, row: Dict[str, str]) -> "Penguin":
        """
        Build a Penguin from a CSV row dict where keys match the CSV headers.
        The row values are strings; this will try to convert numeric fields to numbers,
        and empty strings become None.
        Expected header names:
          'studyName', 'Sample Number', 'Species', 'Region', 'Island', 'Stage',
          'Individual ID', 'Clutch Completion', 'Date Egg', 'Culmen Length (mm)',
          'Culmen Depth (mm)', 'Flipper Length (mm)', 'Body Mass (g)', 'Sex',
          'Delta 15 N (o/oo)', 'Delta 13 C (o/oo)', 'Comments'
        """
        def _parse_int(s: Optional[str]) -> Optional[int]:
            if s is None:
                return None
            if not isinstance(s, str):
                s = str(s)
            s = s.strip()
            if s == "":
                return None
            try:
                return int(float(s))
            except Exception:
                return None

        def _parse_float(s: Optional[str]) -> Optional[float]:
            if s is None:
                return None
            if not isinstance(s, str):
                s = str(s)
            s = s.strip()
            if s == "":
                return None
            try:
                return float(s)
            except Exception:
                return None


        return cls(
            study_name=row.get("studyName") or row.get("studyName".lower()) or row.get("StudyName"),
            sample_number=_parse_int(row.get("Sample Number")),
            species=row.get("Species"),
            region=row.get("Region"),
            island=row.get("Island"),
            stage=row.get("Stage"),
            individual_id=row.get("Individual ID"),
            clutch_completion=row.get("Clutch Completion"),
            date_egg=row.get("Date Egg"),
            culmen_length_mm=_parse_float(row.get("Culmen Length (mm)")),
            culmen_depth_mm=_parse_float(row.get("Culmen Depth (mm)")),
            flipper_length_mm=_parse_float(row.get("Flipper Length (mm)")),
            body_mass_g=_parse_float(row.get("Body Mass (g)")),
            sex=row.get("Sex"),
            delta_15_n=_parse_float(row.get("Delta 15 N (o/oo)")),
            delta_13_c=_parse_float(row.get("Delta 13 C (o/oo)")),
            comments=row.get("Comments"),
        )

    def __str__(self) -> str:
        return (
            f"Penguin(study_name={self.__study_name!r}, sample_number={self.__sample_number!r}, "
            f"species={self.__species!r}, region={self.__region!r}, island={self.__island!r}, "
            f"stage={self.__stage!r}, individual_id={self.__individual_id!r}, "
            f"clutch_completion={self.__clutch_completion!r}, date_egg={self.__date_egg!r}, "
            f"culmen_length_mm={self.__culmen_length_mm!r}, culmen_depth_mm={self.__culmen_depth_mm!r}, "
            f"flipper_length_mm={self.__flipper_length_mm!r}, body_mass_g={self.__body_mass_g!r}, "
            f"sex={self.__sex!r}, delta_15_n={self.__delta_15_n!r}, delta_13_c={self.__delta_13_c!r}, "
            f"comments={self.__comments!r})"
        )

    def __repr__(self) -> str:
        return self.__str__()


