import streamlit as st
import pandas as pd
import numpy as np


# Function to load data
@st.cache_data  # 👈 Add the caching decorator
def load_data():
     try:
        URL = 'https://github.com/JesHP73/climanteinterlense/blob/7119b0a7a9d50d703a3f2f2e0a5ada59a377ea50/dataset/mapping.csv'
        data = pd.read_csv(URL)
        return data #= pickle.load(data, fix_imports=True, encoding='ASCII', errors='strict', buffers=None)
     except Exception as e:
         st.error(f"Error loading data: {e}")
         return pd.DataFrame()  # Return an empty DataFrame in case of error

# Main body of your Streamlit app
def main():
    # Load data
    original_mapping = load_data()
    df = original_mapping.copy()

st.map(df,
    latitude='latitude',
    longitude='longitude',
    size='avg_AQI_Index',
    color=' ig_label')


# This ensures the app runs when the script is executed
if __name__ == "__main__":
  
    main()
