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


# Filtering the data based on user selections
filtered_data = df.copy()
if selected_region != 'All':
    filtered_data = filtered_data[filtered_data['region'] == selected_region]
if selected_country != 'All':
    filtered_data = filtered_data[filtered_data['country'] == selected_country]
if selected_pollutants != ['All']:
    filtered_data = filtered_data[filtered_data['air_pollutant'].isin(selected_pollutants)]


def plot_aqi_and_gni_over_time(data):
    if data.empty:
        st.error('No data available for plotting.')
        return

    # Convert 'year' to numeric if it's not already
    if not pd.api.types.is_numeric_dtype(data['year']):
        data['year'] = pd.to_numeric(data['year'], errors='coerce')

    # Drop rows where 'year' or 'AQI_Index' is NaN
    data = data.dropna(subset=['year', 'AQI_Index'])

    if data.empty:
        st.error('No data available for plotting after cleaning.')
        return

    fig, ax1 = plt.subplots(figsize=(10, 6))

    try:
        ax1.plot(data['year'], data['AQI_Index'], 'r-', label='AQI Index')
    except Exception as e:
        st.error(f'Error plotting AQI Index: {e}')
        return

    ax1.set_xlabel('Year')
    ax1.set_ylabel('AQI Index', color='r')
    ax1.set_title("AQI Index and GNI per Capita Over Time")
    
    if 'GNI_per_capita' in data.columns:
        try:
            ax2 = ax1.twinx()
            ax2.plot(data['year'], data['GNI_per_capita'], 'b-', label='GNI per Capita')
            ax2.set_ylabel('GNI per Capita ($)', color='b')
        except Exception as e:
            st.error(f'Error plotting GNI per Capita: {e}')
            return
    else:
        st.warning("GNI_per_capita data not available for plotting.")
    
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    fig.tight_layout()
    st.pyplot(fig)


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

# Check if there's data to plot
if not filtered_data.empty:
    # Determine the correct plot based on the user's selection of pollutants
    if 'All' in selected_pollutants or len(selected_pollutants) > 1:
        fig = plot_aqi_and_gni_over_time(filtered_data)
        if fig:  # Check if the figure was successfully created
            st.pyplot(fig)
    else:
        for pollutant in selected_pollutants:
            st.subheader(f"Analysis for {pollutant}")
            pollutant_data = filtered_data[filtered_data['air_pollutant'] == pollutant]
            # Check if there is data for the selected pollutant
            if not pollutant_data.empty:
                fig = plot_individual_pollutant_with_levels(pollutant_data, pollutant, 'unit_air_poll_lvl', 'air_pollutant_level')
                st.pyplot(fig)
            else:
                st.error(f'No data available for pollutant: {pollutant}')


        
st.info("The guidelines and reference levels from WHO are designed to keep air quality at a level that's safe for public health. When pollution levels go above these numbers, it can lead to health concerns for the population, especially vulnerable groups like children and the elderly.")


## Additional explanations about AQGs and RLs
st.markdown("### Understanding the Numbers")
st.write("correlation between a country's income levels and its air pollution,suggesting that higher income might be associated with better air quality.")

