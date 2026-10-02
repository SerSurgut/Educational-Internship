import unittest

from material_calculator import calculate_material_quantity


class CalculateMaterialQuantityTest(unittest.TestCase):
    def test_standard_calculation(self):
        result = calculate_material_quantity(1, 1, 10, 2.0, 3.0)
        self.assertEqual(result, 142)

    def test_fractional_result_rounds_up(self):
        result = calculate_material_quantity(2, 2, 1, 1.0, 1.0)
        self.assertEqual(result, 6)

    def test_unknown_type_ids(self):
        self.assertEqual(calculate_material_quantity(99, 1, 10, 2.0, 3.0), -1)
        self.assertEqual(calculate_material_quantity(1, 99, 10, 2.0, 3.0), -1)

    def test_negative_params(self):
        self.assertEqual(calculate_material_quantity(1, 1, 10, -2.0, 3.0), -1)
        self.assertEqual(calculate_material_quantity(1, 1, 10, 2.0, -3.0), -1)

    def test_zero_or_negative_quantity(self):
        self.assertEqual(calculate_material_quantity(1, 1, 0, 2.0, 3.0), -1)
        self.assertEqual(calculate_material_quantity(1, 1, -5, 2.0, 3.0), -1)

    def test_wrong_argument_types(self):
        nan = float("nan")
        inf = float("inf")
        wrong_arguments = [
            ("1", 1, 10, 2.0, 3.0),
            (1, None, 10, 2.0, 3.0),
            (1, 1, True, 2.0, 3.0),
            (1, 1, 10.5, 2.0, 3.0),
            (1, 1, 10, [2], 3.0),
            (1, 1, 10, False, 3.0),
            (1, 1, 10, nan, 3.0),
            (1, 1, 10, 2.0, inf),
            (1, 1, 10, 1e200, 1e200),
        ]
        for arguments in wrong_arguments:
            with self.subTest(arguments=arguments):
                result = calculate_material_quantity(*arguments)
                self.assertEqual(result, -1)


if __name__ == "__main__":
    unittest.main()
