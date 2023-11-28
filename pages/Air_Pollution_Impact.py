#!/usr/bin/env python
# coding: utf-8

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
        # Assuming the dataset has columns 'year', 'pollutant' and 'emission'
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error

# Function to plot emissions data with WHO standards
def plot_emissions(df, pollutant):
    # Aggregate data to get annual averages for the selected pollutant
    annual_data = df[df['pollutant'] == pollutant].groupby('year')['emission'].mean().reset_index()
    
    # Start plotting
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=annual_data, x='year', y='emission', ax=ax, marker='o
