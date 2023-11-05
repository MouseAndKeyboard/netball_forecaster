import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.lines as mlines
from pathlib import Path

REAL_GAME_OUTCOME_DIR = Path('./model_scripts/data')
OUTPUTS_DIR = Path('./model_scripts/outputs')
ID_TO_NAME_DIR = Path('./model_scripts/id_to_name')

# Function to compute number of wins and total games
def compute_stats(df):
    wins = sum((df['min_team'] == df['Team_1_ID']) & (df['home_score'] > df['away_score']) | 
               (df['min_team'] == df['Team_2_ID']) & (df['away_score'] > df['home_score']))
    total_games = len(df)
    return pd.Series([wins, total_games], index=['wins', 'total_games'])

if __name__ == "__main__":
    # loop through every folder in the outputs dir

    all_results = pd.DataFrame()

    for bracket_folder in os.listdir(OUTPUTS_DIR):
        real_bracket_data = pd.read_csv(REAL_GAME_OUTCOME_DIR / (bracket_folder + '.csv'))
        real_bracket_data = real_bracket_data[~real_bracket_data['bye']]

        cols = ["home_team", "away_team", "Team_1_ID", "Team_2_ID", "home_score", "away_score"]
        real_bracket_data = real_bracket_data[cols]

        # First, create consistent pairings by sorting team IDs
        real_bracket_data['min_team'] = real_bracket_data[['Team_1_ID', 'Team_2_ID']].min(axis=1)
        real_bracket_data['max_team'] = real_bracket_data[['Team_1_ID', 'Team_2_ID']].max(axis=1)
        
        # Group by consistent team pairings and apply the function
        results = real_bracket_data.groupby(['min_team', 'max_team']).apply(compute_stats).reset_index()
        results.columns = ['Team_1_ID', 'Team_2_ID', 'wins_for_team_1', 'total_games']

        results['probability_team_1_beats_team_2'] = (results['wins_for_team_1'] + 1) / (results['total_games'] + 2)

        # loop through every round folder in the bracket
        for round_folder in os.listdir(OUTPUTS_DIR / bracket_folder):
            # loop through every csv file in the round folder
            round_data_file = OUTPUTS_DIR / bracket_folder / round_folder / "model.csv"
            if round_data_file.exists():
                
                bracket = str(bracket_folder)
                T = len(pd.read_csv(ID_TO_NAME_DIR / (bracket + ".csv")))

                columns = [f"win_prob.{i}.{j}" for i in range(1, T + 1) for j in range(1, T + 1)]

                predicted_probs = pd.read_csv(round_data_file)[columns].mean()

                # Melt the predictions data
                melted_data = predicted_probs.reset_index()
                melted_data.columns = ['team_pairing', 'predicted_prob']

                # Extract Team IDs from the column names
                melted_data['Team_1_ID'] = melted_data['team_pairing'].str.extract('win_prob\.(\d+)\.\d+').astype(int)
                melted_data['Team_2_ID'] = melted_data['team_pairing'].str.extract('win_prob\.\d+\.(\d+)').astype(int)

                # Merge with the results dataframe
                merged_results = pd.merge(results, melted_data[['Team_1_ID', 'Team_2_ID', 'predicted_prob']], on=['Team_1_ID', 'Team_2_ID'], how='left')

                # add the bracket:
                merged_results['bracket'] = bracket

                # add the merge to the all_results dataframe
                all_results = pd.concat([all_results, merged_results])

    buckets = pd.IntervalIndex.from_tuples([(0, 0.225), (0.225, 0.325), (0.325, 0.45), (0.45, 0.55), (0.55, 0.675), (0.675, 0.775), (0.775, 1)])
    # bucket the predicted probabilities
    all_results['bucket'] = pd.cut(all_results['predicted_prob'], buckets)

    # add the bucket midpoints
    all_results['bucket_midpoint'] = all_results['bucket'].apply(lambda x: x.mid)

    # add the bucket labels
    all_results['bucket_label'] = all_results['bucket'].apply(lambda x: f"[{x.left}, {x.right})")

    # compute the average predicted probability for each bucket
    bucket_means = all_results.groupby('bucket_label')['predicted_prob'].mean().reset_index()
    bucket_means.columns = ['bucket_label', 'bucket_mean']

    # merge the bucket means with the all_results dataframe
    all_results = pd.merge(all_results, bucket_means, on='bucket_label')
        
    # plot the results
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='bucket_midpoint', y='bucket_mean', hue='bucket_label', data=all_results, s=100)
    plt.plot([0, 1], [0, 1], color='black', linestyle='--')
    plt.xlabel("Predicted Probability")
    plt.ylabel("Actual Probability")
    plt.title("Calibration Plot")
    plt.savefig("calibration_plot.png")
    plt.close()
