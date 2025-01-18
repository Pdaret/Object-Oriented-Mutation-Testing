from test_classes import *

def new_method_call_with_child_class(obj):
    obj.process = lambda: "Processed by Child (Mutated)"
    return obj

def member_variable_with_parent_type(obj):
    obj.data = "Parent Data (Mutated)"
    return obj

def process_object_with_child_type(obj):
    obj.display = lambda: "Child Display (Mutated)"
    return obj

def overloading_method_contents_replace(obj):
    obj.add = lambda a, b=None: a * b if b else a * a
    return obj