
#%%

import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
import re

##from pydrive.auth import GoogleAuth
##from pydrive.drive import GoogleDrive
##import pygsheets
##import streamlit as st
import numpy as np
from datetime import datetime

#%%
def get_last_page_number(base_url, headers=None):
    response = requests.get(base_url, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the last page link using the given example structure
    last_page_link = soup.find('a', class_='navi', rel='prev')
    if last_page_link:
        href = last_page_link['href']
        # Extract the page number from the URL
        last_page_num = int(href.split('page')[-1].split('.html')[0])
        return last_page_num
    else:
        return 1  # Default to 1 if no pagination is found

def generate_page_urls(base_url, last_page_num):
    page_urls = [f"{base_url}page{i}.html" for i in range(1, last_page_num + 1)]
    return page_urls


# %%


def get_advertisement_urls(page_url, base_url='https://www.ss.com'):
    """
    Given a page URL, this function extracts and returns a list of full advertisement URLs from that page.
    """
    response = requests.get(page_url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all <a> tags with the class 'am' (which likely contain the ads' URLs)
    ad_links = soup.find_all('a', class_='am')
    
    # Construct the full URLs
    ad_urls = [base_url + link['href'] for link in ad_links]
    
    return ad_urls

def gather_all_advertisement_urls(page_urls):
    """
    This function takes a list of page URLs and returns a complete list of all advertisement URLs from those pages.
    """
    all_ad_urls = []
    
    for page_url in page_urls:
        ad_urls = get_advertisement_urls(page_url)
        all_ad_urls.extend(ad_urls)
    
    return all_ad_urls


#%%

    # URL (adjust to the correct base URL)
base_url = 'https://www.ss.com/lv/transport/cars/bmw/'


#%%


    # Optional: Define headers to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
    
    # Get the last page number
last_page_num = get_last_page_number(base_url, headers)
    
    # Generate all page URLs
page_urls = generate_page_urls(base_url, last_page_num)

#%%

# Generate all adverts URLs
all_advertisement_urls = gather_all_advertisement_urls(page_urls)
    
# %%
