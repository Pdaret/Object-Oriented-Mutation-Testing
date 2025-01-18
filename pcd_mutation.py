import ast
import astor

class PCDVisitor(ast.NodeTransformer):
    def visit_Call(self, node):
        # Check if the function call has a type cast
        if isinstance(node.func, ast.Name):
            # Check if it's a type cast expression
            if len(node.args) == 1 and isinstance(node.args[0], ast.Call):
                # Remove the type cast by replacing it with the original function call
                return node.args[0]  # Assuming node.args[0] is the original call without cast
        return self.generic_visit(node)

def mutate_code(source_code):
    # Parse the source code into an AST
    tree = ast.parse(source_code)
    
    # Create a visitor for removing type casts
    visitor = PCDVisitor()
    
    # Apply the mutation
    mutated_tree = visitor.visit(tree)

    # Convert back to source code
    mutated_code = astor.to_source(mutated_tree)
    
    return mutated_code

# Input code as a string (example with a type cast)
input_code = """
class Parent:
    def display(self):
        return "Parent Display"

class Child(Parent):
    def display(self):
        return "Child Display"

# Test function
def test_display():
    parent_instance = Parent()
    child_instance = Child()
    
    # Original call with type cast
    print(Child(parent_instance).display())
"""

# Mutate by removing type casts using PCD operator
mutated_code = mutate_code(input_code)
print("Original Code:\n", input_code)
print("Mutated Code:\n", mutated_code)
