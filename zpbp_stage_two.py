

import pandas as pd
import re



def get_all_regex_plays(plays_filename):
    df_plays_all = pd.read_excel(plays_filename, sheet_name='others')
    df_plays_all = df_plays_all.drop_duplicates(subset='PLAY_REGEX', keep='first')
    df_plays_all = df_plays_all.drop(['PlayActual'], axis=1)
    df_plays_all = df_plays_all.reset_index(drop=True)
    return df_plays_all

def switch_shot_players(df):
    df[['Player0','Player1']] = df[['Player0','Player1']].mask( df['SHOOTER'] == 2, df[['Player1','Player0']].values)
    return df

def tidy_data(df):
    df = df.drop(['PLAY_REGEX', 'ShotMadeFormulaTest', 'SHOOTER', 'Role1', 'Role2', 'Role3'], axis=1)
    df['TEAM'] = df['Player0'].str.extract('.*\((.*)\).*')
    df['TEAMPLAYER1'] = df['Player1'].str.extract('.*\((.*)\).*')

    # Move TEAM columns to right of EVENT
    col_idx = 5
    for col_name in ['TEAMPLAYER1', 'TEAM']:
        column_to_move = df.pop(col_name)
        df.insert(col_idx, col_name, column_to_move)
    
    # Only keep shots for now.
    df = df[df["PlayType"] == "SHOT"]

    return df

def do_stage_two(input_path, output_path):
    plays_filename = 'pbp_regex.xlsx'

    # https://stackoverflow.com/questions/26521266/using-pandas-to-pd-read-excel-for-multiple-worksheets-of-the-same-workbook

    df = pd.read_csv(input_path)
    df_plays_all = get_all_regex_plays(plays_filename)

    df_game_2 = pd.merge(df, df_plays_all, on='PLAY_REGEX', how='left')
    df_game_2 = switch_shot_players(df_game_2)
    df_game_2 = tidy_data(df_game_2)

    # save_filename_regex = f'game_data_3reports/{fname}'
    df_game_2.to_csv(output_path)


if __name__ == '__main__':
    fname = 'zstreamtest.csv'
    open_filename = f'game_data_2converted/{fname}'
    save_filename = f'game_data_3reports/{fname}'
    pass












