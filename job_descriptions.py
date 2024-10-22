# Used for learning about dataset
import pandas as pd

# Load the dataset
df = pd.read_csv('job_descriptions.csv')

# Display the first few rows to get an overview

with open('sample_jobs.txt', 'w') as f:
    f.write(df.head().to_string())
# Check for missing values
print(df.isnull().sum())

# Print the number of rows in the DataFrame
print("Number of rows:", len(df))

