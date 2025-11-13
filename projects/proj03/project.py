# project.py


import pandas as pd
import numpy as np
from pathlib import Path
import re
import requests
import time


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def get_book(url):
    pure_text = requests.get(url).text
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"

    start_idx = pure_text.find(start_marker)
    end_idx = pure_text.find(end_marker)

    start_line_end = pure_text.find("\n", start_idx)
    content = pure_text[start_line_end:end_idx]
    content = content.replace('\r\n', '\n')
    return content

# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def tokenize(book_string):
    # add \x02 before paragraphs
    book_string = re.sub(r'(?<=\n{2})(?=\S)', ' \x02 ', book_string)
    # add \x03 after paragraphs
    book_string = re.sub(r'(?<=\S)(?=\n{2})', ' \x03 ', book_string)
    # remove all \n values that repeat more than twice
    book_string = re.sub(r'\n{2,}', '', book_string)
    # split based on spaces
    tokens = book_string.replace("\n", " ").split()
    if tokens[-1] != '\x03':
        tokens.append('\x03')
    return tokens

# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


class UniformLM(object):


    def __init__(self, tokens):

        self.mdl = self.train(tokens)
        
    def train(self, tokens):
        uniq_tokens = list(set(tokens))
        num_tokens = len(uniq_tokens)
        return pd.Series({token: 1/num_tokens for token in uniq_tokens})
    
    def probability(self, words):
        prob = 1
        for word in words:
            prob *= self.mdl.get(word, 0)
            if prob == 0: return 0
        return prob
        
    def sample(self, M):
        probs = np.full(len(self.mdl.index), 1/len(self.mdl.index))
        return ' '.join(np.random.choice(self.mdl.index, size=M, replace=True, p=probs))


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


class UnigramLM(object):
    
    def __init__(self, tokens):
        self.mdl = self.train(tokens)
    
    def train(self, tokens):
        count_dict = {}
        for token in tokens:
            count_dict[token] = 1 + count_dict.get(token, 0)
        return pd.Series(count_dict) / len(tokens)
    
    def probability(self, words):
        prob = 1
        for word in words:
            prob *= self.mdl.get(word, 0)
            if prob == 0: return 0
        return prob
        
    def sample(self, M):
        return ' '.join(np.random.choice(self.mdl.index, size=M, replace=True, p=self.mdl.values))


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


class NGramLM(object):
    
    def __init__(self, N, tokens):
        # You don't need to edit the constructor,
        # but you should understand how it works!
        
        self.N = N

        ngrams = self.create_ngrams(tokens)

        self.ngrams = ngrams
        self.mdl = self.train(ngrams)

        if N < 2:
            raise Exception('N must be greater than 1')
        elif N == 2:
            self.prev_mdl = UnigramLM(tokens)
        else:
            self.prev_mdl = NGramLM(N-1, tokens)

    def create_ngrams(self, tokens):
        ngrams = []
        for i in range(len(tokens) - self.N + 1):
            ngrams.append(tuple(tokens[i:i+self.N]))
        return ngrams
        
    def train(self, ngrams):
        # Grab initial ngram probabilities (how many times does each ngram appear in the set of ngrams)
        def create_counts_series(ngrams):
            ngram_counts_dict = {}
            for ngram in ngrams:
                ngram_counts_dict[ngram] = 1 + ngram_counts_dict.get(ngram, 0)
            ngram_counts = pd.DataFrame.from_dict(
                ngram_counts_dict,
                orient='index', columns=['count']
            )
            return ngram_counts

        # Get n1grams from the ngrams
        n1grams_from_ngrams = []
        n1grams_from_ngrams = [ngram[:self.N-1] for ngram in ngrams]

        # get the ngram and n1gram counts
        ngram_counts = create_counts_series(ngrams)
        n1grams_from_ngrams_counts = create_counts_series(n1grams_from_ngrams)
        ngram_counts['n1gram'] = ngram_counts.index.map(lambda x: x[:self.N-1])

        # compute conditional probabilities
        ngram_counts['next_token_count'] = ngram_counts['n1gram'].map(n1grams_from_ngrams_counts['count']).fillna(0)
        ngram_counts['prob'] = ngram_counts['count'] / ngram_counts['next_token_count']

        return ngram_counts.reset_index(names='ngram').drop(columns=['count', 'next_token_count'])
    
    def probability(self, words):
        n1_splits = []
        curr_prob = 1
        curr_mdl = self.prev_mdl
        
        # Handle prefixes shorter than N
        curr_len = 1
        while curr_len < self.N and curr_len <= len(words):
            n1_splits.append(tuple(words[:curr_len]))
            curr_len += 1
        for split in n1_splits:
            curr_mdl = self.prev_mdl
            target_mdl_N = len(split)
            while hasattr(curr_mdl, 'N') and curr_mdl.N > target_mdl_N:
                curr_mdl = curr_mdl.prev_mdl
            # print(curr_mdl.mdl.head())

            if isinstance(curr_mdl.mdl, pd.DataFrame):
                row = curr_mdl.mdl.loc[curr_mdl.mdl['ngram'] == split, 'prob']
                # print(row)
                if row.empty: return 0
                curr_prob *= row.values[0]
                # print(curr_prob)
            else:
                val = curr_mdl.mdl.loc[split[0]]
                # print(val)
                curr_prob *= val
                # print(curr_prob)
        
        # Handle N-gram possibilities
        for i in range(len(words) - self.N + 1):
            ngram = tuple(words[i:i+self.N])
            row = self.mdl.loc[self.mdl['ngram'] == ngram, 'prob']
            if row.empty: return 0
            curr_prob *= row.values[0]
        
        return curr_prob
    
    def sample(self, M):
        output = ['\x02']
        
        def find_sample_given_model(model, input):
            # print("Finding next word from", input, "in model with size", model.N)
            matching_rows = model[model['n1gram'] == input]
            # print("Found matching rows")
            # print(matching_rows)
            if matching_rows.empty:
                return '\x03'
            sampled_value = matching_rows.sample(n=1, weights='prob')['ngram'].values[0][-1]
            # print("Value sampled is", sampled_value)
            return sampled_value

        # step 1 - find all samples for values less than N
        for num in range(2, self.N):
            # print("Current value of num: ", num)
            curr_model = self.prev_mdl
            while curr_model.N > num:
                #print("Moved down by 1 to", curr_model.N)
                curr_model = curr_model.prev_mdl
            # print("Value of the current model's N: ", curr_model.N)
            # print(curr_model.mdl.head())
            output.append(find_sample_given_model(curr_model.mdl, tuple(output)))

        # step 2 - find all samples for values greater than N
        for num in range(self.N, M+1):
            search_tuple = tuple(output[-self.N+1:])
            # print("Search tuple:", search_tuple)
            output.append(find_sample_given_model(self.mdl, search_tuple))
        
        output.append('\x03')
        return ' '.join(output)
