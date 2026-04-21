import unittest

from repository.penguin_repository import PenguinRepository
from service.penguin_service import PenguinService, ServiceError
from domain.penguin import Penguin


class TestPenguinService(unittest.TestCase):
    def setUp(self):
        self.repo = PenguinRepository([
            Penguin(
                species="Adelie",
                island="Torgersen",
                sex="MALE",
                culmen_length_mm=39.1,
                culmen_depth_mm=18.7,
                flipper_length_mm=181,
                body_mass_g=3750,
                individual_id="A-1",
            ),
            Penguin(
                species="Adelie",
                island="Biscoe",
                sex="FEMALE",
                culmen_length_mm=40.3,
                culmen_depth_mm=18.0,
                flipper_length_mm=195,
                body_mass_g=3250,
                individual_id="A-2",
            ),
            Penguin(
                species="Gentoo",
                island="Biscoe",
                sex="MALE",
                culmen_length_mm=50.0,
                culmen_depth_mm=15.0,
                flipper_length_mm=215,
                body_mass_g=5000,
                individual_id="G-1",
            ),
            Penguin(
                species="Chinstrap",
                island="Dream",
                sex=None,
                culmen_length_mm=None,
                culmen_depth_mm=19.2,
                flipper_length_mm=190,
                body_mass_g=None,
                individual_id="C-1",
            ),
        ])
        self.svc = PenguinService(self.repo)

    def test_filter_with_predicate(self):
        res = self.svc.filter(lambda p: (p.get_species() or "").lower() == "gentoo")
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].get_individual_id(), "G-1")

    def test_filter_attribute_numeric_greater_than(self):
        res = self.svc.filter_attribute("body_mass_g", "4000")
        self.assertEqual([p.get_individual_id() for p in res], ["G-1"])

    def test_filter_attribute_numeric_invalid_value_raises(self):
        with self.assertRaises(ServiceError):
            self.svc.filter_attribute("body_mass_g", "not_a_number")

    def test_filter_attribute_text_equals(self):
        res = self.svc.filter_attribute("species", "Adelie")
        self.assertEqual(len(res), 2)
        self.assertCountEqual([p.get_individual_id() for p in res], ["A-1", "A-2"])

    def test_unique_values_text_counts(self):
        counts = self.svc.unique_values("species")
        self.assertEqual(counts.get("Adelie"), 2)
        self.assertEqual(counts.get("Gentoo"), 1)
        self.assertEqual(counts.get("Chinstrap"), 1)

    def test_unique_values_numeric_counts_ignores_none(self):
        counts = self.svc.unique_values("body_mass_g")
        self.assertEqual(counts.get("3750"), 1)
        self.assertEqual(counts.get("3250"), 1)
        self.assertEqual(counts.get("5000"), 1)
        self.assertNotIn("None", counts)

    def test_describe_attribute_returns_min_max_mean(self):
        mn, mx, avg = self.svc.describe_attribute("flipper_length_mm")
        self.assertEqual(mn, 181.0)
        self.assertEqual(mx, 215.0)
        self.assertAlmostEqual(avg, 195.25, places=6)

    def test_describe_attribute_accepts_synonym_field_name(self):
        mn, mx, avg = self.svc.describe_attribute("culmen length")
        self.assertEqual(mn, 39.1)
        self.assertEqual(mx, 50.0)
        self.assertAlmostEqual(avg, (39.1 + 40.3 + 50.0) / 3.0, places=6)

    def test_describe_attribute_raises_for_non_numeric_field(self):
        with self.assertRaises(ServiceError):
            self.svc.describe_attribute("species")

    def test_describe_attribute_raises_if_no_numeric_data(self):
        repo2 = PenguinRepository([
            Penguin(species="Adelie", body_mass_g=None),
            Penguin(species="Gentoo", body_mass_g=None),
        ])
        svc2 = PenguinService(repo2)

        with self.assertRaises(ServiceError):
            svc2.describe_attribute("body_mass_g")


if __name__ == "__main__":
    unittest.main()
