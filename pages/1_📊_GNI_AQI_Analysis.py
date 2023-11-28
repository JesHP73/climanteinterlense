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
def show_gni_aqi_analysis(df):
    if df.empty:
        st.error("No data available to display.")
        return

    st.title("📊 GNI vs AQI Analysis")
    st.write("Here you can analyze how Gross National Income (GNI) correlates with Air Quality Index (AQI).")

    # Sidebar filters
    selected_region = st.sidebar.multiselect('Select Region', options=df['region'].unique(), default=df['region'].unique())
    selected_country = st.sidebar.multiselect('Select Country', options=df['country'].unique(), default=df['country'].unique())
    selected_decade = st.sidebar.multiselect('Select Decade', options=df['decade'].unique(), default=df['decade'].unique())

    # Data filtering based on sidebar selection
    if not selected_region:
        filtered_data = df
    else:
        filtered_data = df[
            (df['region'].isin(selected_region)) &
            (df['country'].isin(selected_country)) &
            (df['decade'].isin(selected_decade))
        ]

    # Plotting
    if not filtered_data.empty:
        fig, ax = plt.subplots()
        sns.scatterplot(data=filtered_data, x='avg_GNI_PPP', y='avg_AQI_Index', hue='region', ax=ax)
        plt.title("Scatter Plot of GNI vs AQI by Region")
        plt.xlabel("Average GNI (PPP)")
        plt.ylabel("Average AQI Index")
        st.pyplot(fig)
    else:
        st.write("No data to display. Please adjust the filter options.")

# Load data
df = load_data()

# Call page content function
show_gni_aqi_analysis(df)
