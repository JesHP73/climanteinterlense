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


df_original = load_data()

# Create a copy of the DataFrame for manipulation
df = df_original.copy()

# Sidebar multiselect for Region and Country
selected_regions = st.sidebar.multiselect('Select Region(s)', options=df['region'].unique(), default=df['region'].unique())
selected_countries = st.sidebar.multiselect('Select Country(ies)', options=df[df['region'].isin(selected_regions)]['country'].unique())

# Filter the DataFrame based on the selections
filtered_df = df[df['region'].isin(selected_regions) & df['country'].isin(selected_countries)]


# Create the AQI Index plot with an explicit name for the legend
fig = px.line(avg_data, x='year', y='AQI_Index', title='Average AQI Index over Time', markers=True, labels={'AQI_Index': 'AQI Index'})
fig.update_traces(name='AQI Index', showlegend=True)

# Create the GNI per Capita plot with an explicit name for the legend
fig.add_scatter(x=avg_data['year'], y=avg_data['GNI_per_capita'], mode='lines+markers', name='GNI per Capita', yaxis='y2', showlegend=True)


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
st.plotly_chart(fig)
      
#st.info("The guidelines and reference levels from WHO are designed to keep air quality at a level that's safe for public health. When pollution levels go above these numbers, it can lead to health concerns for the population, especially vulnerable groups like children and the elderly.")


## Additional explanations about AQGs and RLs
st.markdown("### Understanding the Numbers")
st.write("correlation between a country's income levels and its air pollution,suggesting that higher income might be associated with better air quality.")

