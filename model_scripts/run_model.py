import pandas as pd
import stan
import matplotlib.pyplot as plt
import os
import seaborn as sns
import matplotlib.pyplot as plt

def fit_stan_model(df, progressive = False):
    # Create table of all unique teams
    teams = pd.DataFrame()
    teams['Team_Name'] = pd.concat([df['home_team'], df['away_team']])
    teams = teams.drop_duplicates().reset_index(drop=True)

    teams['Team_ID'] = teams.index

    # the team Ids actually need to start from 1 to work in Stan
    teams['Team_ID'] = teams['Team_ID'] + 1

    print(teams)

    teams.to_csv(f'./model_scripts/id_to_name/{df.iloc[0]["bracket"]}.csv', index=False)

    # Add team IDs to games table
    df = pd.merge(df, teams, left_on='home_team', right_on='Team_Name', how='left')
    df = df.rename(columns={'Team_ID': 'Team_1_ID'})
    df = pd.merge(df, teams, left_on='away_team', right_on='Team_Name', how='left')
    df = df.rename(columns={'Team_ID': 'Team_2_ID'})
    
    # number of rounds
    N = len(df)

    # number of teams
    T = len(teams)

    stan_data = {
        'N': N,
        'goals': df[['home_score', 'away_score']].values,
        'team_1': df['Team_1_ID'].values,
        'team_2': df['Team_2_ID'].values,
        'T': T
    }

    # read the code from netball.stan
    model_code = open('./model_scripts/netball.stan').read()
    if progressive:
        for i in range(1, N + 1):
            stan_data['N'] = i
            stan_data['goals'] = df[['home_score', 'away_score']].values[:i]
            stan_data['team_1'] = df['Team_1_ID'].values[:i]
            stan_data['team_2'] = df['Team_2_ID'].values[:i]
            posterior = stan.build(model_code, data=stan_data)
            fit = posterior.sample(num_chains=4, num_samples=1000)
            m = fit.to_frame().mean()
            offence_means = m[m.index.str.contains('offence')]
            defence_means = m[m.index.str.contains('defence')]

            print(offence_means)
            print(defence_means)
            print(T)
            # scatter plot the mean values
            # plt.scatter(offence_means, defence_means, c="black", s=200)
            # plt.show()
            # plt.cla()
    else:
        stan_data['N'] = N
        stan_data['goals'] = df[['home_score', 'away_score']].values
        stan_data['team_1'] = df['Team_1_ID'].values
        stan_data['team_2'] = df['Team_2_ID'].values
        posterior = stan.build(model_code, data=stan_data)
        fit = posterior.sample(num_chains=4, num_samples=1000) 
        

    return fit

if __name__ == "__main__":
    
    # loop through every file in data/
    for filename in os.listdir('./model_scripts/data'):
        if filename.endswith('.csv'):
            print(filename)
            data = pd.read_csv(f'./model_scripts/data/{filename}')
            data = data[data['bye'] == False]

            print(data.columns)
            fit = fit_stan_model(data, progressive=False)

            fit.to_frame().to_csv(f'./model_scripts/outputs/{filename}', index=False)
