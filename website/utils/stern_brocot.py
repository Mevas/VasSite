from sympy import Rational
from sympy.ntheory import continued_fraction


class Data:
    fractions = []
    fractions_generated = 0
    max_fractions_generated = 1


class SBNode:
    def __init__(self, num, den):
        self.fraction = Rational(num, den)
        self.continued_fraction = list(continued_fraction.continued_fraction_iterator(self.fraction))

    def __str__(self):
        return self.fraction.__str__()

    def get_parent(self):
        parent = self.continued_fraction
        parent[-1] -= 1
        parent_fraction = continued_fraction.continued_fraction_reduce(parent)

        return SBNode(parent_fraction.p, parent_fraction.q)

    def left_operation(self):
        child = self.continued_fraction
        child[-1] += 1
        child_fraction = continued_fraction.continued_fraction_reduce(child)

        return SBNode(child_fraction.p, child_fraction.q)

    def right_operation(self):
        child = self.continued_fraction
        child[-1] -= 1
        child.append(2)
        child_fraction = continued_fraction.continued_fraction_reduce(child)

        return SBNode(child_fraction.p, child_fraction.q)

    def left_child(self):
        if len(self.continued_fraction) % 2 == 1:  # Because the formula is based on the parity of k in [a_0, a_1,..., a_k-1]
            return self.right_operation()
        return self.left_operation()

    def right_child(self):
        if len(self.continued_fraction) % 2 == 1:  # Because the formula is based on the parity of k in [a_0, a_1,..., a_k-1]
            return self.left_operation()
        return self.right_operation()

    def traverse_right_priority(self, numerator, denominator, data):
        if self.fraction.p > numerator or self.fraction.q > denominator or data.fractions_generated + 1 >= data.max_fractions_generated:
            return

        data.fractions_generated += 1

        SBNode(self.fraction.p, self.fraction.q).right_child().traverse_right_priority(numerator, denominator, data)
        data.fractions.append(self.fraction)
        SBNode(self.fraction.p, self.fraction.q).left_child().traverse_right_priority(numerator, denominator, data)
        return

    def traverse_left_priority(self, numerator, denominator, data):
        if self.fraction.p > numerator or self.fraction.q > denominator or data.fractions_generated + 1 >= data.max_fractions_generated:
            return

        SBNode(self.fraction.p, self.fraction.q).left_child().traverse_left_priority(numerator, denominator, data)
        data.fractions.append(self.fraction)
        data.fractions_generated += 1
        SBNode(self.fraction.p, self.fraction.q).right_child().traverse_left_priority(numerator, denominator, data)
        return

    # Iterative function for inorder tree traversal
    def inOrder(self, numerator, denominator, data):

        current = self
        # Set current to root of binary tree
        s = []  # initialze stack
        done = 0

        while not done:
            print(current)
            # Reach the left most Node of the current Node
            if not (current.fraction.p > numerator or current.fraction.q > denominator or data.fractions_generated + 1 >= data.max_fractions_generated):

                # Place pointer to a tree node on the stack
                # before traversing the node's left subtree
                s.append(current)

                current = current.right_child()

                # BackTrack from the empty subtree and visit the Node
            # at the top of the stack; however, if the stack is
            # empty you are done
            elif not data.fractions_generated + 1 >= data.max_fractions_generated:
                if len(s) > 0:
                    current = s.pop()
                    print(current)

                    # We have visited the node and its left
                    # subtree. Now, it's right subtree's turn
                    current = current.left_child()

                else:
                    done = 1

    def get_fractions(self, numerator, denominator, max_elements, previous_data=Data()):
        data = Data()
        data.fractions = []
        data.fractions_generated = previous_data.fractions_generated
        data.max_fractions_generated = max_elements
        self.inOrder(numerator, denominator, previous_data)
        # if numerator < denominator:
        #     self.traverse_right_priority(numerator, denominator, data)
        # else:
        #     self.traverse_left_priority(numerator, denominator, data)
        return data
