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
def show_air_pollution_impact(df):
    if df.empty:
        st.error("No data available to display.")
        return

    st.title("🌍 Air Pollution Impact")
    st.write("Analyze the differential impact of air pollution based on demographic data.")

    # Sidebar filters
    selected_region = st.sidebar.multiselect('Select Region', options=df['region'].unique(), default=df['region'].unique())
    selected_country = st.sidebar.multiselect('Select Country', options=df['country'].unique(), default=df['country'].unique())
    selected_zone = st.sidebar.multiselect('Select Zone', options=df['zone'].unique(), default=df['zone'].unique())

    # Data filtering based on sidebar selection
    if not selected_region and not selected_country and not selected_zone:
        filtered_data = df
    else:
        filtered_data = df[
            (df['region'].isin(selected_region)) &
            (df['country'].isin(selected_country)) &
            (df['zone'].isin(selected_zone))
        ]

    # Plotting
    if not filtered_data.empty:
        fig, ax = plt.subplots()
        sns.barplot(data=filtered_data, x='air_pollutant', y='avg_air_pollutant_level', hue='age_group', ax=ax)
        plt.title("Impact of Air Pollution by Age Group")
        plt.xlabel("Air Pollutant")
        plt.ylabel("Average Air Pollutant Level")
        st.pyplot(fig)
    else:
        st.write("No data to display. Please adjust the filter options.")

# Load data
df = load_data()

# Call page content function
show_air_pollution_impact(df)
