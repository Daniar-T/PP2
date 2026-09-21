def my_function(**kid):
    # **kid allows the function to accept any number of keyword arguments.
    # The keyword arguments are collected into a dictionary named kid.

    print("His last name is " + kid["lname"])
    # "lname" is the dictionary key.
    # "Refsnes" is the value stored for that key.
    # Therefore, kid["lname"] returns "Refsnes".


# The keyword arguments are collected like this:
# kid = {
#     "fname": "Tobias",
#     "lname": "Refsnes"
# }
my_function(fname="Tobias", lname="Refsnes")
