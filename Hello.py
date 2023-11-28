#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import 1_📊_GNI_AQI_Analysis.py
import 2_⏳_Trends_Over_Time.py
import 3_🌍_Air_Pollution_Impact.py

# Function to load data
@st.cache
def load_data():
    DATA_URL = 'https://raw.githubusercontent.com/JesHP73/climanteinterlense/main/dataset/socio_economical_agg_dataset.csv'
    data = pd.read_csv(DATA_URL)
    return data

# Load data
df = load_data()

st.set_page_config(
    page_title="Intersectional Climate Trends",
    page_icon="🌎",
)

st.write("# Welcome to the Intersectional Climate Trends App 🌎")

st.sidebar.success("Select a page above.")

st.markdown(
    """
    This app examines the intersection of climate data with socio-economic factors.
    **👈 Select a page from the sidebar** to begin exploring the visualizations and insights.
    ### Want to learn more?
    - Check out [our GitHub repository](https://github.com/yourusername/your-repo-name)
    """
)

