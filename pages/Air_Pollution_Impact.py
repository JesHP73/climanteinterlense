import streamlit as st
import pandas as pd
#import seaborn as sns
#import matplotlib.pyplot as plt
import numpy as np
import plotly.figure_factory as ff
import scipy
import plotly.express as px

# Function definitions

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
    # Make sure the column is of numeric type
    filtered_data['total_death_attributed_sex_standarized'] = pd.to_numeric(
        filtered_data['total_death_attributed_sex_standarized'], errors='coerce'
    )

    # Group by 'year' and 'ig_label', then calculate the mean of the standardized death total
    aggregated_data = filtered_data.groupby(['year', 'ig_label'], as_index=False)['total_death_attributed_sex_standarized'].mean()

    # Mapping from short labels to full names for income groups
    income_label_mapping = {
        'LM': 'Low Income',
        #'UM': 'Upper Middle Income',
        'H': 'High Income'
    }

    # Apply the mapping to the 'ig_label' column
    aggregated_data['ig_label'] = aggregated_data['ig_label'].map(income_label_mapping)

    # Define the color mapping for income groups
    color_discrete_map = {
        'Low Income': 'blue',
        'High Income': 'green',
        #'Upper Middle Income': 'grey'
    }

    # Plot the line chart using the aggregated data
    fig = px.line(
        aggregated_data,
        x='year',
        y='total_death_attributed_sex_standarized',
        color='ig_label',
        color_discrete_map=color_discrete_map,
        labels={'total_death_attributed_sex_standarized': 'Percentage of Deaths', 'ig_label': 'Income Group'}
    )

    # Improve layout for better readability
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Percentage of population Deaths',
        showlegend=True,
        legend_title_text='Historical Income Group Clasification'
    )

    # Set x-axis tick marks to show each year
    fig.update_xaxes(
        tickvals=aggregated_data['year'].unique(),
        tickangle=45
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
            st.header("Share Rate")
            st.metric(label=f"Avg. deaths rate in {latest_year}", value=f"{latest_avg_death_percentage:.2f}%")
        with col2:
            st.header("Equivalent to")
            if people_affected is not None:
                # Format the number with commas as thousand separators
                formatted_people_affected = f"{people_affected:,.2f}"
                st.metric(label="Number of People affected", value=formatted_people_affected)
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

    st.title(':green[Unequal Impact:] Air Pollution-Related Deaths by Income Group')
    
    st.divider()
    
    # Sidebar for filters
    st.sidebar.header('Filters')

    # Multiselect for Region and Country
    region_options = ['All'] + sorted(df['region'].unique().tolist())
    country_options = ['All'] + sorted(df['country'].unique().tolist())

    selected_region = st.sidebar.multiselect('Select Region', options=region_options, default='All')
    selected_country = st.sidebar.multiselect('Select Country', options=country_options, default='All')

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

    # Plotting
    plot_data(filtered_data)

    st.link_button(":blue[🔗 Data source: IHME, Global Burden of Disease (2019)]", "https://vizhub.healthdata.org/gbd-results/")
    
    # Display statistics
    display_statistics(filtered_data)

    # Define custom styles with green highlights
    custom_css = """
    <style>
    .markdown-style {
        background-color: #e6f4ea;  /* Light green background */
        border-left: 5px solid #34a853;  /* Darker green left border */
        padding: 10px;  /* Padding inside the box */
        font-size: 16px;  /* Text size */
        color: #202124;  /* Text color - dark grey for readability */
    }
    </style>
    """
    
    # Define highlighted text with markdown
    highlighted_text = custom_css + """
    <div class="markdown-style">
    
    **The IHME, Global Burden of Disease Dataset studied**, provides the Death by Risk factors since 1990 until 2019; 
    This dataset has been filtered by the following causes: 
    - **High temperature**
    - **Low temperature**
    - **Ambient particulate matter pollution (PM10, PM2.5)**
    - **Household air pollution from solid fuels** across Europe.
    
    </div>
    """
    
    st.markdown(highlighted_text, unsafe_allow_html=True)


#create and return the page 1 chart figure
def plot_page1():
    if __name__ == "__main__":
        
        main()
        
    st.divider()
    
    with st.expander("### 👀 UNDERSTANDING WHAT YOU SEE"):
        st.write("Here the term :green[Atributes], means it was one of the attributed risk factors for a given disease or cause of death. There can be multiple risk factors for a given disease which corroborate or amplify one another when both are present. This means that in some cases, air pollution was not the only risk factor but one of several.")
    
    with st.expander("💡 WHAT YOU SHOULD KNOW ABOUT THIS DATA"):
        st.write("This data comes from the most recent publication of the Global Burden of Disease study by the Institute for Health Metrics and Evaluation (IHME) in 2019 and the Global Terrorism Database.")
        st.write("These estimates assign each death a single cause, based on data on the ‘underlying cause of death’ listed on death certificates, verbal autopsies, and statistical modeling. This is a simplification, as people often have multiple diseases or injuries that contribute to their death, which may also be listed on death certificates.")
        st.write("This chart shows data on causes of death globally Filtered by Rei Name related to Air pollution and only Europe, from 1990 until 2019, the year before the Covid-19 pandemic started.")
    
        


def show_page2():
    # create and return the page 2 Image
    
    st.title(":green[Unveiling] 2021 Death Statistics in Europe")
    
    st.divider()
    
    st.image("images/attributed_deaths_for_different_causes.jpg", width=700)
    st.write("**Creator:** European Environment Agency (EEA)")
    st.link_button(":blue[🔗 Data source: Harm to human health from air pollution in Europe: burden of disease Nov, 2023 Report]", "https://www.eea.europa.eu/publications/harm-to-human-health-from-air-pollution")

    st.divider()
    
    with st.expander("💡 WHAT YOU SHOULD KNOW ABOUT THIS IMAGE"):
        st.write("In 2021 in the (EU-27 Official countries):")
        st.markdown("-**A. 253,000 deaths** were attributable to exposure to PM2.5 concentrations above WHO’s guideline level of 5 µg/m3 (micrograms per cubic metre of air).")
        st.markdown("-**B. 52,000 deaths** were attributable to exposure to NO2 concentrations above WHO’s guideline level of 10 µg/m3.") 
        st.markdown("-**C. 22,000 deaths** were attributable to short-term exposure to O3 concentrations above 70 µg/m3.")
        
    st.markdown('''
    <style>
    [data-testid="stMarkdownContainer"] ul{
        list-style-position: inside;
    }
    </style>
    ''', unsafe_allow_html=True)

    with st.expander("💡 EU Policy Context"):
        st.write("In 2021, The World Health Organization(WHO) updated its air quality guidelines for the first time since 2005, lowering the recommended levels for PM's, NO2 and O3. This update is based on systematic reviews of the latest scientific evidence outlining how air pollution affects human health. On 26 October 2022 the European Commission adopted a proposal for a revised Ambient Air Quality Directive, aiming, among others, to align air quality standards more closely with WHO’s updated recommendations.")



# Creating tabs
tab1, tab2 = st.tabs(["Causes Of Mortality", "Analisys by Income Groups"])

# Populate tab1 with page 1 content
with tab1:
    
    page1_chart = show_page2() 
    


# Populate tab2 with page 2 content
with tab2:
    
    page2 = plot_page1() 
    


