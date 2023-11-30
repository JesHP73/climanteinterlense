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
    
    # Mapping from short labels to full names for income groups
    income_label_mapping = {
        'LM': 'Low Income',
        'UM': 'Upper Middle Income',
        'H': 'High Income'
    }

    # Replace short labels with full names in the dataframe
    filtered_data['ig_label'] = filtered_data['ig_label'].map(income_label_mapping)

    # Plot the line chart
    fig = px.line(filtered_data, 
                  x='year', 
                  y='total_death_attributed_sex_standarized', 
                  color='ig_label',
                  labels={'total_death_attributed_sex_standarized': 'Percentage of Deaths', 'ig_label': 'Income Group'},
                  title='Time Series of Deaths Attributed to Air Pollution by Income Group')

    # Improve layout for better readability
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Percentage of Deaths',
        yaxis_tickformat='.2%',  # Display y-axis values as percentages with 2 decimal places
        showlegend=True,
        legend_title_text='Income Group'
    )

    # Show the figure
    st.plotly_chart(fig)

  

def display_statistics(filtered_data):
    
    if not filtered_data.empty:
        max_death_percentage = filtered_data['total_death_attributed_sex_standarized'].max()
        correlation = filtered_data['GNI_per_capita_wb_Atlas_USD_EUR'].corr(filtered_data['total_death_attributed_sex_standarized'])
        correlation_label = "Negative" if correlation < 0 else "Positive"
        # Determine the delta color based on the correlation sign
        delta_color = "inverse" if correlation < 0 else "normal"
        
        col1, col2 = st.columns(2)
        with col1:
            st.header("Key Fact")
            st.metric(label="Max Deaths Attributed to Air Pollution", value=f"{max_death_percentage:.2f}%")
        with col2:
            st.header("Correlation Analysis")
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

    st.title('Percentage of Deaths Attributed to Air Pollution, 1990-2022')

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
