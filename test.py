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
    

def MakeSound(parent_instance: Beast):
    return parent_instance.make_sound()

class TestFramework(unittest.TestCase):
    # Test function with parameter of type Parent
    def test_make_sound(self):
        self.assertEqual(MakeSound(Beast()), "Some generic animal sound")

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFramework)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)