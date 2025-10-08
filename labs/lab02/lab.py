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
        most_common = df[col].value_counts()[:N]
        # Add the indices + values and pad the remaining with np.nan
        final_df[col + '_values'] = most_common.index + [np.nan] * max(0, (N - len(most_common)))
        final_df[col + '_counts'] = most_common.values + [np.nan] * max(0, (N - len(most_common)))
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
    ...


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def super_hero_stats():
    ...


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def clean_universities(df):
    ...

def university_info(cleaned):
    ...

