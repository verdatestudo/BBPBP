

import pandas as pd
import re

from zpbp_stage_two import do_stage_two


# Section 3

def get_all_raw_data(xls):
    dfs = {}

    for sheet in xls.sheet_names:
        if sheet == 'HowTo':
            continue

        # df = pd.read_excel(open_filename, sheet_name=sheet)
        df = pd.read_excel(xls, sheet_name=sheet)

        # Split data into df_lineup and df_play - the split happens at the cell 'QTR'.
        search = 'QTR' 
        search_idx = df.loc[df.isin([search]).any(axis=1)].index.tolist()[0]
        df_lineup = df.loc[:search_idx - 1][:]
        df_plays = df.loc[search_idx:][:]

        del df    # To ensure don't accidentally re-use this instead of specific df's.

        # Tidy df_lineup - drop empty columns, rename column headers.
        df_lineup = df_lineup.drop(df_lineup.columns[2:],axis = 1)
        df_lineup.columns = ['POS', 'PLAYER_NAME']

        # Tidy df_play - rename column headers and remove the first row which is the column headers.
        df_plays.columns = df_plays.iloc[0]
        df_plays = df_plays[1:]
        df_plays.columns.name = None
        df_plays.columns = df_plays.columns.str.upper()

        dfs[sheet] = [df_lineup, df_plays]
    
    return dfs
    
# Section 4

def clean_df_lineup(df_lineup):
    # Extract the team from the player name (e.g Bob Smith (A) = A).
    # If you can't extract a team then it's not a player name and you can drop the row.
    get_team_pattern = r"\((.*?)\)"

    df_lineup['TEAM'] = df_lineup['PLAYER_NAME'].str.extract(get_team_pattern, expand=False)
    df_lineup = df_lineup.dropna()
    return df_lineup

# Section 5.

# Convert actual play to regex play - replacing S.Bondi with PLAYERNAME.
# NOTE: still have to convert stuff like timeouts and other team events, this is just players.

def convert_all_plays(df, player_name_pattern):
    df['PLAY_REGEX'] = df['EVENT'].apply(lambda row: convert_play_to_regex(row, player_name_pattern))
    df['PLAY_REGEX'].to_clipboard(sep=',', index=False)
    return df

def convert_play_to_regex(play, pattern):
    return re.sub(pattern, 'PLAYERNAME', play)

# Section 6

def get_all_player_names_from_play(df, player_name_pattern):
    player_names = df['EVENT'].str.extractall(player_name_pattern)
    
    # remove multi-index.
    # https://stackoverflow.com/questions/52143566/how-to-rename-columns-dynamically-before-unstack-in-pandas
    tmp = player_names.unstack().add_prefix('Player')
    tmp.columns = tmp.columns.droplevel(0)
    
    df = df.join(tmp)
    return df

# Section 8

def save_xls(dfs, path):
    """
    Save a dictionary of dataframes to an excel file, 
    with each dataframe as a separate page
    """
    # writer = pd.ExcelWriter(path)
    
    # for sheet, (df_lineup, df_plays) in dfs.items():
    #     df_lineup.to_excel(writer, sheet_name=f'{sheet}_lineup')
    #     df_plays.to_excel(writer, sheet_name=f'{sheet}_plays')

    # removing writer.save
    with pd.ExcelWriter(path, engine='openpyxl') as writer:
        for sheet, (df_lineup, df_plays) in dfs.items():
            df_lineup.to_excel(writer, sheet_name=f'{sheet}_lineup')
            df_plays.to_excel(writer, sheet_name=f'{sheet}_plays')

    # df_plays.to_excel(writer, index=False)
    # writer.save()
    return None

def generate_report(input_path, output_path_stage1, output_path_stage2):
    getting_new_regex = False    # Use True if using this to download new plays so they can be charted.
    # player_name_pattern = re.compile(r'([A-Z]\. .*? \([A|H]\))')
    player_name_pattern = re.compile(r'\b(.\. .*? \([A|H]\))')

    # Section 2

    # https://stackoverflow.com/questions/26521266/using-pandas-to-pd-read-excel-for-multiple-worksheets-of-the-same-workbook

    xls = pd.ExcelFile(input_path)
    dfs = get_all_raw_data(xls)

    # Section 7

    # Clean all pbp data in the excel file.

    for sheet, (df_lineup, df_plays) in dfs.items():
        df_lineup = clean_df_lineup(df_lineup)

        df_plays = convert_all_plays(df_plays, player_name_pattern)
        df_plays = get_all_player_names_from_play(df_plays, player_name_pattern)
        
        if getting_new_regex:
            df_plays = df_plays.drop_duplicates(subset='PLAY_REGEX', keep='first')
            
        dfs[sheet] = [df_lineup, df_plays]

    save_xls(dfs, output_path_stage1)

    do_stage_two(output_path_stage1, output_path_stage2)


if __name__ == '__main__':
    fname = 'zstreamtest.xlsx'

    # Section 1
    open_filename = f'game_data_1raw/{fname}'
    save_filename = f'game_data_2converted/{fname}'

    generate_report(open_filename, save_filename)







































