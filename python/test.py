import os
def check_number(variable):
    if variable.isnumeric():
        print(f"{variable} is a number.")
    else:
        print(f"{variable} is not a number.")

# Example usage
check_number("123.45")  # Output: 123.45 is a number.
check_number("")   # Output: hello is not a number.


# if (os.path.isfile("ecolist.csv")):
#     os.remove("ecolist.csv")
# else:
file = open("data.txt", 'w')
file.write("hello\n")
file.write("12345\n")
file.write("lkhjg\n")
file.write("zxcvb\n")
