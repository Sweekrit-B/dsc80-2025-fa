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
            if 'free_response' in assignment_name.lower():
                continue
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
    project_grades = pd.Series(0, index=grades.index, dtype=float)

    for project in get_assignment_names(grades)['project']:
        points = grades[project].fillna(0)
        max_points = grades[project + ' - Max Points'].fillna(1)

        free_response = project + '_free_response'
        free_response_max_points = free_response + ' - Max Points'

        if free_response in grades.columns:
            points += grades[free_response].fillna(0)
            max_points += grades[free_response_max_points].fillna(1)
        
        project_grades += points / max_points
    
    return project_grades / len(get_assignment_names(grades)['project'])


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
    # Define a dataframe to hold the processed lab grades
    lab_grades = pd.DataFrame(index=grades.index)
    # Iterate through each lab assignment from Q1
    for lab in get_assignment_names(grades)['lab']:
        # Fill in all missing values with 0s for points and 1s for max points
        points = grades[lab].fillna(0)
        max_points_col = lab + ' - Max Points'
        max_points = grades[max_points_col].fillna(1)
        # Calculate the raw score using points and max points
        raw_score = points / max_points

        # Grab the lateness column
        lateness = grades[lab + ' - Lateness (H:M:S)']
        # Calculate the penalty using the lateness column
        penalty = lateness_penalty(lateness)
        # Calculate the final score after applying the penalty
        final_score = raw_score * penalty
        # Fill in the lab grades dataframe with the final score
        lab_grades[lab] = final_score
    # Fill in any remaining stray missing values with 0
    return lab_grades.fillna(0)



# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def lab_total(processed):
    # Define a function that computes the lab total by dropping the lowest score
    return (processed.sum(axis = 1) - processed.min(axis = 1)) / (processed.shape[1] - 1)                                                                    

# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def total_points(grades):
    # Define a function to compute the mean of assignments
    def mean_assignments(grades, assignment):
        # Get the relevant columns for the assignment type
        cols = get_assignment_names(grades)[assignment]
        # Create a dataframe to hold the divided scores (divided by assignment)
        divided = pd.DataFrame()
        # For each column...
        for col in cols:
            # Grab the column with the max points
            max_points_col = col + ' - Max Points'
            # Grab the column with the score and max points and fill missing values
            scores = grades[col].fillna(0)
            max_points = grades[max_points_col].fillna(1)
            # Divide the scores by the max points and add to the divided dataframe
            divided[col] = scores / max_points
        # Return the divided dataframe for future use
        return divided.mean(axis=1)
    
    # Apply that generalized function along the columns of the dataset and fill missing values with 0s
    checkpoints = mean_assignments(grades, 'checkpoint').fillna(0)
    discussions = mean_assignments(grades, 'disc').fillna(0)
    labs = lab_total(process_labs(grades)).fillna(0)
    projects = projects_total(grades).fillna(0)
    midterms = (grades['Midterm'] / grades['Midterm - Max Points']).fillna(0)
    finals = (grades['Final'] / grades['Final - Max Points']).fillna(0)

    # Return everyone's weighted scores
    return 0.2 * labs + 0.3 * projects + 0.15 * midterms + 0.3 * finals + 0.025 * discussions + 0.025 * checkpoints


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
    return letters


# ---------------------------------------------------------------------
# QUESTION 8
# ---------------------------------------------------------------------


def raw_redemption(final_breakdown, question_numbers):
    # Grab the total from the column names of the final breakdown dataframe
    total = sum(float(final_breakdown.columns[i].split('(')[1].split()[0]) for i in question_numbers)
    # Calculate the earned points by:
    #   1) selecting appropriate columns using the question_numbers list provided
    #   2) summing the values along the 1st axis 
    earned_points = final_breakdown.iloc[:, question_numbers].sum(axis=1)
    # Grab the PID as a dataframe from the final_breakdown columns
    raw_redemption_scores = final_breakdown[['PID']].copy()
    # Fill in the raw redemption scores and fill the NA values with 0
    raw_redemption_scores['Raw Redemption Score'] = (earned_points / total).fillna(0)
    return raw_redemption_scores
    
def combine_grades(grades, raw_redemption_scores):
    # Merge these redemption scores with the PID
    return grades.merge(raw_redemption_scores, on='PID', how='left').fillna(0)


# ---------------------------------------------------------------------
# QUESTION 9
# ---------------------------------------------------------------------


def z_score(ser):
    return (ser - ser.mean()) / ser.std(ddof=0)
    
def add_post_redemption(grades_combined):
    def reverse_z_score(z_scores, ser):
        # Reverse z-score function to get score based on z-score
        return z_scores * ser.std(ddof=0) + ser.mean()
    
    redemption_scores = grades_combined['Raw Redemption Score']
    midterm_scores = grades_combined['Midterm'].fillna(0) / grades_combined['Midterm - Max Points']

    grades_combined['Midterm Score Pre-Redemption'] = midterm_scores
    # Calculate the z score of the student's raw redemption score
    z_score_redemption = z_score(redemption_scores)
    # Calculate the z score of the student's pre-redemption score
    z_score_midterm = z_score(midterm_scores)
    # Determine the maximum of the two z scores
    z_score_max = pd.Series(np.maximum(z_score_redemption, z_score_midterm))
    # Calculate the new test score using the reverse z-score calculation
    grades_combined['Midterm Score Post-Redemption'] = reverse_z_score(z_score_max, midterm_scores).clip(upper=1)
    return grades_combined



# ---------------------------------------------------------------------
# QUESTION 10
# ---------------------------------------------------------------------


def total_points_post_redemption(grades_combined):
    # Calculate the initial grade using the previious total_points function
    initial_grade = total_points(grades_combined)
    # Find the pre-redemption midterm scores using the combined grades dataset
    initial_midterms = grades_combined['Midterm Score Pre-Redemption']
    # After redemption score
    new_midterms = grades_combined['Midterm Score Post-Redemption']
    # Midterm added points
    midterm_add = (new_midterms - initial_midterms) * 0.15
    # Find the new grade
    final_scores = initial_grade + midterm_add
    return final_scores
        
def proportion_improved(grades_combined):
    # Define the function for finding the letter grade
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
    
    # Define a mapping for efficient grade checking
    grade_order = {'A': 5, 'B': 4, 'C': 3, 'D': 2, 'F': 1}
    # Find grades for students without redemption
    initial_grade = total_points(grades_combined)
    initial_letter_grade = initial_grade.apply(letter_grade).map(grade_order)
    # Find grades for students with redemption
    grade_after_redemption = total_points_post_redemption(grades_combined)
    final_letter_grade = grade_after_redemption.apply(letter_grade).map(grade_order)
    # Find the number of students for which their grade after redemption was better than their grade before redemption
    num_improved = (final_letter_grade > initial_letter_grade).sum()
    # Find the ratio of the number that improved divided by the number of students
    return num_improved / grades_combined.shape[0]

# ---------------------------------------------------------------------
# QUESTION 11
# ---------------------------------------------------------------------


def section_most_improved(grades_analysis):
    # Define a function that determines if each individual student saw an increase in their letter grade
    def increase_in_letter_grade(row):
        grades = ['A', 'B', 'C', 'D', 'F']
        pre_redemption_letter_index = grades.index(row['Letter Grade Pre-Redemption'])
        post_redemption_letter_index = grades.index(row['Letter Grade Post-Redemption'])
        return post_redemption_letter_index < pre_redemption_letter_index
    
    # Create a copy for grades analysis
    grades_analysis_copy = grades_analysis.copy()
    # Use .apply on axis=1 to determine if the student improved
    grades_analysis_copy['Letter Grade Improved'] = grades_analysis_copy[['Letter Grade Pre-Redemption', 'Letter Grade Post-Redemption']].apply(increase_in_letter_grade, axis=1)
    # Steps to find the most improved section:
    #   1. Group by the section
    #   2. Grab the "Letter Grade Improved" column and find the mean
    #   3. Sort the values and grab the top indexed value
    return grades_analysis_copy.groupby('Section')['Letter Grade Improved'].mean().sort_values(ascending=False).index[0]
    
def top_sections(grades_analysis, t, n):
    # Define a function to calculate the amount of students that meet the cutoff
    def amt_of_cutoff_students(ser):
        return (ser > t).sum()

    # Create a copy for grade analysis
    grades_analysis_copy = grades_analysis.copy()
    # Calculate the final exam score as a new column
    grades_analysis_copy['Final Exam Score'] = (grades_analysis_copy['Final'] / grades_analysis_copy['Final - Max Points']).fillna(0)
    # Group by the section and aggregate by the amoount of students that met the cutoff
    num_greater_than_cutoff = grades_analysis_copy.groupby('Section')['Final Exam Score'].agg(amt_of_cutoff_students)
    # Return an np.array of sections where the amount of students that met the cutoff is greater than t
    return np.array(num_greater_than_cutoff[num_greater_than_cutoff > n].index)



# ---------------------------------------------------------------------
# QUESTION 12
# ---------------------------------------------------------------------


def rank_by_section(grades_analysis):
    # Creates a copy of grades analysis
    grades_analysis_copy = grades_analysis.copy()
    # Determine the final exam score using the final and final max points
    grades_analysis_copy['Final Exam Score'] = (grades_analysis_copy['Final'] / grades_analysis_copy['Final - Max Points']).fillna(0)
    # Sorts values by section and then final exam score for order preservation later on
    grades_analysis_copy = grades_analysis_copy.sort_values(['Section', 'Final Exam Score'], ascending=[True, False])
    # Splits by section and creates a cumulative count -> adds 1 to start from 1 instead of 0
    grades_analysis_copy['Section Rank'] = grades_analysis_copy.groupby('Section').cumcount() + 1
    # Returns the pivot with the NA values filled with empty strings
    return grades_analysis_copy.pivot(
        index='Section Rank',
        columns='Section',
        values='PID',
    ).fillna('')


# ---------------------------------------------------------------------
# QUESTION 13
# ---------------------------------------------------------------------


def letter_grade_heat_map(grades_analysis):
    # Use value counts to get letter grade proportions based on each section
    letter_grades_per_section = grades_analysis.groupby('Section')['Letter Grade Post-Redemption'].value_counts(normalize=True).reset_index()
    # Pivot the dataframe to get the columns as the section and the grade as the rows
    letter_pivot = letter_grades_per_section.pivot(
        index='Letter Grade Post-Redemption',
        columns='Section',
        values='proportion'
    ).fillna(0)
    # Reindex to follow grade order
    grade_order = ['A', 'B', 'C', 'D', 'F']
    letter_pivot = letter_pivot.reindex(grade_order)
    # Create the heatmap
    fig = px.imshow(letter_pivot, color_continuous_scale='Viridis_r', title='Distribution of Letter Grades by Section')
    return fig
