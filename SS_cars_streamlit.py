

#%%

import pandas as pd
#from pydrive.auth import GoogleAuth
#from pydrive.drive import GoogleDrive
#import pygsheets
import streamlit as st
import numpy as np
from datetime import datetime
import plotly.express as px

# Load the data
url = 'https://raw.githubusercontent.com/ri-oz/Cars-Analytics/main/CarData.csv'
data = pd.read_csv(url)

# Clean the data
data.dropna(inplace=True)
data['Price'] = pd.to_numeric(data['Price'], errors='coerce')
data['Mileage'] = pd.to_numeric(data['Mileage'], errors='coerce')
data.dropna(subset=['Price', 'Mileage'], inplace=True)

# Convert categorical columns to string
categorical_columns = ['Manuf', 'Model', 'Body Type', 'Transmission', 'Color', 'Motor Type_0', 'Motor Type_1']
for col in categorical_columns:
    data[col] = data[col].astype(str)

# Set Streamlit app layout
st.set_page_config(page_title='Car Sales Analytics', layout='wide')

# Sidebar filters
st.sidebar.header('Filter Options')

# Manufacturer filter
manufacturer = st.sidebar.multiselect('Select Manufacturer', options=data['Manuf'].unique(), default=data['Manuf'].unique())

# Model filter
model_options = data[data['Manuf'].isin(manufacturer)]['Model'].unique()
model = st.sidebar.multiselect('Select Model', options=model_options, default=model_options)

# Body Type filter
body_type_options = data['Body Type'].unique()
body_type = st.sidebar.multiselect('Select Body Type', options=body_type_options, default=body_type_options)

# Transmission filter
transmission_options = data['Transmission'].unique()
transmission = st.sidebar.multiselect('Select Transmission', options=transmission_options, default=transmission_options)

# Color filter
color_options = data['Color'].unique()
color = st.sidebar.multiselect('Select Color', options=color_options, default=color_options)

# Motor Type_0 filter (Size)
motor_size_options = data['Motor Type_0'].unique()
motor_size = st.sidebar.multiselect('Select Motor Size', options=motor_size_options, default=motor_size_options)

# Motor Type_1 filter (Type)
motor_type_options = data['Motor Type_1'].unique()
motor_type = st.sidebar.multiselect('Select Motor Type', options=motor_type_options, default=motor_type_options)

# Apply filters
filtered_data = data[
    (data['Manuf'].isin(manufacturer)) &
    (data['Model'].isin(model)) &
    (data['Body Type'].isin(body_type)) &
    (data['Transmission'].isin(transmission)) &
    (data['Color'].isin(color)) &
    (data['Motor Type_0'].isin(motor_size)) &
    (data['Motor Type_1'].isin(motor_type))
]

# Main Metrics
st.title('Car Sales Analytics Dashboard')
st.markdown('### Key Metrics')

col1, col2, col3 = st.columns(3)
with col1:
    avg_price = filtered_data['Price'].mean()
    st.metric('Average Price ($)', f"${avg_price:,.2f}")
    
with col2:
    avg_mileage = filtered_data['Mileage'].mean()
    st.metric('Average Mileage', f"{avg_mileage:,.2f} miles")
    
with col3:
    total_cars = len(filtered_data)
    st.metric('Total Cars in Selection', total_cars)

# Additional Metrics
col4, col5, col6 = st.columns(3)
with col4:
    popular_body_type = filtered_data['Body Type'].mode()[0] if not filtered_data.empty else 'N/A'
    st.metric('Most Common Body Type', popular_body_type)

with col5:
    popular_transmission = filtered_data['Transmission'].mode()[0] if not filtered_data.empty else 'N/A'
    st.metric('Most Common Transmission', popular_transmission)

with col6:
    popular_color = filtered_data['Color'].mode()[0] if not filtered_data.empty else 'N/A'
    st.metric('Most Common Color', popular_color)

# Price Distribution
st.markdown('### Price Distribution by Manufacturer')
fig1 = px.box(filtered_data, x='Manuf', y='Price', color='Manuf', title='Price Distribution by Manufacturer')
st.plotly_chart(fig1, use_container_width=True)

# Mileage Distribution
st.markdown('### Mileage Distribution by Manufacturer')
fig2 = px.box(filtered_data, x='Manuf', y='Mileage', color='Manuf', title='Mileage Distribution by Manufacturer')
st.plotly_chart(fig2, use_container_width=True)

# Sales Analysis
st.markdown('### Sales Analysis')

# Average Price by Body Type
st.markdown('#### Average Price by Body Type')
fig3 = px.bar(
    filtered_data.groupby('Body Type')['Price'].mean().reset_index(),
    x='Body Type', y='Price', color='Body Type',
    title='Average Price by Body Type'
)
st.plotly_chart(fig3, use_container_width=True)

# Average Mileage by Transmission
st.markdown('#### Average Mileage by Transmission')
fig4 = px.bar(
    filtered_data.groupby('Transmission')['Mileage'].mean().reset_index(),
    x='Transmission', y='Mileage', color='Transmission',
    title='Average Mileage by Transmission'
)
st.plotly_chart(fig4, use_container_width=True)

# Motor Size Distribution
st.markdown('#### Distribution of Motor Sizes')
fig5 = px.histogram(
    filtered_data, x='Motor Type_0', color='Motor Type_0',
    title='Distribution of Motor Sizes'
)
st.plotly_chart(fig5, use_container_width=True)

# Motor Type Distribution
st.markdown('#### Distribution of Motor Types')
fig6 = px.histogram(
    filtered_data, x='Motor Type_1', color='Motor Type_1',
    title='Distribution of Motor Types'
)
st.plotly_chart(fig6, use_container_width=True)

# Cheapest and Most Expensive Cars
st.markdown('### Cheapest and Most Expensive Cars')

if not filtered_data.empty:
    cheapest_car = filtered_data.loc[filtered_data['Price'].idxmin()]
    expensive_car = filtered_data.loc[filtered_data['Price'].idxmax()]
    
    col7, col8 = st.columns(2)
    with col7:
        st.subheader('Cheapest Car')
        st.write(f"**{cheapest_car['Manuf']} {cheapest_car['Model']}**")
        st.write(f"Price: ${cheapest_car['Price']:,.2f}")
        st.write(f"Mileage: {cheapest_car['Mileage']:,.2f} miles")
        st.write(f"Body Type: {cheapest_car['Body Type']}")
        st.write(f"Transmission: {cheapest_car['Transmission']}")
        st.write(f"Color: {cheapest_car['Color']}")
        st.write(f"Motor Size: {cheapest_car['Motor Type_0']}")
        st.write(f"Motor Type: {cheapest_car['Motor Type_1']}")

    with col8:
        st.subheader('Most Expensive Car')
        st.write(f"**{expensive_car['Manuf']} {expensive_car['Model']}**")
        st.write(f"Price: ${expensive_car['Price']:,.2f}")
        st.write(f"Mileage: {expensive_car['Mileage']:,.2f} miles")
        st.write(f"Body Type: {expensive_car['Body Type']}")
        st.write(f"Transmission: {expensive_car['Transmission']}")
        st.write(f"Color: {expensive_car['Color']}")
        st.write(f"Motor Size: {expensive_car['Motor Type_0']}")
        st.write(f"Motor Type: {expensive_car['Motor Type_1']}")
else:
    st.write("No cars match the selected criteria.")

# Comparative Analysis
st.markdown('### Comparative Analysis')

# Average Price and Mileage by Manufacturer
grouped_manuf = filtered_data.groupby('Manuf').agg(
    avg_price=('Price', 'mean'),
    avg_mileage=('Mileage', 'mean'),
    total_sales=('Manuf', 'count')
).reset_index()

col9, col10 = st.columns(2)
with col9:
    st.markdown('#### Average Price by Manufacturer')
    fig7 = px.bar(
        grouped_manuf, x='Manuf', y='avg_price', color='Manuf',
        title='Average Price by Manufacturer'
    )
    st.plotly_chart(fig7, use_container_width=True)

with col10:
    st.markdown('#### Average Mileage by Manufacturer')
    fig8 = px.bar(
        grouped_manuf, x='Manuf', y='avg_mileage', color='Manuf',
        title='Average Mileage by Manufacturer'
    )
    st.plotly_chart(fig8, use_container_width=True)

# Average Price and Mileage by Model
grouped_model = filtered_data.groupby('Model').agg(
    avg_price=('Price', 'mean'),
    avg_mileage=('Mileage', 'mean'),
    total_sales=('Model', 'count')
).reset_index()

col11, col12 = st.columns(2)
with col11:
    st.markdown('#### Average Price by Model')
    fig9 = px.bar(
        grouped_model, x='Model', y='avg_price', color='Model',
        title='Average Price by Model'
    )
    st.plotly_chart(fig9, use_container_width=True)

with col12:
    st.markdown('#### Average Mileage by Model')
    fig10 = px.bar(
        grouped_model, x='Model', y='avg_mileage', color='Model',
        title='Average Mileage by Model'
    )
    st.plotly_chart(fig10, use_container_width=True)

# Sales Trends Over Time (if Date data is available)
# Note: The provided dataset does not include date/time data.
# If such data exists, you can uncomment and adjust the following code.

# st.markdown('### Sales Trends Over Time')
# data['Sale Date'] = pd.to_datetime(data['Sale Date'])
# sales_over_time = filtered_data.groupby('Sale Date').size().reset_index(name='Sales')
# fig11 = px.line(sales_over_time, x='Sale Date', y='Sales', title='Sales Over Time')
# st.plotly_chart(fig11, use_container_width=True)

# Conclusion
st.markdown('### Summary')
st.write("""
This dashboard provides a comprehensive analysis of car sales, allowing you to filter and compare different manufacturers, models, body types, transmissions, colors, and motor specifications based on price and mileage.

Use the filters on the sidebar to customize the data displayed and gain insights into various aspects of the car market.
""")
