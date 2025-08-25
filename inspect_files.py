
import pandas as pd
import glob
import os

# Get all Excel files in the current directory
excel_files = glob.glob("*.xlsx")
print(f"Found {len(excel_files)} Excel files:")
for file in excel_files:
    print(f"  - {file}")
print("-"*70)

for file in excel_files:
    try:
        df = pd.read_excel(file)
        print(f"File: {file}")
        print(f"Columns: {df.columns.tolist()}")
        print(df.head())
        print("-"*50)
    except FileNotFoundError:
        print(f"File not found: {file}")
    except Exception as e:
        print(f"An error occurred with file {file}: {e}")
