import ast
import astor

class PRVVisitor(ast.NodeTransformer):
    def __init__(self, original_type, new_type):
        self.original_type = original_type
        self.new_type = new_type

    def visit_Assign(self, node):
        # Iterate through all targets of the assignment
        for target in node.targets:
            if isinstance(target, ast.Name):
                # Check if the assigned value is of the original type
                if isinstance(node.value, ast.Str) and self.original_type == 'String':
                    # Change assignment to a new compatible type (e.g., from String to Integer)
                    node.value = ast.Num(n=42)  # Example: Assigning an integer instead of a string
                elif isinstance(node.value, ast.Num) and self.original_type == 'Integer':
                    # Change assignment from Integer to String
                    node.value = ast.Str(s="Hello")  # Example: Assigning a string instead of an integer
        return node

def mutate_code(source_code, original_type, new_type):
    # Parse the source code into an AST
    tree = ast.parse(source_code)
    
    # Create a visitor for changing reference assignments
    visitor = PRVVisitor(original_type, new_type)
    
    # Apply the mutation
    mutated_tree = visitor.visit(tree)

    # Convert back to source code
    mutated_code = astor.to_source(mutated_tree)
    
    return mutated_code

# Input code as a string (example with variable assignments)
input_code = """
def test_assignment():
    obj = "Hello"  # Original assignment with String
    print(obj)

def test_integer_assignment():
    num = 4  # Original assignment with Integer
    print(num)
"""

# Mutate by changing String assignment to Integer using PRV operator
mutated_code_string_to_integer = mutate_code(input_code, 'String', 'Integer')
print("Original Code:\n", input_code)
print("Mutated Code (String to Integer):\n", mutated_code_string_to_integer)

# Mutate by changing Integer assignment to String using PRV operator
mutated_code_integer_to_string = mutate_code(input_code, 'Integer', 'String')
print("Mutated Code (Integer to String):\n", mutated_code_integer_to_string)
