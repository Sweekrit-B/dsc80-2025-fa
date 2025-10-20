# lab.py


import os
import io
from pathlib import Path
import pandas as pd
import numpy as np


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def trick_me():
    return 3


def trick_bool():
    return [4, 10, 13]


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def population_stats(df):
    # Define a function to calculate statistics based on a column
    def calculate_stats(col):
        return {
            'num_nonnull': col.count(),
            'prop_nonnull': col.count() / len(col),
            'num_distinct': col.nunique(),
            'prop_distinct': col.nunique() / col.count()
        }

    # Step 1: apply the function to each column
    # Step 2: convert this row (index = col, value = dict) to a dataframe
    # Step 3: fill all null values
    out_pop = df.apply(calculate_stats).apply(pd.Series).fillna(0)
    return out_pop


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def most_common(df, N=10):
    # Define a final dataframe
    final_df = pd.DataFrame()
    # For each column in the dataframe...
    for col in df:
        # Get the N most common values using Series methods
        most_common = df[col].value_counts().iloc[:N]
        # Add the indices + values and pad the remaining with np.nan
        final_df[col + '_values'] = list(most_common.index) + [np.nan] * max(0, (N - len(most_common)))
        final_df[col + '_counts'] = list(most_common.values) + [np.nan] * max(0, (N - len(most_common)))
    return final_df


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def super_hero_powers(powers):
    hero_powers = powers.set_index('hero_names')
    # Superhero with th e most amount of powers
    amt_powers = hero_powers.sum(axis=1).sort_values(ascending=False)
    most_powers = amt_powers.index[0]
    # Most common superpower among heros who can fly
    fly_most_common = hero_powers[hero_powers['Flight']].sum().sort_values(ascending=False).index[1]
    # Most common superpower among heros with only one power
    one_power = hero_powers[amt_powers == 1]
    one_most_common = one_power.sum().sort_values(ascending=False).index[0]
    return [most_powers, fly_most_common, one_most_common]


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def clean_heroes(heroes):
    return heroes.replace([-99.0, '-'], [np.nan, np.nan])


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def super_hero_stats():
    return ['Onslaught', 'George Lucas', 'bad', 'Marvel Comics', 'NBC - Heroes', 'Groot']


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def clean_universities(df):
    df_copy = df.copy()
    df_copy['institution'] = df_copy['institution'].str.replace('\n', ', ')
    df_copy['broad_impact'] = df_copy['broad_impact'].astype(int)
    df_copy['nation'] = df_copy['national_rank'].str.split(',').str[0]
    df_copy['national_rank_cleaned'] = df_copy['national_rank'].str.split(',').str[1].astype(int)
    df_copy['nation'] = df_copy['nation'].replace({'UK': 'United Kingdom', 'USA': 'United States', 'Czechia': 'Czech Republic'})
    df_copy = df_copy.drop(columns=['national_rank'])
    df_copy['is_r1_public'] = (df_copy['control'] == 'Public') & df_copy['control'].notnull() & df_copy['city'].notnull() & df_copy['state'].notnull()
    return df_copy

def university_info(cleaned):
    # 1. stat whose universities have the lowest mean score
    states_grouped = cleaned['state'].value_counts()[lambda x: x >= 3].index.tolist()
    lowest_scoring_state = cleaned[cleaned['state'].isin(states_grouped)].groupby('state')['score'].mean().idxmin()

    # 2 proportion of institutions in the top 100 for which the quality of faculty ranking is also in the top 100
    prop_hq_faculty = cleaned[(cleaned['world_rank'] <= 100) & (cleaned['quality_of_faculty'] <= 100)].shape[0] / 100

    # 3 the number of states where at least 50% of the institutions are private
    num_public_states = cleaned.groupby('state')['is_r1_public'].mean()[lambda x: x < 0.5].size

    # 4 the lowest ranked institution in the world that is the highest ranked university in its nation
    low_rank_num_1 = cleaned[cleaned['national_rank_cleaned'] == 1].sort_values(by='world_rank').iloc[-1]['institution']

    return [lowest_scoring_state, prop_hq_faculty, num_public_states, low_rank_num_1]