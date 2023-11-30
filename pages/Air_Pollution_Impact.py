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
    
    # Calculate the percentage of deaths
    filtered_data['death_percentage'] = (filtered_data['num_deaths'] / filtered_data['population']) * 100
    
    # Group by 'year' and 'ig_label', then calculate the mean percentage
    aggregated_data = filtered_data.groupby(['year', 'ig_label'], as_index=False)['death_percentage'].mean()

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
        'Upper Middle Income': 'grey'
    }

    # Plot the line chart using the aggregated data
    fig = px.line(
        aggregated_data,
        x='year',
        y='death_percentage',
        color='ig_label',
        color_discrete_map=color_discrete_map,
        labels={'death_percentage': 'Percentage of Deaths', 'ig_label': 'Income Group'},
        title='Deaths Attributed to Air Pollution by Income Group'
    )

    # Improve layout for better readability
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Percentage of Deaths',
        yaxis_tickformat='.2%', # Ensuring that y-axis labels are formatted as percentages
        showlegend=True,
        legend_title_text='Income Group'
    )

    # Show the figure
    st.plotly_chart(fig)


def display_statistics(filtered_data):
    
    if not filtered_data.empty:
        latest_year = filtered_data['year'].max()
        latest_data = filtered_data[filtered_data['year'] == latest_year]
        latest_avg_death_percentage = latest_data['total_death_attributed_sex_standarized'].mean()

        if 'people_affected' in latest_data.columns:
            people_affected = latest_data['people_affected'].mean()
        else:
            st.warning("Column 'people_affected' not found in the data.")
            people_affected = None

        col1, col2 = st.columns(2)
        with col1:
            st.header("Rate Per 100 Thousand Total Population")
            st.metric(label=f"Avg Deaths in {latest_year}", value=f"{latest_avg_death_percentage:.2f}%")
        with col2:
            st.header("Equivalent to")
            if people_affected is not None:
                st.metric(label="Number of People", value=f"{people_affected:.2f}", delta="Delta Value")
            else:
                st.write("People affected data is not available.")
    else:
        st.error("Insufficient data to calculate statistics.")



def main():
    # Load data
    original_data = load_data()
    df = original_data.copy()

    if df.empty:
        st.error("No data available to display.")
        return

    st.title('Percentage of Deaths Attributed to Air Pollution')

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
    st.markdown("### Understanding What You See")
    
    # Plotting
    plot_data(filtered_data)
     # Display statistics
    display_statistics(filtered_data)
    
    st.info(" The IHME, Global Burden of Disease Dataset studied, provides the Death by Risk factors since 1990 umtil 2019; I have filter this risk factors by the following causes: High temperature, Low temperature, Ambient particulate matter pollution, Household air pollution from solid fuels acroos Europe")
    st.caption('Here the term **contributes**, meaning it was one of the attributed risk factors for a given disease or cause of death. There can be multiple risk factors for a given disease which corroborate or amplify one another when both are present. This means that in some cases, air pollution was not the only risk factor but one of several.'


if __name__ == "__main__":
    main()
