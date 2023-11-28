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

# Function to load data
@st.cache
def load_data():
    try:
        DATA_URL = 'https://raw.githubusercontent.com/JesHP73/climanteinterlense/main/dataset/socio_economical_agg_dataset.csv'
        data = pd.read_csv(DATA_URL)
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of an error.
        pass

def plot_emissions(df, selected_pollutants):
    # Data Validation: Check if dataframe is empty
    if df.empty:
        st.error('No data available for the selected filters')
        return

    # Convert decades to string to avoid commas in the x-axis labels
    df['decade'] = df['decade'].astype(str)

    try:
        if 'All' in selected_pollutants:
            # Calculate the mean across all pollutants for each decade
            annual_mean_all = df.groupby('decade')['avg_air_pollutant_level'].mean().reset_index()
            # Rename column for better labeling in the chart
            annual_mean_all.rename(columns={'avg_air_pollutant_level': 'Avg All Pollution Level'}, inplace=True)
            st.line_chart(annual_mean_all.set_index('decade'))
        else:
            # If specific pollutants are selected, filter and plot with WHO standards
            for pollutant in selected_pollutants:
                aqg = WHO_STANDARDS[pollutant]['AQG']
                rl = WHO_STANDARDS[pollutant]['RL']
                # Add columns with the AQG and RL standard
                df[f'{pollutant}_AQG'] = aqg
                df[f'{pollutant}_RL'] = rl

            # Pivot data for selected pollutants
            filtered_data = df[df['air_pollutant'].isin(selected_pollutants)]
            pivot_data = filtered_data.pivot(index='decade', columns='air_pollutant', values='avg_air_pollutant_level')

            # Rename columns for better labeling in the chart
            for pollutant in selected_pollutants:
                pivot_data.rename(columns={pollutant: f'Avg {pollutant} Pollution Level'}, inplace=True)

            st.line_chart(pivot_data.join(df[[f'{pollutant}_AQG' for pollutant in selected_pollutants] + 
                                            [f'{pollutant}_RL' for pollutant in selected_pollutants]]).set_index('decade'))
            
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

        st.write(f"**Air quality concerns:** Air pollution levels exceeded safe limits set by WHO {exceedances_aqg} times.")
        st.write(f"**Reference level concerns:** Pollution levels went beyond the recommended reference levels {exceedances_rl} times.")

        # Population exposure, rounded and simplified
        population_exposed_aqg_pm25 = round(df[df['avg_air_pollutant_level'] > WHO_STANDARDS['PM2.5']['AQG']]['total_population'].sum())
        population_exposed_aqg_pm10 = round(df[df['avg_air_pollutant_level'] > WHO_STANDARDS['PM10']['AQG']]['total_population'].sum())
        st.write(f"**People affected by PM2.5:** Approximately {population_exposed_aqg_pm25:,} people live in areas with PM2.5 above WHO's safe limit.")
        st.write(f"**People affected by PM10:** Around {population_exposed_aqg_pm10:,} people are exposed to PM10 levels exceeding the guidelines.")

        # Correlation between GNI and pollutant levels, rounded and simplified
        correlation_gni_pollution = round(df[['avg_GNI_PPP', 'avg_air_pollutant_level']].corr().iloc[0, 1], 2)
        st.write(f"**Economic correlation:** There's a {correlation_gni_pollution} correlation between a country's income levels and its air pollution, suggesting that higher income might be associated with better air quality.")

        with st.expander("Air Pollution Metrics"):
            display_pollution_metrics(df)

        with st.expander("WHO Standards and Exceedances"):
            display_standard_exceedances(df)

        with st.expander("Population Exposure and Economic Correlation"):
            display_population_exposure_and_economic_correlation(df)

        # Additional explanations about AQGs and RLs
        st.markdown("### Understanding the Numbers")
        st.info("The guidelines and reference levels from WHO are designed to keep air quality at a level that's safe for public health. When pollution levels go above these numbers, it can lead to health concerns for the population, especially vulnerable groups like children and the elderly.")
    else:
        st.error("No data available for the selected criteria.")
    

# Main body of your Streamlit app
def main():
   
    # Load data
    df = load_data()
    
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
        df_filtered = df[np.logical_and.reduce(conditions)]
    else:
        df_filtered = df

        # Example of correct indentation
    if not df_filtered.empty:
        plot_emissions(df_filtered, selected_pollutants)
        display_key_facts(df_filtered, selected_pollutants, selected_zone, selected_region, selected_country)
    else:
        st.error("No data available for the selected criteria.")
    
    # Call the plotting function and show the plot
    plot_emissions(df_filtered, selected_pollutants)

    # Call the function to display key facts with current DataFrame and selections
    display_key_facts(df_filtered, selected_pollutants, selected_zone, selected_region, selected_country) 

# This ensures the app runs when the script is executed
if __name__ == "__main__":
    main()

