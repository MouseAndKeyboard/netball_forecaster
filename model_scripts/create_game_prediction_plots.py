import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.lines as mlines
from pathlib import Path

OUTPUTS_DIR = Path('./model_scripts/outputs')
ID_TO_NAME_DIR = Path('./model_scripts/id_to_name')

# loop through each csv file in outputs directory

MAKE_PLOTS = False

predictions_df = []
for file in os.listdir(OUTPUTS_DIR):
    if file.endswith('.csv'):
        # read the csv into a dataframe
        df = pd.read_csv(OUTPUTS_DIR / file)
        print(file)


        # create folder if it doesn't exist
        Path(f'./model_scripts/game_predictions/{file[:-4]}').mkdir(parents=True, exist_ok=True)

        id_to_name = pd.read_csv(ID_TO_NAME_DIR / file)

        yrep = [[[f'y_rep.{i}.{j}.{k}' for k in range(1, 3)] for i in range(1, 7)] for j in range(1, 7)]
        team_names = id_to_name['Team_Name'].values

        colours = ['Reds', 'Blues', 'Greens', 'Purples', 'pink', 'Oranges']
        solo_colours = ['red', 'blue', 'green', 'purple', 'pink', 'orange']



        for i in range(6):
            for j in range(6):
                home_goals = df[yrep[i][j][1]]
                away_goals = df[yrep[i][j][0]]

                expected_home = home_goals.mean()
                expected_away = away_goals.mean()

                home_win_p = sum(home_goals > away_goals) / len(home_goals)
                away_win_p = sum(home_goals < away_goals) / len(home_goals)
                draw_p = sum(home_goals == away_goals) / len(home_goals)

                predictions_df.append({
                        'Bracket': file[:-4],
                        'Team_1': team_names[i],
                        'Team_2': team_names[j],
                        'Team_1_Win': home_win_p,
                        'Team_2_Win': away_win_p,
                        'Draw': draw_p,
                        'Team_1_Score': expected_home,
                        'Team_2_Score': expected_away
                    })

                if MAKE_PLOTS:
                    sns.set_style("whitegrid")

                    sns.kdeplot(x=home_goals, y=away_goals, fill=True, cmap="viridis", thresh=0.05, levels=100)

                    plt.scatter(expected_home, expected_away, c="black", s=200)
                    plt.annotate(f"Prediction: {round(expected_home)}-{round(expected_away)}", (round(expected_home), round(expected_away)), 
                        textcoords="offset points", xytext=(5,9), ha='center')

                    

                    # draw a y=x dotted line
                    plt.plot([0, 40], [0, 40], 'k--', alpha=0.5)

                    # force the x and y axis to be the same
                    plt.xlim(0, 40)
                    plt.ylim(0, 40)

                    # make sure the x and y axis have the same scale
                    plt.gca().set_aspect('equal', adjustable='box')

                    plt.xlabel(f'{team_names[i]} goals')
                    plt.ylabel(f'{team_names[j]} goals')

                    # Make a white box to put the win probabilities in
                    plt.text(0.5, 0.9, f'{team_names[i]} win: {round(home_win_p*100, 1)}%', horizontalalignment='right', verticalalignment='center', transform=plt.gca().transAxes, bbox=dict(facecolor='white'))
                    plt.text(0.5, 0.85, f'{team_names[j]} win: {round(away_win_p*100, 1)}%', horizontalalignment='right', verticalalignment='center', transform=plt.gca().transAxes, bbox=dict(facecolor='white'))
                    plt.text(0.5, 0.8, f'Draw: {round(draw_p*100, 1)}%', horizontalalignment='right', verticalalignment='center', transform=plt.gca().transAxes, bbox=dict(facecolor='white'))

                    # add a small watermark
                    plt.text(0.5, 0.05, 'Created by Michael Nefiodovas', horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes, bbox=dict(facecolor='white', alpha=0.5), alpha=0.2)


                    plt.tight_layout()

                    filename = f'{team_names[i]}_vs_{team_names[j]}.png'
                    # sanetise the filename
                    filename = filename.replace('/', '-')

                    plt.savefig(f'./model_scripts/game_predictions/{file[:-4]}/{filename}')
                    plt.clf()

        pd.DataFrame(predictions_df).to_csv(f'./model_scripts/game_predictions/predictions.csv', index=False)
