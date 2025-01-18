import ast
import astor

class PNCVisitor(ast.NodeTransformer):
    def __init__(self):
        self.class_hierarchy = {}

    def visit_ClassDef(self, node):
        print(f"Visiting ClassDef: {node.name}")
        # Record all parent classes for each child class
        for base in node.bases:
            if isinstance(base, ast.Name):
                # Ensure we record the correct child-to-parent mapping
                self.class_hierarchy[base.id] = node.name
                print(f"Recorded hierarchy: {base.id} -> {node.name}")
        return self.generic_visit(node)

    def visit_Call(self, node):
        print(f"Visiting Call: {ast.dump(node)}")
        # Check if the call is to create an instance of a parent class
        if isinstance(node.func, ast.Name) and node.func.id in self.class_hierarchy:
            # Replace with an instance of the child class
            node.func.id = self.class_hierarchy[node.func.id]
            print(f"Changed call to: {node.func.id}")
        return self.generic_visit(node)

def mutate_code(source_code):
    # Parse the source code into an AST
    tree = ast.parse(source_code)

    # Create a visitor for replacing parent class with child class
    visitor = PNCVisitor()

    # Apply the mutation by visiting the tree again
    mutated_tree = visitor.visit(tree)

    # Convert back to source code
    mutated_code = astor.to_source(mutated_tree)

    return mutated_code

# Input code as a string (example with Parent and Child classes)
input_code = """
import unittest

class Beast:
    def make_sound(self):
        return "Some generic animal sound"

class Animal(Beast):
    def make_sound(self):
        return "Woof!"

class Cat(Animal):
    def make_sound(self):
        return "Meow!"

class TestFramework(unittest.TestCase):
    # Test function with parameter of type Parent
    def test_make_sound(self):
        parent_instance = Beast()
        self.assertEqual(parent_instance.make_sound(), "Some generic animal sound")

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFramework)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
"""

# Mutate by changing Parent instance to Child instance using PNC operator
mutated_code = mutate_code(input_code)

from run_tests import calculate_mutation_score

calculate_mutation_score(input_code, mutated_codes=[mutated_code])
