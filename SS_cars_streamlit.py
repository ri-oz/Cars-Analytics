import streamlit as st
import pandas as pd

# Load the data
url = 'https://raw.githubusercontent.com/ri-oz/Cars-Analytics/main/CarData.csv'
data = pd.read_csv(url)

# Normalize column names: strip whitespace and convert to lowercase
data.columns = data.columns.str.strip().str.lower().str.replace(' ', '_')

# Expected columns
expected_columns = ['manuf', 'model', 'body_type', 'transmission', 'color', 'motor_type_0', 'motor_type_1', 'price', 'mileage']

# Verify the columns exist in the dataset and handle missing ones gracefully
missing_columns = [col for col in expected_columns if col not in data.columns]
if missing_columns:
    st.error(f"Missing columns in the dataset: {', '.join(missing_columns)}")
else:
    # Clean the data and handle non-numeric Price and Mileage columns
    data['price'] = pd.to_numeric(data['price'], errors='coerce')
    data['mileage'] = pd.to_numeric(data['mileage'], errors='coerce')

    # Drop rows with missing values in the important columns
    data.dropna(subset=['price', 'mileage'], inplace=True)

    # Convert categorical columns to string
    categorical_columns = ['manuf', 'model', 'body_type', 'transmission', 'color', 'motor_type_0', 'motor_type_1']
    for col in categorical_columns:
        data[col] = data[col].astype(str)

    # Set Streamlit app layout
    st.set_page_config(page_title='Car Sales Analytics', layout='wide')

    # Sidebar filters
    st.sidebar.header('Filter Options')

    # Manufacturer filter
    manufacturer = st.sidebar.multiselect('Select Manufacturer', options=data['manuf'].unique(), default=data['manuf'].unique())

    # Model filter
    model_options = data[data['manuf'].isin(manufacturer)]['model'].unique()
    model = st.sidebar.multiselect('Select Model', options=model_options, default=model_options)

    # Body Type filter
    body_type_options = data['body_type'].unique()
    body_type = st.sidebar.multiselect('Select Body Type', options=body_type_options, default=body_type_options)

    # Transmission filter
    transmission_options = data['transmission'].unique()
    transmission = st.sidebar.multiselect('Select Transmission', options=transmission_options, default=transmission_options)

    # Color filter
    color_options = data['color'].unique()
    color = st.sidebar.multiselect('Select Color', options=color_options, default=color_options)

    # Motor Type_0 filter (Size)
    motor_size_options = data['motor_type_0'].unique()
    motor_size = st.sidebar.multiselect('Select Motor Size', options=motor_size_options, default=motor_size_options)

    # Motor Type_1 filter (Type)
    motor_type_options = data['motor_type_1'].unique()
    motor_type = st.sidebar.multiselect('Select Motor Type', options=motor_type_options, default=motor_type_options)

    # Apply filters
    filtered_data = data[
        (data['manuf'].isin(manufacturer)) &
        (data['model'].isin(model)) &
        (data['body_type'].isin(body_type)) &
        (data['transmission'].isin(transmission)) &
        (data['color'].isin(color)) &
        (data['motor_type_0'].isin(motor_size)) &
        (data['motor_type_1'].isin(motor_type))
    ]

    # Main Metrics
    st.title('Car Sales Analytics Dashboard')
    st.markdown('### Key Metrics')

    col1, col2, col3 = st.columns(3)
    with col1:
        avg_price = filtered_data['price'].mean()
        st.metric('Average Price ($)', f"${avg_price:,.2f}")
        
    with col2:
        avg_mileage = filtered_data['mileage'].mean()
        st.metric('Average Mileage', f"{avg_mileage:,.2f} miles")
        
    with col3:
        total_cars = len(filtered_data)
        st.metric('Total Cars in Selection', total_cars)

    # Additional Metrics
    col4, col5, col6 = st.columns(3)
    with col4:
        popular_body_type = filtered_data['body_type'].mode()[0] if not filtered_data.empty else 'N/A'
        st.metric('Most Common Body Type', popular_body_type)

    with col5:
        popular_transmission = filtered_data['transmission'].mode()[0] if not filtered_data.empty else 'N/A'
        st.metric('Most Common Transmission', popular_transmission)

    with col6:
        popular_color = filtered_data['color'].mode()[0] if not filtered_data.empty else 'N/A'
        st.metric('Most Common Color', popular_color)

    # Price Distribution by Manufacturer using bar chart
    st.markdown('### Price Distribution by Manufacturer')

    if not filtered_data.empty:
        price_by_manuf = filtered_data.groupby('manuf')['price'].mean()
        st.bar_chart(price_by_manuf)
    else:
        st.write("No data available for the selected filters.")

    # Mileage Distribution by Manufacturer using bar chart
    st.markdown('### Mileage Distribution by Manufacturer')

    if not filtered_data.empty:
        mileage_by_manuf = filtered_data.groupby('manuf')['mileage'].mean()
        st.bar_chart(mileage_by_manuf)

    # Sales Analysis
    st.markdown('### Sales Analysis')

    # Average Price by Body Type
    st.markdown('#### Average Price by Body Type')

    if not filtered_data.empty:
        avg_price_by_body = filtered_data.groupby('body_type')['price'].mean()
        st.bar_chart(avg_price_by_body)

    # Average Mileage by Transmission
    st.markdown('#### Average Mileage by Transmission')

    if not filtered_data.empty:
        avg_mileage_by_transmission = filtered_data.groupby('transmission')['mileage'].mean()
        st.bar_chart(avg_mileage_by_transmission)

    # Motor Size Distribution
    st.markdown('#### Distribution of Motor Sizes')

    if not filtered_data.empty:
        motor_size_dist = filtered_data['motor_type_0'].value_counts()
        st.bar_chart(motor_size_dist)

    # Motor Type Distribution
    st.markdown('#### Distribution of Motor Types')

    if not filtered_data.empty:
        motor_type_dist = filtered_data['motor_type_1'].value_counts()
        st.bar_chart(motor_type_dist)

    # Cheapest and Most Expensive Cars
    st.markdown('### Cheapest and Most Expensive Cars')

    if not filtered_data.empty:
        cheapest_car = filtered_data.loc[filtered_data['price'].idxmin()]
        expensive_car = filtered_data.loc[filtered_data['price'].idxmax()]
        
        col7, col8 = st.columns(2)
        with col7:
            st.subheader('Cheapest Car')
            st.write(f"**{cheapest_car['manuf']} {cheapest_car['model']}**")
            st.write(f"Price: ${cheapest_car['price']:,.2f}")
            st.write(f"Mileage: {cheapest_car['mileage']:,.2f} miles")
            st.write(f"Body Type: {cheapest_car['body_type']}")
            st.write(f"Transmission: {cheapest_car['transmission']}")
            st.write(f"Color: {cheapest_car['color']}")
            st.write(f"Motor Size: {cheapest_car['motor_type_0']}")
            st.write(f"Motor Type: {cheapest_car['motor_type_1']}")

        with col8:
            st.subheader('Most Expensive Car')
            st.write(f"**{expensive_car['manuf']} {expensive_car['model']}**")
            st.write(f"Price: ${expensive_car['price']:,.2f}")
            st.write(f"Mileage: {expensive_car['mileage']:,.2f} miles")
            st.write(f"Body Type: {expensive_car['body_type']}")
            st.write(f"Transmission: {expensive_car['transmission']}")
            st.write(f"Color: {expensive_car['color']}")
            st.write(f"Motor Size: {expensive_car['motor_type_0']}")
            st.write(f"Motor Type: {expensive_car['motor_type_1']}")
    else:
        st.write("No cars match the selected criteria.")

    # Comparative Analysis
    st.markdown('### Comparative Analysis')

    # Average Price and Mileage by Manufacturer
    grouped_manuf = filtered_data.groupby('manuf').agg(
        avg_price=('price', 'mean'),
        avg_mileage=('mileage', 'mean'),
        total_sales=('manuf', 'count')
    ).reset_index()

    col9, col10 = st.columns(2)
    with col9:
        st.markdown('#### Average Price by Manufacturer')
        
        if not grouped_manuf.empty:
            st.bar_chart(grouped_manuf.set_index('manuf')['avg_price'])

    with col10:
        st.markdown('#### Average Mileage by Manufacturer')
        
        if not grouped_manuf.empty:
            st.bar_chart(grouped_manuf.set_index('manuf')['avg_mileage'])
