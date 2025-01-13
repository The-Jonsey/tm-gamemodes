import os
import re

# Get the current date from environment variables (set by GitHub Action)
current_date = os.getenv("CURRENT_DATE")

# Define the pattern to match lines with #Const Version
version_pattern = r'#Const\s+Version\s+"(\d{4}-\d{2}-\d{2})(\+(\d+))?"'

# Function to update the version in the file
def update_version_in_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Loop through lines to find and update version
    updated_lines = []
    for line in lines:
        match = re.search(version_pattern, line)
        if match:
            old_date = match.group(1)
            old_increment = match.group(3) if match.group(3) else '1'
            if old_date == current_date:
                # Increment the number after '+'
                new_line = line.replace(f'+{old_increment}"', f'+{int(old_increment) + 1}"')
            else:
                # Set new date and reset the increment to 1
                new_line = line.replace(old_date, current_date).replace(f'+{old_increment}"', '+1"')
            updated_lines.append(new_line)
        else:
            updated_lines.append(line)

    # Write the updated lines back to the file
    with open(file_path, "w") as file:
        file.writelines(updated_lines)

# Iterate over all modified .Script.txt files and update them
modified_files = os.getenv('MODIFIED_FILES').splitlines()
for file_path in modified_files:
    if file_path.endswith('.Script.txt'):
        update_version_in_file(file_path)
