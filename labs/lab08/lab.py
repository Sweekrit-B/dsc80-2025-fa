# lab.py


import pandas as pd
import numpy as np
import plotly.express as px
import statsmodels.api as sm
from pathlib import Path
from sklearn.preprocessing import Binarizer, QuantileTransformer, FunctionTransformer

import warnings
warnings.filterwarnings('ignore')


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def best_transformation():
    return 1


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------



def create_ordinal(df):
    cut_map = {
        'Fair': 0,
        'Good': 1,
        'Very Good': 2,
        'Premium': 3,
        'Ideal': 4
    }
    color_map = {
        'J': 0,
        'I': 1,
        'H': 2,
        'G': 3,
        'F': 4,
        'E': 5,
        'D': 6
    }
    clarity_map = {
        'I1': 0,
        'SI2': 1,
        'SI1': 2,
        'VS2': 3,
        'VS1': 4,
        'VVS2': 5,
        'VVS1': 6,
        'IF': 7
    }
    def encode_ordinal(ordinal_df, reference_df, col, mapping):
        ordinal_df = ordinal_df.copy()
        ordinal_df['ordinal_' + col] = reference_df[col].map(mapping)
        return ordinal_df

    ordinal_df = pd.DataFrame()
    ordinal_df = encode_ordinal(ordinal_df, df, 'cut', cut_map)
    ordinal_df = encode_ordinal(ordinal_df, df, 'color', color_map)
    ordinal_df = encode_ordinal(ordinal_df, df, 'clarity', clarity_map)
    return ordinal_df


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------



def create_one_hot(df):

    def create_one_hot_helper(one_hot_df, reference_df, col):
        one_hot_df = one_hot_df.copy()
        for category in reference_df[col].unique():
            one_hot_df[f'one_hot_{col}_{category}'] = (reference_df[col] == category).astype(int)
        return one_hot_df

    one_hot_df = pd.DataFrame()
    one_hot_df = create_one_hot_helper(one_hot_df, df, 'cut')
    one_hot_df = create_one_hot_helper(one_hot_df, df, 'color')
    one_hot_df = create_one_hot_helper(one_hot_df, df, 'clarity')

    return one_hot_df


def create_proportions(df):

    def encode_proportions(ordinal_df, reference_df, col):
        ordinal_df = ordinal_df.copy()
        ordinal_df['proportion_' + col] = reference_df[col].map(reference_df[col].value_counts(normalize=True))
        return ordinal_df

    encode_prop_df = pd.DataFrame()
    encode_prop_df = encode_proportions(encode_prop_df, df, 'cut')
    encode_prop_df = encode_proportions(encode_prop_df, df, 'color')
    encode_prop_df = encode_proportions(encode_prop_df, df, 'clarity')
    return encode_prop_df

# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def create_quadratics(df):
    import itertools
    cols = list(df.select_dtypes(include=['number']).columns)
    cols.remove('price')
    pairs = list(itertools.combinations(cols, 2))

    quad_df = pd.DataFrame()

    for pair in pairs:
        quad_df[f'{pair[0]} * {pair[1]}'] = df[pair[0]] * df[pair[1]]

    return quad_df


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------



def comparing_performance():
    # create a model per variable => (variable, R^2, RMSE) table
    return [0.8493305264354858, 1548.5331930613174, 'x', 'carat * x', 'ordinal_color', 1434.840008904733]


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


class TransformDiamonds(object):
    
    def __init__(self, diamonds):
        self.data = diamonds
        
    # Question 6.1
    def transform_carat(self, data):
        from sklearn.preprocessing import Binarizer
        bi = Binarizer(threshold=1.0)
        return bi.fit_transform(data[['carat']])
    
    # Question 6.2
    def transform_to_quantile(self, data):
        from sklearn.preprocessing import QuantileTransformer
        qt = QuantileTransformer(n_quantiles=100)
        qt.fit(self.data[['carat']])
        return qt.transform(data[['carat']])

    
    # Question 6.3
    def transform_to_depth_pct(self, data):
        def depth_pct(X):
            x, y, z = X['x'], X['y'], X['z']
            return ((2 * z) / (x + y)) * 100
        ft = FunctionTransformer(depth_pct)
        return ft.transform(data[['x', 'y', 'z']])
