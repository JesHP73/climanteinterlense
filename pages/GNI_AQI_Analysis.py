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
df = load_data()

# Create a copy of the DataFrame for manipulation
df_original = df.copy()

# Sidebar - User input areas
st.sidebar.header("Filters")
selected_region = st.sidebar.selectbox('Select Region', ['All'] + sorted(df_original['region'].unique()))
selected_country = st.sidebar.selectbox('Select Country', ['All'] + sorted(df_original['country'].unique()))
selected_pollutants = st.sidebar.multiselect('Select Pollutant', ['All'] + sorted(df_original['air_pollutant'].unique()))

# Filtering the data based on user selections
filtered_data = df_original.copy()
if selected_region != 'All':
    filtered_data = filtered_data[filtered_data['region'] == selected_region]
if selected_country != 'All':
    filtered_data = filtered_data[filtered_data['country'] == selected_country]
if 'All' not in selected_pollutants:
    filtered_data = filtered_data[filtered_data['air_pollutant'].isin(selected_pollutants)]

# Function for plotting AQI Index and GNI per Capita over time
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
        
    ax1.set_xlabel('Year')
    ax1.set_ylabel('AQI Index', color='r')
    ax1.set_title("AQI Index and GNI per Capita Over Time")

    if 'GNI_per_capita' in data.columns:
        try:
            gni_per_capita = data['GNI_per_capita'].to_numpy()
            ax2 = ax1.twinx()
            ax2.plot(years, gni_per_capita, 'b-', label='GNI per Capita')
            ax2.set_ylabel('GNI per Capita ($)', color='b')
        except Exception as e:
            st.error(f'Error plotting GNI per Capita: {e}')
            return
    else:
        st.warning("GNI_per_capita data not available for plotting.")

    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    
    # Plot with Plotly
    fig = px.line(data, x='year', y='AQI_Index', title='AQI Index over Time', markers=True)
    
    # Create a secondary y-axis for GNI per capita
    fig.add_scatter(x=data['year'], y=data['GNI_per_capita'], mode='lines+markers', name='GNI per Capita', yaxis='y2')
    
    # Update layout to add a secondary y-axis
    fig.update_layout(
        yaxis2=dict(
            title='GNI per Capita',
            overlaying='y',
            side='right'
        ),
        yaxis=dict(
            title='AQI Index'
        )
    )
    # Show the plot
    st.plotly(fig)

# Call the function to plot data
if not filtered_data.empty:
    plot_aqi_and_gni_over_time(filtered_data)
else:
    st.error("No data available for the selected filters.")


# Function for plotting individual pollutants with emissions levels and units
def plot_individual_pollutant_with_levels(data, pollutant, unit_column, level_column):
    # Check if columns exist
    if unit_column not in data.columns or level_column not in data.columns:
        st.error(f"Column names {unit_column} or {level_column} not found in data.")
        return

    # Drop missing values
    data = data.dropna(subset=['year', level_column])

    # Ensure data types are correct
    data['year'] = pd.to_numeric(data['year'], errors='coerce')
    data[level_column] = pd.to_numeric(data[level_column], errors='coerce')

    # Check if data is empty after processing
    if data.empty:
        st.error("No data available for plotting after processing.")
        return

    fig, ax = plt.subplots()
    try:
        sns.lineplot(x='year', y=level_column, data=data, ax=ax, label=pollutant)
    except Exception as e:
        st.error(f"Error plotting data: {e}")
        return

    ax.set_ylabel(f"{pollutant} ({data[unit_column].iloc[0]})")
    ax.set_xlabel('Year')
    ax.set_title(f"Yearly Trend of {pollutant}")

    # Pass the figure object to st.pyplot()
    st.pyplot(fig)


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

