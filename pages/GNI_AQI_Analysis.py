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

# User input areas
region_options = ['All'] + sorted(df['region'].unique().tolist())
country_options = ['All'] + sorted(df['country'].unique().tolist())
pollutants_options = ['All'] + sorted(df['air_pollutant'].unique().tolist())

# Sidebar filters
selected_region = st.sidebar.multiselect('Select Region', options=region_options, default=['All'])
selected_country = st.sidebar.multiselect('Select Country', options=country_options, default=['All'])
selected_pollutants = st.sidebar.multiselect('Select Pollutant', options=pollutants_options, default=['All'])
selected_year = st.sidebar.slider('Select Year', min_value=int(df['year'].min()), max_value=int(df['year'].max()), value=int(df['year'].min()))

# Efficient combined filtering
conditions = []
if 'All' not in selected_region:
    conditions.append(df['region'].isin(selected_region))
if 'All' not in selected_country:
    conditions.append(df['country'].isin(selected_country))
if 'All' not in selected_pollutants:
    conditions.append(df['air_pollutant'].isin(selected_pollutants))
conditions.append(df['year'] == selected_year)

if conditions:
    filtered_data = df[np.logical_and.reduce(conditions)]
else:
    filtered_data = df.copy()

# Sort the data for line plotting
filtered_data.sort_values(by='year', inplace=True)

# Function for plotting AQI Index and GNI per Capita over time as lines
def plot_aqi_and_gni_over_time(data):
    # Debugging: print out the data types and lengths of the series being plotted
    print("Year data type:", data['year'].dtype, "Length:", len(data['year']))
    print("AQI Index data type:", data['AQI_Index'].dtype, "Length:", len(data['AQI_Index']))
    print("GNI per Capita data type:", data['GNI_per_capita'].dtype, "Length:", len(data['GNI_per_capita']))
    
    # Ensure data is sorted by year
    data = data.sort_values('year')
    
    fig, ax1 = plt.subplots()

    # Plot AQI_Index
    ax1.plot(data['year'], data['AQI_Index'], 'r-')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('AQI Index', color='r')
    
    # Create a second y-axis for GNI per capita
    ax2 = ax1.twinx()
    ax2.plot(data['year'], data['GNI_per_capita'], 'b-')
    ax2.set_ylabel('GNI per Capita', color='b')

    # Make the layout tight to handle the second y-axis
    fig.tight_layout()
    return fig


# Function for plotting individual pollutants with emissions levels and units
def plot_individual_pollutant_with_levels(data, pollutant, unit_column, level_column):
    fig, ax = plt.subplots()
    sns.lineplot(x='year', y=level_column, data=data, ax=ax, label=pollutant)
    ax.set_ylabel(f"{pollutant} ({data[unit_column].iloc[0]})")
    ax.set_xlabel('Year')
    ax.set_title(f"Yearly Trend of {pollutant}")
    return fig


# Visualization Header
st.header("GNI per Capita and AQI Index Analysis Over Time")

# Determine the correct plot based on the user's selection of pollutants
if 'All' in selected_pollutants or len(selected_pollutants) > 1:
    st.pyplot(plot_aqi_and_gni_over_time(filtered_data))
else:
    for pollutant in selected_pollutants:
        st.subheader(f"Analysis for {pollutant}")
        pollutant_data = filtered_data[filtered_data['air_pollutant'] == pollutant]
        # Assume 'unit_air_poll_lvl' and 'air_pollutant_level' are the columns with units and levels
        st.pyplot(plot_individual_pollutant_with_levels(pollutant_data, pollutant, 'unit_air_poll_lvl', 'air_pollutant_level'))

# Additional insights or summaries based on the filtered data
st.write("Additional insights or data summaries can go here.")

