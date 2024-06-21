"""
====================== USAGE ======================
    + Prepare a ecolist.xlsx file with fully informations about constraints and declarations.
    + Edit excel_file_path, sheet_names and output_folder
"""

import openpyxl
import csv
import os

def excel_to_csv(excel_file_path, sheet_name, output_folder="."):
    """
    Reads an Excel file and saves specified sheets as CSV files.

    Args:
        excel_file_path (str)   : Path to the Excel file.
        sheet_name (str)        : List of sheet names to save as CSV.
        output_folder (str)     : Path to the output folder where CSV files will be saved.
                                  (default output folder is current directory.)
    Return:
        csv_file_path (str)     : Path to the CSV file.
    """
    wb = openpyxl.load_workbook(excel_file_path, read_only=True, data_only=True)
    sheet = wb[sheet_name]
    csv_file_path = f"{output_folder}/{sheet_name}.csv"
    with open(csv_file_path, "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        for row in sheet.iter_rows():
            csv_writer.writerow([cell.value for cell in row])
    print(f">>>>>>>>>>>> {sheet_name} saved as: {csv_file_path}\n")
    return csv_file_path

def gen_sgdc(csv_file_path, output_folder=".", design="DESIGN_NAME"):
    """
    Reads a CSV file and generates SGDC file constraint.

    Args:
        csv_file_path (str)     : Path to the CSV file.
        output_folder (str)     : Path to the output folder where SGDC files will be saved.
        design (str)            : Design name (Ex: "HLB18_MAIN", default is "DESIGN_NAME")

    Return:
        sgdc_file_path (str)    : Path to the SGDC file.
    """
    sgdc_file_path = f"{output_folder}/{design}.sgdc"
    writelist = [f'current_design "{design}"\n\n']

    with open(csv_file_path, 'r') as csvfile:
        csvload = csv.reader(csvfile, delimiter=',')
        next(csvload) # ignore first title row
        for row in csvload:
            if (row[0].isnumeric()):    # Check No. col is number
                if (row[2] == "reset"): # Check Type col
                    writelist.append(f'reset -async -name "{row[1]}"\n\ttest_mode -scanshift -value {row[3]} -name "{row[1]}"\n')
                elif (row[2] == "clock"):
                    if (row[3].isnumeric()):    # Check Value col
                        writelist.append(f'clock -testclock -frequency {row[3]} -name "{row[1]}"\n')
                    else:
                        writelist.append(f'clock -testclock -name "{row[1]}"\n')
                elif (row[2] == "constraint"):
                    writelist.append(f'test_mode -value {row[3]} -name "{row[1]}"\n')
                else:
                    print(f'Error: Unknow type "{row[2]}" at row: {" | ".join(map(str, row))}')
                    return False
    
    sgdc_writer = open(sgdc_file_path, 'w')
    sgdc_writer.writelines(writelist)
    sgdc_writer.close()
    return sgdc_file_path

def convertPATH(sgdcPATH="top.stringPATH"):
       """
       Convert SGDC formatted hierarchical path to StarECO formatted path.
       Args:
              sgdcPATH (str): SGDC formatted path
       Return:
              status (bool) : True or False
              location (str): Port or pin
              starPATH (str): StarECO formatted path
       """
       hier = sgdcPATH.split('.')
       hier.pop(0)   # Remove block DESIGN name (Ex: "HLB10_MAIN")
       location = "unknow"
       starPATH = "unknow"
       if (hier.__len__() == 1):
              location = "port"
       elif (hier.__len__() > 1):
              if (hier[hier.__len__() - 1].__len__() <= 3):
                     location = "pin"
              else:
                     print(f'Error: "{sgdcPATH}" can be a NET. Cannot ECO to NET, the path must be pin or port.')
                     return [False, location, starPATH]
       else:
              print("Error: Path is invalid.")
              return [False, location, starPATH]
       starPATH = "/".join(map(str, hier))
       return [True, location, starPATH]

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

    csvfile.close()
    starECO_writer.close()
    return starECO_file_path

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#                   MAIN.py
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
excel_file_path = "ecolist.xlsx"
sheet_names_to_save = "ecolist"  # Add the desired sheet names
output_folder_path = "."  # Specify the output folder
design_name = "HLB18_MAIN"

csv_file_path = excel_to_csv(excel_file_path, sheet_names_to_save, output_folder_path)
# csv_file_path = "./ecolist.csv"
sgdc_file_path = gen_sgdc(csv_file_path, output_folder_path, design_name)
starECO_file_path = gen_starECO(csv_file_path, output_folder_path, design_name)
# os.remove(csv_file_path)
print(starECO_file_path)