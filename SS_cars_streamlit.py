

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
df_avg_price_mileage = df_Car.groupby(['Model', 'Manuf'])[['Price', 'Mileage']].mean().reset_index()
st.dataframe(df_avg_price_mileage)

# 2. Count of Model Details per Manuf
df_count_model_details = df_Car.groupby('Manuf')['Model Details'].count().reset_index(name='Count Model')
st.dataframe(df_count_model_details)

# Use st.container to organize the widget and chart inside a container
with st.container():
    # Multi-select widget to filter manufacturers
    selected_models = st.multiselect(
        'Select Manufacturer(s)',
        options=df_avg_price_mileage['Manuf'].unique(),
        default=df_avg_price_mileage['Manuf'].unique()
    )

    # Filter the DataFrame based on selected manufacturers
    filtered_df = df_avg_price_mileage[df_avg_price_mileage['Manuf'].isin(selected_models)]

    # Scatter chart showing filtered data
    st.scatter_chart(
        filtered_df,
        x="Price",
        y="Mileage",
        color="Model",
    )


st.bar_chart(df_count_model_details, x="Manuf", y="Count Model", color="Count Model")

# 3. Average year by Model Details
df_avg_year = df_Car.groupby('Model Details')['Year'].mean().reset_index()
st.dataframe(df_avg_year)




