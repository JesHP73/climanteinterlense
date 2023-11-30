#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np

# WHO standards for pollutants
WHO_STANDARDS = {
    'PM10': {'AQG': 15, 'RL': 45},
    'PM2.5': {'AQG': 5, 'RL': 15},
    'O3': {'AQG': 60, 'RL': 100},
    'NO2': {'AQG': 10, 'RL': 25},
    'CO': {'AQG': 4, 'RL': 10}  # Assuming the unit is mg/m3 for simplicity
}

# Function to get the standard value for a given pollutant and standard type
def get_standard(pollutant, standard_type):
    return WHO_STANDARDS.get(pollutant, {}).get(standard_type, None)
    
# Function to load data
@st.cache
def load_data():
    try:
        DATA_URL = 'https://raw.githubusercontent.com/JesHP73/climanteinterlense/main/dataset/air_quality_vs_gni_agg.csv'
        data = pd.read_csv(DATA_URL)
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error

# Assuming load_data() is defined elsewhere
df_original = load_data()

# Create a copy of the DataFrame for manipulation
df = df_original.copy()

def plot_emissions(df, selected_pollutants):
    # Data Validation: Check if dataframe is empty
    if df.empty:
        st.error('No data available for the selected filters')
        return

    # Convert decades to string to avoid commas in the x-axis labels
    df['year'] = df['year'].astype(str)
    
    # Add a new column for each pollutant indicating if it's above the WHO standard
    for pollutant, standards in WHO_STANDARDS.items():
        # Create a mask for rows where the current pollutant matches
        mask = df['air_pollutant'] == pollutant
        # Directly compare where the mask is True
        df.loc[mask, f'{pollutant}_above_AQG'] = df.loc[mask, 'air_pollutant_level'] > standards['AQG']
    
    # Now create a single column 'pollution_above_who' indicating if any pollutant is above its AQG
    pollutants_above_columns = [f'{pollutant}_above_AQG' for pollutant in WHO_STANDARDS]
    df['pollution_above_who'] = df[pollutants_above_columns].any(axis=1, skipna=True)

    # This will hold the countries with the most pollution above WHO standard
    countries_above_who = None

    try:
        if 'All' in selected_pollutants:
            # Calculate the mean across all pollutants for each decade
            overall_mean = df.groupby('year')['air_pollutant_level']

            # Assuming AQG and RL are constants, use a representative value for all pollutants
            aqg = sum([WHO_STANDARDS[pollutant]['AQG'] for pollutant in WHO_STANDARDS]) / len(WHO_STANDARDS)
            rl = sum([WHO_STANDARDS[pollutant]['RL'] for pollutant in WHO_STANDARDS]) / len(WHO_STANDARDS)

            # Create a DataFrame for plotting
            plot_data = overall_mean.to_frame(name='Average Pollution Level')
            plot_data['WHO AQG'] = aqg
            plot_data['WHO RL'] = rl

            # Plot the data using st.line_chart
            st.line_chart(plot_data)

        else:
            # Initialize an empty DataFrame for joined data
            joined_data = pd.DataFrame(index=df['year'].unique())

            # If specific pollutants are selected, filter and plot with WHO standards
            for pollutant in selected_pollutants:
                aqg = WHO_STANDARDS[pollutant]['AQG']
                rl = WHO_STANDARDS[pollutant]['RL']

                # Filter data for the current pollutant
                pollutant_data = df[df['air_pollutant'] == pollutant]

                # Calculate the average pollutant level per decade
                avg_pollutant_data = pollutant_data.groupby('year')['air_pollutant_level'].rename(f'Avg {pollutant} Pollution Level')
                                                                                                               
                # Join the average data with the joined_data DataFrame
                joined_data = joined_data.join(avg_pollutant_data, how='left')

                # Add the AQG and RL values as constant columns to joined_data
                joined_data[f'{pollutant}_AQG'] = aqg
                joined_data[f'{pollutant}_RL'] = rl

            # Check if joined_data is empty after processing
            if joined_data.empty:
                st.error('No data available to plot after processing.')
                return

            # Plot the data using st.line_chart
            st.line_chart(joined_data)

            countries_above_who = df[df['pollution_above_who']].groupby('country').size().sort_values(ascending=False)
            if not countries_above_who.empty:
                most_polluted_country = countries_above_who.idxmax()
                st.warning(f"The country with the most pollution above WHO standard is: {most_polluted_country}")

            # If only one pollutant is selected, add a caption for clarity
            if len(selected_pollutants) == 1:
                st.caption(f'Line represents average levels of {selected_pollutants[0]} over time. '
                           f'WHO AQG and RL for {selected_pollutants[0]} are also shown.')


        # User input areas
        region_options = ['All'] + sorted(df['region'].unique().tolist())
        country_options = ['All'] + sorted(df['country'].unique().tolist())
        pollutants_options = ['All'] + sorted(df['air_pollutant'].unique().tolist())
        
        # Sidebar filters
        selected_region = st.sidebar.multiselect('Select Region', options=region_options, default=['All'])
        selected_country = st.sidebar.multiselect('Select Country', options=country_options, default=['All'])
        selected_pollutants = st.sidebar.multiselect('Select Pollutant', options=pollutants_options, default=['All'])
        selected_year = st.sidebar.slider('Select Year', min_value=int(df['year'].min()), max_value=int(df['year'].max()), value=int(df['year'].min()))
        
        # Efficient combined filtering
        conditions = []
        if 'All' not in selected_region:
            conditions.append(df['region'].isin(selected_region))
        if 'All' not in selected_country:
            conditions.append(df['country'].isin(selected_country))
        if 'All' not in selected_pollutants:
            conditions.append(df['air_pollutant'].isin(selected_pollutants))
        conditions.append(df['year'] == selected_year)
        
        if conditions:
            filtered_data = df[np.logical_and.reduce(conditions)]
        else:
            filtered_data = df.copy()
        
        # Sort the data for line plotting
        filtered_data.sort_values(by='year', inplace=True)

 except Exception as e:
        st.error(f"An error occurred while plotting: {e}")


# Function for plotting AQI Index and GNI per Capita over time as lines
def plot_aqi_and_gni_over_time(data):
    # Debugging: print out the data types and lengths of the series being plotted
    print("Year data type:", data['year'].dtype, "Length:", len(data['year']))
    print("AQI Index data type:", data['AQI_Index'].dtype, "Length:", len(data['AQI_Index']))
    print("GNI per Capita data type:", data['GNI_per_capita'].dtype, "Length:", len(data['GNI_per_capita']))
    
    # Ensure data is sorted by year
    data = data.sort_values('year')
    
    fig, ax1 = plt.subplots()

    # Plot AQI_Index
    ax1.plot(data['year'], data['AQI_Index'], 'r-')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('AQI Index', color='r')
    
    # Create a second y-axis for GNI per capita
    ax2 = ax1.twinx()
    ax2.plot(data['year'], data['GNI_per_capita'], 'b-')
    ax2.set_ylabel('GNI per Capita', color='b')

    # Make the layout tight to handle the second y-axis
    fig.tight_layout()
    return fig


# Function for plotting individual pollutants with emissions levels and units
def plot_individual_pollutant_with_levels(data, pollutant, unit_column, level_column):
    fig, ax = plt.subplots()
    sns.lineplot(x='year', y=level_column, data=data, ax=ax, label=pollutant)
    ax.set_ylabel(f"{pollutant} ({data[unit_column].iloc[0]})")
    ax.set_xlabel('Year')
    ax.set_title(f"Yearly Trend of {pollutant}")
    return fig


# Visualization Header
st.header("GNI per Capita and AQI Index Analysis Over Time")

# Determine the correct plot based on the user's selection of pollutants
if 'All' in selected_pollutants or len(selected_pollutants) > 1:
    st.pyplot(plot_aqi_and_gni_over_time(filtered_data))
else:
    for pollutant in selected_pollutants:
        st.subheader(f"Analysis for {pollutant}")
        pollutant_data = filtered_data[filtered_data['air_pollutant'] == pollutant]
        # Assume 'unit_air_poll_lvl' and 'air_pollutant_level' are the columns with units and levels
        st.pyplot(plot_individual_pollutant_with_levels(pollutant_data, pollutant, 'unit_air_poll_lvl', 'air_pollutant_level'))
        # Call the plotting function and show the plot
        plot_emissions(df, selected_pollutants)
        
st.info("The guidelines and reference levels from WHO are designed to keep air quality at a level that's safe for public health. When pollution levels go above these numbers, it can lead to health concerns for the population, especially vulnerable groups like children and the elderly.")


## Additional explanations about AQGs and RLs
st.markdown("### Understanding the Numbers")
st.write("correlation between a country's income levels and its air pollution,suggesting that higher income might be associated with better air quality.")

