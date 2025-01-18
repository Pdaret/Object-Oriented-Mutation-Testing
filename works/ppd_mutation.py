import ast
import astor

class PPDVisitor(ast.NodeTransformer):
    def __init__(self):
        self.class_hierarchy = {}

    def visit_ClassDef(self, node):
        print(f"Visiting ClassDef: {node.name}")
        # Record all parent classes for each child class
        for base in node.bases:
            if isinstance(base, ast.Name):
                # Ensure we record the correct child-to-parent mapping
                self.class_hierarchy[node.name] = base.id
        return self.generic_visit(node)

    def visit_FunctionDef(self, node):
        print(f"Visiting FunctionDef: {node.name}")
        if node.name.startswith('test_'):
            for arg in node.args.args:
                if isinstance(arg.annotation, ast.Name):
                    print(f"Original annotation: {arg.annotation.id}")
                    # Check if the argument annotation matches the parent class
                    if arg.annotation.id in self.class_hierarchy.values():
                        # Find the corresponding child class
                        child_class = next(key for key, value in self.class_hierarchy.items() if value == arg.annotation.id)
                        # Change the argument's annotation to the child class type
                        arg.annotation.id = child_class
                        print(f"Changed annotation to: {arg.annotation.id}")
        return self.generic_visit(node)

def mutate_code(source_code):
    # Parse the source code into an AST
    tree = ast.parse(source_code)

    # Create a visitor for changing parameter variable declarations
    visitor = PPDVisitor()

    # Apply the mutation
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
    def test_display(parent_instance: Beast):
        print(parent_instance.display())

if __name__ == "__main__":
    unittest.main()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
"""

# Mutate the code
mutated_code = mutate_code(input_code)


from run_tests import calculate_mutation_score

calculate_mutation_score(input_code, mutated_codes=[mutated_code])
