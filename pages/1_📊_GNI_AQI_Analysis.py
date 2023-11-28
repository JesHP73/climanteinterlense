#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Function to load data
@st.cache
def load_data():
    DATA_URL = 'https://raw.githubusercontent.com/JesHP73/climanteinterlense/main/dataset/socio_economical_agg_dataset.csv'
    data = pd.read_csv(DATA_URL)
    return data

# Page content function
def show_gni_aqi_analysis(df):
    st.title("📊 GNI vs AQI Analysis")
    st.write("Here you can analyze how Gross National Income (GNI) correlates with Air Quality Index (AQI).")

    # Sidebar filters
    selected_region = st.sidebar.multiselect('Select Region', options=df['region'].unique())
    selected_country = st.sidebar.multiselect('Select Country', options=df['country'].unique())
    selected_decade = st.sidebar.multiselect('Select Decade', options=df['decade'].unique())

    # Data filtering based on sidebar selection
    filtered_data = df[
        (df['region'].isin(selected_region)) &
        (df['country'].isin(selected_country)) &
        (df['decade'].isin(selected_decade))
    ]

    # Plotting
    fig, ax = plt.subplots()
    sns.scatterplot(data=filtered_data, x='avg_GNI_PPP', y='avg_AQI_Index', hue='region', ax=ax)
    st.pyplot(fig)

# Load data
df = load_data()

# Call page content function
show_gni_aqi_analysis(df)

