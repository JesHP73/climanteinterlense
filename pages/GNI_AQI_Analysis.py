#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np

# Function to load data
@st.cache
def load_data():
    try:
        DATA_URL = 'https://raw.githubusercontent.com/JesHP73/climanteinterlense/main/dataset/air_quality_vs_gni_agg.csv'
        data = pd.read_csv(DATA_URL)
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error

# Assuming load_data() is defined elsewhere
df_original = load_data()

# Create a copy of the DataFrame for manipulation
df = df_original.copy()

def show_gni_aqi_analysis(df):
    if df.empty:
        st.error("No data available to display.")
        return

    st.title("📊 Income Per Person vs AQI Analysis")
    st.write("Here you can analyze how Gross National Income (GNI) correlates with Air Quality Index (AQI).")
    
    # User input areas
    region_options = ['All'] + sorted(df['region'].unique().tolist())
    country_options = ['All'] + sorted(df['country'].unique().tolist())
    pollutants_options = ['All'] + sorted(df['air_pollutant'].unique().tolist())
     
    # Sidebar filters
    selected_region = st.sidebar.multiselect('Select Region', options=region_options, default=['All'])
    selected_country = st.sidebar.multiselect('Select Country', options=country_options, default=['All'])
    selected_pollutants = st.sidebar.multiselect('Select Decade', options=pollutants_options, default=['All'])

    # Efficient combined filtering
    conditions = []
    if 'All' not in selected_region:
        conditions.append(df['region'].isin(selected_region))
    if 'All' not in selected_country:
        conditions.append(df['country'].isin(selected_country))
    if 'All' not in selected_pollutants:
        conditions.append(df['air_pollutant'].isin(selected_pollutants))

    if conditions:
        filtered_data = df[np.logical_and.reduce(conditions)]
    else:
        filtered_data = df.copy()

    # Check if there is data to display after filtering
    if filtered_data.empty:
        st.error("No data available for the selected criteria.")
        return

    # Plotting with Plotly
    fig = px.scatter(
        filtered_data,
        x="GNI_per_capita",
        y="AQI_Index",
        size="total_population", 
        color="region",
        hover_name="country",
        log_x=True, 
        size_max=60
    )

    st.plotly_chart(fig, use_container_width=True)

# Call page content function
show_gni_aqi_analysis(df)

