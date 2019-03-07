from django.test import TestCase
from website.utils.ratio_calculator import Calculation
from fractions import Fraction
from website.utils import utils


class CalculationTestCase(TestCase):
    limit = 100

    def test_normal_ratio(self):
        data = Calculation(188, 55, 10, 4, self.limit, self.limit).run()
        self.assert_empty(data)
        self.assert_has_simplifiable_terms(data)
        self.assert_not_nth_element(data, 0, 188, 55)
        self.assert_nth_element(data, 0, 41, 12)
        self.assert_nth_element(data, 9, 44, 13)
        self.assertTrue(data['fractions'][0]['ratio'] > 1)

    def test_inverse_ratio(self):
        inverse_data = Calculation(55, 188, 10, 4, self.limit, self.limit).run()
        self.assert_empty(inverse_data)
        self.assert_has_simplifiable_terms(inverse_data)
        self.assert_not_nth_element(inverse_data, 0, 55, 188)
        self.assert_nth_element(inverse_data, 0, 19, 65)
        self.assert_nth_element(inverse_data, 9, 11, 38)
        self.assertTrue(inverse_data['fractions'][0]['ratio'] < 1)

    def test_other(self):
        data2 = Calculation(100, 13, 24, 16, self.limit, self.limit).run()
        self.assert_empty(data2)
        data1 = Calculation(1, 7, 10, 4, self.limit, self.limit).run()
        self.assert_empty(data1)
        self.assert_has_simplifiable_terms(data1)
        self.assert_not_nth_element(data1, 0, 1, 7)
        self.assert_nth_element(data1, 0, 14, 99)
        self.assert_nth_element(data1, 8, 13, 93)
        self.assert_nth_element(data1, 9, 6, 43)

    def test_humanize_seconds(self):
        self.assertEqual(utils.humanize_seconds(654321.123456), '181 hours, 45 minutes, 21 seconds, 123 milliseconds and 456 microseconds')
        self.assertEqual(utils.humanize_seconds(3660.123456), '1 hour, 1 minute, 123 milliseconds and 456 microseconds')
        self.assertEqual(utils.humanize_seconds(3660.123456), '1 hour, 1 minute, 123 milliseconds and 456 microseconds')
        self.assertEqual(utils.humanize_seconds(3660), '1 hour and 1 minute')
        self.assertEqual(utils.humanize_seconds(0.001001), '1 millisecond and 1 microsecond')

    def assert_has_simplifiable_terms(self, data):
        self.assertFalse(any(value['numerator'] != Fraction(value['numerator'], value['denominator']).numerator for value in data['fractions']), 'There are simplifiable terms')

    def assert_nth_element(self, data, n, numerator_result, denominator_result):
        self.assertTrue(data['fractions'][n]['numerator'] == numerator_result and data['fractions'][n]['denominator'] == denominator_result, f'Element {n} is {data["fractions"][n]["numerator"]}/{data["fractions"][n]["denominator"]} instead of {numerator_result}/{denominator_result}')

    def assert_not_nth_element(self, data, n, numerator_result, denominator_result):
        self.assertFalse(data['fractions'][n]['numerator'] == numerator_result and data['fractions'][n]['denominator'] == denominator_result, f'Element {n} shouldn\'t be {numerator_result} / {denominator_result} in {data["fractions"]}')

    def assert_empty(self, data):
        self.assertTrue(utils.is_empty(data), f'The list is empty')

    def assert_not_empty(self, data):
        self.assertFalse(utils.is_empty(data), f'The list is not empty')
