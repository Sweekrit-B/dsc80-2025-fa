# lab.py


import os
import pandas as pd
import numpy as np
import requests
import bs4
import lxml


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def question1():
    """
    NOTE: You do NOT need to do anything with this function.
    The function for this question makes sure you
    have a correctly named HTML file in the right
    place. Note: This does NOT check if the supplementary files
    needed for your page are there!
    """
    # Don't change this function body!
    # No Python required; create the HTML file.
    return


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------



def extract_book_links(text):
    soup = bs4.BeautifulSoup(text)
    res = []
    for product_pod in soup.find_all('article', class_='product_pod'):
        price = float(product_pod.find('p', class_='price_color').text.strip()[2:])
        rating = product_pod.find('p').get('class')[1]
        if rating in ['Four', 'Five'] and price < 50:
            res.append(product_pod.find('a').get('href'))
    return res

def get_product_info(text, categories):
    soup = bs4.BeautifulSoup(text)
    category = soup.find('ul', class_='breadcrumb').find_all('a')[-1].text.strip()
    if category in categories:
        product_type = soup.find('ul', class_='breadcrumb').find_all('a')[1].text.strip()
        upc = soup.find('th', string=lambda x: x.strip() == 'UPC').find_next_sibling('td').text.strip()
        price_excl_tax = soup.find('th', string=lambda x: x.strip() == 'Price (excl. tax)').find_next_sibling('td').text.strip()
        price_incl_tax = soup.find('th', string=lambda x: x.strip() == 'Price (incl. tax)').find_next_sibling('td').text.strip()
        tax = soup.find('th', string=lambda x: x.strip() == 'Tax').find_next_sibling('td').text.strip()
        availability = soup.find('th', string=lambda x: x.strip() == 'Availability').find_next_sibling('td').text.strip()
        num_reviews = soup.find('th', string=lambda x: x.strip() == 'Number of reviews').find_next_sibling('td').text.strip()
        rating = soup.find('p', class_='star-rating').get('class')[1]
        description = soup.find('div', id='product_description').find_next_sibling('p').text.strip()
        title = soup.find('div', class_='product_main').find('h1').text.strip()
        return {
            'UPC': upc,
            'Product Type': product_type,
            'Price (excl. tax)': price_excl_tax,
            'Price (incl. tax)': price_incl_tax,
            'Tax': tax,
            'Availability': availability,
            'Number of reviews': num_reviews,
            'Category': category,
            'Rating': rating,
            'Description': description,
            'Title': title
        }
    return None

def scrape_books(k, categories):
    rows = []

    def download_page_num(i):
        url = f'http://books.toscrape.com/catalogue/page-{i}.html'
        request = requests.get(url)
        return bs4.BeautifulSoup(request.text)

    def download_page_book(suffix):
        url = f'http://books.toscrape.com/catalogue/{suffix}'
        request = requests.get(url)
        return bs4.BeautifulSoup(request.text)
    
    for i in range(1, k+1):
        links = extract_book_links(download_page_num(i).prettify())
        for link in links:
            info = get_product_info(download_page_book(link).prettify(), categories)
            if info:
                rows.append(info)
    
    if rows:
        return pd.DataFrame(rows)
    else:
        return pd.DataFrame(columns=['UPC', 'Product Type', 'Price (excl. tax)', 'Price (incl. tax)', 'Tax', 'Availability', 'Number of reviews', 'Category', 'Rating', 'Description', 'Title'])


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def get_comments(storyid):
    rows = []

    def get_item(item_id):
        url=f'https://hacker-news.firebaseio.com/v0/item/{item_id}.json'
        return requests.get(url).json()

    def add_to_df(parsed_json):
        rows.append({
            'id': parsed_json.get('id'),
            'by': parsed_json.get('by'),
            'text': parsed_json.get('text'),
            'parent': parsed_json.get('parent'),
            'time': parsed_json.get('time')
        })

    visited = set()
    
    # Method 1 for DFS - recursion
    # def dfs(item_id):
    #     if item_id in visited:
    #         return
    #     visited.add(item_id)

    #     parsed_json = get_item(item_id)
    #     if not parsed_json:
    #         return
    #     if parsed_json.get('dead'):
    #         return 
        
    #     if parsed_json.get('type') == 'story':
    #         for kid in parsed_json.get('kids', []):
    #             dfs(kid)
    #         return

    #     add_to_df(parsed_json)
        
    #     for kid in parsed_json.get('kids', []):
    #         dfs(kid)

    # dfs(storyid)

    # Method 2 for DFS - stack
    stack = [storyid]
    visited = set()
    while stack:
        curr = stack.pop()
        if curr in visited:
            continue
        visited.add(curr)

        parsed_json = get_item(curr)
        if not parsed_json:
            continue
        if parsed_json.get('dead'):
            continue
        
        if parsed_json.get('type') == 'story':
            stack.extend(parsed_json.get('kids', [])[::-1])
        else:
            add_to_df(parsed_json)
            stack.extend(parsed_json.get('kids', [])[::-1])
    
    df = pd.DataFrame(rows)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df
