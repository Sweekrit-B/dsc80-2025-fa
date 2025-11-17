# lab.py


import pandas as pd
import numpy as np
import os
import re


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def match_1(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_1("abcde]")
    False
    >>> match_1("ab[cde")
    False
    >>> match_1("a[cd]")
    False
    >>> match_1("ab[cd]")
    True
    >>> match_1("1ab[cd]")
    False
    >>> match_1("ab[cd]ef")
    True
    >>> match_1("1b[#d] _")
    True
    """
    pattern = r'^.{2}\[.{2}\].*'

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None


def match_2(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_2("(123) 456-7890")
    False
    >>> match_2("858-456-7890")
    False
    >>> match_2("(858)45-7890")
    False
    >>> match_2("(858) 456-7890")
    True
    >>> match_2("(858)456-789")
    False
    >>> match_2("(858)456-7890")
    False
    >>> match_2("a(858) 456-7890")
    False
    >>> match_2("(858) 456-7890b")
    False
    """
    pattern = r'^\(858\) \d{3}-\d{4}$'

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None


def match_3(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_3("qwertsd?")
    True
    >>> match_3("qw?ertsd?")
    True
    >>> match_3("ab c?")
    False
    >>> match_3("ab   c ?")
    True
    >>> match_3(" asdfqwes ?")
    False
    >>> match_3(" adfqwes ?")
    True
    >>> match_3(" adf!qes ?")
    False
    >>> match_3(" adf!qe? ")
    False
    """
    pattern = r'^[A-Za-z0-9 ?]{5,9}\?$'

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None


def match_4(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_4("$$AaaaaBbbbc")
    True
    >>> match_4("$!@#$aABc")
    True
    >>> match_4("$a$aABc")
    False
    >>> match_4("$iiuABc")
    False
    >>> match_4("123$$$Abc")
    False
    >>> match_4("$$Abc")
    True
    >>> match_4("$qw345t$AAAc")
    False
    >>> match_4("$s$Bca")
    False
    >>> match_4("$!@$")
    False
    """
    pattern = r'^\$[^abc$]*\$([aA])+([bB])+([cC])+'

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None


def match_5(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_5("dsc80.py")
    True
    >>> match_5("dsc80py")
    False
    >>> match_5("dsc80..py")
    False
    >>> match_5("dsc80+.py")
    False
    """
    pattern = r'^[A-Za-z0-9_]+\.py'

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None


def match_6(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_6("aab_cbb_bc")
    False
    >>> match_6("aab_cbbbc")
    True
    >>> match_6("aab_Abbbc")
    False
    >>> match_6("abcdef")
    False
    >>> match_6("ABCDEF_ABCD")
    False
    """
    pattern = r'^[a-z]+_[a-z]+$'

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None


def match_7(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_7("_abc_")
    True
    >>> match_7("abd")
    False
    >>> match_7("bcd")
    False
    >>> match_7("_ncde")
    False
    """
    pattern = r'^_.*_$'

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None



def match_8(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_8("ASJDKLFK10ASDO")
    False
    >>> match_8("ASJDKLFK0ASDo!!!!!!! !!!!!!!!!")
    True
    >>> match_8("JKLSDNM01IDKSL")
    False
    >>> match_8("ASDKJLdsi0SKLl")
    False
    >>> match_8("ASDJKL9380JKAL")
    True
    """
    pattern = r'^[^Oi1]+$'

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None



def match_9(string):
    '''
    DO NOT EDIT THE DOCSTRING!
    >>> match_9('NY-32-NYC-1232')
    True
    >>> match_9('ca-23-SAN-1231')
    False
    >>> match_9('MA-36-BOS-5465')
    False
    >>> match_9('CA-56-LAX-7895')
    True
    >>> match_9('NY-32-LAX-0000') # If the state is NY, the city can be any 3 letter code, including LAX or SAN!
    True
    >>> match_9('TX-32-SAN-4491')
    False
    '''
    pattern = r'^((CA-\d{2}-(SAN|LAX)-\d{4})|(NY-\d{2}-[A-Z]{3}-\d{4}))$'

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None


def match_10(string):
    '''
    DO NOT EDIT THE DOCSTRING!
    >>> match_10('ABCdef')
    ['bcd']
    >>> match_10(' DEFaabc !g ')
    ['def', 'bcg']
    >>> match_10('Come ti chiami?')
    ['com', 'eti', 'chi']
    >>> match_10('and')
    []
    >>> match_10('Ab..DEF')
    ['bde']
    
    '''
    sub_string = re.sub(r'[^\w]|a', '', string.lower())
    return re.findall(r'.{3}', sub_string)


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def extract_personal(s):
    email_pattern = r'[a-zA-Z0-9.]+@[a-zA-Z0-9.]+'
    email_list = re.findall(email_pattern, s)
    social_security_pattern = r'\d{3}-\d{2}-\d{4}'
    social_security_list = re.findall(social_security_pattern, s)
    bitcoin_pattern = r'bitcoin:[a-zA-Z0-9]+'
    bitcoin_list = re.findall(bitcoin_pattern, s)
    bitcoin_list = [b.replace('bitcoin:', '') for b in bitcoin_list if b[-4:] != 'null']
    street_address_pattern = r'\d+ \w+ \w+'
    street_address_list = re.findall(street_address_pattern, s)
    return (email_list, social_security_list, bitcoin_list, street_address_list)


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def tfidf_data(reviews_ser, review):
    review = review.lower()
    split_words = review.split()
    unique_words = np.unique(split_words)
    review_data = pd.DataFrame(columns=['cnt', 'tf', 'idf', 'tfidf'])

    for word in unique_words:
        re_word = fr'\b{word.lower()}\b'
        cnt = len(re.findall(re_word, review))
        tf = cnt / len(split_words)
        idf = np.log(len(reviews_ser) / (reviews_ser.str.contains(re_word).sum()))
        tfidf = tf * idf
        review_data.loc[word] = [cnt, tf, idf, tfidf]

    return review_data


def relevant_word(out):
    return out['tfidf'].idxmax()


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def hashtag_list(tweet_text):
    hashtag_pattern = r'#\S+'
    hashtags = tweet_text.apply(lambda x: re.findall(hashtag_pattern, x))
    hashtags = hashtags.apply(lambda lst: [tag[1:] for tag in lst])
    return hashtags


def most_common_hashtag(tweet_lists):
    hashtag_counts = {}
    
    for hashtag in tweet_lists.explode():
        hashtag_counts[hashtag] = hashtag_counts.get(hashtag, 0) + 1
    
    def get_most_common(lst):
        if not lst:
            return np.nan
        if len(lst) == 1:
            return lst[0]
        most_common = max(lst, key=lambda x: hashtag_counts[x])
        return most_common

    most_common = tweet_lists.apply(get_most_common)
    return most_common


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------

def create_features(ira):
    def cleanup_text(text):
        hashtag_pattern = r'#\S+'
        tag_pattern = r'@\S+'
        hyperlink_pattern = r'https?://\S+'
        non_text_pattern = r'[^a-zA-Z0-9 ]'
        # Step 1: Remove retweet information, hashtags, tags, and hyperlinks
        text = text.replace('RT ', ' ')
        text = re.sub(hashtag_pattern, ' ', text)
        text = re.sub(tag_pattern, ' ', text)
        text = re.sub(hyperlink_pattern, ' ', text)
        # Step 2: Remove non-text characters
        text = re.sub(non_text_pattern, ' ', text)
        # Step 3: Convert to lowercase
        text = text.lower()
        # Step 4: Remove extra spaces
        text = ' '.join(text.split())
        text = text.strip()
        return text

    hashtag_pattern = r'#\S+'
    tag_pattern = r'@\S+'
    hyperlink_pattern = r'https?://\S+'
    
    num_hashtags = ira['text'].apply(lambda x: len(re.findall(hashtag_pattern, x)))
    mc_hashtags = most_common_hashtag(hashtag_list(ira['text']))
    num_tags = ira['text'].apply(lambda x: len(re.findall(tag_pattern, x)))
    num_links = ira['text'].apply(lambda x: len(re.findall(hyperlink_pattern, x)))
    is_retweet = ira['text'].str.startswith('RT')
    text = ira['text'].apply(cleanup_text)

    return pd.DataFrame({'text': text, 'num_hashtags': num_hashtags, 'mc_hashtags': mc_hashtags, 'num_tags': num_tags, 'num_links': num_links, 'is_retweet': is_retweet})