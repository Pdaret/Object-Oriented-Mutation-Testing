import unittest
from copy import deepcopy


class MutationTestingFramework:
    def __init__(self, original_objects, mutation_operators, test_case):
        """
        Initialize the mutation testing framework.

        :param original_objects: List of original objects (classes/instances).
        :param mutation_operators: List of mutation operator functions.
        :param test_case: The unittest Class containing test cases.
        """
        self.original_objects = original_objects
        self.mutation_operators = mutation_operators

        # Validate and initialize the test suite
        # if not isinstance(test_case, unittest.TestCase):
        #     raise ValueError("test_suite must be a unittest.TestSuite object.")
        self.test_case = test_case

        self.killed_mutants = 0
        self.total_mutants = 0

    def apply_mutation(self, mutation_operator, obj):
        """
        Apply a mutation operator to an object.

        :param mutation_operator: The mutation operator function.
        :param obj: The object to mutate.
        :return: The mutated object.
        """
        mutated_obj = deepcopy(obj)  # Ensure the original object remains intact
        mutated_obj = mutation_operator(mutated_obj)

        # Verification Step: Compare mutated and original object
        if mutated_obj == obj:
            print("Warning: Mutation operator did not change the object.")
        else:
            print(f"Mutation successfully applied by {mutation_operator.__name__}.")
        
        print("Original Object:", obj)
        print("Mutated Object:", mutated_obj)
        
        return mutated_obj

    def run_tests(self, mutated_objects=None):
        """
        Run the test suite on the provided objects.

        :param mutated_objects: List of mutated objects (optional).
        :return: True if all tests pass, False if any test fails.
        """

        if mutated_objects:
            # Replace original objects with mutated ones for testing
            for i, obj in enumerate(self.original_objects):
                self.original_objects[i] = mutated_objects[i]

        # Create test suite using TestLoader
        loader = unittest.TestLoader()
        test_suite = unittest.TestSuite(loader.loadTestsFromTestCase(self.test_case))
        
        # Run the test suite
        result = unittest.TextTestRunner(verbosity=2).run(test_suite)
        return result.wasSuccessful()

    def calculate_mutation_score(self):
        """
        Perform mutation testing and calculate the mutation score.
        """
        # Step 1: Run tests on original objects to ensure they pass
        if not self.run_tests():
            print("Original code failed the test suite. Fix tests before proceeding.")
            return

        print("Original code passed all tests.")

        # Step 2: Apply mutations and run tests
        for mutation_operator in self.mutation_operators:
            mutated_objects = [
                self.apply_mutation(mutation_operator, obj) for obj in self.original_objects
            ]
            self.total_mutants += 1

            # Step 3: Run tests on mutated objects
            if not self.run_tests(mutated_objects):
                print(f"Mutation killed by operator: {mutation_operator.__name__}")
                self.killed_mutants += 1
            else:
                print(f"Mutation survived by operator: {mutation_operator.__name__}")

        # Step 4: Calculate mutation score
        mutation_score = (self.killed_mutants / self.total_mutants) * 100
        print(f"\nMutation Score: {mutation_score:.2f}%")
