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

# User input areas
region_options = ['All'] + sorted(df['region'].unique().tolist())
pollutans_options = ['All'] + sorted(df['air_pollutant'].unique().tolist())

# Sidebar for user input
selected_region = st.sidebar.multiselect('Select Region', options=['All'] + sorted(df['region'].unique().tolist()), default=['All'])
selected_pollutants = st.sidebar.multiselect('Select Pollutant', options=['All'] + sorted(df['air_pollutant'].unique().tolist()), default=['All'])

# Data Filtering
if 'All' not in selected_region:
    df = df[df['region'].isin(selected_region)]
if 'All' not in selected_pollutants:
    df = df[df['air_pollutant'].isin(selected_pollutants)]

# Plotting Function
def plot_data(df, selected_pollutants):
    # Decide which column to use based on pollutant selection
    value_col = 'AQI_Index' if 'All' in selected_pollutants else 'air_pollutant_level'

    # Create a figure with Plotly
    fig = px.bar(df, x='country', y=value_col, color='region', title='Air Pollutant Emissions by Country',
                 category_orders={"region": sorted(df['region'].unique().tolist())})  # Sort regions
    
    # Rotate the x-axis labels
    fig.update_layout(xaxis_tickangle=-45)
    
    # Add lines for WHO standards
    for pollutant in selected_pollutants:
        if pollutant in who_standards:
            standard_value = who_standards[pollutant]['annual']
            fig.add_hline(y=standard_value, line_dash="dash", line_color='red',
                          annotation_text=f'WHO {pollutant} Standard', annotation_position="bottom right")
    
    # If 'All' pollutants are selected, add all standard lines
    if 'All' in selected_pollutants:
        for pollutant, standard in who_standards.items():
            fig.add_hline(y=standard['annual'], line_dash="dash", line_color='red',
                          annotation_text=f'WHO {pollutant} Standard', annotation_position="bottom right")
    
    st.plotly_chart(fig)

# Execute Plotting
plot_data(df, selected_pollutants) 
