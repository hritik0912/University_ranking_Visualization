import streamlit as st
import pandas as pd
import numpy as np
import re
from pathlib import Path

DATA_PATH = Path('THE World University Rankings 2016-2025.csv')

def assign_continent(country):
    """Maps a country to its continent."""
    asia = ['China', 'Japan', 'Singapore', 'South Korea', 'Turkey',
            'India', 'Iran', 'Malaysia', 'Taiwan', 'Thailand',
            'Pakistan', 'Jordan', 'Kazakhstan', 'Philippines',
            'Vietnam', 'Sri Lanka', 'Hong Kong', 'Brunei Darussalam',
            'Indonesia', 'Bangladesh', 'Russian Federation', 'Iraq',
            'Azerbaijan', 'Israel', 'Saudi Arabia', 'Macao', 'Lebanon',
            'Qatar', 'Oman', 'United Arab Emirates', 'Kuwait', 'Nepal', 'Palestine']
    africa = ['South Africa', 'Uganda', 'Egypt', 'Ghana', 'Morocco',
              'Algeria', 'Tunisia', 'Kenya', 'Botswana', 'Ethiopia',
              'Zimbabwe', 'Namibia', 'Tanzania', 'Mozambique',
              'Nigeria', 'Mauritius', 'Zambia']
    europe = ['United Kingdom', 'Switzerland', 'Sweden', 'Germany',
              'Belgium', 'Austria', 'Spain', 'Portugal', 'Norway',
              'Bulgaria', 'Ireland', 'Italy', 'Czech Republic',
              'Greece', 'Estonia', 'Cyprus', 'Hungary', 'Slovakia',
              'Ukraine', 'Latvia', 'Lithuania', 'Serbia', 'Montenegro',
              'Kosovo', 'North Macedonia', 'Bosnia and Herzegovina',
              'France', 'Netherlands', 'Finland', 'Denmark', 'Romania',
              'Iceland', 'Luxembourg', 'Poland', 'Slovenia', 'Georgia',
              'Croatia', 'Armenia', 'Malta', 'Belarus', 'Northern Cyprus']
    north_america = ['United States', 'Canada', 'Mexico', 'Puerto Rico', 'Jamaica']
    oceania = ['Australia', 'New Zealand', 'Fiji']
    south_america = ['Brazil', 'Argentina', 'Chile', 'Colombia',
                     'Venezuela', 'Peru', 'Ecuador', 'Uruguay',
                     'Paraguay', 'Bolivia', 'Costa Rica', 'Cuba']
    if country in asia: return 'Asia'
    if country in africa: return 'Africa'
    if country in europe: return 'Europe'
    if country in north_america: return 'North America'
    if country in oceania: return 'Oceania'
    if country in south_america: return 'South America'
    return 'Unknown'

@st.cache_data
def load_data():
    """Loads, cleans, and processes the university rankings data."""
    df = pd.read_csv(DATA_PATH)

    # Basic Cleaning
    df['Year'] = df['Year'].astype(int)
    df['Rank'] = df['Rank'].astype(str).str.replace('=', '').astype(float)

    # --- International Students ---
    valid_intl = df[df['International Students'] != '%'].groupby('Name')['International Students'].first()
    df['International Students'] = df.apply(
        lambda row: valid_intl.get(row['Name'], row['International Students']) if row['International Students'] == '%' else row['International Students'],
        axis=1
    )
    df['International Students'] = pd.to_numeric(df['International Students'].astype(str).str.replace('%', '').str.strip(), errors='coerce')

    # --- Gender Ratios ---
    def ratio_to_pct(r):
        if pd.isna(r): return np.nan
        parts = [float(x) for x in re.split(r'\D+', str(r)) if x]
        return parts[0] / sum(parts) * 100 if len(parts) >= 2 else np.nan

    df['Female %'] = df['Female to Male Ratio'].apply(ratio_to_pct)

    # Smart imputation for missing Female %
    female_by_name = df.groupby('Name')['Female %'].mean()
    df['Female %'] = df['Female %'].fillna(df['Name'].map(female_by_name))
    female_by_country = df.groupby('Country')['Female %'].mean()
    df['Female %'] = df['Female %'].fillna(df['Country'].map(female_by_country))

    df['Male %'] = 100 - df['Female %']
    df['Female Ratio'] = df['Female %'].round(0).astype('Int64')
    df['Male Ratio'] = 100 - df['Female Ratio']

    # --- Students to Staff Ratio ---
    df['Students to Staff Ratio'] = pd.to_numeric(df['Students to Staff Ratio'], errors='coerce')
    df.loc[df['Students to Staff Ratio'] > 100, 'Students to Staff Ratio'] = np.nan
    df['Country'] = df['Country'].str.strip()
    df.drop(columns=['Female to Male Ratio'], inplace=True)
    
    # --- Assign Continent ---
    df['Continent'] = df['Country'].apply(assign_continent)

    return df