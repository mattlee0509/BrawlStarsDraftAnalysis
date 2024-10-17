
import requests
import pandas as pd
from pandas import json_normalize
from tabulate import tabulate



url = "https://api.brawlstars.com/v1/players/%238JYPJ0V8/battlelog"
headers = {
    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjNjMTQxNzdkLTU4ZGMtNDJmZS05YTE3LTJjNDIzYjNiNjk0YyIsImlhdCI6MTcyOTA5OTc3MCwic3ViIjoiZGV2ZWxvcGVyLzUxOTQ5Y2RjLWQzNTYtNTY1OC05MjAyLWRhYmQ3OGRhN2IxNiIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiODkuMTMxLjE5Ny4xMzQiXSwidHlwZSI6ImNsaWVudCJ9XX0.SLL93SIeShfIVb6fO_C_05CnQxBv_39gnfjnjvaPpZdiKNBnf5qd4q8mO1dPTxpH5NaqfetZGWZYW4UJ-WHdOw",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    battle_log = response.json()
    
    # Create a list to store the expanded data only for 'soloRanked' battles
    battle_data_expanded = []

    # Now handle the teams' and players' information separately
    for game in battle_log['items']:
        # Check if the game type is 'soloRanked'
        if game['battle']['type'] == 'soloRanked':
            battle_time = game['battleTime']
            event_mode = game['event']['mode']
            event_map = game['event']['map']
            battle_mode = game['battle']['mode']
            battle_type = game['battle']['type']
            battle_result = game['battle'].get('result', 'N/A')
            battle_duration = game['battle'].get('duration', 'N/A')
            
            battle_result_bool = battle_result == 'victory'

            # Check if starPlayer exists and is not None
            star_player = game['battle'].get('starPlayer')
            star_player_name = star_player.get('name', 'None') if star_player else 'None'

            # Process the teams and players data
            for team_idx, team in enumerate(game['battle']['teams']):
                for player_idx, player in enumerate(team):
                    player_tag = player.get('tag', 'N/A')
                    player_name = player.get('name', 'N/A')
                    brawler_name = player['brawler']['name']
                    brawler_power = player['brawler']['power']
                    brawler_trophies = player['brawler']['trophies']

                    # Append the flattened information with unique player columns
                    battle_data_expanded.append({
                        'battle_time': battle_time,
                        'event_mode': event_mode,
                        'event_map': event_map,
                        'battle_mode': battle_mode,
                        'battle_type': battle_type,
                        'battle_result': battle_result_bool,
                        'battle_duration': battle_duration,
                        'star_player': star_player_name,
                        f'team_{team_idx+1}_player_{player_idx+1}_tag': player_tag,
                        f'team_{team_idx+1}_player_{player_idx+1}_name': player_name,
                        f'team_{team_idx+1}_player_{player_idx+1}_brawler_name': brawler_name,
                        f'team_{team_idx+1}_player_{player_idx+1}_brawler_power': brawler_power,
                        f'team_{team_idx+1}_player_{player_idx+1}_brawler_trophies': brawler_trophies
                    })

    # Convert the list of dictionaries to a pandas DataFrame
    df = pd.DataFrame(battle_data_expanded)

    # Transpose the DataFrame so each row represents a unique battle_time
    # Group by battle_time and team/player-related columns spread across
    transposed_df = df.groupby('battle_time').first().reset_index()

    # Display the transposed DataFrame
    transposed_df.to_csv('test2.csv', index=False)

    print(transposed_df)
