import streamlit as st
import pandas as pd
#import seaborn as sns
#import matplotlib.pyplot as plt
import numpy as np
import plotly.figure_factory as ff
import scipy
import plotly.express as px


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
        return data 
     except Exception as e:
         st.error(f"Error loading data: {e}")
         return pd.DataFrame()  # Return an empty DataFrame in case of error


def display_pollutant_summary(pollutants):
    return 'All' if 'All' in pollutants else ', '.join(pollutants)

def display_geographical_focus(regions, countries):
    if 'All' not in regions:
        return ', '.join(regions)
    elif 'All' not in countries:
        return ', '.join(countries)

def plot_emissions(df, selected_region, selected_country, selected_pollutant): # ⚠️
    try:
        if df.empty:
            st.error('No data available for the selected filters')
            return
    
        fig = go.Figure()

        if selected_region == 'All' and selected_country == 'All' and selected_pollutant == 'All':
            # Add lines for the WHO standards
            for pollutant, standards in WHO_STANDARDS.items():
                fig.add_hline(y=standards['AQG'], line_dash="dash", line_color="green", annotation_text=f"{pollutant} AQG")
                fig.add_hline(y=standards['RL'], line_dash="dash", line_color="red", annotation_text=f"{pollutant} RL")
            
            # Average pollution levels by decade
            df['decade'] = pd.to_datetime(df['decade'], format='%Y').dt.year
            avg_pollution_by_decade = df.groupby('decade')['avg_AQI_Index'].mean().reset_index()
            fig.add_trace(go.Scatter(x=avg_pollution_by_decade['decade'], y=avg_pollution_by_decade['avg_AQI_Index'],
                                     mode='lines', name='Average Pollution Level'))
          
        else:
        # Initialize list for histogram data and group labels
            hist_data = []
            group_labels = []
            
             # Loop through the selected pollutants
            for pollutant in selected_pollutants:
                if pollutant != 'All':  # Skip 'All' if it's in the list 
                    pollutant_data = df[df['air_pollutant'] == pollutant]['avg_air_pollutant_level'].dropna()
                    if not pollutant_data.empty:
                        hist_data.append(pollutant_data)
                        group_labels.append(pollutant)
    
                # Check if we have any data to plot
            if not hist_data:
                st.error('No data available for the selected pollutants after filtering.')
                return


            # Create distribution plot
            fig = ff.create_distplot(hist_data, group_labels, show_hist=False, show_rug=False)

            # Add WHO AQG and RL lines for the pollutants
            for pollutant in selected_pollutants:
                if pollutant != 'All':  # Skip 'All' if it's in the list
                    aqg = WHO_STANDARDS[pollutant]['AQG']
                    rl = WHO_STANDARDS[pollutant]['RL']
                    fig.add_vline(x=aqg, line_dash="dash", line_color="green", annotation_text=f"{pollutant} AQG")
                    fig.add_vline(x=rl, line_dash="dash", line_color="red", annotation_text=f"{pollutant} RL")
    
        # Update layout for a cleaner look
        fig.update_layout(
            xaxis_title='Pollutant Level (μg/m3)',
            yaxis_title='Decades',
            title='Distribution of Air Pollutant Levels and WHO Limit Standards'
        )

        # Display the plot in Streamlit
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"An error occurred while plotting: {e}")

        
    
def main():
    # Load data
    original_data = load_data()
    df = original_data.copy()
    
    if df.empty:
        st.error("No data available to display.")
        return

    st.title("Understanding Air Pollution and Its Impact")
    st.write("This page provides a simple overview of key aspects of air pollution and its impact on climate change.")
    
    # Filters
    region_options = ['All'] + sorted(df['region'].unique().tolist())
    country_options = ['All'] + sorted(df['country'].unique().tolist())
    pollutant_options = ['All'] + sorted(WHO_STANDARDS.keys())
    
    selected_region = st.sidebar.multiselect('Select Region', options=region_options, default=['All'])
    selected_country = st.sidebar.multiselect('Select Country', options=country_options, default=['All'])
    selected_pollutants = st.sidebar.multiselect('Select Pollutant(s)', options=pollutant_options, default=['All'])
    
    # Efficient combined filtering
    conditions = []
    if 'All' not in selected_region:
        conditions.append(df['region'].isin(selected_region))
    if 'All' not in selected_country:
        conditions.append(df['country'].isin(selected_country))
    if 'All' not in selected_pollutants:
        conditions.append(df['air_pollutant'].isin(selected_pollutants))
    
    if conditions:
        filtered_data = df[np.logical_and.reduce(conditions)]
    else:
        filtered_data = df

    if filtered_data.empty:
        st.error("No data available for the selected criteria.")
        return

   # Main Content - Three Columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.header("Avg. AQI")
        avg_aqi = filtered_data['avg_AQI_Index'].mean()
        col1.metric("Average AQI", f"{avg_aqi:.2f} μg/m3")
    
    with col2:
        st.header("Point 2: Regional Impact")
        # Show how selected region is affected
        # Include relevant content or visualizations for regional impact here
    
    with col3:
        st.header("Higher Income vs Air Quality")
    
        # Check if columns exist
        if 'avg_GNI_PPP' in filtered_data.columns and 'avg_air_pollutant_level' in filtered_data.columns:
            # Calculate correlation
            correlation_gni_pollution = filtered_data[['avg_GNI_PPP', 'avg_air_pollutant_level']].corr().iloc[0, 1]
            col3.metric("Economic Correlation", f"{correlation_gni_pollution:.2f}")
            # Explanatory note about correlation
            col3.caption("A positive value indicates that higher income correlates with higher air pollution levels, and vice versa.")
        else:
            col3.write("Data not available for correlation analysis.")
        

        # Call the plotting function and show the plot
        plot_emissions(df, selected_region, selected_country, selected_pollutant) 
        
        # Additional explanations about AQGs and RLs
        st.markdown("### Understanding the Numbers")
                
        st.info("The guidelines and reference levels from WHO are designed to keep air quality at a level that's safe for public health. When pollution levels go above these numbers, it can lead to health concerns for the population, especially vulnerable groups like children and the elderly.")

# This ensures the app runs when the script is executed
if __name__ == "main":
    main()



