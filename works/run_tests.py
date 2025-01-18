import subprocess
import tempfile
import os
import shutil

def run_mutated_tests(mutated_code):
    # Create a temporary directory to store the mutated code
    temp_dir = tempfile.mkdtemp(dir=os.getcwd())  # Ensure the temp directory is on the same drive
    try:
        # Write the mutated code to a temporary file
        mutated_file_path = os.path.join(temp_dir, "mutated_code.py")
        with open(mutated_file_path, "w") as f:
            f.write(mutated_code)

        # Run the tests in the mutated code file
        result = subprocess.run(
            ["python", "-m", "unittest", "-v", mutated_file_path],
            capture_output=True,
            text=True
        )
        # Check for failed tests
        passed = "OK" in result.stderr
        failed_tests = "FAILED" in result.stderr

        return {
            "passed": passed,
            "failed_tests": failed_tests,
            "output": result.stdout,
            "error": result.stderr
        }
    finally:
        # Clean up the temporary directory
        shutil.rmtree(temp_dir)

def calculate_mutation_score(original_code, mutated_codes):
    # Run original code tests to ensure they pass
    original_test_result = run_mutated_tests(original_code)
    if not original_test_result["passed"]:
        print("Original test cases failed. Fix the tests before proceeding.")
        return None

    # Run tests for each mutation and track results
    detected_mutations = 0
    total_mutations = len(mutated_codes)

    for index, mutated_code in enumerate(mutated_codes, start=1):
        print(f"Running tests for mutation {index}/{total_mutations}...")
        result = run_mutated_tests(mutated_code)
        print(result)
        if result["failed_tests"]:
            detected_mutations += 1
            print(f"Mutation {index} detected by tests.")
        else:
            print(f"Mutation {index} was NOT detected by tests.")

        # Print the test output for debugging
        print(result["output"])

    # Calculate mutation score
    mutation_score = (detected_mutations / total_mutations) * 100
    print(f"\nMutation Score: {mutation_score:.2f}% ({detected_mutations}/{total_mutations} mutations detected)")
    return mutation_score