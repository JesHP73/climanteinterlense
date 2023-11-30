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

    # Aggregating data by year for AQI and GNI
    aggregated_data = filtered_data.groupby('year').agg({'AQI_Index':'mean', 'GNI_per_capita':'mean'}).reset_index() #am I calculating the mean of the mean?

    # Plot with Plotly
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add AQI Index trace

   fig.add_trace(
       go.Scatter(x=aggregated_data['year'], y=aggregated_data['AQI_Index'], name='AQI Index',
                  mode='lines+markers', line=dict(color='orange')),
       secondary_y=False,
    )

    # Add GNI per Capita trace

    if 'GNI_per_capita' in aggregated_data.columns:
        fig.add_trace(
            go.Scatter(x=aggregated_data['year'], y=aggregated_data['GNI_per_capita'], name='GNI per Capita',
                       mode='lines+markers', line=dict(color='darkblue')),
            secondary_y=True,
        )

    # Set x-axis title
    fig.update_xaxes(title_text="Year")

    # Set y-axes titles
    fig.update_yaxes(title_text="Air Quality Index", secondary_y=False)
    fig.update_yaxes(title_text="GNI per Capita (EUR)", secondary_y=True)

    # Set figure title and legend
    fig.update_layout(
        title_text="AQI Index and Worl Bank GNI per Capita over Time",
        legend_title_text='Metric',
        legend=dict(
            x=1.05,  # This places the legend to the right of the plot
            y=1,
            xanchor='left',  # This anchors the legend at the left side at x position
            bgcolor='rgba(255,255,255,0.5)'  #This makes the legend slightly transparent
        )
    )

    # Show the plot
    st.plotly_chart(fig)

# Call the function to plot data
if not filtered_data.empty:
    plot_aqi_and_gni_over_time(filtered_data)
else:
    st.error("No data available for the selected filters.")

# Additional insights or summaries based on the filtered data
st.write("Additional insights or data summaries can go here.")

