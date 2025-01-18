import unittest

class StringManipulator:
    def concatenate(self, str1, str2):
        return str1 + str2

    def concatenate(self, str1):
        return str1 * 2

# Test cases for StringManipulator
class TestStringManipulator(unittest.TestCase):
    def setUp(self):
        self.manipulator = StringManipulator()

    def test_concatenate_two_strings(self):
        self.assertEqual(self.manipulator.concatenate("Hello, ", "World!"), "Hello, World!")  # Original call
        self.assertEqual(self.manipulator.concatenate("World!", "Hello, "), "World!Hello, ")  # Changed argument order

    def test_concatenate_one_string(self):
        self.assertEqual(self.manipulator.concatenate("Hello"), "HelloHello")  # Original call
        self.assertEqual(self.manipulator.concatenate("World"), "WorldWorld")  # New call with different argument

    def test_concatenate_no_arguments(self):
        with self.assertRaises(TypeError):
            self.manipulator.concatenate()  # Should raise TypeError

# Running the tests
if __name__ == '__main__':
    unittest.main()
