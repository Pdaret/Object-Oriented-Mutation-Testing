import ast
import astor
import unittest

class MutationVisitor(ast.NodeTransformer):
    def __init__(self, method_name):
        self.method_name = method_name
        self.method_body = None

    def visit_FunctionDef(self, node):
        # Check if the function name matches the target method for mutation
        if node.name == self.method_name:
            # Save the body of the first method found
            if self.method_body is None:
                self.method_body = node.body
            else:
                # Replace the body of the current method with the saved body
                node.body = self.method_body
        return node

def mutate_code(source_code, method_name):
    # Parse the source code into an AST
    tree = ast.parse(source_code)
    
    # Create a mutation visitor for the specified method
    visitor = MutationVisitor(method_name)
    
    # Apply the mutation
    mutated_tree = visitor.visit(tree)
    
    # Convert back to source code
    mutated_code = astor.to_source(mutated_tree)
    
    return mutated_code

# Input code as a string
input_code = """
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
        self.calculator = Calculator()
        self.child = Child()
        self.parent = Parent()
"""

# Mutate the 'add' method using OMR operator
mutated_code = mutate_code(input_code, 'add')
print("Mutated Code:\n", mutated_code)
