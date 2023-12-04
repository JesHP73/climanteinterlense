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

# User input areas for filtering
region_options = ['All'] + sorted(df['region'].unique().tolist())
pollutants_options = ['All'] + sorted(df['air_pollutant'].unique().tolist())

# Sidebar for user input
selected_region = st.sidebar.multiselect('Select Region', options=region_options, default=['All'])
selected_pollutant = st.sidebar.selectbox('Select Pollutant', options=pollutants_options)

# Data Filtering
if 'All' not in selected_region:
    df = df[df['region'].isin(selected_region)]
if selected_pollutant and selected_pollutant != 'All':
    df = df[df['air_pollutant'] == selected_pollutant]

# Plotting Function
def plot_data(df, who_standards):

    # Filter for PM10, PM2.5, and NO2 pollutants only
    df = df[df['air_pollutant'].isin(['PM10', 'PM2.5', 'NO2'])]
    
    # Create a figure with Plotly
    fig = px.bar(df, x='country', y='air_pollutant_level', color='region', 
                 title='Air Pollutant Emissions by Country',
                 labels={'country': 'Country', 'air_pollutant_level': 'Average Level (μg/m³)'})
    
    # Rotate the x-axis labels
    fig.update_layout(xaxis_tickangle=-45)

    # Add lines for WHO standards if a specific pollutant is selected
    if selected_pollutant and selected_pollutant != 'All':
        standard = who_standards[selected_pollutant]['annual']
        fig.add_hline(y=standard, line_dash="dash", line_color='red',
                      annotation_text=f'WHO {selected_pollutant} Standard', annotation_position="bottom right")
    
    # Set dynamic y-axis range based on the data
    max_value = df['air_pollutant_level'].max()
    fig.update_yaxes(range=[0, max(max_value, standard) * 1.1])  # Scale to the higher of max value or standard

    st.plotly_chart(fig)

# Execute Plotting
plot_data(df, who_standards)
