import timeit
from fractions import Fraction
from mpmath import mp
from undercutter.utils import utils


class Calculation:
    def __init__(self, numerator, denominator, n_elements=3, precision=4, max_numerator=100, max_denominator=100):
        mp.dps = 10
        self.numerator = numerator
        self.denominator = denominator
        self.fraction = Fraction(numerator, denominator)
        self.precision = precision
        self.combinations_checked = 0
        self.fractions = []
        self.n_elements = n_elements
        self.ratio = mp.mpf(numerator) / mp.mpf(denominator)  # if ratio_to_surpass < 1 else 1 / ratio_to_surpass  # left page number
        self.max_denominator = max_denominator
        self.max_numerator = max_numerator
        self.total_elements = 0

    def remove_overflow(self):
        if len(self.fractions) > self.n_elements:
            self.fractions = self.fractions[:-1]

    def check_fraction(self, numerator, denominator):
        fraction = Fraction(numerator / denominator)
        if fraction < self.fraction:
            if self.fractions:
                if fraction > self.fractions[-1] and not any(value == fraction for value in self.fractions) or len(self.fractions) < self.n_elements:
                    self.fractions.append(fraction)
                    self.remove_overflow()
            else:
                self.fractions.append(fraction)
        self.combinations_checked += 1

        return fraction

    def generate_fraction(self, numerator, min_denominator):
        if min_denominator > 0:
            for denominator in range(min_denominator, min_denominator + 4):
                fraction = Fraction(denominator, numerator)
                if not any(value == fraction for value in self.fractions):
                    self.fractions.append(fraction)
                    self.fractions.sort()
                    self.remove_overflow()
                    self.total_elements += 1
                self.combinations_checked += 1
        else:
            for den in range(1, self.max_denominator + 1):
                ratio = self.check_fraction(numerator, den)
                if self.fractions and ratio < self.fractions[-1] and len(self.fractions) == self.n_elements:
                    break

    def generate_fraction_list(self):
        if self.ratio < 1:
            self.fraction = Fraction(self.fraction.denominator, self.fraction.numerator)
            self.ratio = mp.mpf(1) / self.ratio

        max_numerator = min(self.max_numerator, int(self.max_denominator * self.numerator / self.denominator))
        for numerator in range(1, max_numerator + 1):
            min_denominator = int(numerator * self.denominator / self.numerator) + (1 if self.ratio > 1 else 0)
            self.generate_fraction(numerator, min_denominator)

    def run(self):
        start_time = timeit.default_timer()
        self.generate_fraction_list()

        mp.dps = self.precision
        data = []
        for i, fraction in enumerate(self.fractions):
            temp = {'numerator': fraction.denominator, 'denominator': fraction.numerator, 'ratio': utils.inverse_ratio(fraction), 'inverse_ratio': utils.ratio(fraction)}
            if i > 0:
                temp['ratio_diff'] = temp['ratio'] - data[i - 1]['ratio']
                temp['inverse_ratio_diff'] = data[i - 1]['inverse_ratio'] - temp['inverse_ratio']
                temp['ratio_diff_total'] = data[0]['ratio'] - temp['ratio']
                temp['inverse_ratio_diff_total'] = temp['inverse_ratio'] - data[0]['inverse_ratio']
            data.append(temp)

        elapsed = timeit.default_timer() - start_time

        return {'fractions': data, 'iterations': self.combinations_checked, 'time': utils.humanize_seconds(elapsed), 'n_elements': self.n_elements}
