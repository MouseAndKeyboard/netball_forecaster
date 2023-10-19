import streamlit as st
from PIL import Image
import pandas as pd
import os
st.set_page_config(layout="wide")

DIVISION = 7
DAY = "Monday"

title = f"2023 Semester 2 Social Sports - Netball - {DAY} Netball - Division {DIVISION}"

image = Image.open(f"./model_scripts/plots/{title}.png")


st.title("Offence/Defence Analysis Plot")
st.image(image, caption=f"Offence/Defence Analysis for {title}", use_column_width="auto")


raw_predictions_data = pd.read_csv(f"./model_scripts/game_predictions/predictions.csv")
this_bracket_predictions = raw_predictions_data[raw_predictions_data["Bracket"] == title]
this_bracket_predictions = this_bracket_predictions[["Team_1", "Team_2", "Team_1_Win", "Team_2_Win", "Team_1_Score", "Team_2_Score"]]

# Round all the scores to 0 decimal places
this_bracket_predictions["Team_1_Score"] = this_bracket_predictions["Team_1_Score"].round(0)
this_bracket_predictions["Team_2_Score"] = this_bracket_predictions["Team_2_Score"].round(0)

# Make all the probabilities percentages
this_bracket_predictions["Team_1_Win"] = this_bracket_predictions["Team_1_Win"] * 100
this_bracket_predictions["Team_2_Win"] = this_bracket_predictions["Team_2_Win"] * 100

# Round the percentages to 1 decimal place
this_bracket_predictions["Team_1_Win"] = this_bracket_predictions["Team_1_Win"].round(1)
this_bracket_predictions["Team_2_Win"] = this_bracket_predictions["Team_2_Win"].round(1)

# append a percentage sign
this_bracket_predictions["Team_1_Win"] = this_bracket_predictions["Team_1_Win"].astype(str) + "%"
this_bracket_predictions["Team_2_Win"] = this_bracket_predictions["Team_2_Win"].astype(str) + "%"

prediction_image_folder = f"./model_scripts/game_predictions/{title}/"

# loop through all pngs in the folder and display them
prev_team = ''

all_files = sorted(os.listdir(prediction_image_folder))
all_files = [file for file in all_files if file.endswith(".png")]
all_teams = set(file[:-4].split('_vs_')[0] for file in all_files)

st.title("Game Predictions")

for team in all_teams:
    with st.expander(f"Match predictions for {team}"):
        if team == "5-12 Jocks":
            this_bracket_predictions[this_bracket_predictions["Team_1"] == "5/12 Jocks"]
        else:    
            this_bracket_predictions[this_bracket_predictions["Team_1"] == team]
        for file in all_files:
            if file.startswith(team):
                image = Image.open(prediction_image_folder + file)
                st.image(image, caption=f"Game Prediction for {file[:-4].replace('_', ' ')}", use_column_width="auto")
