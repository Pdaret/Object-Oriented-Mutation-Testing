from mutation_operators import *
import unittest
from mutation_testing_framework import MutationTestingFramework
from test_classes import *

mutation_operators = [
    new_method_call_with_child_class,
    member_variable_with_parent_type,
    process_object_with_child_type,
    overloading_method_contents_replace,
]

original_objects = [Parent(), Child(), Calculator()]


# Test cases
class TestFramework(unittest.TestCase):
    def test_parent_process(self):
        parent = Parent()
        self.assertEqual(parent.process(), "Processed by Parent")

    def test_child_display(self):
        child = Child()
        self.assertEqual(child.display(), "Child Display")

    def test_calculator_add(self):
        calc = Calculator()
        self.assertEqual(calc.add(3), 6)
        self.assertEqual(calc.add(3, 4), 7)
    def setUp(self):
        """
        Set up common objects for the tests.
        """
        self.calculator = Calculator()
        self.child = Child()
        self.parent = Parent()

    # Existing tests (leave unchanged)
    def test_calculator_add(self):
        self.assertEqual(self.calculator.add(2, 3), 5)
        self.assertEqual(self.calculator.add(-1, 1), 0)

    def test_child_display(self):
        self.assertEqual(self.child.display(), "Child method called")

    def test_parent_process(self):
        self.assertEqual(self.parent.process(), "Parent process")

    # New tests to kill mutants
    def test_calculator_add_negative(self):
        """
        Test the add method with negative numbers.
        This should catch issues like incorrect operations in the mutated add method.
        """
        self.assertEqual(self.calculator.add(-5, -3), -8)
        self.assertEqual(self.calculator.add(-10, 5), -5)

    def test_child_inherited_method(self):
        """
        Test inherited methods to ensure parent-child relationships are intact.
        This will help catch mutations that modify parent methods or relationships.
        """
        self.assertTrue(self.child.is_inherited())
        self.assertEqual(self.child.display(), "Child method called")
        self.assertEqual(self.parent.display(), "Parent method called")

    def test_overloading_behavior(self):
        """
        Test method overloading scenarios to ensure proper behavior of overloaded methods.
        This targets mutations affecting overloaded method calls.
        """
        self.assertEqual(self.child.overloaded_method(5), "Method with one argument")
        self.assertEqual(
            self.child.overloaded_method(5, 10), "Method with two arguments"
        )

    def test_type_casting(self):
        """
        Test type casting logic to identify mutations in type conversions or cast operators.
        """
        self.assertEqual(self.child.cast_type(5), "Integer cast successful")
        self.assertEqual(self.child.cast_type("test"), "String cast successful")
        with self.assertRaises(TypeError):
            self.child.cast_type(5.5)  # Invalid type for casting

    def test_reference_assignment(self):
        """
        Test reference assignment changes for catching reference mutations.
        """
        new_child = Child()
        self.child.reference_assignment(new_child)
        self.assertEqual(self.child.reference, new_child)
        self.assertNotEqual(self.child.reference, None)


# Initialize and run the framework
framework = MutationTestingFramework(original_objects, mutation_operators, TestFramework)
framework.calculate_mutation_score()
