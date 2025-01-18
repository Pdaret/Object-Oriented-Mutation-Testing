import ast
import astor
import unittest


class OACVisitor(ast.NodeTransformer):
    def __init__(self):
        super().__init__()
        self.overloaded_methods = {}
        self.new_assertions = []

    def visit_FunctionDef(self, node):
        # Track overloaded methods by their names
        if node.name not in self.overloaded_methods:
            self.overloaded_methods[node.name] = []
        self.overloaded_methods[node.name].append(node)
        return self.generic_visit(node)

    def visit_Call(self, node):
        # Check if the function call is an overloaded method
        if isinstance(node.func, ast.Attribute):
            method_name = node.func.attr
            if method_name in self.overloaded_methods:
                # Mutate arguments (e.g., reverse first two arguments if applicable)
                if len(node.args) >= 2:
                    reversed_call = ast.Call(
                        func=node.func,
                        args=[node.args[1], node.args[0], *node.args[2:]],
                        keywords=node.keywords,
                    )
                    self.new_assertions.append(
                        ast.parse(
                            f"self.assertEqual({astor.to_source(reversed_call).strip()}, {astor.to_source(node).strip()})"
                        ).body[0]
                    )

                # Generate test cases for fewer arguments
                if len(node.args) > 0:
                    for i in range(len(node.args)):
                        fewer_args_call = ast.Call(
                            func=node.func,
                            args=node.args[:i],
                            keywords=node.keywords,
                        )
                        self.new_assertions.append(
                            ast.parse(
                                f"self.assertRaises(TypeError, lambda: {astor.to_source(fewer_args_call).strip()})"
                            ).body[0]
                        )

                # Generate a test case for no arguments
                if len(node.args) == 0:
                    no_args_call = ast.Call(
                        func=node.func,
                        args=[],
                        keywords=node.keywords,
                    )
                    self.new_assertions.append(
                        ast.parse(
                            f"self.assertRaises(TypeError, lambda: {astor.to_source(no_args_call).strip()})"
                        ).body[0]
                    )

        return self.generic_visit(node)

    def add_new_assertions(self, test_case_body):
        # Append new assertions to the test case body
        test_case_body.extend(self.new_assertions)


def mutate_code(source_code):
    # Parse the source code into an AST
    tree = ast.parse(source_code)

    # Create a visitor to handle argument mutation and assertion generation
    visitor = OACVisitor()
    visitor.visit(tree)

    # Apply mutations to test methods
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for n in node.body:
                if isinstance(n, ast.FunctionDef) and n.name.startswith("test_"):
                    visitor.add_new_assertions(n.body)

    # Convert back to source code
    mutated_code = astor.to_source(tree)
    return mutated_code


# Example input code
input_code = """
class Calculator:
    def add(self, a, b):
        return a + b

    def add(self, a):
        return a + a

    def add(self):
        return 0

class StringManipulator:
    def concatenate(self, str1, str2):
        return str1 + str2

    def concatenate(self, str1):
        return str1 * 2

# Test cases for Calculator
class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_add(self):
        self.assertEqual(self.calc.add(3), 6)
        self.assertEqual(self.calc.add(3, 4), 7)

# Test cases for StringManipulator
class TestStringManipulator(unittest.TestCase):
    def setUp(self):
        self.manipulator = StringManipulator()

    def test_concatenate(self):
        self.assertEqual(self.manipulator.concatenate("Hello", " World"), "Hello World")
        self.assertEqual(self.manipulator.concatenate("Hello"), "HelloHello")

if __name__ == "__main__":
    unittest.main()
"""

# Mutate the code
mutated_code = mutate_code(input_code)

print("Original Code:\n", input_code)
print("\nMutated Code:\n", mutated_code)
