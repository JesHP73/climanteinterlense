import streamlit as st
import pandas as pd
#import seaborn as sns
#import matplotlib.pyplot as plt
import numpy as np
import plotly.figure_factory as ff
import scipy
import plotly.express as px


# Function to load data
@st.cache_data  # 👈 Add the caching decorator
def load_data():
    try:
        URL = 'https://raw.githubusercontent.com/JesHP73/climanteinterlense/main/dataset/socio_economical_agg_dataset.csv'
        data = pd.read_csv(URL)
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error


def main():
     # Load data
    original_data = load_data()
    df = original_data.copy()
    
    if df.empty:
        st.error("No data available to display.")
        return
        
    st.title('Percentage of Deaths Attributed to Air Pollution, 1990-2022')

    # Sidebar for filters
    st.sidebar.header('Filters')

    # Multiselect for Region and Country
    regions = df['region'].unique()
    selected_regions = st.sidebar.multiselect('Select Region', regions, default=regions)

    countries = df[df['region'].isin(selected_regions)]['country'].unique()
    selected_countries = st.sidebar.multiselect('Select Country', countries, default=countries)

    # Filter the DataFrame based on selections
    filtered_df = df[df['region'].isin(selected_regions) & df['country'].isin(selected_countries)]

    # Plotting
    plot_data(filtered_df)

    # Display statistics
    display_statistics(filtered_df)

if __name__ == "__main__":
    main()

def plot_data(filtered_df):
    fig = px.line(filtered_df, x='year', y='total_death_attributed_sex_standarized',
                  color='ig_label', title='Line Chart')
    st.plotly_chart(fig)

def display_statistics(filtered_df):
    # Calculate the average percentage of deaths and the correlation
    avg_death_percentage = filtered_df['total_death_attributed_sex_standarized'].mean()
    correlation = filtered_df['GNI_per_capita_wb_Atlas_USD_EUR'].corr(filtered_df['total_death_attributed_sex_standarized'])

    # Using columns to display the statistics
    col1, col2 = st.columns(2)

    with col1:
        st.header("Key Fact")
        st.metric(label="Average Deaths Attributed to Air Pollution", value=f"{avg_death_percentage:.2f}%")

    with col2:
        st.header("Correlation Analysis")
        correlation_label = "Positive" if correlation > 0 else "Negative"
        st.metric(label="Income vs. Death Correlation", value=f"{correlation:.2f}", delta=correlation_label)



