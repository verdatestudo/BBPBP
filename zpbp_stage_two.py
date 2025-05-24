

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

def save_xls(dfs, path):
    """
    Save a dictionary of dataframes to an excel file, 
    with each dataframe as a separate page
    """
    # writer = pd.ExcelWriter(path)
    
#     for opponent in dfs.keys():
# #         dfs[opponent]['lineup'].to_excel(writer, sheet_name=f'{opponent}_lineup')
#         dfs[opponent]['plays'].to_excel(writer, sheet_name=f'{opponent}_plays')

    # removing writer.save
    with pd.ExcelWriter(path, engine='openpyxl') as writer:
        for opponent in dfs.keys():
            dfs[opponent]['plays'].to_excel(writer, sheet_name=f'{opponent}_plays')

    # writer.save()
    return None


def do_stage_two(input_path, output_path):
    plays_filename = 'pbp_regex.xlsx'

    # https://stackoverflow.com/questions/26521266/using-pandas-to-pd-read-excel-for-multiple-worksheets-of-the-same-workbook

    xls = pd.ExcelFile(input_path)

    dfs = {}

    for sheet in xls.sheet_names:
        opponent, sheet_type = sheet.split('_')
        df = pd.read_excel(input_path, sheet_name=sheet)
        
        # can also use this as a sanity check if we have two files vs same opponent, ensure we're not overwriting.
        if opponent not in dfs:
            dfs[opponent] = {}
        
        dfs[opponent][sheet_type] = df

    df_plays_all = get_all_regex_plays(plays_filename)

    for opponent in dfs:
        df_game_2 = dfs[opponent]['plays']
        df_game_2 = pd.merge(df_game_2, df_plays_all, on='PLAY_REGEX', how='left')
        df_game_2 = switch_shot_players(df_game_2)
        df_game_2 = tidy_data(df_game_2)
        dfs[opponent]['plays'] = df_game_2

    # save_filename_regex = f'game_data_3reports/{fname}'
    save_xls(dfs, output_path)

if __name__ == '__main__':
    fname = 'zstreamtest.xlsx'
    open_filename = f'game_data_2converted/{fname}'
    save_filename = f'game_data_3reports/{fname}'
    pass












