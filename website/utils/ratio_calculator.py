import timeit
from fractions import Fraction
from mpmath import mp
from sympy import Rational

from website.utils import utils
from sympy.ntheory import continued_fraction

from website.utils.stern_brocot import SBNode


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
        self.ratio = mp.mpf(numerator) / mp.mpf(denominator)
        self.max_denominator = max_denominator
        self.max_numerator = max_numerator
        self.total_elements = 0

    def remove_overflow(self):
        if len(self.fractions) <= self.n_elements:
            return

        self.fractions = self.fractions[:-1]

    def generate_fraction(self, numerator, min_denominator):
        for denominator in range(min_denominator, min_denominator + 4):
            fraction = Fraction(denominator, numerator)
            self.combinations_checked += 1

            # Check to see if the fraction is already in the list
            if any(value == fraction for value in self.fractions):
                break

            self.fractions.append(fraction)
            self.fractions.sort()
            self.remove_overflow()
            self.total_elements += 1

    def generate_fraction_list_old(self):
        if self.ratio < 1:
            self.fraction = Fraction(self.fraction.denominator, self.fraction.numerator)
            self.ratio = mp.mpf(1) / self.ratio

        max_numerator = min(self.max_numerator, int(self.max_denominator * self.numerator / self.denominator))
        for numerator in range(1, max_numerator + 1):
            min_denominator = int(numerator * self.denominator / self.numerator) + (1 if self.ratio > 1 else 0)
            self.generate_fraction(numerator, min_denominator)

    def generate_fraction_list(self):
        if self.numerator < self.denominator:
            child_tree_data = SBNode(self.numerator, self.denominator).left_child().get_fractions(self.max_numerator, self.max_denominator, self.n_elements)
            neighbour_fraction_tree_data = SBNode(self.numerator, self.denominator).get_parent().left_child().get_fractions(self.max_numerator, self.max_denominator, self.n_elements, child_tree_data)
        else:
            child_tree_data = SBNode(self.numerator, self.denominator).right_child().get_fractions(self.max_numerator, self.max_denominator, self.n_elements)
            neighbour_fraction_tree_data = SBNode(self.numerator, self.denominator).get_parent().right_child().get_fractions(self.max_numerator, self.max_denominator, self.n_elements, child_tree_data)
        parent = [SBNode(self.numerator, self.denominator).get_parent().fraction]

        if parent[0].p > self.max_numerator or parent[0].q > self.max_denominator or child_tree_data.fractions_generated >= 10:
            parent = []

        self.fractions = [Fraction(el.p, el.q) for el in child_tree_data.fractions + parent + neighbour_fraction_tree_data.fractions]

    def run(self):
        start_time = timeit.default_timer()

        self.generate_fraction_list_new()

        data = []
        for i, fraction in enumerate(self.fractions):
            temp = {'numerator': fraction.numerator, 'denominator': fraction.denominator, 'ratio': utils.ratio(fraction), 'inverse_ratio': utils.inverse_ratio(fraction)}
            if i > 0:
                temp['ratio_diff'] = temp['ratio'] - data[i - 1]['ratio']
                temp['inverse_ratio_diff'] = data[i - 1]['inverse_ratio'] - temp['inverse_ratio']
                temp['ratio_diff_total'] = data[0]['ratio'] - temp['ratio']
                temp['inverse_ratio_diff_total'] = temp['inverse_ratio'] - data[0]['inverse_ratio']

            for k, v in temp.items():
                temp[k] = round(v, self.precision) if self.precision > 0 else int(temp[k])

            data.append(temp)

        elapsed = timeit.default_timer() - start_time

        return {'fractions': data, 'iterations': self.combinations_checked, 'time': utils.humanize_seconds(elapsed), 'n_elements': self.n_elements}

    def generate_fraction_list_new(self):
        for den in range(1, self.max_denominator + 1):
            for num in range(1, self.max_numerator + 1):
                self.combinations_checked += 1
                if num * self.denominator >= self.numerator * den:
                    break

                fraction = Fraction(num, den)
                if fraction.numerator != num or fraction.denominator != den:
                    continue

                self.fractions.append(fraction)
                self.fractions.sort(reverse=True)
                self.remove_overflow()
                self.total_elements += 1
