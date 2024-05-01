import mesa
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from OD_model.model import opinionsModel

params = {
    "N": 1000,  # Vary the number of agents
    # "inst_info": [-1, 0, 0.5, 1],  # Vary the institution information value
    "inst_info": [-1],
}

results = mesa.batch_run(
    opinionsModel,
    parameters = params,
    iterations = 50,  # Number of model runs per parameter combination
    max_steps = 200,  # Maximum number of steps per model run
    data_collection_period = 1,
    number_processes = 1,
    display_progress = True,
)


results_df = pd.DataFrame(results)

# Optionally, save the data to a CSV file
results_df.to_csv("Results/NO_I.csv", index=False)

# Visualization
# Plot the data using seaborn (or matplotlib)
# sns.set(style="whitegrid")


# # Example: Line plot for each value of 'N' with different colors for 'opinion_update_prob'
# plt.figure(figsize=(10, 6))

# pastel_colors = {0.2: "#FF9999", 0.5: "#99FF99", 0.8: "#9999FF"}
# sns.lineplot(x="N", y="Step", hue="opinion_update_prob", data=results_df, marker="o", palette=pastel_colors)

# # plt.title("Opinions Convergence Speed vs. Number of Agents (N) with Different Opinion Update Probabilities")
# plt.xlabel("Number of Agents")
# plt.ylabel("Opinions Convergence Speed")
# plt.legend(title="Opinion Update Probability")
# plt.show()

plt.figure(figsize=(8,  5))
# pastel_colors = {0: "#FF9999", 0.5: "#99FrFF99", 1: "#9999FF"}
# sns.lineplot(x="Step", y="op_avg", data=results_df, marker="o", palette=pastel_colors)
sns.lineplot(x="Step", y="op_avg", hue="inst_info", data=results_df, marker="o")

plt.xlabel("Time Step")
plt.ylabel("Opinions Average")
plt.legend(title="Institution Information")
plt.title("Opinion Avg per time step (Giardini & Vilone Model) ")
plt.show()