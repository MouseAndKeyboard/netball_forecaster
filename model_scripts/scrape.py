import requests
from datetime import datetime
from bs4 import BeautifulSoup
import pytz
import pandas as pd

def scrape_uwa_sports_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    rounds_data = []

    smalls = soup.find_all('small')
    bracket = smalls[0].get_text(strip=True)
    
    rounds = soup.find_all('h3')
    for round_header in rounds:
        round_name = round_header.get_text(strip=True)
        
        table = round_header.find_next('table')
        rows = table.find_all('tr', class_='withIcon')
        
        for row in rows:
            home_team_data = row.find_all('td', class_='team')[0].get_text(strip=True).rsplit(' -', 1)
            away_team_data = row.find_all('td', class_='team')[1].get_text(strip=True).rsplit(' -', 1)
            
            home_team = home_team_data[0]
            away_team = away_team_data[0]
            
            # Handle the case where a team has a "Bye" round
            
            date_time = row.find_all('td')[-1].get_text(strip=True)

            if (home_team == 'Bye') or (away_team == 'Bye'):
                rounds_data.append({
                    "bracket": bracket,
                    "round": round_name,
                    "home_team": home_team,
                    "away_team": away_team,
                    "home_score": -1,
                    "away_score": -1,
                    "date_time": date_time
                })
                continue

            if len(home_team_data) == 1:
                # game hasn't happened yet:
                continue

            home_score = int(home_team_data[1].strip('<em></em>'))
            away_score = int(away_team_data[1].strip('<em></em>'))
            
            rounds_data.append({
                "bracket": bracket,
                "round": round_name,
                "home_team": home_team,
                "away_team": away_team,
                "home_score": home_score,
                "away_score": away_score,
                "date_time": date_time
            })
    
    return rounds_data

def scrape_sports_url(url):
    output = scrape_uwa_sports_page(url)

    processed = []

    for game_data in output:
        bye = False
        if "0:00am" in game_data['date_time']:
            game_data['date_time'] = game_data['date_time'].replace("0:00am", "12:00am")
            bye = True

            

        if 'Bye' in game_data['home_team'] or 'Bye' in game_data['away_team']:
            bye = True

        game_data['bye'] = bye
        game_data['date_time'] = datetime.strptime(game_data['date_time'], "%d/%m/%Y %I:%M%p")
        # set timezone to Perth
        game_data['date_time'] = pytz.timezone('Australia/Perth').localize(game_data['date_time'])

        processed.append(game_data)

    pd.DataFrame(processed).to_csv(f'model_scripts/data/{processed[0]["bracket"]}.csv', index=False)

if __name__ == "__main__":
    urls = [
        # tuesday league
        'https://uwaresults.fusesport.com/drawresult.asp?id=1474766&seasonid=1125', # D1
        'https://uwaresults.fusesport.com/drawresult.asp?id=1474767&seasonid=1125', # D2 
        'https://uwaresults.fusesport.com/drawresult.asp?id=1474768&seasonid=1125', # D3
        'https://uwaresults.fusesport.com/drawresult.asp?id=1489115&seasonid=1125', # D4
        'https://uwaresults.fusesport.com/drawresult.asp?id=1489116&seasonid=1125', # D5
        # monday league
        'https://uwaresults.fusesport.com/drawresult.asp?id=1489111&seasonid=1125', # D7
        'https://uwaresults.fusesport.com/drawresult.asp?id=1474764&seasonid=1125', # D6
        'https://uwaresults.fusesport.com/drawresult.asp?id=1474763&seasonid=1125', # D5
        'https://uwaresults.fusesport.com/drawresult.asp?id=1474762&seasonid=1125', # D4
        'https://uwaresults.fusesport.com/drawresult.asp?id=1474761&seasonid=1125', # D3
        'https://uwaresults.fusesport.com/drawresult.asp?id=1474760&seasonid=1125', # D2
    ]

    for url in urls:
        scrape_sports_url(url)
