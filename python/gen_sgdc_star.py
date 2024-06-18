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
            if (row[0].isnumeric()):
                if (row[2] == "reset"):
                    writelist.append(f'reset -async -name "{row[1]}"\n\ttest_mode -scanshift -value {row[3]} -name "{row[1]}"\n')
                elif (row[2] == "clock"):
                    if (row[3].isnumeric()):
                        writelist.append(f'clock -testclock -frequency {row[3]} -name "{row[1]}"\n')
                    else:
                        writelist.append(f'clock -testclock -name "{row[1]}"\n')
                elif (row[2] == "contraint"):
                    writelist.append(f'test_mode -value {row[3]} -name "{row[1]}"\n')
    
    sgdc_writer = open(sgdc_file_path, 'w')
    sgdc_writer.writelines(writelist)
    sgdc_writer.close()
    return sgdc_file_path


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
    starECO_file_path = f"{output_folder}/{design}_star_scr_gen.tcl"
    writelist = ['##############################\n', \
                '#         COMMON             #\n', \
                '##############################\n', \
                'add_instance SNIDFT_MBIST_OR_SCAN -reference ${ma_stdor}\n', \
                'add_connection -from SNIDFT_mbist_mode -to SNIDFT_MBIST_OR_SCAN/A1\n', \
                'add_connection -from SNIDFT_scan_mode -to SNIDFT_MBIST_OR_SCAN/A2\n\n']

    # Add code to processing csv file

    starECO_writer = open(starECO_file_path, 'w')
    starECO_writer.writelines(writelist)
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
sgdc_file_path = gen_sgdc(csv_file_path, output_folder_path, design_name)
starECO_file_path = gen_starECO(csv_file_path, output_folder_path, design_name)
