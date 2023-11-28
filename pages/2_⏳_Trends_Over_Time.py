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
    DATA_URL = 'https://github.com/JesHP73/climanteinterlense/blob/1bdbb328a91258a4f0021ec3392e95d7126ae9fb/dataset/socio_economical_agg_dataset.csv'
    data = pd.read_csv(DATA_URL)
    return data

# Page content function
def show_trends_over_time(df):
    st.title("⏳ Trends Over Time")
    st.write("Explore trends in air quality and economic development over time.")

    # Sidebar filters
    selected_metric = st.sidebar.selectbox('Select Metric', options=['avg_AQI_Index', 'avg_GNI_PPP', 'total_population'])
    selected_region = st.sidebar.multiselect('Select Region', options=df['region'].unique())

    # Data filtering based on sidebar selection
    filtered_data = df[df['region'].isin(selected_region)]

    # Plotting
    fig, ax = plt.subplots()
    sns.lineplot(data=filtered_data, x='decade', y=selected_metric, hue='region', ax=ax)
    st.pyplot(fig)

# Load data
df = load_data()

# Call page content function
show_trends_over_time(df)

