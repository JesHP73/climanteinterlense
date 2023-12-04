#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objs as go
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


df_original = load_data()

# Create a copy of the DataFrame for manipulation
df = df_original.copy()

# WHO Standards with correct averaging periods
who_standards = {
    'PM10': {'annual': 15},  # Annual mean: 15 μg/m3
    'PM2.5': {'annual': 5},  # Annual mean: 5 μg/m3
    #'O3': {'8_hour_max': 100000},  # Max daily 8-hour mean: 100 μg/m3
    'NO2': {'annual': 10},  # Annual mean: 10 μg/m3
    #'CO': {'8_hour_max': 4000}  # Max daily 8-hour mean: 4000 μg/m3 (4 mg/m3)
}
 
# O3 and CO are excluded as their standards are not based on annual averages


# Plotting Function

def plot_data(df_filtered, who_standards, selected_pollutant):
    # Making sure the selected pollutant is in the WHO standards dictionary
    if selected_pollutant not in who_standards:
        st.error(f"Selected pollutant {selected_pollutant} does not have a WHO standard defined.")
        return

    # Create a figure with Plotly
    fig = px.bar(df_filtered, x='country', y='air_pollutant_level', color='region',
                 title=f'Average {selected_pollutant} Emissions by Country in 2023',
                 labels={'country': 'Country', 'air_pollutant_level': f'Average {selected_pollutant} Level (μg/m³)'})

    # Rotate the x-axis labels
    fig.update_layout(xaxis_tickangle=-45)

    # Set the y-axis type to linear (default)
    fig.update_yaxes(type='linear')

    # Add a line for the WHO standard
    standard = who_standards[selected_pollutant]['annual']
    fig.add_hline(y=standard, line_dash='solid', line_color='red')

    # Update the layout to move the legend to the right side
    fig.update_layout(legend=dict(
        yanchor='top',
        y=0.99,
        xanchor="left",
        x=1.01
    ))

    # Moving the annotation out of the plot area to the right side
    fig.add_annotation(
        text=f'WHO {selected_pollutant} Standard',
        xref="paper", yref="paper",
        x=1, y=1.05,  # positions to the right of the plot area
        showarrow=False,
        align='left',
        bgcolor='white',
        bordercolor='red',
        borderwidth=1
    )

    # Update the layout to add space for the annotation
    fig.update_layout(
        margin=dict(r=160, t=50)  
    )

    # Display the figure in Streamlit
    st.plotly_chart(fig)


# Filtering for PM10, PM2.5, and NO2 pollutants only, and for the year 2023
df_filtered = df[df['air_pollutant'].isin(['PM10', 'PM2.5', 'NO2'])]

# User input areas for filtering
region_options = ['All'] + sorted(df_filtered['region'].unique().tolist())
pollutants_options = sorted(df_filtered['air_pollutant'].unique().tolist())

# Sidebar for user input
selected_region = st.sidebar.multiselect('Select Region', options=region_options, default=['All'])
selected_pollutant = st.sidebar.selectbox('Select Pollutant', options=pollutants_options)

# Apply the selected region filter
if 'All' not in selected_region:
    df_filtered = df_filtered[df_filtered['region'].isin(selected_region)]

# Apply the selected pollutant filter
df_filtered = df_filtered[df_filtered['air_pollutant'] == selected_pollutant]

# Check if the DataFrame is empty after all filters have been applied
if df_filtered.empty:
    st.error('No data available for the selected filters.')
    # If there is no data, we should not attempt to plot
else:
    # If data is present, call the plotting function
    plot_data(df_filtered, who_standards, selected_pollutant)

# Debugging: Print descriptive statistics of the filtered data
st.write(df_filtered['air_pollutant_level'].describe())

# Debugging: Display the first few rows of the filtered DataFrame to check values
st.dataframe(df_filtered.head())



