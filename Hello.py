#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd
#from annotated_text import annotated_text

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

st.markdown("""
    <h1 style='text-align: center;'>
        <span style='font-size: 1.5em;'>W</span>elcome to the Intersectional 
        <span style='color: green;'>Climate</span> Learning and Action Helper
    </h1>
    """, unsafe_allow_html=True)

#st.markdown("### Welcome to the Intersectional :green[Climate] Learning and Action Helper")
#st.markdown("Hello, *World!* :earth_americas:", unsafe_allow_html=True)

st.divider()

with st.expander("👋 Hey! Thanks for Stopping By"):
    st.write("I'm here to communicate a really complicated topic as simply as I can, so bear with me.")
    st.write("Let’s get to know each other with a few fun definitions.")

with st.expander("🌬️ What is Air Pollution?"):
    st.write("Imagine you're playing outside, and the air is filled with tiny, invisible specks that you can't see—kind of like during Covid times. These specks can make you feel sick :sneezing_face: if you breathe too much of them. This is what air pollution is like. It's like having tiny bits of dirt and smoke in the air that can hurt our lungs and hearts.")

with st.expander("🧩 What is Intersectionality?"):
    st.write("Well, now imagine everyone is different, like pieces in a puzzle. I believe that some people get sicker from air pollution than others because of where they live :house_buildings: or how much money :euro: they have. This is what we adults call 'intersectionality.' It means that many things about a person, like where they live or what they look like, can change how something, like air pollution, affects them.")
    
st.divider()

st.write("I wish you a good snooping! 👋, I'll be around, with **Learn More buttons**, and simplifying this hot topic for you.")

st.markdown("""
    This site examines the intersection of climate data with socio-economic factors.
    **👈 Select a page from the sidebar** to begin exploring the visualizations and insights.
    ### Want to learn more?  
""")

st.sidebar.success("Select a page above.")
st.sidebar.header("Quick Guide")
st.sidebar.write("Explore the tabs to dive into the impacts of air pollution through an intersectional lens.")

st.divider()

# Educational Links
st.markdown("### Educational Resources")
st.markdown("[Learn more about Air Pollution](https://example.com/airpollution)")
st.markdown("[Understanding Intersectionality](https://example.com/intersectionality)")

# Disclaimer
st.markdown("## Disclaimer")
st.write("The information provided here is for educational purposes only...")

# Credits and Data Sources
st.markdown("## Credits and Data Sources")
st.write("The data used in this application is sourced from ...")
st.markdown("[Data Source 1](https://example.com/source1)")
st.markdown("[Data Source 2](https://example.com/source2)")
