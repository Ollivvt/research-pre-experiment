import os

root_directory = r"\\205.233.161.11\ai-primary3\AIRM\BCWomen\BDenStorage\Diagnostic\20130116\20190906_7cpdmf\20130116_MG Diagnostic RT"

# Test access to the network directory
for dirpath, _, filenames in os.walk(root_directory):
    for file in filenames:
        print(f"Found file: {file}")
    break  # Just to print the first directory's contents