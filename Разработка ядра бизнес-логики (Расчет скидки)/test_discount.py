import unittest

from discount import calculate_partner_discount


class TestCalculatePartnerDiscount(unittest.TestCase):
    def test_zero_quantity(self):
        self.assertEqual(calculate_partner_discount(0), 0)

    def test_below_ten_thousand(self):
        self.assertEqual(calculate_partner_discount(9999), 0)

    def test_lower_bound_of_five_percent(self):
        self.assertEqual(calculate_partner_discount(10000), 5)

    def test_upper_bound_of_five_percent(self):
        self.assertEqual(calculate_partner_discount(49999), 5)

    def test_lower_bound_of_ten_percent(self):
        self.assertEqual(calculate_partner_discount(50000), 10)

    def test_upper_bound_of_ten_percent(self):
        self.assertEqual(calculate_partner_discount(299999), 10)

    def test_lower_bound_of_fifteen_percent(self):
        self.assertEqual(calculate_partner_discount(300000), 15)

    def test_above_three_hundred_thousand(self):
        self.assertEqual(calculate_partner_discount(1000000), 15)


if __name__ == "__main__":
    unittest.main()
