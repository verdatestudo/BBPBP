

import pandas as pd
import re

from zpbp_stage_two import do_stage_two


def get_all_raw_data(df):
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

    return df_plays
    
def convert_all_plays(df, player_name_pattern):
    df = df[df['EVENT'].notna()].copy()
    df.loc[:, 'EVENT'] = df['EVENT'].astype(str)

    df['PLAY_REGEX'] = df['EVENT'].apply(lambda row: convert_play_to_regex(row, player_name_pattern))
    return df

def convert_play_to_regex(play, pattern):
    return re.sub(pattern, 'PLAYERNAME', play)


def get_all_player_names_from_play(df, player_name_pattern):
    player_names = df['EVENT'].str.extractall(player_name_pattern)
    
    # remove multi-index.
    # https://stackoverflow.com/questions/52143566/how-to-rename-columns-dynamically-before-unstack-in-pandas
    tmp = player_names.unstack().add_prefix('Player')
    tmp.columns = tmp.columns.droplevel(0)
    
    df = df.join(tmp)
    return df

def generate_report(input_path, output_path_stage1, output_path_stage2):
    getting_new_regex = False    # Use True if using this to download new plays so they can be charted.
    player_name_pattern = re.compile(r'\b(.\. .*? \([A|H]\))')

    df = pd.read_csv(input_path)
    df_plays = get_all_raw_data(df)

    df_plays = convert_all_plays(df_plays, player_name_pattern)
    df_plays = get_all_player_names_from_play(df_plays, player_name_pattern)
        
    if getting_new_regex:
        df_plays = df_plays.drop_duplicates(subset='PLAY_REGEX', keep='first')
            
    df_plays.to_csv(output_path_stage1)
    do_stage_two(output_path_stage1, output_path_stage2)


if __name__ == '__main__':
    fname = 'zstreamtest.csv'
    fname = 'b3finals67.csv'

    # Section 1
    open_filename = f'game_data_1raw/{fname}'
    save_filename = f'game_data_2converted/{fname}'
    save_filename_2 = f'game_data_3reports/{fname}'

    generate_report(open_filename, save_filename, save_filename_2)







































