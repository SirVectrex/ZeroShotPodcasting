import matplotlib
matplotlib.use('Agg')

import pandas as pd
import matplotlib.pyplot as plt

# Load CSV 
df = pd.read_csv("scripts/Wordcount.csv", delimiter=";", header=0, names=["Model", "Wordcount"])

models = df["Model"].unique()
data = [df[df["Model"] == model]["Wordcount"] for model in models]

# Create and save boxplot
plt.figure(figsize=(7, 6))
box = plt.boxplot(data, patch_artist=True)

# Set colors
colors = plt.cm.Set3.colors
for patch, color in zip(box["boxes"], colors):
    patch.set_facecolor(color)

# Add horizontal target line
plt.axhline(y=240, color='red', linestyle='--', linewidth=2, label='Target (240 words)')

# Customize axes
plt.xticks(ticks=range(1, len(models) + 1), labels=models, rotation=90)
plt.ylabel("Word Count")
plt.title("Word Counts per Model on same prompt - Target 240")
plt.grid(axis='y', linestyle=':', alpha=0.7)
plt.legend(loc="upper left", frameon=True)

# Save and close
plt.tight_layout()
plt.savefig("SVGs/model_wordcounts_boxplot.svg", format="svg")
plt.close()
