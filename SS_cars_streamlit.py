

#%%

import pandas as pd
#from pydrive.auth import GoogleAuth
#from pydrive.drive import GoogleDrive
#import pygsheets
import streamlit as st
import numpy as np
from datetime import datetime

 

url = 'https://raw.githubusercontent.com/ri-oz/Cars-Analytics/main/CarData.csv'

df_Car = pd.read_csv(url, index_col=0)

# Drop error / na rows

df_Car.dropna(how='any')


df_Car_analytics_Model_skaits = df_Car['Model'].value_counts(ascending=True)

df_Car_analytics_Body_Type_skaits = df_Car['Body Type'].value_counts(ascending=True)

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


# overview section

st.header('Auto pārskats')

st.bar_chart(df_Car_analytics_Pilseta_skaits)

st.dataframe(df_Car_analytics_Pilseta_skaits)


# Type of land overview question

st.header('Body Type')

st.bar_chart(df_Car_analytics_Body_Type_skaits)

st.dataframe(df_Car_analytics_Body_Type_skaits)



