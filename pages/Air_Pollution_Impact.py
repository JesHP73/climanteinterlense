import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
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

# to handle if 'air_pollutant' could contain values not present in WHO_STANDARDS, you might run into a KeyError.
def get_standard(pollutant, standard_type):
    return WHO_STANDARDS.get(pollutant, {}).get(standard_type, float('nan'))

# Function to plot annual average pollutant levels and compare with WHO standards
def plot_emissions(df, selected_pollutants):
    plt.figure(figsize=(10, 5))

    # Data Validation: Check if dataframe is empty
    if df.empty:
        plt.text(0.5, 0.5, 'No data available for the selected filters', ha='center', va='center', fontsize=12)
        return plt

    # Check if required columns are present
    if 'decade' not in df.columns or 'avg_air_pollutant_level' not in df.columns:
        plt.text(0.5, 0.5, 'Required columns not found in the data', ha='center', va='center', fontsize=12)
        return plt

    try:
        # Check if 'All' pollutants are selected
        if 'All' in selected_pollutants:
            # Calculate the mean across all pollutants for each decade
            annual_mean_all = df.groupby('decade')['avg_air_pollutant_level'].mean().reset_index()
            if df['decade'].nunique() == 1:
                # Use bar plot for a single decade
                sns.barplot(x='decade', y='avg_air_pollutant_level', data=annual_mean_all)
                plt.axhline(y='avg_air_pollutant_level', color='blue', label='Average All Airpollutants', alpha=0.5)
            else:
                # Use line plot for multiple decades
                sns.lineplot(x='decade', y='avg_air_pollutant_level', data=annual_mean_all, label='Average All Pollutants')

            # Plot the average WHO guidelines for all pollutants
            avg_AQG = np.mean([get_standard(pollutant, 'AQG') for pollutant in WHO_STANDARDS])
            avg_RL = np.mean([get_standard(pollutant, 'RL') for pollutant in WHO_STANDARDS])
            plt.axhline(y=avg_AQG, color='teal', linestyle='--', label='Average WHO AQG', alpha=0.5)
            plt.axhline(y=avg_RL, color='orange', linestyle='--', label='Average WHO RL', alpha=0.5)

        else:
            # Plot each selected pollutant and its WHO guidelines
            for pollutant in selected_pollutants:
                # Filter and calculate mean for the selected pollutant
                annual_data = df[df['air_pollutant'] == pollutant].groupby('decade')['avg_air_pollutant_level'].mean().reset_index()
                sns.lineplot(x='decade', y='avg_air_pollutant_level', data=annual_data, label=pollutant)
                # Plot WHO guideline lines for the selected pollutant using get_standard
                plt.axhline(y=get_standard(pollutant, 'AQG'), color='teal', linestyle='--', label=f'WHO AQG ({pollutant})', alpha=0.5)
                plt.axhline(y=get_standard(pollutant, 'RL'), color='orange', linestyle='--', label=f'WHO RL ({pollutant})', alpha=0.5)

        # Set plot titles and labels
        plt.title('Annual Average Levels of Pollutants (compared to WHO guidelines)')
        plt.xlabel('Decade')
        plt.ylabel('Average Level (μg/m3)')

        # Place the legend outside the plot
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
        plt.tight_layout()

    except Exception as e:
        # Handle any errors that occur during plotting
        plt.text(0.5, 0.5, f'Error while plotting: {e}', ha='center', va='center', fontsize=12)

    return plt

               

def display_key_facts(df, pollutants, zones, regions, countries):
    st.subheader("Key Facts")

    # Simplified Selection summaries for a non-expert audience
    st.write(f"**Pollutants being analyzed:** {'All' if 'All' in pollutants else ', '.join(pollutants)}")
    st.write(f"**Geographical focus:** {', '.join(zones if 'All' not in zones else regions if 'All' not in regions else countries)}")

    # Check if there is data to display
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

    # Filter the DataFrame based on selections
    if 'All' not in selected_decade:
        df = df[df['decade'].isin(selected_decade)]
    if 'All' not in selected_zone:
        df = df[df['zone'].isin(selected_zone)]
    if 'All' not in selected_region:
        df = df[df['region'].isin(selected_region)]
    if 'All' not in selected_country:
        df = df[df['country'].isin(selected_country)]
    if 'All' not in selected_pollutants:
        df = df[df['air_pollutant'].isin(selected_pollutants)]

    # Call the plotting function and show the plot
    fig = plot_emissions(df, selected_pollutants)
    st.pyplot(fig)


    # Call the function to display key facts with current DataFrame and selections
    display_key_facts(df, selected_pollutants, selected_zone, selected_region, selected_country)

# This ensures the app runs when the script is executed
if __name__ == "__main__":
    main()

