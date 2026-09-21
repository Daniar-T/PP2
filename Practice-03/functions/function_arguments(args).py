def my_function(*args):
    # *args allows the function to receive any number of positional arguments.
    # Python collects all the arguments into a tuple called args.

    print("Type:", type(args))
    # The type of args is a tuple.

    print("First argument:", args[0])
    # args[0] is the first argument.
    # Tuple indexes start counting from 0.

    print("Second argument:", args[1])
    # args[1] is the second argument.

    print("All arguments:", args)
    # This prints the complete tuple of arguments.


# These three positional arguments are collected into the args tuple:
# args = ("Emil", "Tobias", "Linus")
my_function("Emil", "Tobias", "Linus")