
       


port = "HLB18_MAIN.path_to_net_port"
pin = "HLB18_MAIN.path_to_net_pin.hierarchy_to_cell.name_of_pin.pin"

path_list = [port, pin]
for p in path_list:
       print(processPATH(p))