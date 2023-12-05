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

def plot_data(df_mean_levels, who_standards, selected_pollutant):
    # Making sure the selected pollutant is in the WHO standards dictionary
    if selected_pollutant not in who_standards:
        st.error(f"Selected pollutant {selected_pollutant} does not have a WHO standard defined.")
        return

    # Calculating the difference from the WHO standard and sort
    standard = who_standards[selected_pollutant]['annual']
    df_filtered = df_mean_levels.assign(difference=lambda x: x['air_pollutant_level'] - standard)
    df_filtered = df_mean_levels.sort_values('difference', ascending=False)

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
        height=600,  # Adjust the height as needed
        width=800,   # Adjust the width as needed
        legend=dict(
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05  # This places the legend outside the plot to the right
        ),
        # Adjust the right margin to ensure there is enough space for the legend
        margin=dict(r=150) 
    )
    
    # Adding a dummy trace for the WHO standard to appear in the legend
    fig.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode='lines',
            name=f"WHO {selected_pollutant} Annual Standard (μg/m³)",
            line=dict(color='red', width=2)
        )
    )

    # Add the actual WHO standard line (without a name parameter)
    fig.add_hline(y=standard, line_dash='solid', line_color='red')

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

# Ensure the air pollutant level is a numeric type
df_filtered['air_pollutant_level'] = pd.to_numeric(df_filtered['air_pollutant_level'], errors='coerce')

# Group by both country and region, then calculate the mean air pollution level
df_mean_levels = df_filtered.groupby(['country', 'region'])['air_pollutant_level'].mean().reset_index()

# Add a 'difference' column to df_mean_levels
standard = who_standards[selected_pollutant]['annual']
df_mean_levels['difference'] = df_mean_levels['air_pollutant_level'] - standard

# Now sorting by 'difference'
df_mean_levels = df_mean_levels.sort_values('difference', ascending=False)

# Check if the DataFrame is empty after all filters have been applied
if df_mean_levels.empty:
    st.error('No data available for the selected filters.')
else:
    # If data is present, call the plotting function with the mean levels
    plot_data(df_mean_levels, who_standards, selected_pollutant)


# Function to load data
@st.cache
def load_data2():
    try:
        DATA_URL = 'https://raw.githubusercontent.com/JesHP73/climanteinterlense/main/dataset/pollution_by_industry_2023.csv'
        data = pd.read_csv(DATA_URL)
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error


df_pie = load_data2()

# Create a copy of the DataFrame for manipulation
pie = df_pie.copy()


# Function to filter data and plot the pie chart
def plot_pollution_pie_chart(pie):
    # Filter the DataFrame for entries from the year 2023
    data_2023 = pie[pie['year'] == 2023]

    # Group by 'air_qual_stat_type' and sum up 'air_pollutant_level'
    pollution_by_industry_2023 = pie.groupby('air_qual_stat_type')['air_pollutant_level'].mean()

    # Plot a pie chart
    plt.figure(figsize=(10, 8))
    plt.pie(pollution_by_industry_2023, labels=pollution_by_industry_2023.index, autopct='%1.1f%%', startangle=140)
    plt.title('Percentage of Pollution Responsibility by Industry for 2023')
    return plt

 
# Plotting the pie chart
st.subheader("Pollution Responsibility by Industry for 2023")
plot_pollution_pie_chart(pie)
st.pyplot(chart)





