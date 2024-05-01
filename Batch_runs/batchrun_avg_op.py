import mesa
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from OD_model.model import opinionsModel

params = {
    "N": 1000,  # Vary the number of agents
    "inst_info": np.arange(0.0, 1.1, 0.1),  # Vary the institution information value
}

results = mesa.batch_run(
    opinionsModel,
    parameters = params,
    iterations = 1,  # Number of model runs per parameter combination
    max_steps = 2000,  # Maximum number of steps per model run
    number_processes = 1,
    display_progress = True,
)

results_df = pd.DataFrame(results)

# Optionally, save the data to a CSV file
results_df.to_csv("Results/V02.4_Extended_OD(avg_opinion).csv", index=False)


