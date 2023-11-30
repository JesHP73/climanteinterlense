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
    # Filters
    region_options = ['All'] + sorted(df['region'].unique().tolist())
    country_options = ['All'] + sorted(df['country'].unique().tolist())
    
    selected_region = st.sidebar.multiselect('Select Region', options=region_options, default=['All'])
    selected_country = st.sidebar.multiselect('Select Country', options=country_options, default=['All'])

    # Efficient combined filtering
    conditions = []
    if 'All' not in selected_region:
        conditions.append(df['region'].isin(selected_region))
    if 'All' not in selected_country:
        conditions.append(df['country'].isin(selected_country))
    if conditions:
        filtered_data = df[np.logical_and.reduce(conditions)]
    else:
        filtered_data = df.copy()

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

def plot_data(filtered_data):
    fig = px.line(filtered_data, x='year', y='total_death_attributed_sex_standarized',
                  color='ig_label', title='Line Chart')
    st.plotly_chart(fig)  

def display_statistics(filtered_data):
    # Calculate the average percentage of deaths and the correlation
    avg_death_percentage = filtered_data['total_death_attributed_sex_standarized'].mean()
    correlation = filtered_data['GNI_per_capita_wb_Atlas_USD_EUR'].corr(filtered_data['total_death_attributed_sex_standarized'])

    # Using columns to display the statistics
    col1, col2 = st.columns(2)

    with col1:
        st.header("Key Fact")
        st.metric(label="Average Deaths Attributed to Air Pollution", value=f"{avg_death_percentage:.2f}%")

    with col2:
        st.header("Correlation Analysis")
        correlation_label = "Positive" if correlation > 0 else "Negative"
        st.metric(label="Income vs. Death Correlation", value=f"{correlation:.2f}", delta=correlation_label)



