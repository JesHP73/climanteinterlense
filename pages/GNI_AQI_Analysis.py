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
pollutants_options = ['All'] + sorted(df['air_pollutant'].unique().tolist())

# Sidebar filters
selected_region = st.sidebar.multiselect('Select Region', options=region_options, default=['All'])
selected_country = st.sidebar.multiselect('Select Country', options=country_options, default=['All'])
selected_pollutants = st.sidebar.multiselect('Select Pollutant', options=pollutants_options, default=['All'])
selected_year = st.sidebar.slider('Select Year', min_value=int(df['year'].min()), max_value=int(df['year'].max()), value=int(df['year'].min()))

# Efficient combined filtering
conditions = []
if 'All' not in selected_region:
    conditions.append(df['region'].isin(selected_region))
if 'All' not in selected_country:
    conditions.append(df['country'].isin(selected_country))
if 'All' not in selected_pollutants:
    conditions.append(df['air_pollutant'].isin(selected_pollutants))
conditions.append(df['year'] == selected_year)

if conditions:
    filtered_data = df[np.logical_and.reduce(conditions)]
else:
    filtered_data = df.copy()

# Function for plotting AQI Index vs GNI per Capita
def plot_aqi_vs_gni(data):
    fig, ax = plt.subplots()
    scatter = ax.scatter(data['GNI_per_capita'], data['AQI_Index'], c=data['year'], cmap='viridis')
    legend1 = ax.legend(*scatter.legend_elements(), title="Years")
    ax.add_artist(legend1)
    ax.set_xlabel('GNI per Capita')
    ax.set_ylabel('AQI Index')
    ax.set_title('GNI per Capita vs AQI Index')
    return fig

# Function for plotting individual pollutants
def plot_individual_pollutant(data, pollutant):
    fig, ax = plt.subplots()
    ax.bar(data['country'], data['AQI_Index'])
    ax.set_xlabel('Country')
    ax.set_ylabel('AQI Index')
    ax.set_title(f'AQI Index for {pollutant}')
    return fig

# Visualization Header
st.header("GNI per Capita and AQI Index Analysis")

# Plotting logic
if 'All' in selected_pollutants or len(selected_pollutants) > 1:
    st.pyplot(plot_aqi_vs_gni(filtered_data))
else:
    for pollutant in selected_pollutants:
        st.subheader(f"Analysis for {pollutant}")
        pollutant_data = filtered_data[filtered_data['air_pollutant'] == pollutant]
        st.pyplot(plot_individual_pollutant(pollutant_data, pollutant))

# Additional insights or summaries based on the filtered data
st.write("Additional insights or data summaries can go here.")
