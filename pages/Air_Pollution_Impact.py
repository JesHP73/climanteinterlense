import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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

# Function to plot annual average pollutant levels and compare with WHO standards
def plot_emissions(df, pollutant):
    # Aggregate your data to get annual averages for the selected pollutant
    annual_data = df[df['air_pollutant'] == pollutant].groupby('decade')['avg_air_pollutant_level'].mean().reset_index()

    # Start plotting
    plt.figure(figsize=(10, 5))
    ax = sns.lineplot(x='decade', y='avg_air_pollutant_level', data=annual_data)

    # WHO guidelines
    plt.axhline(y=WHO_STANDARDS[pollutant]['AQG'], color='green', linestyle='--', label='WHO AQG')
    plt.axhline(y=WHO_STANDARDS[pollutant]['RL'], color='red', linestyle='--', label='WHO RL')

    # Enhance the plot
    plt.title(f'Annual Average Levels of {pollutant} (compared to WHO guidelines)')
    plt.xlabel('Decade')
    plt.ylabel('Average Level (μg/m3)')
    plt.legend()

    return plt


# New function to display key facts
def display_key_facts(df, pollutants, zones, regions, countries):
    st.subheader("Key Facts")
    
    # Selection summaries for a non-expert audience
    st.write(f"**Pollutants selected:** {'All' if 'All' in pollutants else ', '.join(pollutants)}")
    st.write(f"**Zones selected:** {'All' if 'All' in zones else ', '.join(zones)}")
    st.write(f"**Regions selected:** {'All' if 'All' in regions else ', '.join(regions)}")
    st.write(f"**Countries selected:** {'All' if 'All' in countries else ', '.join(countries)}")

    # Ensure there is data to display
    if not df.empty:
        # Mean pollutant levels
        mean_pollutant_levels = df['avg_air_pollutant_level'].mean()
        st.write(f"**Average pollutant level:** {mean_pollutant_levels:.2f} μg/m3 - This is the average level of pollutants in the air for the selected criteria.")

        # Highest and Lowest Pollutant Levels
        max_pollutant_level = df['avg_air_pollutant_level'].max()
        min_pollutant_level = df['avg_air_pollutant_level'].min()
        st.write(f"**Highest pollutant level:** {max_pollutant_level:.2f} μg/m3 - This represents the peak level of air pollution recorded in the selected data.")
        st.write(f"**Lowest pollutant level:** {min_pollutant_level:.2f} μg/m3 - This is the lowest level of air pollution observed in the selected data.")

        # Instances exceeding WHO standards
        exceedances_aqg = df[df['avg_air_pollutant_level'] > df['air_pollutant'].apply(lambda x: WHO_STANDARDS[x]['AQG'])].shape[0]
        exceedances_rl = df[df['avg_air_pollutant_level'] > df['air_pollutant'].apply(lambda x: WHO_STANDARDS[x]['RL'])].shape[0]
        st.write(f"**Instances above WHO Air Quality Guidelines (AQG):** {exceedances_aqg} times - This number shows how often the pollution levels have exceeded safe limits set by WHO.")
        st.write(f"**Instances above WHO Reference Levels (RL):** {exceedances_rl} times - This count indicates the frequency of pollution levels going beyond the recommended reference levels.")

        # Zone, Region, and Country specific averages
        if 'All' not in zones:
            zone_stats = df.groupby('zone')['avg_air_pollutant_level'].mean()
            st.write(f"**Average pollutant levels by zone:** {zone_stats.to_dict()} - Averages for each selected zone are shown here.")

        if 'All' not in regions:
            region_stats = df.groupby('region')['avg_air_pollutant_level'].mean()
            st.write(f"**Average pollutant levels by region:** {region_stats.to_dict()} - These are the regional averages of air pollution.")

        if 'All' not in countries:
            country_stats = df.groupby('country')['avg_air_pollutant_level'].mean()
            st.write(f"**Average pollutant levels by country:** {country_stats.to_dict()} - This presents the average pollution levels for each chosen country.")

        # Population exposure to high levels of PM2.5 and PM10
        population_exposed_aqg_pm25 = df[df['avg_air_pollutant_level'] > WHO_STANDARDS['PM2.5']['AQG']]['total_population'].sum()
        st.write(f"**Population exposed above PM2.5 WHO AQG:** {population_exposed_aqg_pm25} - Indicates the total number of people living in areas where the PM2.5 levels are above the safe limit.")

        population_exposed_aqg_pm10 = df[df['avg_air_pollutant_level'] > WHO_STANDARDS['PM10']['AQG']]['total_population'].sum()
        st.write(f"**Population exposed above PM10 WHO AQG:** {population_exposed_aqg_pm10} - Reflects the total population exposed to PM10 levels that exceed WHO's air quality guidelines.")

        # Correlation between GNI and pollutant levels
        correlation_gni_pollution = df[['avg_GNI_PPP', 'avg_air_pollutant_level']].corr().iloc[0, 1]
        st.write(f"**Correlation between GNI and pollutant levels:** {correlation_gni_pollution:.2f} - A measure of the relationship between a country's income levels and its air pollution. A higher value indicates a stronger relationship.")

        # Additional explanations about AQGs and RLs
        st.markdown("### WHO Air Quality Guidelines (AQGs) and Reference Levels (RLs)")
        st.write("AQGs provide guidance on air quality standards to protect public health. RLs are more lenient standards used for intermediate targets.")
    else:
        st.error("No data available for the selected criteria.")

# Main body of your Streamlit app
def main():
    # Load data
    df = load_data()

# Page content function for Air Pollution Impact
# Modified page content function with added multiselects and 'All' option
def air_pollution_impact(df):
    if df.empty:
        st.error("No data available to display.")
        return

    st.title("Air Pollution Impact")
    st.write("Visualize the impact of air pollutants over time compared to WHO standards.")

    # Sidebar filters
    zone_options = ['All'] + df['zone'].unique().tolist()
    region_options = ['All'] + df['region'].unique().tolist()
    country_options = ['All'] + df['country'].unique().tolist()
    pollutant_options = ['All'] + list(WHO_STANDARDS.keys())

    selected_zone = st.sidebar.multiselect('Select Zone', options=zone_options, default='All')
    selected_region = st.sidebar.multiselect('Select Region', options=region_options, default='All')
    selected_country = st.sidebar.multiselect('Select Country', options=country_options, default='All')
    selected_pollutants = st.sidebar.multiselect('Select Pollutant(s)', options=pollutant_options, default='All')

    # Filter the DataFrame based on selections
    if 'All' not in selected_zone:
        df = df[df['zone'].isin(selected_zone)]
    if 'All' not in selected_region:
        df = df[df['region'].isin(selected_region)]
    if 'All' not in selected_country:
        df = df[df['country'].isin(selected_country)]
    if 'All' not in selected_pollutants:
        df = df[df['air_pollutant'].isin(selected_pollutants)]

    # Call the plotting function for each selected pollutant or all if 'All' is selected
    if 'All' in selected_pollutants:
        pollutants_to_plot = list(WHO_STANDARDS.keys())
    else:
        pollutants_to_plot = selected_pollutants

    for pollutant in pollutants_to_plot:
        fig = plot_emissions(df, pollutant)
        st.pyplot(fig)

        # After plotting, call the function to display key facts
        display_key_facts(df, selected_pollutants, selected_zone, selected_region, selected_country)


# Load data
df = load_data()

# Call page content function
air_pollution_impact(df);

# Call the main function to run the app
if __name__ == "__main__":
    main()
