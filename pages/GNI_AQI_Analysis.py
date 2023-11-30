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

# Sidebar filters
selected_region = st.sidebar.multiselect('Select Region', options=region_options, default=['All'])
selected_country = st.sidebar.multiselect('Select Country', options=country_options, default=['All'])

# Efficient combined filtering
conditions = []
if 'All' not in selected_region:
    conditions.append(df['region'].isin(selected_region))
if 'All' not in selected_country:
    conditions.append(df['country'].isin(selected_country))

if conditions:
    filtered_data = df[np.logical_and.reduce(conditions)]
else:
    filtered_data = df.copy()


# Function for plotting AQI Index vs GNI per Capita

def plot_aqi_and_gni_over_time(filtered_data):
    if filtered_data.empty:
        st.error('No data available for plotting.')
        return

    # Convert 'year' to numeric
    if not pd.api.types.is_numeric_dtype(filtered_data['year']):
        filtered_data['year'] = pd.to_numeric(filtered_data['year'], errors='coerce')

    # Drop rows where 'year' or 'AQI_Index' is NaN
    filtered_data = filtered_data.dropna(subset=['year', 'AQI_Index'])

    if filtered_data.empty:
        st.error('No data available for plotting after cleaning.')
        return

    if 'GNI_per_capita' in filtered_data.columns:
        # Plot with Plotly
        fig = px.line(filtered_data, x='year', y='AQI_Index', title='AQI Index over Time', markers=True)
        
        # Create a secondary y-axis for GNI per capita
        fig.add_scatter(x=filtered_data['year'], y=filtered_data['GNI_per_capita'], mode='lines+markers', name='GNI per Capita', yaxis='y2')
        
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
    else:
        st.warning("GNI_per_capita data not available for plotting.")


# Call the function to plot data
if not filtered_data.empty:
    plot_aqi_and_gni_over_time(filtered_data)
else:
    st.error("No data available for the selected filters.")

# Additional insights or summaries based on the filtered data
st.write("Additional insights or data summaries can go here.")

