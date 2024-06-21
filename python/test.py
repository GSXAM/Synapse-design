def show_val(vals, name):
    print("Name:", name, "val:", vals[name])

vals = {'a': 1, 'b': 2}
show_val(vals, 'b')


my_variable = 42
print(list(globals().keys())[list(globals().values()).index(my_variable)])
print(list(globals().values()).index(my_variable))
