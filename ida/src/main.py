# pylint: disable=invalid-name, line-too-long, too-many-arguments, too-many-locals, too-few-public-methods

def example_function(arg1, arg2=None, *args, **kwargs):
    """Example function description."""

    # Some long code here to exceed 80 characters line limit.

    local_var = some_function()  # Use lowercase for imported functions if they are not classes.
    other_local_var = AnotherClass()  # Class names should be capitalized.

    # ... rest of function