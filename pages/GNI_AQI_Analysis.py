#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np

# WHO standards for pollutants
WHO_STANDARDS = {
    'PM10': {'AQG': 15, 'RL': 45},
    'PM2.5': {'AQG': 5, 'RL': 15},
    'O3': {'AQG': 60, 'RL': 100},
    'NO2': {'AQG': 10, 'RL': 25},
    'CO': {'AQG': 4, 'RL': 10}  # Assuming the unit is mg/m3 for simplicity
}


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

# Sidebar - User input areas
st.sidebar.header("Filters")
selected_region = st.sidebar.selectbox('Select Region', ['All'] + sorted(df['region'].unique()))
selected_country = st.sidebar.selectbox('Select Country', ['All'] + sorted(df['country'].unique()))
selected_pollutants = st.sidebar.multiselect('Select Pollutant', ['All'] + sorted(df['air_pollutant'].unique()))
selected_year = st.sidebar.selectbox('Select Year', ['All'] + sorted(df['year'].unique().astype(str)))

# Filtering the data based on user selections
filtered_data = df.copy()
if selected_region != 'All':
    filtered_data = filtered_data[filtered_data['region'] == selected_region]
if selected_country != 'All':
    filtered_data = filtered_data[filtered_data['country'] == selected_country]
if selected_pollutants != ['All']:
    filtered_data = filtered_data[filtered_data['air_pollutant'].isin(selected_pollutants)]
if selected_year != 'All':
    filtered_data = filtered_data[filtered_data['year'] == int(selected_year)]

def plot_emissions(df):
    # Check if dataframe is empty
    if df.empty:
        st.error('No data available for the selected filters.')
        return

    # Convert year to string for plotting purposes
    df['year'] = df['year'].astype(str)

    # Create a plot comparing each pollutant's level to WHO standards
    fig, ax = plt.subplots()
    for pollutant in WHO_STANDARDS.keys():
        if pollutant in df['air_pollutant'].unique():
            sns.lineplot(x='year', y='air_pollutant_level', data=df[df['air_pollutant'] == pollutant], ax=ax, label=pollutant)
            ax.axhline(y=WHO_STANDARDS[pollutant]['AQG'], color='red', linestyle='--', label=f"{pollutant} WHO AQG")
    ax.set_title('Pollutant Levels Over Time Compared to WHO Standards')
    ax.set_xlabel('Year')
    ax.set_ylabel('Pollutant Level')
    ax.legend()
    return fig

# Plot based on the filtered data
if not filtered_data.empty:
    fig = plot_emissions(filtered_data)
    st.pyplot(fig)


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
        # Call the plotting function and show the plot
        plot_emissions(df, selected_pollutants)
        
st.info("The guidelines and reference levels from WHO are designed to keep air quality at a level that's safe for public health. When pollution levels go above these numbers, it can lead to health concerns for the population, especially vulnerable groups like children and the elderly.")


## Additional explanations about AQGs and RLs
st.markdown("### Understanding the Numbers")
st.write("correlation between a country's income levels and its air pollution,suggesting that higher income might be associated with better air quality.")

