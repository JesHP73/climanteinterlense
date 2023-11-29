#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Function to load data
@st.cache
def load_data():
    try:
        DATA_URL = 'https://raw.githubusercontent.com/JesHP73/climanteinterlense/main/dataset/socio_economical_agg_dataset.csv'
        data = pd.read_csv(DATA_URL)
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error

# Load data
df_original = load_data()

# Create a copy of the DataFrame for manipulation
df = df_original.copy()

def show_gni_aqi_analysis(df):
    if df.empty:
        st.error("No data available to display.")
        return

    st.title("📊 Income Per Person vs AQI Analysis")
    st.write("Here you can analyze how Gross National Income (GNI) correlates with Air Quality Index (AQI).")
    
    # Data filtering based on sidebar selection
    if not selected_region:
        filtered_data = df
    else:
        filtered_data = df[
            (df['region'].isin(selected_region)) &
            (df['country'].isin(selected_country)) &
            (df['decade'].isin(selected_decade))
        ]

    # Plotting with Plotly
    if not filtered_data.empty:
        fig = px.scatter(
            filtered_data,
            x="avg_GNI_Atlas",
            y="avg_AQI_Index",
            size="total_population", 
            color="region",
            hover_name="country",
            log_x=True, 
            size_max=60
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No data to display. Please adjust the filter options.")

def gni_impact(df):
    if df.empty:
        st.error("No data available to display.")
        return
    
    # User input areas
    region_options = ['All'] + sorted(df['region'].unique().tolist())
    country_options = ['All'] + sorted(df['country'].unique().tolist())
    decade_options = ['All'] + sorted(df['decade'].unique().tolist())
     
    # Sidebar filters
    selected_region = st.sidebar.multiselect('Select Region', options=region_options, default='All')
    selected_country = st.sidebar.multiselect('Select Country', options=country_options, default='All')
    selected_decade = st.sidebar.multiselect('Select Decade', options=decade_options, default='All')

    # Efficient combined filtering
    conditions = []
    if 'All' not in selected_region:
        conditions.append(df['region'].isin(selected_region))
    if 'All' not in selected_country:
        conditions.append(df['country'].isin(selected_country))
    if 'All' not in selected_decade:
        conditions.append(df['decade'].isin(selected_decade))
    if conditions:
        df_filtered = df[np.logical_and.reduce(conditions)].copy()
        # Further processing with df_filtered
    else:
        st.error("No data available for the selected criteria.")



# Call page content function
show_gni_aqi_analysis(df)





