from fractions import Fraction

from django.test import TestCase

from website.utils import utils
from website.utils.ratio_calculator import Calculation


class IndexTest(TestCase):
    def test_index_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'website/homepage.html')


class CalculationTestCase(TestCase):
    limit = 100

    def test_normal_ratio(self):
        data = Calculation(188, 55, 10, 4, self.limit, self.limit).run()
        self.assert_empty(data)
        self.assert_has_simplifiable_terms(data)
        self.assert_not_nth_element(data, 1, 188, 55)
        self.assert_nth_element(data, 1, 65, 19)
        self.assert_nth_element(data, 10, 38, 11)
        self.assertTrue(data['fractions'][0]['ratio'] > 1)

    def test_inverse_ratio(self):
        inverse_data = Calculation(55, 188, 10, 4, self.limit, self.limit).run()
        self.assert_empty(inverse_data)
        self.assert_has_simplifiable_terms(inverse_data)
        self.assert_not_nth_element(inverse_data, 1, 55, 188)
        self.assert_nth_element(inverse_data, 1, 12, 41)
        self.assert_nth_element(inverse_data, 10, 13, 44)
        self.assertTrue(inverse_data['fractions'][0]['ratio'] < 1)

    def test_other(self):
        data2 = Calculation(100, 13, 24, 16, self.limit, self.limit).run()
        self.assert_empty(data2)
        data1 = Calculation(1, 7, 10, 4, self.limit, self.limit).run()
        self.assert_empty(data1)
        self.assert_has_simplifiable_terms(data1)
        self.assert_not_nth_element(data1, 1, 1, 7)
        self.assert_nth_element(data1, 1, 14, 97)
        self.assert_nth_element(data1, 9, 13, 89)
        self.assert_nth_element(data1, 10, 6, 41)

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
        self.assertFalse(data['fractions'][n]['numerator'] == numerator_result and data['fractions'][n]['denominator'] == denominator_result, f'Element {n} shouldn\'t be {numerator_result} / {denominator_result} in {0}')

    def assert_empty(self, data):
        self.assertTrue(utils.is_empty(data), f'The list is empty')
