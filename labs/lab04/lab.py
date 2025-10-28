# lab.py


import pandas as pd
import numpy as np
import io
from pathlib import Path
import os


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def prime_time_logins(login):
    # Define the groupby aggregation function to determine if a value is between 4 PM and 8 PM
    def between_4_and_8(ser):
        return ser[(ser.dt.hour >= 16) & (ser.dt.hour < 20)].shape[0]
    
    # Create a copy of the existing dataframe
    login_copy = login.copy()
    # Convert the 'Time' column to datetime format to ensure clean aggregation
    login_copy['Time'] = pd.to_datetime(login_copy['Time'])
    # Return the grouped dataframe with the aggregation applied
    return login_copy.groupby('Login Id').agg(between_4_and_8)


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def count_frequency(login):
    # Define the groupby aggregation function to calculate login frequency
    def count_frequency_agg(ser):
        # Sort dates in ascending order (lowest date at the top)
        ser = ser.sort_values(ascending=True)
        # Grab the oldest date
        oldest_date = ser.iloc[0]
        # Calculate the difference between the current date and the oldest date
        num_days = (pd.to_datetime('2024-01-31 11:59:00 PM') - oldest_date).days
        # Calculate the number of logins by the user
        num_logins = ser.shape[0]
        # Return the frequency of logins
        return num_logins / num_days

    # Create a copy of the existing dataframe
    login_copy = login.copy()
    # Convert the 'Time' column to datetime format to ensure clean aggregation
    login_copy['Time'] = pd.to_datetime(login_copy['Time'])
    # Return the grouped dataframe with the aggregation applied
    return login_copy.groupby('Login Id').agg(count_frequency_agg)


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def cookies_null_hypothesis():
    return [2]
            
def cookies_p_value(N):
    N_cookies = 250
    observed_burnt = 15
    # simulate under the null hypothesis
    burnt_simulation = np.random.multinomial(N_cookies, [0.04, 0.96], size=100_000)[:, 0]
    # calculate the p value
    return (np.array(burnt_simulation) >= observed_burnt).mean()


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def car_null_hypothesis():
    # We expect the tires to be worse than claimed, so the null hypothesis should reflect the tires performing as claimed
    return [1, 4]

def car_alt_hypothesis():
    # We expect the tires to be worse than claimed, so the alternative hypothesis should reject the tires performing worse than claimed
    return [2, 6]

def car_test_statistic():
    return [1, 4]

def car_p_value():
    return 4


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def superheroes_test_statistic():
    return [1]
    
def bhbe_col(heroes):
    # Define the boolean series for blond hair and blue eyes
    bhbe_col = (heroes['Hair color'].str.lower().str.contains('blond')) & (heroes['Eye color'].str.lower().str.contains('blue'))
    return bhbe_col

def superheroes_observed_statistic(heroes):
    # Create a copy of the heroes dataframe
    heroes_copy = heroes.copy()
    # Add the bhbe column to the dataframe
    heroes_copy['bhbe'] = bhbe_col(heroes_copy)
    # Calculate the number of good bhbe heroes
    num_good_bhbe = heroes_copy[heroes_copy['bhbe'] & (heroes_copy['Alignment'] == 'good')].shape[0]
    # Return the proportion of good bhbe heroes as the observed statistic
    return num_good_bhbe / heroes_copy['bhbe'].sum()

def simulate_bhbe_null(heroes, N):
    # Calculate the number of bhbe heroes
    num_bhbe_heroes = bhbe_col(heroes).sum()
    # Calculate the overall proportion of good heroes for simulation
    prop_good = (heroes['Alignment'] == 'good').mean()
    # Simulate the null distribution -> multinomial distribution of the regular distribution of good vs. not good to see if the bhbe heroes align with that
    simulated_stats = np.random.multinomial(num_bhbe_heroes, [prop_good, 1 - prop_good], size = N)[:, 0] / num_bhbe_heroes
    # Return the list of simulated values given a size N
    return simulated_stats

def superheroes_p_value(heroes):
    # Calculate the observed statistic for bhbe heroes
    observed_stat = superheroes_observed_statistic(heroes)
    # Simulate the null distribution 100000 times
    simulated_stats = simulate_bhbe_null(heroes, 100_000)
    # Calculate the p-value based on the simulated statistics
    p_value = (np.array(simulated_stats) >= observed_stat).mean()
    # Return the p-value and the hypothesis test result
    if p_value < 0.01:
        return p_value, 'Reject'
    else:
        return p_value, 'Fail to reject'


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def diff_of_means(data, col='orange'):
    # Get the skittles from Waco
    waco_skittles = data[data['Factory'] == 'Waco']
    # Get the skittles from Yorkville
    yorkville_skittles = data[data['Factory'] == 'Yorkville']
    # Return the absolute difference in means of the skittles from Waco and the skittles from Yorkville
    return abs(waco_skittles[col].mean() - yorkville_skittles[col].mean())


def simulate_null(data, col='orange'):
    # Create a copy of the data to shuffle
    data_shuffled = data.copy()
    # Shuffle the 'Factory' column to simulate the null hypothesis
    data_shuffled = data_shuffled[[col, 'Factory']]
    data_shuffled['Factory'] = np.random.permutation(data_shuffled['Factory'])
    # Calculate the difference of means for the shuffled data
    difference = diff_of_means(data_shuffled, col)
    return difference


def color_p_value(data, col='orange'):
    # Define the number of repetitions for the simulation
    n_repetitions = 1000
    differences = []
    # Simulate the null distribution n_repetitions times
    for _ in range(n_repetitions):
        differences.append(simulate_null(data, col))
    # Calculate the observed difference in means
    observed_difference = diff_of_means(data, col)
    # Calculate the p-value based on the simulated differences
    p_value = (np.array(differences) >= observed_difference).mean()
    return p_value


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def ordered_colors():
    return [('yellow', 0.0), ('orange', 0.045), ('red', 0.212), ('green', 0.471), ('purple', 0.968)]


# ---------------------------------------------------------------------
# QUESTION 8
# ---------------------------------------------------------------------


    
def same_color_distribution():
    return (0.004, 'Reject')


# ---------------------------------------------------------------------
# QUESTION 9
# ---------------------------------------------------------------------


def perm_vs_hyp():
    return ['P', 'P', 'H', 'H', 'P']
