import streamlit as st
import pandas as pd
#import seaborn as sns
#import matplotlib.pyplot as plt
import numpy as np
import plotly.figure_factory as ff
import scipy
import plotly.express as px


# Function to load data
@st.cache  # Corrected cache decorator
def load_data():
    try:
        URL = 'https://raw.githubusercontent.com/JesHP73/climanteinterlense/main/dataset/global_bourden_risk_factor.csv'
        data = pd.read_csv(URL)
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error
        
def plot_data(filtered_data):
    # Convert the percentage column to numeric, handling non-numeric entries
    filtered_data['total_death_attributed_sex_standarized'] = pd.to_numeric(
        filtered_data['total_death_attributed_sex_standarized'], errors='coerce'
    )

    # Group by 'year' and 'ig_label', then calculate the mean
    aggregated_data = filtered_data.groupby(['year', 'ig_label'], as_index=False)['total_death_attributed_sex_standarized'].mean()

    # Mapping from short labels to full names for income groups
    income_label_mapping = {
        'LM': 'Low Income',
        'UM': 'Upper Middle Income',
        'H': 'High Income'
    }
    # Apply the mapping to the 'ig_label' column
    aggregated_data['ig_label'] = aggregated_data['ig_label'].map(income_label_mapping)

    # Define the color mapping for income groups
    color_discrete_map = {
        'Low Income': 'blue',
        'High Income': 'green',
        'Upper Middle Income': 'brown'
    }

    # Plot the line chart using the aggregated data
    fig = px.line(
        aggregated_data,
        x='year',
        y='total_death_attributed_sex_standarized',
        color='ig_label',
        color_discrete_map=color_discrete_map,
        labels={'total_death_attributed_sex_standarized': 'Percentage of Deaths', 'ig_label': 'Income Group'},
        title='Time Series of Deaths Attributed to Air Pollution by Income Group'
    )

    # Improve layout for better readability
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Percentage of Deaths',
        yaxis_tickformat='.2%',
        showlegend=True,
        legend_title_text='Income Group'
    )

    # Show the figure
    st.plotly_chart(fig)

def display_statistics(filtered_data):
    if not filtered_data.empty:
        # For a dynamic metric, choose a relevant statistic like the latest year's data
        latest_year = filtered_data['year'].max()
        latest_data = filtered_data[filtered_data['year'] == latest_year]
        latest_avg_death_percentage = latest_data['total_death_attributed_sex_standarized'].mean()
        
        correlation = filtered_data['GNI_per_capita_wb_Atlas_USD_EUR'].corr(filtered_data['total_death_attributed_sex_standarized'])
        correlation_label = "Negative" if correlation < 0 else "Positive"
        
        col1, col2 = st.columns(2)
        with col1:
            st.header("Key Fact")
            # Display the latest average percentage or another dynamic statistic
            st.metric(label=f"Avg Deaths in {latest_year}", value=f"{latest_avg_death_percentage:.2f}%")
        with col2:
            st.header("Correlation Analysis")
            # Use Streamlit's built-in method to set the delta color
            delta_color = "inverse" if correlation < 0 else "normal"
            st.metric(label="Income vs. Death Correlation", value=f"{correlation:.2f}", delta=correlation_label, delta_color=delta_color)
    else:
        st.error("Insufficient data to calculate statistics.")

def main():
    # Load data
    original_data = load_data()
    df = original_data.copy()

    if df.empty:
        st.error("No data available to display.")
        return

    st.title('Percentage of Deaths Attributed to Air Pollution, 1990-2019')

    # Sidebar for filters
    st.sidebar.header('Filters')

    # Multiselect for Region and Country
    region_options = ['All'] + sorted(df['region'].unique().tolist())
    country_options = ['All'] + sorted(df['country'].unique().tolist())

    selected_region = st.sidebar.multiselect('Select Region', options=region_options, default=['All'])
    selected_country = st.sidebar.multiselect('Select Country', options=country_options, default=['All'])

    # Apply regional and country filters
    if 'All' not in selected_region:
        df = df[df['region'].isin(selected_region)]
    if 'All' not in selected_country:
        df = df[df['country'].isin(selected_country)]

    # Specify the income groups to filter on
    income_groups = ['LM', 'UM', 'H']  # Use the short labels if those are present in the 'ig_label' column

    # Filter the DataFrame to include only the specified income groups
    filtered_data = df[df['ig_label'].isin(income_groups)]

    if filtered_data.empty:
        st.error("No data available for the selected criteria.")
        return

    # Additional explanations about AQGs and RLs
    st.markdown("### Understanding the Numbers")

    st.info("The guidelines and reference levels from WHO are designed to keep air quality at a level that's safe for public health. When pollution levels go above these numbers, it can lead to health concerns for the population, especially vulnerable groups like children and the elderly.")

    # Plotting
    plot_data(filtered_data)

    # Display statistics
    display_statistics(filtered_data)

if __name__ == "__main__":
    main()
