class Parent:
    def __init__(self):
        self.data = "Parent Data"
    
    def display(self):
        return "Parent Display"
    
    def process(self):
        return "Processed by Parent"


class Child(Parent):
    def __init__(self):
        super().__init__()
        self.data = "Child Data"
    
    def display(self):
        return "Child Display"
    
    def process(self):
        return "Processed by Child"


class Calculator:
    def add(self, a, b=None):
        if b is not None:
            return a + b  # Overloaded for two arguments
        return a + a  # Single argument (default behavior)