

#%%

import pandas as pd
#from pydrive.auth import GoogleAuth
#from pydrive.drive import GoogleDrive
#import pygsheets
import streamlit as st
import numpy as np
from datetime import datetime

 

url = 'https://raw.githubusercontent.com/ri-oz/Cars-Analytics/main/CarData.csv'

df_Car = pd.read_csv(url, index_col=0, sep=';')

# Title

st.title('Auto Cenu pārskats Latvijā')


# Description

st.text('Datu analīzes projekts par auto pārdošanu un cenām Latvijā.')


# Create a section for the dataframe statistics

st.header('Datu statistiskā anaīze')
st.write(df_Car.describe())

# Create a section for the dataframe
st.header('Sludinājumu dati')
st.dataframe(df_Car)



# 1. Average price and mileage per Model Details and Manuf
df_avg_price_mileage = df_Car.groupby(['Model Details', 'Manuf'])[['Price', 'Mileage']].mean().reset_index()
st.dataframe(df_avg_price_mileage)

# 2. Count of Model Details per Manuf
df_count_model_details = df_Car.groupby('Manuf')['Model Details'].count().reset_index(name='Count Model')
st.dataframe(df_count_model_details)

st.bar_chart(df_count_model_details)
st.bar_chart(df_count_model_details, x="Manuf", y="Count", color="col3")

# 3. Average year by Model Details
df_avg_year = df_Car.groupby('Model Details')['Year'].mean().reset_index()
st.dataframe(df_avg_year)




