import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.lines as mlines
from pathlib import Path

OUTPUTS_DIR = Path('./model_scripts/outputs')
ID_TO_NAME_DIR = Path('./model_scripts/id_to_name')

POSTERIOR_PLOTS_DIR = Path('./model_scripts/probability_posteriors')

if __name__ == "__main__":
    # loop through every folder in the outputs dir

    for bracket_folder in os.listdir(OUTPUTS_DIR):
        # loop through every round folder in the bracket
        for round_folder in os.listdir(OUTPUTS_DIR / bracket_folder):
            # loop through every csv file in the round folder
            round_data_file = OUTPUTS_DIR / bracket_folder / round_folder / "model.csv"
            if round_data_file.exists():
                
                bracket = str(bracket_folder)
                T = len(pd.read_csv(ID_TO_NAME_DIR / (bracket + ".csv")))

                columns = [f"win_prob.{i}.{j}" for i in range(1, T + 1) for j in range(1, T + 1)]

                data = pd.read_csv(round_data_file)

                for col in columns:
                    # make a density plot on [0, 1] for this column
                    plt.figure()
                    sns.distplot(data[col], hist=False)
                    plt.title(f"Probability of {col}")
                    plt.xlabel("Probability")
                    plt.ylabel("Density")

                    save_loc = POSTERIOR_PLOTS_DIR / bracket_folder / round_folder
                    save_loc.mkdir(parents=True, exist_ok=True)

                    plt.savefig(save_loc / f"{col}.png")
                    plt.close()