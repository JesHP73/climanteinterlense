#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd
#from annotated_text import annotated_text

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
    st.write("Well, now imagine everyone is different, like pieces in a puzzle. I believe that some people get sicker from air pollution than others because of where they live :house_buildings: or how much money :euro: they have. Intersectionality, in the context of Climate and socio-economic data, refers to the recognition that individuals and communities are shaped by multiple intersecting social identities and factors. It emphasises that people's experiences and vulnerabilities are not determined by a single characteristic or variable but are the result of the interplay between various dimensions of identity and social context. These dimensions can include gender, race, ethnicity, socioeconomic status, age, and more.")
    
st.divider()

# Define the custom CSS style
custom_css = """
<style>
.markdown-style {
    background-color: #e6f4ea;  /* Light green background */
    border-left: 5px solid #34a853;  /* Darker green left border */
    padding: 10px;  /* Padding inside the box */
    font-size: 16px;  /* Text size */
    color: #202124;  /* Text color - dark grey for readability */
}
</style>
"""

# Define highlighted text with markdown
highlighted_text = custom_css + """
<div class="markdown-style">
While the climate crisis affects us all, <strong>marginalised communities</strong> feel its effects the most. The struggles for <strong>climate, racial, social, and economic justice</strong> are inherently interconnected, yet much of Europe's climate work has yet to embrace an intersectional approach.
</div>
<div class="markdown-style">
<strong>👈🏽Embark on an enlightening exploration</strong> of how climate intertwines with <strong>socio-economic dynamics</strong>. <strong>Begin your journey</strong> by selecting a page from the sidebar.
</div>
<div class="markdown-style">
<strong>Dive in and explore</strong> with interactive <strong>"Learn More" buttons</strong>, designed to unravel the complexities of this crucial topic and inspire action towards a more equitable and sustainable future.
</div>
"""


# Display the combined content with the styling
st.markdown(highlighted_text, unsafe_allow_html=True)

st.sidebar.success("Select a page above.")
st.sidebar.header("Quick Guide")
st.sidebar.write("Explore the tabs to dive into the impacts of air pollution through an intersectional lens.")

st.divider()

# Educational Links
st.markdown("### Educational Resources:")    
st.markdown("[Climate Justice](https://systemicjustice.ngo/what-we-do/community-litigation/climate-justice/)")
st.markdown("[Understanding Intersectionality](https://www.intersectionaljustice.org/who-we-are)")

# Credits and Data Sources
st.markdown("## Credits and Data Sources")
st.write("The data used in this application is sourced from:")
st.markdown("[World Bank - Global Economic Monitor](https://datahelpdesk.worldbank.org/knowledgebase/articles/906519-world-bank-country-and-lending-groups)")
st.markdown("[Eurostat - Statistical Office of the European Union.](https://ec.europa.eu/eurostat/databrowser/explore/all/all_themes?lang=en&display=list&sort=category)")

# Disclaimer
st.markdown("## Disclaimer:")
st.write("The information provided here is for educational purposes only")
