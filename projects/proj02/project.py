# project.py


import pandas as pd
import numpy as np
from pathlib import Path

import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
pd.options.plotting.backend = 'plotly'

from IPython.display import display

# DSC 80 preferred styles
pio.templates["dsc80"] = go.layout.Template(
    layout=dict(
        margin=dict(l=30, r=30, t=30, b=30),
        autosize=True,
        width=600,
        height=400,
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True),
        title=dict(x=0.5, xanchor="center"),
    )
)
pio.templates.default = "simple_white+dsc80"
import warnings
warnings.filterwarnings("ignore")


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def clean_loans(loans):
    def offset_date(row):
        return row['issue_d'] + pd.DateOffset(months=row['term'])
    
    loans_copy = loans.copy()
    loan_issue_ids = loans_copy['issue_d'].str.replace('-', ' ')
    loans_copy['issue_d'] = pd.to_datetime(loan_issue_ids, format="%b %Y")
    loans_copy['term'] = loans_copy['term'].str.split().str[0].astype(int)
    loans_copy['emp_title'] = loans_copy['emp_title'].str.lower().str.strip().apply(lambda x: 'registered nurse' if x.lower() == 'rn' else x)
    loans_copy['term_end'] = loans_copy.apply(offset_date, axis=1)
    return loans_copy

# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------



def correlations(df, pairs):
    series = pd.Series()
    for pair in pairs:
        name = 'r_' + pair[0] + '_' + pair[1]
        series[name] = df[pair[0]].corr(df[pair[1]])
    return series




# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def create_boxplot(loans):
    fico_map = {(580, 669): '[580, 670)', (670, 739): '[670, 740)', (740, 799): '[740, 800)', (800, 850): '[800, 850)'}
    custom_colors = ['purple', 'gold']

    def get_fico_category(score):
        for (low, high), category in fico_map.items():
            if low <= score <= high:
                return category

    loans_copy = loans.copy()
    loans_copy['fico_category'] = loans_copy['fico_range_low'].apply(get_fico_category)
    loans_copy = loans_copy.sort_values('fico_range_low')
    return px.box(loans_copy, x='fico_category', y='int_rate', color='term', color_discrete_sequence=custom_colors, labels={'fico_category': 'Credit Score Range', 'int_rate': 'Interest Rate (%)', 'term': 'Loan Length (Months)'}, title='Interest Rate vs. Credit Score')



# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def ps_test(loans, N):
    # Create a copy of the loans dataframe
    loans_copy = loans.copy()
    # Define the has_ps column
    loans_copy['has_ps'] = loans_copy['desc'].notna()
    # Retrieve the relevant columns from the dataframe
    loans_copy = loans_copy[['int_rate', 'has_ps']]
    # Calculate the observed statistic
    int_rate_by_ps = loans_copy.groupby('has_ps')['int_rate'].mean()
    diff_by_ps = int_rate_by_ps[True] - int_rate_by_ps[False]
    # Define the list to hold the simulated statistics
    simulated_diffs = []
    # Simulate the null distribution (that there is no difference) N times
    for _ in range(N):
        # Shuffle the has_ps column
        loans_copy['shuffled_has_ps'] = np.random.permutation(loans_copy['has_ps'])
        # Compute the test statistic for the shuffled data
        int_rate_by_ps_shuffled = loans_copy.groupby('shuffled_has_ps')['int_rate'].mean()
        diff_by_ps_shuffled = int_rate_by_ps_shuffled[True] - int_rate_by_ps_shuffled[False]
        # Append the simulated difference to the list
        simulated_diffs.append(diff_by_ps_shuffled)
    # Calculate the p value
    p_value = (np.array(simulated_diffs) >= diff_by_ps).mean()
    return p_value
    
def missingness_mechanism():
    return 2
    
def argument_for_nmar():
    '''
    Put your justification here in this multi-line string.
    Make sure to return your string!
    '''
    return "Personal statements might be NMAR because applicants who have weaker reasons to take a loan or fear that their reason for taking the loan might reflect poorly on their finanicial responsibility might omit their personal statement altogether."

# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def tax_owed(income, brackets):
    tax = 0
    for i in range(len(brackets)):
        rate, lower = brackets[i]
        if i+1 < len(brackets):
            upper = brackets[i + 1][1]
        else:
            upper = float('inf')
        taxable_income = min(income, upper) - lower
        if taxable_income > 0:
            tax += taxable_income * rate
    return tax



# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def clean_state_taxes(state_taxes_raw): 
    def drop_all_nulls(df):
        return df.dropna(how='all')

    def clean_state_column(df):
        df = df.copy()
        df['State'] = (
            df['State']
            .replace(r'.*\(.*', np.nan, regex=True)
            .fillna(method='ffill')
        )
        return df

    def clean_rate_column(df):
        df = df.copy()
        df['Rate'] = (
            df['Rate']
            .str.replace('none', '0.00')
            .str.replace('%', '')
            .astype(float) / 100
        )
        df['Rate'] = df['Rate'].round(2)
        return df

    def clean_lower_limit_column(df):
        df = df.copy()
        df['Lower Limit'] = (
            df['Lower Limit']
            .str.replace('$', '')
            .str.replace(',', '')
            .fillna('0')
            .astype(int)
        )
        return df

    state_taxes_raw_cleaned = (state_taxes_raw
        .pipe(drop_all_nulls)
        .pipe(clean_state_column)
        .pipe(clean_rate_column)
        .pipe(clean_lower_limit_column)
    )

    return state_taxes_raw_cleaned


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def state_brackets(state_taxes):
    state_tax_brackets = state_taxes.groupby('State').apply(lambda x: list(zip(x['Rate'], x['Lower Limit'])))
    state_tax_brackets = state_tax_brackets.to_frame(name='bracket_list')
    return state_tax_brackets
    
def combine_loans_and_state_taxes(loans, state_taxes):
    # Start by loading in the JSON file.
    # state_mapping is a dictionary; use it!
    import json
    state_mapping_path = Path('data') / 'state_mapping.json'
    with open(state_mapping_path, 'r') as f:
        state_mapping = json.load(f)
        
    # Now it's your turn:
    state_tax_brackets = state_brackets(state_taxes).reset_index()
    state_tax_brackets['State'] = state_tax_brackets['State'].map(state_mapping)
    loans_copy = loans.copy()
    loans_copy = loans_copy.merge(state_tax_brackets, how="left", left_on='addr_state', right_on='State').drop(columns=['addr_state'])
    return loans_copy


# ---------------------------------------------------------------------
# QUESTION 8
# ---------------------------------------------------------------------


def find_disposable_income(loans_with_state_taxes):
    FEDERAL_BRACKETS = [
        (0.1, 0), 
        (0.12, 11000), 
        (0.22, 44725), 
        (0.24, 95375), 
        (0.32, 182100),
        (0.35, 231251),
        (0.37, 578125)
    ]
    loans_with_state_taxes_copy = loans_with_state_taxes.copy()
    loans_with_state_taxes_copy['federal_tax_owed'] = loans_with_state_taxes_copy.apply(lambda x: tax_owed(x['annual_inc'], FEDERAL_BRACKETS), axis=1)
    loans_with_state_taxes_copy['state_tax_owed'] = loans_with_state_taxes_copy.apply(lambda x: tax_owed(x['annual_inc'], x['bracket_list']), axis=1)
    loans_with_state_taxes_copy['disposable_income'] = loans_with_state_taxes_copy['annual_inc'] - loans_with_state_taxes_copy['federal_tax_owed'] - loans_with_state_taxes_copy['state_tax_owed']
    return loans_with_state_taxes_copy


# ---------------------------------------------------------------------
# QUESTION 9
# ---------------------------------------------------------------------


def aggregate_and_combine(loans, keywords, quantitative_column, categorical_column):
    dfs_list = []
    loans_copy = loans.copy()
    for keyword in keywords:
        loans_copy_keyword =  loans_copy[loans_copy['emp_title'].str.contains(keyword)]
        cat_col_keyword = loans_copy_keyword.groupby(categorical_column)[quantitative_column].mean()
        cat_col_keyword['OVERALL'] = loans_copy_keyword[quantitative_column].mean()
        cat_col_keyword = cat_col_keyword.to_frame(name=f'{keyword}_mean_{quantitative_column}')
        dfs_list.append(cat_col_keyword)
    final_df = pd.concat(dfs_list, axis=1)
    return final_df


# ---------------------------------------------------------------------
# QUESTION 10
# ---------------------------------------------------------------------


def exists_paradox(loans, keywords, quantitative_column, categorical_column):
    paradox_df = aggregate_and_combine(loans, keywords, quantitative_column, categorical_column)
    return (paradox_df.iloc[:, 0] > paradox_df.iloc[:, 1]).to_list() == [True, True, True, False]

    
def paradox_example(loans):
    return {
        'loans': loans,
        'keywords': ['teacher', 'manager'],
        'quantitative_column': 'loan_amnt',
        'categorical_column': 'verification_status'
    }
