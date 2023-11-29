import streamlit as st
import pandas as pd
#import seaborn as sns
#import matplotlib.pyplot as plt
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
@st.cache_data  # 👈 Add the caching decorator
def load_data():
     try:
        URL = 'https://raw.githubusercontent.com/JesHP73/climanteinterlense/main/dataset/socio_economical_agg_dataset.csv'
        data = pd.read_csv(URL)
        return data #= pickle.load(data, fix_imports=True, encoding='ASCII', errors='strict', buffers=None)
     except Exception as e:
         st.error(f"Error loading data: {e}")
         return pd.DataFrame()  # Return an empty DataFrame in case of error


def plot_emissions(df, selected_pollutants):
    # Data Validation: Check if dataframe is empty
    if df.empty:
        st.error('No data available for the selected filters')
        return

    # Convert decades to string to avoid commas in the x-axis labels
    df['decade'] = df['decade'].astype(str)
    
    # Add a new column for each pollutant indicating if it's above the WHO standard
    for pollutant, standards in WHO_STANDARDS.items():
        # Create a mask for rows where the current pollutant matches
        mask = df['air_pollutant'] == pollutant
        # Directly compare where the mask is True
        df.loc[mask, f'{pollutant}_above_AQG'] = df.loc[mask, 'avg_air_pollutant_level'] > standards['AQG']
    
    # Now create a single column 'pollution_above_who' indicating if any pollutant is above its AQG
    pollutants_above_columns = [f'{pollutant}_above_AQG' for pollutant in WHO_STANDARDS]
    df['pollution_above_who'] = df[pollutants_above_columns].any(axis=1, skipna=True)

    # This will hold the countries with the most pollution above WHO standard
    countries_above_who = None

    try:
        if 'All' in selected_pollutants:
            # Calculate the mean across all pollutants for each decade
            overall_mean = df.groupby('decade')['avg_air_pollutant_level'].mean()

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
            joined_data = pd.DataFrame(index=df['decade'].unique())

            # If specific pollutants are selected, filter and plot with WHO standards
            for pollutant in selected_pollutants:
                aqg = WHO_STANDARDS[pollutant]['AQG']
                rl = WHO_STANDARDS[pollutant]['RL']

                # Filter data for the current pollutant
                pollutant_data = df[df['air_pollutant'] == pollutant]

                # Calculate the average pollutant level per decade
                avg_pollutant_data = pollutant_data.groupby('decade')['avg_air_pollutant_level'].mean().rename(f'Avg {pollutant} Pollution Level')
                                                                                                               
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
    except Exception as e:
        st.error(f"An error occurred while plotting: {e}")


        
def display_pollutant_summary(pollutants):
    return 'All' if 'All' in pollutants else ', '.join(pollutants)

def display_geographical_focus(zones, regions, countries):
    if 'All' not in zones:
        return ', '.join(zones)
    elif 'All' not in regions:
        return ', '.join(regions)
    else:
        return ', '.join(countries)

def display_key_facts(df, pollutants, zones, regions, countries):
    
    st.subheader("Key Facts")

    # Simplified Selection summaries for a non-expert audience
    st.write(f"**Pollutants being analyzed:** {display_pollutant_summary(pollutants)}")
    st.write(f"**Geographical focus:** {display_geographical_focus(zones, regions, countries)}")

    if not df.empty:
        # Simplified metrics
        avg_pollutant_level = round(df['avg_air_pollutant_level'].mean())
        max_pollutant_level = round(df['avg_air_pollutant_level'].max())
        min_pollutant_level = round(df['avg_air_pollutant_level'].min())
        st.metric(label="Average level of air pollution", value=f"{avg_pollutant_level} μg/m3")
        st.metric(label="Highest recorded air pollution level", value=f"{max_pollutant_level} μg/m3")
        st.metric(label="Lowest recorded air pollution level", value=f"{min_pollutant_level} μg/m3")

        # Instances exceeding WHO standards
        exceedances_aqg = df[df['avg_air_pollutant_level'] > df['air_pollutant'].apply(lambda x: get_standard(x, 'AQG'))].shape[0]
        exceedances_rl = df[df['avg_air_pollutant_level'] > df['air_pollutant'].apply(lambda x: get_standard(x, 'RL'))].shape[0]

        st.metric(label='How many times the limits has been exceed', value=f"({exceedances_aqg})
                
    


        # Population exposure, rounded and simplified
        population_exposed_aqg_pm25 = round(df[df['avg_air_pollutant_level'] > WHO_STANDARDS['PM2.5']['AQG']]['total_population'].sum())
        population_exposed_aqg_pm10 = round(df[df['avg_air_pollutant_level'] > WHO_STANDARDS['PM10']['AQG']]['total_population'].sum())
                  
                  
        st.metric(label=f"**People**", value=f"{population_exposed_aqg_pm25:,} people live in areas with PM2.5 is above WHO's safe limit.")
        st.metric(label=f"**Approximately**", value=f"{population_exposed_aqg_pm10:,} people are exposed to PM10 levels exceeding the guidelines.")

        # Correlation between GNI and pollutant levels, rounded and simplified
        correlation_gni_pollution = round(df[['avg_GNI_PPP', 'avg_air_pollutant_level']].corr().iloc[0, 1], 2)
        st.metric(f"**Economic correlation:** There's a {correlation_gni_pollution} correlation between a country's income levels and its air pollution, suggesting that higher income might be associated with better air quality.")

        #with st.expander("Air Pollution Metrics"):
            #display_pollution_metrics(df)

        #with st.expander("WHO Standards and Exceedances"):
            #display_standard_exceedances(df)

        #with st.expander("Population Exposure and Economic Correlation"):
            #display_population_exposure_and_economic_correlation(df)

        # Additional explanations about AQGs and RLs
        st.markdown("### Understanding the Numbers")
        st.info("The guidelines and reference levels from WHO are designed to keep air quality at a level that's safe for public health. When pollution levels go above these numbers, it can lead to health concerns for the population, especially vulnerable groups like children and the elderly.")
    else:
        st.error("No data available for the selected criteria.")


# Main body of your Streamlit app
def main():
    # Load data
    original_data = load_data()
    df = original_data.copy()
    
    # Call the page content function
    air_pollution_impact(df)
    

# Page content function for Air Pollution Impact
def air_pollution_impact(df):
    if df.empty:
        st.error("No data available to display.")
        return

    st.title("Air Pollution Impact")
    st.write("Visualize the impact of air pollutants over time compared to WHO standards.")

    # User input areas
    # Sidebar filters
    decade_options = ['All'] + sorted(df['decade'].unique().tolist())
    zone_options = ['All'] + sorted(df['zone'].unique().tolist())
    region_options = ['All'] + sorted(df['region'].unique().tolist())
    country_options = ['All'] + sorted(df['country'].unique().tolist())
    pollutant_options = ['All'] + sorted(WHO_STANDARDS.keys())

    selected_decade = st.sidebar.multiselect('Select Decade', options=decade_options, default=['All'])
    selected_zone = st.sidebar.multiselect('Select Zone', options=zone_options, default=['All'])
    selected_region = st.sidebar.multiselect('Select Region', options=region_options, default=['All'])
    selected_country = st.sidebar.multiselect('Select Country', options=country_options, default=['All'])
    selected_pollutants = st.sidebar.multiselect('Select Pollutant(s)', options=pollutant_options, default=['All'])

    
    # Efficient combined filtering
    conditions = []
    if 'All' not in selected_decade:
        conditions.append(df['decade'].isin(selected_decade))
    if 'All' not in selected_zone:
        conditions.append(df['zone'].isin(selected_zone))
    if 'All' not in selected_region:
        conditions.append(df['region'].isin(selected_region))
    if 'All' not in selected_country:
        conditions.append(df['country'].isin(selected_country))
    if 'All' not in selected_pollutants:
        conditions.append(df['air_pollutant'].isin(selected_pollutants))
    
    if conditions:
        df_filtered = df[np.logical_and.reduce(conditions)].copy()
    else:
        df_filtered = df.copy()

        # Example of correct indentation
    if not df_filtered.empty:
        plot_emissions(df_filtered, selected_pollutants)
        display_key_facts(df_filtered, selected_pollutants, selected_zone, selected_region, selected_country)
    else:
        st.error("No data available for the selected criteria.")
    
        # Call the plotting function and show the plot
        plot_emissions(df, selected_pollutants)
    
        # Call the function to display key facts with current DataFrame and selections
        display_key_facts(df, selected_pollutants, selected_zone, selected_region, selected_country) 

# This ensures the app runs when the script is executed
if __name__ == "__main__":
    # Adding a button to clear the cache
    if st.sidebar.button('Clear Cache'):
        st.legacy_caching.clear_cache()
        st.success('Cache cleared!')

    main()


