import os
import pandas as pd
import shutil

number_of_strands = 8
number_of_relabel = 2

# Define the Month to match digits
month_mapping = {
    "01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr",
    "05": "May", "06": "Jun", "07": "Jul", "08": "Aug",
    "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"
}

# Define the variables to substitute
variables = {
    'strand': 1,
    'month': 'Jan',
    'month_num': '01',
    'new_month': 'Feb',
    'new_month_num': '02',
    'start_day': '02',
    'end_day': '03',
}

variables_relabel = {
    'date_num': '010224',
    'RR': 1,
    'month': 'Jan',
    'start_day': '02',
}

# Function: Last Day checker
def is_last_day_of_month(date_str):
    date = pd.to_datetime(date_str, format="%m-%d-%Y")
    return date.is_month_end

def get_next_date(input_date_str):
    input_date = pd.to_datetime(input_date_str, format="%m-%d-%Y")
    if input_date.is_month_end:
        next_date = input_date + pd.Timedelta(days=1)
        return next_date.strftime("%m-%d-%Y")
    else:
        return input_date.strftime("%m-%d-%Y")

# Load batch file locations
batch_file_locations = {}
with open("Batch_File_Loc.txt", "r") as file:
    for line in file:
        key, value = line.strip().split(" = ")
        batch_file_locations[key] = value

# Ask for input parameters and update variables
Gib_Location_input = input("Provide folder location: ")
normalized_path = os.path.normpath(Gib_Location_input)
needed_information = normalized_path[-10:]
Month = needed_information[0:2]
Day = needed_information[3:5]
Year = needed_information[-2:]

# Changing dictionary: variables values
variables["month_num"] = Month
variables["month"] = month_mapping[Month]
variables["start_day"] = Day
variables_relabel["month"] = month_mapping[Month]
variables_relabel["start_day"] = Day
variables_relabel["date_num"] = Month + Day + Year

if is_last_day_of_month(needed_information):
    new_end_date = get_next_date(needed_information)
    variables['new_month_num'] = new_end_date[0:2]
    variables["new_month"] = month_mapping[variables["new_month_num"]]
    variables["end_day"] = "01"

# Make batch files for strands
with open("Looped_List.txt", "r") as file:
    looped_content = file.read()
    file.seek(0)
    strand_line_count = sum(1 for line in file)

for strand_count in range(1, number_of_strands + 1):
    variables['strand'] = strand_count
    line_looped_content = looped_content.splitlines()
    formatted_strings_looped_content = [template.format(**variables) for template in line_looped_content]

    filename = f"{strand_count}_reports.bat"
    with open(filename, "w") as file:
        for item in formatted_strings_looped_content:
            file.write(f"{item}\n")

    # Move the created file to the specified location for the strand
    target_directory = batch_file_locations[f"Strand {strand_count}"]
    shutil.move(filename, os.path.join(target_directory, filename))

# Make batch files for relabel
with open("Looped_List_Not.txt", "r") as file:
    looped_content_relabel = file.read()
    file.seek(0)
    relabel_line_count = sum(1 for line in file)

for relabel_count in range(1, number_of_relabel + 1):
    variables_relabel['RR'] = relabel_count
    line_looped_content = looped_content_relabel.splitlines()
    formatted_strings_looped_content = [template.format(**variables_relabel) for template in line_looped_content]

    filename = f"Relabel {relabel_count}_reports.bat"
    with open(filename, "w") as file:
        for item in formatted_strings_looped_content:
            file.write(f"{item}\n")

    # Move the created file to the specified location for the relabel
    target_directory = batch_file_locations[f"Relabel {relabel_count}"]
    shutil.move(filename, os.path.join(target_directory, filename))

expected_total_number_of_files = (number_of_strands*strand_line_count) + (number_of_relabel*relabel_line_count)

print("Batch files updated, please run them on FMPCS.")
print(f"You shoud expect {expected_total_number_of_files} total files.")