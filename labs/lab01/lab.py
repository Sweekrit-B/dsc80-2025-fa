# lab.py


from pathlib import Path
import io
import pandas as pd
import numpy as np
np.set_printoptions(legacy='1.21')


# ---------------------------------------------------------------------
# QUESTION 0
# ---------------------------------------------------------------------


def consecutive_ints(ints):
    if len(ints) == 0:
        return False

    for k in range(len(ints) - 1):
        diff = abs(ints[k] - ints[k+1])
        if diff == 1:
            return True

    return False


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def median_vs_mean(nums):
    nums = sorted(nums)
    n = len(nums)
    if n % 2 == 1:
        median = nums[n // 2]
    else:
        median = (nums[n // 2 - 1] + nums[n // 2]) / 2
    mean = sum(nums) / n
    return median <= mean


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def n_prefixes(s, n):
    final_str = ""
    for i in range(n, -1, -1):
        final_str += s[:i]
    return final_str


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def exploded_numbers(ints, n):
    max_len = len(str(sorted(ints)[-1] + n))
    final_list = []
    for int in ints:
        current = ""
        for i in range(int - n, int + n + 1):
            current_num = str(i).zfill(max_len)
            current += current_num + " "
        final_list.append(current.strip())
    return final_list
            


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def last_chars(fh):
    lines = fh.readlines()
    final_str = ""
    for line in lines:
        line = line.strip()
        if len(line) > 0:
            final_str += line[-1]
    return final_str


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def add_root(A):
    output_arr = []
    for i in range(len(A)):
        output_arr.append(A[i] + np.sqrt(i))
    return np.array(output_arr)
    

def where_square(A):
    output_arr = []
    for i in range(len(A)):
        if np.sqrt(A[i]) % 1 == 0:
            output_arr.append(True)
        else:
            output_arr.append(False)
    return np.array(output_arr)


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def filter_cutoff_loop(matrix, cutoff):
    output_matrix = []
    for i in range(len(matrix[0])): # iterate through each column
        col_sum = 0 # initialize the sum for each column
        for j in range(len(matrix)): # iterate through each row
            col_sum += matrix[j, i] # add each element into the column sum
        if col_sum/len(matrix[0]) > cutoff: # if the mean of the column is greater than the cutoff
            output_matrix.append(matrix[:, i]) # append the entire column as a numpy array to the output matrix
    return np.array(output_matrix) # return the output matrix as a numpy array
        


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def filter_cutoff_np(matrix, cutoff):
    col_means = np.mean(matrix, axis=0) # compute the mean of each column by "compressing" along axis 0
    return matrix[:, col_means > cutoff] # return the columns where the mean is greater than the cutoff


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def growth_rates(A):
    diff = (A[1:] - A[:-1]) # compute difference -> everything but the first minus everything but the last allows for a difference between each consecutive element
    growth_rate = diff / A[:-1] # divide the difference by everything but the last to get the growth 
    return np.round(growth_rate, 2)

def with_leftover(A):
    leftover = 20 % A # determine the leftover each day by taking the modulus of 20 and A
    cumulative = np.cumsum(leftover) # compute the cumulative sum array of the leftover array
    days = np.where(cumulative >= A)[0] # determine the indices where the cumulative sum is greater than or equal to A
    return days[0] if days.size > 0 else -1 # return the first index if it exists, otherwise return -1

# ---------------------------------------------------------------------
# QUESTION 8
# ---------------------------------------------------------------------


def salary_stats(salary):
    # Initialize the series
    indices = ['num_players', 'num_teams', 'total_salary', 'highest_salary', 'avg_los', 'fifth_lowest', 'duplicates', 'total_highest']
    stats = pd.Series(index=indices, dtype='float64')
    # Number of players
    stats['num_players'] = len(salary['Player'])
    # Number of teams
    stats['num_teams'] = salary['Team'].nunique()
    # Total salary amount for all players
    stats['total_salary'] = salary['Salary'].sum()
    # Player with the highest salary
    stats['highest_salary'] = salary[salary['Salary'] == salary['Salary'].max()]['Player'].values[0]
    # Average salary for the Los Angeles Lakers
    stats['avg_los'] = round(salary[salary['Team'] == 'Los Angeles Lakers']['Salary'].mean(), 2)
    # Name and team of the player with who has the fifth lowest salary
    fifth_lowest = salary[salary['Salary'] == salary['Salary'].nsmallest(5).max()][['Player', 'Team']]
    stats['fifth_lowest'] = f"{fifth_lowest['Player'].iloc[0]}, {fifth_lowest['Team'].iloc[0]}"
    # Whether there are any duplicate last names
    last_names = salary['Player'].str.split().str[1]
    stats['duplicates'] = len(last_names) > len(last_names.unique())
    # Total salary of the team with the highest paid pllayer
    team_with_highest_Paid_player = salary[salary['Player'] == stats['highest_salary']]['Team'].values[0]
    stats['total_highest'] = salary[salary['Team'] == team_with_highest_Paid_player]['Salary'].sum()
    return stats

# ---------------------------------------------------------------------
# QUESTION 9
# ---------------------------------------------------------------------


def parse_malformed(fp):
    with open(fp) as fp:
        # Read all lines from the file
        lines = fp.readlines()
        # Extract the column header and remove it from lines
        col_header = lines[0]
        lines = lines[1:]
        # Initialize an empty list to hold processed rows
        rows = []
        for line in lines:
            # Clean the line by removing quotes and newline characters
            line = line.replace('"', '').replace('\n', '')
            # Split the line by commas
            split = line.split(',')
            # Remove empty strings from the split list
            split = [x for x in split if x != '']
            # Merge the last two elements to form the full location
            split[-2] = split[-2] + ',' + split[-1]
            # Remove the last element as it's now merged
            split.pop()
            # Convert the numeric fields to float
            split[2] = float(split[2].replace('"', ''))
            split[3] = float(split[3].replace('"', ''))
            # Append the cleaned and processed row to rows
            rows.append(split)
        # Create a DataFrame from the processed rows
        df = pd.DataFrame(rows, columns=col_header.strip().split(','))
        return df

