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

# Function for plotting AQI Index vs GNI per Capita
def plot_aqi_vs_gni(data):
    fig, ax = plt.subplots()
    scatter = ax.scatter(data['GNI_per_capita'], data['AQI_Index'], c=data['year'], cmap='viridis')
    legend1 = ax.legend(*scatter.legend_elements(), title="Years")
    ax.add_artist(legend1)
    ax.set_xlabel('GNI per Capita')
    ax.set_ylabel('AQI Index')
    ax.set_title('GNI per Capita vs AQI Index')
    return fig
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

# Function for plotting AQI Index vs GNI per Capita
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

# Additional insights or summaries based on the filtered data
st.write("Additional insights or data summaries can go here.")

