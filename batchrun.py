import mesa
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from OD_model.model import opinionsModel

params = {
    "N": range(10, 50, 10), # [10, 20, 30],  # Vary the number of agents
    "opinion_update_prob": [0.2, 0.5, 0.8],  # Vary the opinion update probability
}

results = mesa.batch_run(
    opinionsModel,
    parameters=params,
    iterations=10,  # Number of model runs per parameter combination
    max_steps=500,  # Maximum number of steps per model run
    display_progress=True,
)

results_df = pd.DataFrame(results)

# Optionally, save the data to a CSV file
results_df.to_csv("batch_results.csv", index=False)


# Plot the data using seaborn (or matplotlib)
sns.set(style="whitegrid")


# Example: Line plot for each value of 'N' with different colors for 'opinion_update_prob'
plt.figure(figsize=(10, 6))

pastel_colors = {0.2: "#FF9999", 0.5: "#99FF99", 0.8: "#9999FF"}
sns.lineplot(x="N", y="Step", hue="opinion_update_prob", data=results_df, marker="o", palette=pastel_colors)

# plt.title("Opinions Convergence Speed vs. Number of Agents (N) with Different Opinion Update Probabilities")
plt.xlabel("Number of Agents")
plt.ylabel("Opinions Convergence Speed")
plt.legend(title="Opinion Update Probability")
plt.show()
