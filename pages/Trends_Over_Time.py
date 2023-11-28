#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Function to load data
@st.cache
def load_data():
    try:
        DATA_URL = 'https://raw.githubusercontent.com/JesHP73/climanteinterlense/main/dataset/socio_economical_agg_dataset.csv'
        data = pd.read_csv(DATA_URL)
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error

# Page content function
def show_trends_over_time(df):
    if df.empty:
        st.error("No data available to display.")
        return

    st.title("⏳ Trends Over Time")
    st.write("Explore trends in air quality and economic development over time.")

    # Sidebar filters
    selected_metric = st.sidebar.selectbox('Select Metric', options=['avg_AQI_Index', 'avg_GNI_PPP', 'total_population'])
    selected_region = st.sidebar.multiselect('Select Region', options=df['region'].unique(), default=df['region'].unique())

    # Data filtering based on sidebar selection
    if not selected_region:
        filtered_data = df
    else:
        filtered_data = df[df['region'].isin(selected_region)]

    # Plotting
    if not filtered_data.empty:
        fig, ax = plt.subplots()
        sns.lineplot(data=filtered_data, x='decade', y=selected_metric, hue='region', ax=ax)
        plt.title(f"Trends of {selected_metric} Over Decades by Region")
        plt.xlabel("Decade")
        plt.ylabel(selected_metric)
        st.pyplot(fig)
    else:
        st.write("No data to display. Please adjust the filter options.")

# Load data
df = load_data()

# Call page content function
show_trends_over_time(df)
