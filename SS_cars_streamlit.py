import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure matplotlib does not crash in Streamlit
plt.switch_backend('Agg')

# Load the data
url = 'https://raw.githubusercontent.com/ri-oz/Cars-Analytics/main/CarData.csv'
data = pd.read_csv(url)

# Check column names and handle cases where some are missing or have unexpected names
expected_columns = ['Manuf', 'Model', 'Body Type', 'Transmission', 'Color', 'Motor Type_0', 'Motor Type_1', 'Price', 'Mileage']

# Verify the columns exist in the dataset and handle missing ones gracefully
missing_columns = [col for col in expected_columns if col not in data.columns]
if missing_columns:
    st.error(f"Missing columns in the dataset: {', '.join(missing_columns)}")
else:
    # Clean the data and handle non-numeric Price and Mileage columns
    data['Price'] = pd.to_numeric(data['Price'], errors='coerce')
    data['Mileage'] = pd.to_numeric(data['Mileage'], errors='coerce')

    # Drop rows with missing values in the important columns
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

    # Create Matplotlib charts
    st.markdown('### Price Distribution by Manufacturer')

    if not filtered_data.empty:
        # Price distribution by manufacturer
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=filtered_data, x='Manuf', y='Price')
        plt.xticks(rotation=45)
        plt.title('Price Distribution by Manufacturer')
        st.pyplot(plt.gcf())
    else:
        st.write("No data available for the selected filters.")

    st.markdown('### Mileage Distribution by Manufacturer')

    if not filtered_data.empty:
        # Mileage distribution by manufacturer
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=filtered_data, x='Manuf', y='Mileage')
        plt.xticks(rotation=45)
        plt.title('Mileage Distribution by Manufacturer')
        st.pyplot(plt.gcf())

    # Sales Analysis
    st.markdown('### Sales Analysis')

    # Average Price by Body Type
    st.markdown('#### Average Price by Body Type')

    if not filtered_data.empty:
        avg_price_by_body = filtered_data.groupby('Body Type')['Price'].mean().reset_index()
        plt.figure(figsize=(10, 6))
        sns.barplot(data=avg_price_by_body, x='Body Type', y='Price')
        plt.title('Average Price by Body Type')
        st.pyplot(plt.gcf())

    # Average Mileage by Transmission
    st.markdown('#### Average Mileage by Transmission')

    if not filtered_data.empty:
        avg_mileage_by_transmission = filtered_data.groupby('Transmission')['Mileage'].mean().reset_index()
        plt.figure(figsize=(10, 6))
        sns.barplot(data=avg_mileage_by_transmission, x='Transmission', y='Mileage')
        plt.title('Average Mileage by Transmission')
        st.pyplot(plt.gcf())

    # Motor Size Distribution
    st.markdown('#### Distribution of Motor Sizes')

    if not filtered_data.empty:
        plt.figure(figsize=(10, 6))
        sns.histplot(filtered_data['Motor Type_0'], kde=False, bins=10)
        plt.title('Distribution of Motor Sizes')
        st.pyplot(plt.gcf())

    # Motor Type Distribution
    st.markdown('#### Distribution of Motor Types')

    if not filtered_data.empty:
        plt.figure(figsize=(10, 6))
        sns.histplot(filtered_data['Motor Type_1'], kde=False, bins=10)
        plt.title('Distribution of Motor Types')
        st.pyplot(plt.gcf())

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
        
        if not grouped_manuf.empty:
            plt.figure(figsize=(10, 6))
            sns.barplot(data=grouped_manuf, x='Manuf', y='avg_price')
            plt.title('Average Price by Manufacturer')
            plt.xticks(rotation=45)
            st.pyplot(plt.gcf())

    with col10:
        st.markdown('#### Average Mileage by Manufacturer')
        
        if not grouped_manuf.empty:
            plt.figure(figsize=(10, 6))
            sns.barplot(data=grouped_manuf, x='Manuf', y='avg_mileage')
            plt.title('Average Mileage by Manufacturer')
            plt.xticks(rotation=45)
            st.pyplot(plt.gcf())