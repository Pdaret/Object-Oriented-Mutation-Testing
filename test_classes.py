import unittest


class Parent:
    def __init__(self):
        self.data = "Parent Data"
    
    def display(self):
        return "Parent Display"
    
    def process(self):
        return "Processed by Parent"


class Child(Parent):
    def __init__(self):
        super().__init__()
        self.data = "Child Data"
    
    def display(self):
        return "Child Display"
    
    def process(self):
        return "Processed by Child"


class Calculator:
    def add(self, a, b=None):
        if b is not None:
            return a + b  # Overloaded for two arguments
        return a + a  # Single argument (default behavior)
    

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
