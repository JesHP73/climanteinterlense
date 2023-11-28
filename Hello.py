#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd

# This should be the first Streamlit command
st.set_page_config(
    page_title="Intersectional Climate Trends",
    page_icon="🌎"
)

# Function to load data
@st.cache
def load_data():
    DATA_URL = 'https://raw.githubusercontent.com/JesHP73/climanteinterlense/main/dataset/socio_economical_agg_dataset.csv'
    data = pd.read_csv(DATA_URL)
    return data

# Load data
df = load_data()

st.write("# Welcome to the Intersectional Climate Trends App 🌎")

st.sidebar.success("Select a page above.")

st.markdown(
    """
    This app examines the intersection of climate data with socio-economic factors.
    **👈 Select a page from the sidebar** to begin exploring the visualizations and insights.
    ### Want to learn more?  
    """
)
