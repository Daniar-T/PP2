def my_function(name = "friend"):
  print("Hello", name)

my_function("Emil")                 # Uses the provided argument
my_function("Tobias")               # Uses the provided argument
my_function()                       # Uses the default value: "friend"
my_function("Linus")                # Uses the provided argument