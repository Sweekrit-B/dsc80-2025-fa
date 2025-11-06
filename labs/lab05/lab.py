# lab.py


from pathlib import Path
import pandas as pd
import numpy as np
from scipy import stats


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def after_purchase():
    # 1. NMAR - people are more likely to review when satisfied
    # 2. MD - people who don't have accounts can't review, so missing by design
    # 3. MAR - people who return an item are more likely to review it
    # 4. MAR - people who bought certain items might be less likely to review it
    # 5. MAR - people who bought less expensive/trivial items might be less incentivized to review
    return ['NMAR', 'MD', 'MAR', 'MAR', 'MAR']


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def multiple_choice():
    # 1. MAR - people who choose an on campus restaurant likely don't have a delivery address for their orders
    # 2. NMAR - not everyone has a middle name
    # 3. MAR - the people who have 0 number_of_sports_played likely don't have any sports_previously_played
    # 4. NMAR - people who left the question blank were likely satisfied
    # 5. MCAR - since users must provide their phone number, the values are missing completely ar random
    return ['MAR', 'NMAR', 'MAR', 'NMAR', 'MCAR']


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def first_round():
    return [0.0779, 'NR']


def second_round():
    return [0.023496102828775643, 'R', 'D']


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def verify_child(heights):
    child_X_cols = heights.columns[2:]
    child_X_series = pd.Series(dtype=float)

    for child_X in child_X_cols:
        heights_copy = heights[['father', child_X]].copy()
        heights_copy['child_age_missing'] = heights_copy[child_X].isna()
        
        ks_p_value = stats.ks_2samp(
            heights_copy.loc[~heights_copy['child_age_missing'], 'father'],
            heights_copy.loc[heights_copy['child_age_missing'], 'father']
        ).pvalue
        
        child_X_series[child_X] = ks_p_value
    
    return child_X_series


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def cond_single_imputation(new_heights):
    new_heights_copy = new_heights.copy()
    new_heights_copy['father_quartile'] = pd.qcut(new_heights_copy['father'], 4, labels=[1, 2, 3, 4])
    new_heights_copy['child'] = new_heights_copy.groupby('father_quartile')['child'].transform(lambda x: x.fillna(x.mean()))
    return new_heights_copy['child']

# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def quantitative_distribution(child, N):
    observed = child.dropna()
    hist = np.histogram(observed, bins=10)
    probs, bins = hist[0]/hist[0].sum(), hist[1]
    
    imputed_vals = []

    for _ in range(N):
        bin_index = np.random.choice(range(len(probs)), p=probs)
        value = np.random.uniform(bins[bin_index], bins[bin_index+1])
        imputed_vals.append(value)
    
    return np.array(imputed_vals)


def impute_height_quant(child):
    child_copy = child.copy()
    n_missing = child_copy.isna().sum()
    imputed_vals = quantitative_distribution(child_copy, n_missing)
    child_copy.loc[child_copy.isna()] = imputed_vals
    return child_copy

# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def answers():
    return [1, 2, 2, 1], ['data.gov', 'instagram.com']
