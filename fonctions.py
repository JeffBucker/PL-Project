import requests
import pandas as pd
import matplotlib.pyplot as plt

# Fonction pour enrichir df_players avec les données des n derniers matchs

def enrich_players_with_last_n_matches_data(df_players, n_last_matches=4):
    # Colonnes à ajouter
    cols_to_add = ['minutes_last', 'xGI_last', 'xG_last', 'ict_last', 'total_points_last']
    for col in cols_to_add:
        df_players[col] = 0.0  # initialisation à zéro

    for idx, player_id in enumerate(df_players['id']):
        url = f"https://fantasy.premierleague.com/api/element-summary/{player_id}/"
        try:
            resp = requests.get(url)
            data = resp.json()
            history = data.get('history', [])

            # Garde les n derniers matchs joués (déjà ordonnés par gw)
            recent_games = history[-n_last_matches:] if len(history) >= n_last_matches else history

            # Moyennes
            if recent_games:
                minutes_avg = sum(float(g.get('minutes', 0)) for g in recent_games) / len(recent_games)
                xgi_avg = sum(float(g.get('expected_goal_involvements', 0)) for g in recent_games) / len(recent_games)
                xg_avg = sum(float(g.get('expected_goals', 0)) for g in recent_games) / len(recent_games)
                ict_avg = sum(float(g.get('ict_index', 0)) for g in recent_games) / len(recent_games)
                points_avg = sum(float(g.get('total_points', 0)) for g in recent_games) / len(recent_games)

            else:
                minutes_avg = xgi_avg = xg_avg = ict_avg = points_avg = 0.0

            # Mise à jour dans df_players
            df_players.at[idx, 'minutes_last'] = minutes_avg
            df_players.at[idx, 'xGI_last'] = xgi_avg
            df_players.at[idx, 'xG_last'] = xg_avg
            df_players.at[idx, 'ict_last'] = ict_avg
            df_players.at[idx, 'total_points_last'] = points_avg

        except Exception as e:
            print(f"Erreur pour player_id={player_id} : {e}")
            # Remplit avec zéro en cas d’erreur
            for col in cols_to_add:
                df_players.at[idx, col] = 0.0

    return df_players


#   Transfer in et out sur les n derniers matchs

def get_recent_transfers(df_players, n_last_matches=4):
    transfer_data = []

    for player_id in df_players['id']:
        url = f"https://fantasy.premierleague.com/api/element-summary/{player_id}/"
        resp = requests.get(url).json()
        history = resp.get('history', [])[-n_last_matches:]  # Derniers n matchs

        # Somme des transfers_in et transfers_out sur ces matchs
        transfers_in = sum(int(match.get('transfers_in', 0)) for match in history)
        transfers_out = sum(int(match.get('transfers_out', 0)) for match in history)
        total_transfers = transfers_in + transfers_out

        transfer_data.append({
            'id': player_id,
            'web_name': df_players.loc[df_players['id'] == player_id, 'web_name'].values[0],
            'transfers_in': transfers_in,
            'transfers_out': transfers_out,
            'total_transfers': total_transfers
        })

    return pd.DataFrame(transfer_data)
