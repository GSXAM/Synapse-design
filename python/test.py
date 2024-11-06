def gen_starECO(csv_file_path, output_folder=".", design="DESIGN_NAME"):
    """
    Reads a CSV file and generates StarECO file commands.

    Args:
        csv_file_path (str)     : Path to the CSV file.
        output_folder (str)     : Path to the output folder where SGDC files will be saved.
        design (str)            : Design name (Ex: "HLB18_MAIN", default is "DESIGN_NAME")

    Return:
        starECO_file_path (str) : Path to the StarECO file.
    """

    # Add code to processing csv file
    starECO_file_path = f"{output_folder}/{design}_star_scr_gen.tcl"
    writelist = ['##############################\n', \
                '#         COMMON             #\n', \
                '##############################\n', \
                'add_instance SNIDFT_MBIST_OR_SCAN -reference ${ma_stdor}\n', \
                'add_connection -from SNIDFT_mbist_mode -to SNIDFT_MBIST_OR_SCAN/A1\n', \
                'add_connection -from SNIDFT_scan_mode -to SNIDFT_MBIST_OR_SCAN/A2\n\n']
    starECO_writer = open(starECO_file_path, 'w')
    starECO_writer.writelines(writelist)
    csvfile = open(csv_file_path, 'r')
    csvload = csv.reader(csvfile, delimiter=',')
    next(csvload) # ignore first title row
    MasterRST_cnt = 0
    MasterRST_ECO_flag = 0
    MasterRST_row = 0
    eco_clock_mux_list = ['set eco_clock_mux_list {\\\n']
    eco_reset_mux_output_internal_list_1 = ['set eco_reset_mux_output_internal_list_1 {\\\n']
    eco_reset_mux_output_internal_list_0 = ['set eco_reset_mux_output_internal_list_0 {\\\n']
    eco_reset_mux_input_internal_list_1 = ['set eco_reset_mux_input_internal_list_1 {\\\n']
    eco_reset_mux_input_internal_list_0 = ['set eco_reset_mux_input_internal_list_0 {\\\n']
    eco_reset_mux_input_external_list_1 = ['set eco_reset_mux_input_external_list_1 {\\\n']
    eco_reset_mux_input_external_list_0 = ['set eco_reset_mux_input_external_list_0 {\\\n']
    # Count specified MasterRST ports
    for row in csvload:
        if (row[0].isnumeric()):    # Check No. col is number
            if (row[2] == "reset"): # Check Type col
                if (row[6] == "x"): # Check MasterReset
                    MasterRST_row = row
                    MasterRST_cnt += 1
                else:
                    print(f'Info: Ignore row: {" | ".join(map(str, row))}')
            else:
                print(f'Info: Ignore row: {" | ".join(map(str, row))}')
        else:
            print(f'Info: Ignore row: {" | ".join(map(str, row))}')
    # Check if there have MasterRST port, only 1 port is MasterRST and value of this port should be 1
    if (MasterRST_cnt == 0):
        print("Infor: No MasterRST was specified")
        MasterRST_ECO_flag = 0
    elif (MasterRST_cnt > 1):
        print("Error: Too many MasterRST ports were assigned")
        return False
    elif (MasterRST_cnt == 1):
        if (MasterRST_row[3] == 0):
            print("Warning: MasterRST port should be inactive with value 1 (Current value is 0)")
        else:
            MasterRST_ECO_flag = 1
            print("Info: MasterRST port have value 1")
    # Starting ECO
    for row in csvload:
        if (row[0].isnumeric()):    # Check No. col is number
            if (row[5] == "x"):     # Check do ECO
                if (row[2] == 'clock'):     # If ECO for clock
                    if (row[4] == 'output'):    # Check clock direction
                        pkg = convertPATH(row[1])
                        if (pkg[0] == False):
                            print('>>>>>>>> Python script had interrupted!')
                        elif (pkg[1] == 'port'):
                            print(f'Warning: Cannot ECO for clock port. Ignore row: {" | ".join(map(str, row))}')
                        elif (pkg[1] == 'pin'):
                            eco_clock_mux_list.append(f'{pkg[2]} \\\n')
                        else:
                            print(f'Error: occured at {" | ".join(map(str, row))}')
                    elif (row[4] == 'input'):   # Ignore ECO input clock
                        print(f'Warning: Ignore ECO input clock at row: {" | ".join(map(str, row))}')
                    else:
                        print(f'Error: Unknow direction "{row[4]}" at row: {" | ".join(map(str, row))}')
                        return False
                elif (row[2] == 'reset'):   # If ECO for reset
                    if (row[4] == 'output'):    # Check reset direction
                        pkg = convertPATH(row[1])
                        if (pkg[0] == False):
                            print('>>>>>>>> Python script had interrupted!')
                        elif (pkg[1] == 'port'):
                            print(f'Warning: No ECO on output reset port. Ignore row: {" | ".join(map(str, row))}')
                        elif (pkg[1] == 'pin'):
                            if (row[3] == 1):   # Reset inactive at 1
                                eco_reset_mux_output_internal_list_1.append(f'{pkg[2]} \\\n')
                            else:   # Reset inactive at 0
                                eco_reset_mux_output_internal_list_0.append(f'{pkg[2]} \\\n')
                        else:
                            print(f'Error: occured at {" | ".join(map(str, row))}')
                    elif (row[4] == 'input'):   # Ignore ECO input clock
                        pkg = convertPATH(row[1])
                        if (pkg[0] == False):
                            print('>>>>>>>> Python script had interrupted!')
                        elif (pkg[1] == 'port'):
                            if (row[3] == 1):   # Reset inactive at 1
                                eco_reset_mux_input_external_list_1.append(f'{pkg[2]} \\\n')
                            else:   # Reset inactive at 0
                                eco_reset_mux_input_external_list_0.append(f'{pkg[2]} \\\n')
                        elif (pkg[1] == 'pin'):
                            if (row[3] == 1):   # Reset inactive at 1
                                eco_reset_mux_input_internal_list_1.append(f'{pkg[2]} \\\n')
                            else:   # Reset inactive at 0
                                eco_reset_mux_input_internal_list_0.append(f'{pkg[2]} \\\n')
                        else:
                            print(f'Error: occured at {" | ".join(map(str, row))}')
                    else:
                        print(f'Error: Unknow direction "{row[4]}" at row: {" | ".join(map(str, row))}')
                        return False
                elif (row[2] == 'constraint'):  # If ECO for constraint value
                    #
                    print('>>>>>>>>> Python code is continued here...')
                else:
                    print(f'Error: Unknow type "{row[2]}" at row: {" | ".join(map(str, row))}')
                    return False
            else:
                print(f'Info: Ignore row: {" | ".join(map(str, row))}')
        else:
            print(f'Info: Ignore row: {" | ".join(map(str, row))}')

    # Filter row following type: reset, clock, constraint
    filter_resets = []
    filter_clocks = []
    filter_constraints = []
    # Get filter resets
    for row in csvload:
        if (row[0].isnumeric()):    # Check No. col is number
            if (row[2] == "reset"): # Check Type col
                if (row[6] == "x"): # Check MasterReset
                    MasterRST_row = row
                    MasterRST_cnt += 1
                else:
                    print(f'Info: Ignore row: {" | ".join(map(str, row))}')
            else:
                print(f'Info: Ignore row: {" | ".join(map(str, row))}')
        else:
            print(f'Info: Ignore row: {" | ".join(map(str, row))}')

    csvfile.close()
    starECO_writer.close()
    return starECO_file_path