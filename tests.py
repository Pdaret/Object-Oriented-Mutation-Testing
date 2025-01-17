from mutation_operators import *
import unittest

class TestMutationOperators(unittest.TestCase):

    def test_new_method_call_with_child_class(self):
        parent = Parent()
        self.assertEqual(parent.process(), "Processed by Parent")  # Original
        self.assertEqual(new_method_call_with_child_class(parent), "Processed by Child")  # Mutated

    def test_member_variable_with_parent_type(self):
        child = Child()
        self.assertEqual(child.data, "Child Data")  # Original
        self.assertEqual(member_variable_with_parent_type(child), "Parent Data")  # Mutated

    def test_process_object_with_child_type(self):
        parent = Parent()
        child = Child()
        self.assertEqual(parent.display(), "Parent Display")  # Original Parent
        self.assertEqual(child.display(), "Child Display")  # Original Child
        self.assertEqual(process_object_with_child_type(child), "Child Display")  # Mutated

    def test_overloading_method_contents_replace(self):
        calc = Calculator()
        self.assertEqual(calc.add(3), 6)  # Original: Single argument
        self.assertEqual(calc.add(3, 4), 7)  # Original: Two arguments
        self.assertEqual(overloading_method_contents_replace(calc, 3), 9)  # Mutated: Single argument
        self.assertEqual(overloading_method_contents_replace(calc, 3, 4), 12)  # Mutated: Two arguments

if __name__ == "__main__":
    unittest.main()