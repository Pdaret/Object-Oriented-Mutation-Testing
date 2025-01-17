from test_classes import *

# Mutation Operator Implementations
def new_method_call_with_child_class(parent_obj):
    child_obj = Child()
    return child_obj.process()


def member_variable_with_parent_type(child_obj):
    parent_obj = Parent()  # Declare as parent type
    return parent_obj.data


def process_object_with_child_type(child_obj: Child):
    return child_obj.display()


def overloading_method_contents_replace(calc_obj, a, b=None):
    if b is not None:
        return a * b  # Mutation: Replace addition with multiplication
    return a * a  # Replace addition with multiplication for single argument