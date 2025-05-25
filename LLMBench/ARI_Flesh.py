import pandas as pd
import json

# Example CSV path (replace with your actual CSV)
csv_file = "results_utf8.csv"

# Load the CSV file into a pandas DataFrame
df = pd.read_csv(csv_file, sep=";", encoding='ISO-8859-1')

# Clean the column names by stripping unwanted characters like BOM or extra spaces
df.columns = df.columns.str.strip().str.replace('ï»¿', '')

# Check the cleaned column names
print("Cleaned columns in the CSV:", df.columns)

# Group by model and calculate the min/max word count (age)
model_results = {}

for model in df["Model"].unique():
    model_data = df[df["Model"] == model]
    
    # Get the word counts for the current model
    word_counts = model_data["Wordcount"]
    
    # Calculate min and max word counts (ages)
    min_age = int(word_counts.min())  # Convert to native Python int
    max_age = int(word_counts.max())  # Convert to native Python int
    
    model_results[model] = {
        "min_age": min_age,
        "max_age": max_age
    }

# Save results to a JSON file
output_file = "model_age_range.json"
with open(output_file, 'w') as json_file:
    json.dump(model_results, json_file, indent=4)

# Optionally print the results (for verification)
print(json.dumps(model_results, indent=4))
