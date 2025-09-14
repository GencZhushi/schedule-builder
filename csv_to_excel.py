import pandas as pd

# Read the CSV file
df = pd.read_csv('sample_lectures.csv')

# Convert to Excel
df.to_excel('sample_lectures.xlsx', index=False)

print("Excel file 'sample_lectures.xlsx' has been created successfully!")