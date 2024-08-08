
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


# Helper function to get the BeautifulSoup object from a URL
def get_url_text_html(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.content, 'html.parser')

# 1. Get the Model of the car
def get_car_model(url):
    soup = get_url_text_html(url)
    model_soup = soup.find(id="tdo_31")
    return model_soup.get_text(strip=True) if model_soup else "NA"

# 2. Get the Year of the car
def get_car_year(url):
    soup = get_url_text_html(url)
    year_soup = soup.find(id="tdo_18")
    return year_soup.get_text(strip=True) if year_soup else "NA"

# 3. Get the Type of Motor of the car
def get_car_motor_type(url):
    soup = get_url_text_html(url)
    motor_type_soup = soup.find(id="tdo_15")
    return motor_type_soup.get_text(strip=True) if motor_type_soup else "NA"

# 4. Get the Transmission of the car
def get_car_transmission(url):
    soup = get_url_text_html(url)
    transmission_soup = soup.find(id="tdo_35")
    return transmission_soup.get_text(strip=True) if transmission_soup else "NA"

# 5. Get the Mileage of the car
def get_car_mileage(url):
    soup = get_url_text_html(url)
    mileage_soup = soup.find(id="tdo_16")
    return mileage_soup.get_text(strip=True) if mileage_soup else "NA"

# 6. Get the Color of the car
def get_car_color(url):
    soup = get_url_text_html(url)
    color_soup = soup.find(id="tdo_17")
    if color_soup:
        color_text = color_soup.get_text(strip=True)
        # Extract the first word (which is the color) before any additional details like 'metālika'
        color = color_text.split()[0]
        return color
    return "NA"

# 7. Get the Body Type of the car
def get_car_body_type(url):
    soup = get_url_text_html(url)
    body_type_soup = soup.find(id="tdo_32")
    return body_type_soup.get_text(strip=True) if body_type_soup else "NA"

# 8. Get the Price of the car
def get_car_price(url):
    soup = get_url_text_html(url)
    price_soup = soup.find(id="tdo_8")
    return price_soup.get_text(strip=True) if price_soup else "NA"

# Example of gathering all details for one ad
def gather_car_details(url):
    details = {
        "Model": get_car_model(url),
        "Year": get_car_year(url),
        "Motor Type": get_car_motor_type(url),
        "Transmission": get_car_transmission(url),
        "Mileage": get_car_mileage(url),
        "Color": get_car_color(url),
        "Body Type": get_car_body_type(url),
        "Price": get_car_price(url)
    }
    return details


# Gather and print details for the given ad URL
car_details = gather_car_details()
  
