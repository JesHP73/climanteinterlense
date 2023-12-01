#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

data = [
    {"country": "Turkiye", "latitude": 38.959759, "longitude": 34.924965, "avg_air_pollutant_level": 38.613282},
    {"country": "North Macedonia", "latitude": 41.617121, "longitude": 21.716839, "avg_air_pollutant_level": 37.784629},
    {"country": "Cyprus", "latitude": 34.917416, "longitude": 32.889903, "avg_air_pollutant_level": 34.235318},
    {"country": "Montenegro", "latitude": -12.699819, "longitude": -38.326076, "avg_air_pollutant_level": 32.072987},
    {"country": "Greece", "latitude": 43.209784, "longitude": -77.693060, "avg_air_pollutant_level": 29.474272},
    {"country": "Serbia", "latitude": 44.024323, "longitude": 21.076574, "avg_air_pollutant_level": 29.314807},
    {"country": "Italy", "latitude": 42.638426, "longitude": 12.674297, "avg_air_pollutant_level": 29.269817},
    {"country": "Slovenia", "latitude": 46.119944, "longitude": 14.815333, "avg_air_pollutant_level": 28.151276},
    {"country": "Norway", "latitude": 64.573154, "longitude": 11.528036, "avg_air_pollutant_level": 28.036179},
    {"country": "Poland", "latitude": 52.215933, "longitude": 19.134422, "avg_air_pollutant_level": 27.893044},
    {"country": "Malta", "latitude": 35.888599, "longitude": 14.447691, "avg_air_pollutant_level": 27.486028},
    {"country": "Croatia", "latitude": 45.365844, "longitude": 15.657521, "avg_air_pollutant_level": 27.228628},
    {"country": "United Kingdom", "latitude": 54.702354, "longitude": -3.276575, "avg_air_pollutant_level": 26.000324},
    {"country": "Albania", "latitude": 1.231526, "longitude": -75.892043, "avg_air_pollutant_level": 25.924407},
    {"country": "Hungary", "latitude": 41.976763, "longitude": -72.778984, "avg_air_pollutant_level": 25.905718},
    {"country": "Bulgaria", "latitude": 46.788917, "longitude": 23.618491, "avg_air_pollutant_level": 25.848658},
    {"country": "Portugal", "latitude": 39.662165, "longitude": -8.135352, "avg_air_pollutant_level": 25.549835},
    {"country": "Spain", "latitude": 39.326068, "longitude": -4.837979, "avg_air_pollutant_level": 25.234821},
    {"country": "Latvia", "latitude": 56.840649, "longitude": 24.753764, "avg_air_pollutant_level": 24.614239},
    {"country": "Switzerland", "latitude": 46.798562, "longitude": 8.231974, "avg_air_pollutant_level": 24.179193},
    {"country": "Netherlands", "latitude": 52.243498, "longitude": 5.634323, "avg_air_pollutant_level": 24.090245},
    {"country": "Austria", "latitude": 47.593970, "longitude": 14.124560, "avg_air_pollutant_level": 23.463365},
    {"country": "Belgium", "latitude": 50.640281, "longitude": 4.666715, "avg_air_pollutant_level": 23.344792},
    {"country": "Germany", "latitude": 40.420348, "longitude": -79.116698, "avg_air_pollutant_level": 23.340626},
    {"country": "Denmark", "latitude": 55.670249, "longitude": 10.333328, "avg_air_pollutant_level": 23.283157},
    {"country": "Ireland", "latitude": 52.865196, "longitude": -7.979460, "avg_air_pollutant_level": 23.155319},
    {"country": "France", "latitude": 46.603354, "longitude": 1.888334, "avg_air_pollutant_level": 22.743511},
    {"country": "Lithuania", "latitude": 55.350000, "longitude": 23.750000, "avg_air_pollutant_level": 22.580176},
    {"country": "Romania", "latitude": 45.985213, "longitude": 24.685923, "avg_air_pollutant_level": 22.569274},
    {"country": "Finland", "latitude": 63.246778, "longitude": 25.920916, "avg_air_pollutant_level": 22.017252}
]


# Create a DataFrame
df = pd.DataFrame(data)

fig = px.choropleth(df, 
                    locations="country", 
                    locationmode="country names",
                    color="avg_air_pollutant_level",
                    hover_name="country",
                    color_continuous_scale=px.colors.sequential.Plasma,
                    title="Average Air Pollution Levels by Country",
                    scope="europe",  # Set the scope to 'europe'
                    projection="natural earth")  # Choose a projection that fits 

# Improve map aesthetics
fig.update_layout(
    geo=dict(
        showframe=False,  # Removes the frame around the map
        showcoastlines=True,  # Shows coastline
        projection_type='equirectangular'  # Change the projection type if needed
    ),
    paper_bgcolor='rgba(0,0,0,0)',  # Sets the background color of the paper
    plot_bgcolor='rgba(0,0,0,0)'  # Sets the background color of the plot
)

# Update the color scale to be more distinctive
fig.update_traces(marker_line_width=0, selector=dict(type='choropleth'))

# Show the figure
fig.show()

# Inside your Streamlit app script
st.plotly_chart(fig, use_container_width=True)





