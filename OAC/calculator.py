import unittest

class Calculator:
    def add(self, a, b):
        return a + b

    def add(self, a):
        return a + a

# Test cases for Calculator
class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_add_two_arguments(self):
        self.assertEqual(self.calc.add(3, 4), 7)  # Original call

    def test_add_one_argument(self):
        self.assertEqual(self.calc.add(3), 6)      # Original call

    def test_add_no_arguments(self):
        with self.assertRaises(TypeError):
            self.calc.add()                          # Should raise TypeError

# Running the tests
if __name__ == '__main__':
    unittest.main()


from oac_mutation import mutate_code


input_code = """
import unittest

class Calculator:
    def add(self, a, b):
        return a + b

    def add(self, a):
        return a + a

# Test cases for Calculator
class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_add_two_arguments(self):
        self.assertEqual(self.calc.add(3, 4), 7)

    def test_add_one_argument(self):
        self.assertEqual(self.calc.add(3), 6)

    def test_add_no_arguments(self):
        with self.assertRaises(TypeError):
            self.calc.add()

# Running the tests
if __name__ == '__main__':
    unittest.main()
"""

mutated_code = mutate_code(input_code)


from run_tests import calculate_mutation_score

mutated_codes = [
    mutated_code
]

# Calculate mutation score
calculate_mutation_score(input_code, mutated_codes)