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

# Function to plot annual emissions and compare with WHO standards
def plot_emissions(df, pollutant):
    # Aggregate your data to get annual averages for the selected pollutant
    annual_data = df[df['air_pollutant'] == pollutant].groupby('decade')['emission'].mean().reset_index()

    # Start plotting
    plt.figure(figsize=(10, 5))
    ax = sns.lineplot(x='year', y='emission', data=annual_data)

    # WHO guidelines
    plt.axhline(y=WHO_STANDARDS[pollutant]['AQG'], color='green', linestyle='--', label='WHO AQG')
    plt.axhline(y=WHO_STANDARDS[pollutant]['RL'], color='red', linestyle='--', label='WHO RL')

    # Enhance the plot
    plt.title(f'Annual Average Emissions of {pollutant} (compared to WHO guidelines)')
    plt.xlabel('Year')
    plt.ylabel('Emission Level (μg/m3)')
    plt.legend()

    return plt

# Page content function for Air Pollution Impact
def air_pollution_impact(df):
    if df.empty:
        st.error("No data available to display.")
        return

    st.title("Air Pollution Impact")
    st.write("Visualize the impact of air pollutants over time compared to WHO standards.")

    # Sidebar filter to select pollutants
    selected_pollutant = st.sidebar.selectbox('Select Pollutant', options=list(WHO_STANDARDS.keys()))

    # Call the plotting function
    fig = plot_emissions(df, selected_pollutant)
    st.pyplot(fig)

    # Additional explanations about AQGs and RLs
    st.markdown("### WHO Air Quality Guidelines (AQGs) and Reference Levels (RLs)")
    st.write("AQGs provide guidance on air quality standards to protect public health.")
    st.write("RLs are more lenient standards used for intermediate targets.")

# Load data
df = load_data()

# Call page content function
air_pollution_impact(df)
