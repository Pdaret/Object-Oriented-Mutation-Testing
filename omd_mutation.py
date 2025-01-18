import ast
import astor

class MutationVisitor(ast.NodeTransformer):
    def __init__(self, method_name):
        self.method_name = method_name
        self.method_count = 0

    def visit_FunctionDef(self, node):
        # Count methods with the same name
        if node.name == self.method_name:
            self.method_count += 1
            # If it's the second occurrence, delete it
            if self.method_count == 2:
                return None  # Remove this method
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

# Input code as a string (example with overloaded methods)
input_code = """
class Calculator:
    def add(self, a, b):
        return a + b  # Overloaded for two arguments

    def add(self, a):
        return a + a  # Single argument (default behavior)

    def subtract(self, a, b):
        return a - b  # Subtraction method
"""

# Mutate by deleting one of the 'add' methods using OMD operator
mutated_code = mutate_code(input_code, 'add')
print("Original Code:\n", input_code)
print("Mutated Code:\n", mutated_code)
