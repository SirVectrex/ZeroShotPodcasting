import matplotlib
matplotlib.use('Agg')  # Headless-safe backend

import json
import pandas as pd
import matplotlib.pyplot as plt

# Load JSON
with open("scripts/model_scores.json", "r") as f:
    results = json.load(f)

# Load CSV
df_models = pd.read_csv("scripts/scripts_utf8.csv", sep=";")

data = []
for item in results:
    index = item["index"]
    score = item["score"]
    model = df_models.loc[index, "Model"]
    data.append({"Model": model, "Score": score})

df = pd.DataFrame(data)

# Prepare data for boxplot
models = df["Model"].unique()
data_by_model = [df[df["Model"] == model]["Score"] for model in models]

# Create plot
plt.figure(figsize=(7, 6))
box = plt.boxplot(data_by_model, patch_artist=True)

# Color each box
colors = plt.cm.Set3.colors
for patch, color in zip(box["boxes"], colors):
    patch.set_facecolor(color)

# Customize plot
plt.xticks(ticks=range(1, len(models) + 1), labels=models, rotation=90)
plt.ylabel("GEval Score")
plt.title("GEval Scores per Model on same prompt")
plt.grid(axis='y', linestyle=':', alpha=0.7)
plt.tight_layout()

# Save and close
plt.savefig("SVGs/model_scores_boxplot.svg", format="svg")
plt.close()
