import ast
import astor

class PMDVisitor(ast.NodeTransformer):
    def __init__(self):
        self.class_hierarchy = {}

    def visit_ClassDef(self, node):
        print(f"Visiting ClassDef: {node.name}")
        # If the class has a parent, record the relationship
        if node.bases:
            parent_class_name = node.bases[0].id if isinstance(node.bases[0], ast.Name) else None
            if parent_class_name:
                self.class_hierarchy[node.name] = parent_class_name
        return self.generic_visit(node)

    def visit_Call(self, node):
        print(f"Visiting Call: {ast.dump(node)}")
        # Check if the call is to any class constructor
        if isinstance(node.func, ast.Name):
            # If the class being called is a child class, replace it with the parent class
            if node.func.id in self.class_hierarchy:
                node.func.id = self.class_hierarchy[node.func.id]
                print(f"Changed call to: {node.func.id}")
        return self.generic_visit(node)

def mutate_code(source_code):
    # Parse the source code into an AST
    tree = ast.parse(source_code)

    # Create a visitor to track class hierarchy and mutate calls
    visitor = PMDVisitor()

    # First pass: visit all classes to build the hierarchy
    visitor.visit(tree)

    # Second pass: mutate the code based on the detected hierarchy
    mutated_tree = visitor.visit(tree)

    # Convert back to source code
    mutated_code = astor.to_source(mutated_tree)

    return mutated_code

input_code = """
import unittest

class Animal:
    def make_sound(self):
        return "Some generic animal sound"

class Dog(Animal):
    def make_sound(self):
        return "Woof!"

class Cat(Animal):
    def make_sound(self):
        return "Meow!"

class Bird(Animal):
    def make_sound(self):
        return "Chirp!"

class Person:
    def __init__(self, name):
        self.name = name
        self.pet = None

    def adopt_pet(self, pet):
        self.pet = pet

    def make_pet_sound(self):
        if self.pet:
            return self.pet.make_sound()
        else:
            return "No pet adopted"

class TestFramework(unittest.TestCase):
    # Test functions
    def test_sounds(self):
        # dog = Dog()
        # cat = Cat()
        bird = Bird()

        # person1 = Person("Alice")
        # person1.adopt_pet(dog)
        # person2 = Person("Bob")
        # person2.adopt_pet(cat)
        person3 = Person("Charlie")
        person3.adopt_pet(bird)

        # print(person1.make_pet_sound())  # Should print "Woof!"
        # print(person2.make_pet_sound())  # Should print "Meow!"
        self.assertEqual(person3.make_pet_sound(), "Chirp!")
        # print(person3.make_pet_sound())  # Should print "Chirp!"

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFramework)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
"""

# Mutate by automatically changing Child instance to Parent instance using PMD operator
mutated_code = mutate_code(input_code)


from run_tests import calculate_mutation_score

calculate_mutation_score(input_code, mutated_codes=[mutated_code])
