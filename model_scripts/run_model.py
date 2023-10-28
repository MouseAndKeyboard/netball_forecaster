import pandas as pd
import stan
import matplotlib.pyplot as plt
import os
import seaborn as sns
from pathlib import Path

def fit_model(N, T, goals, team_1, team_2):
    # read the code from netball.stan
    model_code = open('./model_scripts/netball.stan').read()

    stan_data = {
        'N': N,
        'goals': goals,
        'team_1': team_1,
        'team_2': team_2,
        'T': T
    }


    print(stan_data)

    posterior = stan.build(model_code, data=stan_data)
    fit = posterior.sample(num_chains=4, num_samples=1000)

    return fit

def run_model(data, OUTPUTS_FOLDER = "./model_scripts/outputs", FINAL_ONLY = False):
    # group by round
    rounds = data.groupby('round_index')
    bracket = data["bracket"].iloc[0]
    # now we want to fit the model considering all rounds up to and including the current round

    # Get number of teams
    teams = pd.read_csv(f'./model_scripts/id_to_name/{bracket}.csv')
    T = len(teams)

    for i, (round_index, round_data) in enumerate(rounds):

        if FINAL_ONLY and i != len(rounds) - 1:
            continue
        # create folder if it doesn't exist
        Path(f'{OUTPUTS_FOLDER}/{bracket}/{round_index}').mkdir(parents=True, exist_ok=True)

        all_data = data[data['round_index'] <= round_index]



        # fit the model
        fit = fit_model(
            N=len(all_data),
            T=T,
            goals=all_data[['home_score', 'away_score']].values,
            team_1=all_data['Team_1_ID'].values.astype(int),
            team_2=all_data['Team_2_ID'].values.astype(int)
        )

        # save the model
        fit.to_frame().to_csv(f'{OUTPUTS_FOLDER}/{bracket}/{round_index}/model.csv', index=False)


if __name__ == "__main__":
    # loop through every file in data/
    for filename in os.listdir('./model_scripts/data'):
        if filename.endswith('.csv'):
            data = pd.read_csv(f'./model_scripts/data/{filename}')
            data = data[data['bye'] == False]

            run_model(data, FINAL_ONLY = True)