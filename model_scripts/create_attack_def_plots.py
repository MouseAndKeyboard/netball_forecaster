import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.lines as mlines
from pathlib import Path

OUTPUTS_DIR = Path('./model_scripts/outputs')
ID_TO_NAME_DIR = Path('./model_scripts/id_to_name')

# loop through each csv file in outputs directory
for file in os.listdir(OUTPUTS_DIR):
    if file.endswith('.csv'):

        if not file.endswith('Tuesday Netball - Division 2.csv'):
            continue

        # read the csv into a dataframe
        df = pd.read_csv(OUTPUTS_DIR / file)
        print(file)

        id_to_name = pd.read_csv(ID_TO_NAME_DIR / file)

        # get number of teams:
        T = len(id_to_name)

        offence_cols = [f'offence.{i}' for i in range(1, T + 1)]
        defence_cols = [f'defence.{i}' for i in range(1, T + 1)]

        team_names = id_to_name['Team_Name'].values
        colours = ['Reds', 'Blues', 'Greens', 'Purples', 'pink', 'Oranges', 'crest', 'viridis']
        solo_colours = ['red', 'blue', 'green', 'purple', 'pink', 'orange', 'blue', 'green']

        colours = colours[:T]
        solo_colours = solo_colours[:T]

        sns.set_style("whitegrid")

        fig, ax = plt.subplots(ncols=1, figsize=(9, 5))  # Adjust the width (e.g., from 15 to 18) 

        # Create a list to hold the custom legend handles
        legend_handles = []

        # plot the offence and defence values
        for offence_col, defence_col, colour, name, solo_col in zip(offence_cols, defence_cols, colours, team_names, solo_colours):
            offence_samples = df[offence_col]
            defence_samples = df[defence_col]
            sns.kdeplot(x=offence_samples, y=defence_samples, cmap=colour, fill=True, thresh=0.85, ax=ax, alpha=0.3)

            legend_handles.append(mlines.Line2D([0], [0], color=solo_col, marker='o', markersize=10, label=name, linestyle='None'))

        biggest = 0
        for offence_col, defence_col, colour, name in zip(offence_cols, defence_cols, solo_colours, team_names):
            # take the mean of the offence and defence values
            offence_mean = df[offence_col].mean()
            defence_mean = df[defence_col].mean()

            print(offence_mean, defence_mean, name)
            biggest = max(biggest, abs(offence_mean), abs(defence_mean))

            # plot the mean values
            ax.scatter(offence_mean, defence_mean, c="black", s=200)
            # Plot an X
            ax.scatter(offence_mean, defence_mean, c=colour, s=100, marker="x")
            ax.annotate(name, (offence_mean, defence_mean), 
                textcoords="offset points", xytext=(5,9), ha='center')

        ax.set_xlabel("Offence")
        ax.set_ylabel("Defence")

        # ensure the x-y axis have the same scale
        ax.set_aspect('equal', adjustable='box')

        print(biggest)
        
        # set the x and y axis limits to be symmetric about 0
        ax.set_xlim(-biggest-0.25, biggest+0.25)
        ax.set_ylim(-biggest-0.25, biggest+0.25)

        plt.tight_layout()

        # Current code
        ax.legend(handles=legend_handles, loc='center left', bbox_to_anchor=(1, 0.5))

        # add a small watermark
        plt.text(0.5, 0.05, 'Created by Michael Nefiodovas', horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes, bbox=dict(facecolor='white', alpha=0.5), alpha=0.2)

        # show the plot
        plt.savefig(f'./model_scripts/plots/{file[:-4]}.png')
        print("Plot saved to ./model_scripts/plots/")