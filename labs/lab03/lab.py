# lab.py


import os
import io
from pathlib import Path
import pandas as pd
import numpy as np


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def read_linkedin_survey(dirname):
    dirname = Path(dirname)

    # Define a function to normalize the columns of a dataframe
    def normalize_cols(df):
        df.columns = df.columns.str.lower()
        df.columns = df.columns.str.replace('_', ' ')
        return df

    # Define a list for which we add dataframes to
    dfs = []

    # For each path in the directory:
    #   1. Read the CSV as a dataframe
    #   2. Normalize the columns of the dataframe
    #   3. Append the dataframe to the list

    for path in list(dirname.iterdir()):
        df = pd.read_csv(str(path))
        df = normalize_cols(df)
        dfs.append(df)

    # Concatenate the dataframes and reset the index
    combined = pd.concat(dfs, ignore_index=True)
    combined = combined.reset_index(drop=True)
    return combined


def com_stats(df):
    df_copy = df.fillna('')
    # Proportion of people with 'Programmer' in their job title who went to a university with 'Ohio" in it
    ohio_programmers = df_copy[df_copy['job title'].str.contains('Programmer') & df_copy['university'].str.contains('Ohio')].shape[0] / df_copy.shape[0]
    # Number of job titles that end in 'Engineer'
    engineer_job_titles = df_copy[df_copy['job title'].str.split().str[-1] == 'Engineer']['job title'].nunique()
    # Job title with the longest name
    longest_name_job_titles = max(df_copy['job title'].fillna('').unique(), key=len)
    # Number of people with manager in their job title
    manager_job_titles = df_copy['job title'].str.lower().str.contains('manager').sum()
    return [ohio_programmers, engineer_job_titles, longest_name_job_titles, manager_job_titles]

# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def read_student_surveys(dirname):
    dirname = Path(dirname)
    final_df = None

    for path in list(dirname.iterdir()):
        df = pd.read_csv(str(path))
        if final_df is None:
            final_df = df
        else:
            final_df = pd.merge(final_df, df, on='id')

    return final_df.set_index('id')


def check_credit(df):
    # Step 0 - replace '(no genres listed)' with np.nan to invalidate it as a response
    df_copy = df.copy()
    df_copy = df_copy.replace('(no genres listed)', np.nan)
    df_copy = df_copy.reset_index()
    df_copy = df_copy.set_index(['id', 'name'])
    
    # Step 1 - for each student, check whether they answered at least half the questions
    df_copy['ec'] = df_copy.isna().mean(axis=1) < 0.5
    df_copy['ec'] = df_copy['ec'].map({True: 5, False: 0})

    # Step 2 - check how many questions had more than 90% of the class answer --> -1 to remove the 'ec' column
    class_ec = min((df_copy.isna().mean(axis=0) < 0.1).sum() - 1, 2)
    df_copy['ec'] += class_ec

    df_copy = df_copy.reset_index()
    return df_copy[['name', 'ec']]


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def most_popular_procedure(pets, procedure_history):
    # Inner join because we only care about pets who have had procedures done on them
    pet_procedures = pd.merge(pets, procedure_history, how='inner', on='PetID')
    procedure_value_counts = pet_procedures['ProcedureType'].value_counts()
    return procedure_value_counts.sort_values(ascending=False).index[0]

def pet_name_by_owner(owners, pets):
    # Do an inner join on the owner
    owners_and_pets = pd.merge(owners, pets, how='inner', on='OwnerID')

    # Define a function for the groupby
    def get_str_or_list(ser):
        if len(ser) == 1:
            return ser.iloc[0]
        return list(ser)

    # Group by the owner ID and first name and provide a string or a list of pet names
    owners_and_pets_grouped = pd.DataFrame(owners_and_pets.groupby(['OwnerID', 'Name_x'])['Name_y'].agg(get_str_or_list))
    # Reset the indices and drop the unnecessary columns
    owners_and_pets_grouped = owners_and_pets_grouped.reset_index().drop(columns='OwnerID')
    # Rename the columns to be more descriptive
    owners_and_pets_grouped.columns = ['Owner Name', 'Pet Name(s)']
    # Set the index of the dataframe
    owners_and_pets_grouped = owners_and_pets_grouped.set_index('Owner Name')
    
    return owners_and_pets_grouped


def total_cost_per_city(owners, pets, procedure_history, procedure_detail):
    # Combine the procedures with their details --> inner join because procedures that do not have details are "invalid" (and don't exist)
    detailed_procedures = pd.merge(procedure_history, procedure_detail, how='inner', on=['ProcedureType', 'ProcedureSubCode'])
    # Combine the pets with their procedures --> left join because we want every pet's information whether they have had a procedure or not, but don't care about every procedure if it's not associated with a pet in our dataset
    pets_detailed_procedures = pd.merge(pets, detailed_procedures, how='left', on='PetID')
    # Merge owners with pets --> inner rjoin because we don't care about pets that don't have owners since we are looking at the city in the owners dataframe
    owners_pets_detailed_procedures = pd.merge(owners, pets_detailed_procedures, how='inner', on='OwnerID')
    # Groupby the city and obtain the sum of the procedures that took place in that city
    city_grouped_price = owners_pets_detailed_procedures.groupby('City')['Price'].sum()

    return city_grouped_price


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def average_seller(sales):
    # Define the pivot table
    average_seller_pivot = sales.pivot_table(values='Total', index='Name', aggfunc='mean')
    # Rename the columns
    average_seller_pivot.columns = ['Average Sales']
    return average_seller_pivot

def product_name(sales):
    return sales.pivot_table(index='Name', columns='Product', values='Total', aggfunc='sum')

def count_product(sales):
    return sales.pivot_table(index=['Product', 'Name'], columns='Date', values='Total', aggfunc='sum').fillna(0)

def total_by_month(sales):
    # Create a copy of the sales
    sales_copy = sales.copy()
    # Create a month column
    sales_copy['Month'] = sales_copy['Date'].str.split('.').str[0]
    # Define the month map
    month_map = {
        '01': 'January', '02': 'February', '03': 'March',
        '04': 'April', '05': 'May', '06': 'June',
        '07': 'July', '08': 'August', '09': 'September',
        '10': 'October', '11': 'November', '12': 'December'
    }
    # Remap the month values
    sales_copy['Month'] = sales_copy['Month'].map(month_map)
    # Create the pivot table
    return sales_copy.pivot_table(index=['Product', 'Name'], columns='Month', values='Total', aggfunc='sum').fillna(0)
