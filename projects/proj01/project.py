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
    for col in grades.columns:
        assignment_name = col.split()[0]
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
        
        if general_area not in assignments:
            assignments[general_area] = [col]
        else:
            if assignment_name not in assignments[general_area]:
                assignments[general_area].append(col)
    return assignments


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def projects_total(grades):
    projects = grades[[col for col in grades.columns if 'project' in col.lower() and 'checkpoint' not in col.lower() and 'lateness' not in col.lower()]]
    
    def project_score(row):
        total_score = 0
        total_points = 0
        for col in row.index:
            if 'Max Points' in col:
                total_points += row[col]
            else: # it's a score column
                total_score += row[col]
        return total_score / total_points

    per_project = projects.T.groupby(lambda x: x.split()[0].split('_')[0]).agg(project_score).T.fillna(0)
    return per_project.mean(axis=1)

# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def lateness_penalty(col):
    def penalty(val):
        val = pd.to_timedelta(val)
        if val > pd.Timedelta(hours=2) and val <= pd.Timedelta(weeks=1):
            return 0.9
        elif val > pd.Timedelta(weeks=1) and val <= pd.Timedelta(weeks=2):
            return 0.7
        elif val > pd.Timedelta(weeks=2):
            return 0.4
    
    return col.apply(penalty).fillna(1)


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def process_labs(grades):
    labs = grades[[col for col in grades.columns if 'lab' in col.lower()]]

    def penalty(val):
        val = pd.to_timedelta(val)
        if val > pd.Timedelta(hours=2) and val <= pd.Timedelta(weeks=1):
            return 0.9
        elif val > pd.Timedelta(weeks=1) and val <= pd.Timedelta(weeks=2):
            return 0.7
        elif val > pd.Timedelta(weeks=2):
            return 0.4

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
        return total_score / total_points * lateness_multiplier

    process_labs = labs.T.groupby(lambda x: x.split()[0]).agg(lab_score).T.fillna(0)
    return process_labs



# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def lab_total(processed):
    def compute_score(row):
        return ((sum(row) - min(row)) / (len(row) - 1))

    return processed.apply(compute_score, axis=1).fillna(0)
                                                                               



# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def total_points(grades):
    def checkpoints_discussions_exams(row):
        ch_sum = 0
        ch_total = 0
        disc_sum = 0
        disc_total = 0

        midterm_sum = 0
        midterm_total = 0
        final_sum = 0
        final_total = 0
        for col in row.index:
            if 'checkpoint' in col.lower():
                if 'Lateness' not in col:
                    if 'Max Points' in col:
                        ch_total += row[col]
                    else:
                        ch_sum += row[col]
            elif 'disc' in col.lower():
                if 'Lateness' not in col:
                    if 'Max Points' in col:
                        disc_total += row[col]
                    else:
                        disc_sum += row[col]
            elif 'midterm' in col.lower():
                if 'Lateness' not in col:
                    if 'Max Points' in col:
                        midterm_total += row[col]
                    else:
                        midterm_sum += row[col]
            elif 'final' in col.lower():
                if 'Lateness' not in col:
                    if 'Max Points' in col:
                        final_total += row[col]
                    else:
                        final_sum += row[col]
        return 0.025 * (ch_sum / ch_total) + 0.025 * (disc_sum / disc_total) + 0.15 * (midterm_sum / midterm_total) + 0.30 * (final_sum / final_total)

    checkpoints_discussions_exams = grades.apply(checkpoints_discussions_exams, axis=1).fillna(0)
    return projects_total(grades) * 0.3 + lab_total(process_labs(grades)) * 0.2 + checkpoints_discussions_exams


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def final_grades(total):
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
