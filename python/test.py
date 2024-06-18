import os
# def check_number(variable):
#     if variable.isnumeric():
#         print(f"{variable} is a number.")
#     else:
#         print(f"{variable} is not a number.")

# # Example usage
# check_number("123.45")  # Output: 123.45 is a number.
# check_number("")   # Output: hello is not a number.


# if (os.path.isfile("ecolist.csv")):
#     os.remove("ecolist.csv")
# else:
writelist = ["1. initilized string\n"]

a = 199

cmd = f"2. second line\n"
writelist.append(cmd)
cmd = f"3. third line\n"
writelist.append(cmd)
cmd = f"4. fourth line\n"
writelist.append(cmd)
cmd = f"5. fiveth line: a={a}\n"
writelist.append(cmd)

cmd = ['##############################\n', \
       '#         COMMON             #\n', \
       '##############################\n', \
       'add_instance SNIDFT_MBIST_OR_SCAN -reference ${ma_stdor}\n', \
       'add_connection -from SNIDFT_mbist_mode -to SNIDFT_MBIST_OR_SCAN/A1\n', \
       'add_connection -from SNIDFT_scan_mode -to SNIDFT_MBIST_OR_SCAN/A2\n']
writelist.extend(cmd)
a = 299
cmd = f"changed. a={a}\n"
writelist.append(cmd)


file = open("data.txt", 'w')
print(writelist)
file.writelines(writelist)
file.close()