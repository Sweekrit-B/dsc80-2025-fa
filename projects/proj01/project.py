# project.py


import pandas as pd
import numpy as np
from pathlib import Path

import plotly.express as px


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def get_assignment_names(grades):
    assignments = {}
    # Iterate through every column
    for col in grades.columns:
        # Get the first word in the assignment name to make comparison easier
        assignment_name = col.split()[0]
        # If statement chain to sort columns into dictionary
        if 'checkpoint' in assignment_name.lower(): 
            general_area = 'checkpoint'
        elif 'lab' in assignment_name.lower():
            general_area = 'lab'
        elif 'project' in assignment_name.lower():
            general_area = 'project'
        elif 'midterm' in assignment_name.lower():
            general_area = 'midterm'
        elif 'final' in assignment_name.lower():
            general_area = 'final'
        elif 'disc' in assignment_name.lower():
            general_area = 'disc'
        elif 'hw' in assignment_name.lower():
            general_area = 'homework'
        else:
            continue
        
        # If the item does not already exist in the dictionary...
        if general_area not in assignments:
            assignments[general_area] = [col]
        else:
            # If the specific assignment is not already in the dictionary...
            if assignment_name not in assignments[general_area]:
                assignments[general_area].append(col)
    return assignments


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def projects_total(grades):
    # Filter out project columns (ignoring checkpoints and lateness)
    projects = grades[[col for col in grades.columns if 'project' in col.lower() and 'checkpoint' not in col.lower() and 'lateness' not in col.lower()]]
    
    # Define a function that determines the score for a single project on a per row basis
    def project_score(row):
        total_score = 0
        total_points = 0
        for col in row.index:
            if 'Max Points' in col:
                total_points += row[col]
            else: # it's a score column
                total_score += row[col]
        return total_score / total_points

    # Step 1: transpose the database so that projects are rows and students are columns
    # Step 2: group by project name (and ignore the free response part of the name)
    # Step 3: aggregate by applying the project_score function defined above
    # Step 4: transpose back so that students are rows and projects are columns
    # Step 5: fill NaNs with 0 (in case a student didn't do a project)
    per_project = projects.T.groupby(lambda x: x.split()[0].split('_')[0]).agg(project_score).T.fillna(0)
    return per_project.mean(axis=1)

# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def lateness_penalty(col):
    # Define a function to calculate lateness for students
    def penalty(val):
        # Convert to pd.Timedelta to ensure easy comparison
        val = pd.to_timedelta(val)
        if val > pd.Timedelta(hours=2) and val <= pd.Timedelta(weeks=1):
            return 0.9
        elif val > pd.Timedelta(weeks=1) and val <= pd.Timedelta(weeks=2):
            return 0.7
        elif val > pd.Timedelta(weeks=2):
            return 0.4
    
    # Default value is 1 because if NA assume assignment is not late
    return col.apply(penalty).fillna(1)


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def process_labs(grades):
    # Filter out lab columns
    labs = grades[[col for col in grades.columns if 'lab' in col.lower()]]
    
    # Redefine the penalty function inside the process_labs function
    def penalty(val):
        val = pd.to_timedelta(val)
        if val > pd.Timedelta(hours=2) and val <= pd.Timedelta(weeks=1):
            return 0.9
        elif val > pd.Timedelta(weeks=1) and val <= pd.Timedelta(weeks=2):
            return 0.7
        elif val > pd.Timedelta(weeks=2):
            return 0.4
        
    # Define a function that determines the score for a single lab on a per row basis
    def lab_score(row):
        total_score = 0
        total_points = 0
        lateness_multiplier = 1
        for col in row.index:
            if 'Max Points' in col:
                total_points += row[col]
            elif 'Lateness' in col:
                time = pd.to_timedelta(row[col])
                lateness_multipler = penalty(time) if penalty(time) else 1
            else: # it's a score column
                total_score += row[col]
        score = total_score / total_points
        changed_score = score * lateness_multipler
        return changed_score

    # Step 1: transpose the database so that labs are rows and students are columns
    # Step 2: group by lab name (and ignore the free response part of the name
    # Step 3: aggregate by applying the lab_score function defined above
    # Step 4: transpose back so that students are rows and labs are columns
    # Step 5: fill NaNs with 0 (in case a student didn't do a lab)
    process_labs = labs.T.groupby(lambda x: x.split()[0]).agg(lab_score).T.fillna(0)
    return process_labs



# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def lab_total(processed):
    # Define a function that computes the lab total by dropping the lowest score
    def compute_score(row):
        return ((sum(row) - min(row)) / (len(row) - 1))

    return processed.apply(compute_score, axis=1).fillna(0)
                                                                               



# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def total_points(grades):
    
    # Define a generalized function for finding the average score
    def find_avg_score(row, value):
        value_sum = 0
        value_total = 0

        for col in row.index:
            if value.lower() in col.lower():
                if 'Lateness' not in col:
                    if 'Max Points' in col:
                        value_total += row[col]
                    else:
                        value_sum += row[col]
        
        return value_sum / value_total
    
    # Apply that generalized function along the columns of the dataset and fill missing values with 0s
    checkpoints = grades.apply(lambda x: find_avg_score(x, 'checkpoint'), axis=1).fillna(0)
    discussions = grades.apply(lambda x: find_avg_score(x, 'discussion'), axis=1).fillna(0)
    midterms = grades.apply(lambda x: find_avg_score(x, 'midterm'), axis=1).fillna(0)
    finals = grades.apply(lambda x: find_avg_score(x, 'final'), axis=1).fillna(0)

    # Return everyone's weighted scores
    return 0.025 * checkpoints + 0.025 * discussions + 0.15 * midterms + 0.3 * finals + projects_total(grades) * 0.3 + lab_total(process_labs(grades)) * 0.2


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def final_grades(total):
    # Define a function that converts a numeric score to a letter grade
    def letter_grade(val):
        if val >= 0.9:
            return 'A'
        elif val >= 0.8:
            return 'B'
        elif val >= 0.7:
            return 'C'
        elif val >= 0.6:
            return 'D'
        else:
            return 'F'
    
    return total.apply(letter_grade)

def letter_proportions(total):
    # Apply that function to the total Series and return a Series of normalized value counts
    letters = final_grades(total).value_counts(normalize=True)
    print(letters)
    return letters


# ---------------------------------------------------------------------
# QUESTION 8
# ---------------------------------------------------------------------


def raw_redemption(final_breakdown, question_numbers):
    ...
    
def combine_grades(grades, raw_redemption_scores):
    ...


# ---------------------------------------------------------------------
# QUESTION 9
# ---------------------------------------------------------------------


def z_score(ser):
    ...
    
def add_post_redemption(grades_combined):
    ...


# ---------------------------------------------------------------------
# QUESTION 10
# ---------------------------------------------------------------------


def total_points_post_redemption(grades_combined):
    ...
        
def proportion_improved(grades_combined):
    ...


# ---------------------------------------------------------------------
# QUESTION 11
# ---------------------------------------------------------------------


def section_most_improved(grades_analysis):
    ...
    
def top_sections(grades_analysis, t, n):
    ...


# ---------------------------------------------------------------------
# QUESTION 12
# ---------------------------------------------------------------------


def rank_by_section(grades_analysis):
    ...







# ---------------------------------------------------------------------
# QUESTION 13
# ---------------------------------------------------------------------


def letter_grade_heat_map(grades_analysis):
    ...
