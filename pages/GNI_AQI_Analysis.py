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


# Assuming 'load_data()' is a function that loads and returns the aggregated DataFrame
df = load_data()
df_original = df.copy()

# Sidebar - Selecting 'All' or specific regions/countries
all_regions = ['All'] + list(df_original['region'].unique())
all_countries = ['All'] + list(df_original['country'].unique())
selected_regions = st.sidebar.multiselect('Select Region(s)', options=all_regions, default='All')
selected_countries = st.sidebar.multiselect('Select Country(ies)', options=all_countries, default='All')

# Handling 'All' selections
if 'All' in selected_regions:
    selected_regions = all_regions[1:]  # Exclude 'All' from the list
if 'All' in selected_countries:
    selected_countries = all_countries[1:]  # Exclude 'All' from the list

# Filter the DataFrame based on the selections
filtered_df = df_original[
    df_original['region'].isin(selected_regions) &
    df_original['country'].isin(selected_countries)
]

# Create the plot
fig = px.line(
    filtered_df,
    x='year',
    y=['AQI_Index', 'GNI_per_capita'],
    labels={'value':'Index', 'variable':'Indicator'},
    title='AQI and GNI per Capita over Time'
)

# Simplify the legend and layout
fig.update_layout(
    legend_title_text='Indicator',
    yaxis_title='AQI Index',
    yaxis2=dict(
        title='GNI per Capita',
        overlaying='y',
        side='right'
    )
)

## Additional explanations about AQGs and RLs
st.markdown("### Understanding the Numbers")
st.write("correlation between a country's income levels and its air pollution,suggesting that higher income might be associated with better air quality.")

# Show the plot
st.plotly_chart(fig)

