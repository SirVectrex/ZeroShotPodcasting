import matplotlib.pyplot as plt
import numpy as np

# Data: Min and Max Age Ranges per Model
data = {
    "Gemini Flash V2.5": [7, 12],
    "Deepseek R1": [5, 7],
    "Deepseek V3": [5, 11],
    "GROK 3": [5, 9],
    "GROK 3 Mini": [5, 10],
    "Claude 3.7 Sonnet": [9, 13],
    "GPT o4 Mini": [7, 14],
    "GPT 4O Mini": [6, 11],
    "Mistral Medium": [9, 12]
}
# Extract the models, min and max values
models = list(data.keys())
min_ages = [age_range[0] for age_range in data.values()]
max_ages = [age_range[1] for age_range in data.values()]

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))


for i, model in enumerate(models):
    ax.plot([i, i], [min_ages[i], max_ages[i]], marker='o', color='blue', markersize=8, label='_nolegend_' if i > 0 else 'Min-Max Range')

# Plot dotted red reference lines at ages 8 and 12
ax.axhline(y=8, color='red', linestyle='--', label="Age 8")
ax.axhline(y=12, color='red', linestyle='--', label="Age 12")

# Set labels and title
ax.set_ylabel('Age')
ax.set_xlabel('Model')
ax.set_title('Min to Max Age Ranges per Model with Reference Ages')

# Set x-ticks (models) and adjust x-axis
ax.set_xticks(np.arange(len(models)))
ax.set_xticklabels(models, rotation=45, ha="right")


ax.legend(loc='upper left')
fig.tight_layout()

# Save the plot as an SVG file
plt.savefig('SVGs/min_max_age_per_model_range_with_references.svg', bbox_inches='tight', format='svg')

plt.show()