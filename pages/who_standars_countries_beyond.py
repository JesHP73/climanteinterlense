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
        DATA_URL = 'https://raw.githubusercontent.com/JesHP73/climanteinterlense/main/dataset/who_standars_air_quality_countries.csv'
        data = pd.read_csv(DATA_URL)
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error


df_original = load_data()

# Create a copy of the DataFrame for manipulation
df = df_original.copy()

# WHO Standards
who_standards = {
    'PM10': {'annual': 15},
    'PM2.5': {'annual': 5},
    'NO2': {'annual': 10}
}

# EU Standards
eu_standards = {
    'PM10': {'annual': 40, '24_hours': 50},
    'PM2.5': {'annual': 25, 'stage2_annual': 20},
    'NO2': {'annual': 40, '1_hour': 200}
}

# Plotting Function

def plot_data(df_mean_levels, who_standards, eu_standards, selected_pollutant):
    # Making sure the selected pollutant is in the WHO standards dictionary
    if selected_pollutant not in who_standards:
        st.error(f"Selected pollutant {selected_pollutant} does not have a WHO standard defined.")
        return

    # Calculating the difference from the WHO standard and sort
    standard_who = who_standards[selected_pollutant]['annual']
    df_filtered = df_mean_levels.assign(difference=lambda x: x['air_pollutant_level'] - standard_who)
    df_filtered = df_filtered.sort_values('difference', ascending=False)

    # Define a custom color sequence for the regions
    custom_colors = ['teal', 'crimson', 'forestgreen', 'darkorange', 'goldenrod', 'darkslateblue', 'plum']

    # Updating the Plotly figure to use the sorted data with custom colors
    fig = px.bar(df_filtered, x='country', y='air_pollutant_level', color='region',
                 title=f'Average {selected_pollutant} Emissions by Country in 2023',
                 labels={'country': 'Country', 'air_pollutant_level': f'Average {selected_pollutant} Level (μg/m³)'},
                 color_discrete_sequence=custom_colors)

    # Rotating the x-axis labels
    fig.update_layout(xaxis_tickangle=-45)
      

    # Setting a fixed y-axis range
    fig.update_yaxes(autorange=True)

    # Setting the figure size and moving the legend position outside to the right
    fig.update_layout(
        height=600,
        width=1000,
        legend=dict(
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05  # This places the legend outside the plot to the right
        ),
        margin=dict(r=150) 
    )

    # Add the EU standard line if it exists for the selected pollutant
    eu_standard = eu_standards.get(selected_pollutant, {}).get('annual')
    if eu_standard is not None:
        # Add a dummy trace for the EU standard to appear in the legend
        fig.add_trace(
            go.Scatter(
                x=[None], 
                y=[None], 
                mode='lines', 
                name=f"EU {selected_pollutant} Annual Standard 2011 (μg/m³)", 
                line=dict(color='blue', dash='dash')
            )
        )
        # Add the actual EU standard line (without a name parameter)
        fig.add_hline(y=eu_standard, line_dash='dash', line_color='blue')

    # Add the WHO standard line and a corresponding dummy trace for the legend
    fig.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode='lines',
            name=f"WHO {selected_pollutant} Annual Standard 2021 (μg/m³)",
            line=dict(color='red', width=2)
        )
    )
    # Add the actual WHO standard line (without a name parameter)
    fig.add_hline(y=standard_who, line_dash='solid', line_color='red')

    # Display the figure in Streamlit
    st.plotly_chart(fig, use_container_width=True)



# User input areas for filtering
region_options = ['All'] + sorted(df['region'].unique().tolist())
pollutants_options = sorted(df['air_pollutant'].unique().tolist())

# Sidebar for user input
selected_region = st.sidebar.multiselect('Select Region', options=region_options, default=['All'])
selected_pollutant = st.sidebar.selectbox('Select Pollutant', options=pollutants_options)

# Filtering for the selected pollutant and the year 2023
df_filtered = df[(df['air_pollutant'] == selected_pollutant) & (df['year'] == 2023)]

# Apply the selected region filter if not 'All'
if 'All' not in selected_region:
    df_filtered = df_filtered[df_filtered['region'].isin(selected_region)]

# Exclude Türkiye from the dataset
df_filtered = df_filtered[df_filtered['country'] != 'Turkiye']

# Ensure the air pollutant level is a numeric type
df_filtered['air_pollutant_level'] = pd.to_numeric(df_filtered['air_pollutant_level'], errors='coerce')

# Group by both country and region, then calculate the mean air pollution level
df_mean_levels = df_filtered.groupby(['country', 'region'])['air_pollutant_level'].mean().reset_index()

standard = who_standards[selected_pollutant]['annual']
df_mean_levels['difference'] = df_mean_levels['air_pollutant_level'] - standard

df_mean_levels = df_mean_levels.sort_values('difference', ascending=False)

if df_mean_levels.empty:
    st.error('No data available for the selected filters.')
else:
    plot_data(df_mean_levels, who_standards, eu_standards, selected_pollutant)

import streamlit as st

# Custom CSS for styling
custom_css = """
<style>
.markdown-style-teal {
    background-color: #d8f3f0;  /* Light teal background */
    padding: 10px;
    border-radius: 10px;  /* Rounded corners */
}
.markdown-style-crimson {
    background-color: #f2d8d8;  /* Light crimson background */
    padding: 10px;
    border-radius: 10px;
}
.markdown-style-forestgreen {
    background-color: #d8f2df;  /* Light forest green background */
    padding: 10px;
    border-radius: 10px;
}
</style>
"""

# Define the explanations
explanation_pm10 = custom_css + """
<div class="markdown-style-teal">

**PM10 (like tiny dust):** These are really small bits like dust that can get into our nose when we breathe. They can make it hard to breathe and cause coughs.

</div>
"""
explanation_pm25 = custom_css + """
<div class="markdown-style-crimson">

**PM2.5 (even tinier than PM10):** These are super tiny particles, even smaller than PM10. They can go deep into our lungs causing problems like asthma.

</div>
"""
explanation_no2 = custom_css + """
<div class="markdown-style-forestgreen">

**NO2 (comes from cars and factories):** This gas comes from cars and factories. It can make the air smelly and hard to breathe, and it's not good for our lungs.

</div>
"""

# Display the explanations in columns
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(explanation_pm10, unsafe_allow_html=True)
with col2:
    st.markdown(explanation_pm25, unsafe_allow_html=True)
with col3:
    st.markdown(explanation_no2, unsafe_allow_html=True)







