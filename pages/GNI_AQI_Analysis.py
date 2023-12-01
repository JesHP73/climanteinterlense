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

    # Aggregating data by year and income group for AQI and GNI
    aggregated_data = filtered_data.groupby(['year', 'ig_label']).agg({'AQI_Index':'mean', 'GNI_per_capita':'mean'}).reset_index()

       # Define the color mapping for income groups with long names
    color_mapping = {
        'LM': ('Low Income', 'blue'),
        'UM': ('Middle Income', 'grey'),
        'H': ('High Income', 'grey'),
    }
    
    # Create the subplots
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add AQI Index trace with its own legend group
    fig.add_trace(
        go.Scatter(x=aggregated_data['year'], y=aggregated_data['AQI_Index'], name='AQI Index',
                   mode='lines+markers', line=dict(color='orange'), legendgroup='AQI'),
        secondary_y=False,
    )
    
    # Add GNI per Capita traces for each income group with their own legend group
    legend_groups = {'LM': 'Low Income', 'UM': 'Middle Income', 'H': 'High Income'}
    colors = {'LM': 'blue', 'UM': 'grey', 'H': 'grey'}
    
    for ig_label, name in legend_groups.items():
        # Filter the data for the current income group
        income_group_data = aggregated_data[aggregated_data['ig_label'] == ig_label]
        fig.add_trace(
            go.Scatter(x=income_group_data['year'], y=income_group_data['GNI_per_capita'],
                       name=name, mode='lines+markers', line=dict(color=colors[ig_label]),
                       legendgroup='GNI'),
            secondary_y=True,
        )
    
    # Set x-axis title
    fig.update_xaxes(title_text="Year")
    
    # Set y-axes titles
    fig.update_yaxes(title_text="AQI Index", secondary_y=False)
    fig.update_yaxes(title_text="GNI per Capita (EUR)", secondary_y=True)
    
    # Set figure title
    fig.update_layout(
        title_text="AQI Index and World Bank GNI per Capita over Time",
        legend_title_text='Metric',
        legend=dict(
            orientation="h",
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1
            
        )
    )
    
    # Set the position of the legend for AQI Index
    fig['data'][0]['showlegend'] = True
    fig['data'][0]['legendgroup'] = 'AQI'
    
    # Set the position of the legends for GNI per Capita income groups
    
    for i, ig_label in enumerate(legend_groups, start=1):
        fig['data'][i]['showlegend'] = True
        fig['data'][i]['legendgroup'] = 'GNI'
    
    # Show the plot
    st.plotly_chart(fig)


# Call the function to plot data
if not filtered_data.empty:
    plot_aqi_and_gni_over_time(filtered_data)
else:
    st.error("No data available for the selected filters.")

# Additional insights or summaries based on the filtered data
st.write("Additional insights or data summaries can go here.")

