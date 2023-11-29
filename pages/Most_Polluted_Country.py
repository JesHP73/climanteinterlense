#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd
import numpy as np

# Function to load data
#@st.cache_data  # 👈 Add the caching decorator
def load_data():
     try:
        URL = 'https://github.com/JesHP73/climanteinterlense/blob/7119b0a7a9d50d703a3f2f2e0a5ada59a377ea50/dataset/mapping.csv'
        data_mapping = pd.read_csv(URL)
        return data_mapping #= pickle.load(data, fix_imports=True, encoding='ASCII', errors='strict', buffers=None)
     except Exception as e:
         st.error(f"Error loading data: {e}")
         return pd.DataFrame()  # Return an empty DataFrame in case of error

# Main body of your Streamlit app
def main():
     original_mapping = load_data()
     df = original_mapping.copy()
     return st.map(df, token='sk.eyJ1IjoiamVzd2JzIiwiYSI6ImNscGswZzJsMTA1YnYyanF2Y2liNDZ0bjgifQ.rgJ4q6jeVsotKmyGXxabdQ' )


# This ensures the app runs when the script is executed
if __name__ == "__main__":
     main()
