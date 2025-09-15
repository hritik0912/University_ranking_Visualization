import streamlit as st
import pandas as pd

# 1. Import your custom modules
from data_processing import load_data
from tabs.overview_tab import render_overview_tab
from tabs.geo_tab import render_geo_tab
from tabs.map_tab import render_map_tab
from tabs.diversity_tab import render_diversity_tab
from tabs.research_tab import render_research_tab
from tabs.pairwise_tab import render_pairwise_tab
from tabs.cluster_tab import render_cluster_tab
from tabs.advanced_insights_tab import render_advanced_insights_tab
from tabs.comparer_tab import render_comparer_tab
from tabs.conclusions_tab import render_conclusions_tab
from tabs.data_view_tab import render_data_view_tab
from tabs.eda_tab import render_eda_tab

# --- 2. Page Configuration ---
st.set_page_config(page_title='World University Rankings Dashboard', page_icon='🎓', layout='wide')

# --- 3. Data Loading and Caching ---
DF = load_data()
df = DF.copy()  # Create a mutable copy for filtering

# --- 4. Sidebar Filters ---
st.sidebar.success("✅ Dataset loaded and cleaned!")
st.sidebar.header('Dashboard Filters')

years = ['All'] + sorted(DF['Year'].unique().astype(str))
sel_year = st.sidebar.selectbox('Year', years, index=len(years) - 1)
if sel_year != 'All':
    df = df[df['Year'] == int(sel_year)]

all_countries = sorted(df['Country'].unique())
sel_ctry = st.sidebar.multiselect('Country', all_countries, default=[])
if sel_ctry:
    df = df[df['Country'].isin(sel_ctry)]

# Ensure rank and score ranges are valid after filtering
min_rank, max_rank = int(df.Rank.min()), int(df.Rank.max())
if min_rank < max_rank:
    rank_rng = st.sidebar.slider('Rank range', min_rank, max_rank, (min_rank, max_rank))
else:
    rank_rng = (min_rank, max_rank) # Handle case with only one rank

min_score, max_score = 0.0, 100.0
score_rng = st.sidebar.slider('Overall Score range', min_score, max_score, (min_score, max_score))

# Apply final filters
df = df[df['Rank'].between(*rank_rng) & df['Overall Score'].between(*score_rng)]

if not sel_ctry and sel_year == 'All':
    st.sidebar.info("Displaying global data for all years. Use filters to refine your view.")
else:
    st.sidebar.success("✅ Filters successfully applied!")

# --- 5. Main Page ---
st.title("🎓 THE World University Ranking Analysis 2016-2025")
st.markdown("An interactive dashboard for exploring trends, clusters, and insights in global higher education.")

# --- KPI Metrics ---
c1, c2, c3, c4 = st.columns(4)
if not df.empty:
    c1.metric('Universities', f"{df.Name.nunique():,}")
    c2.metric('Countries', f"{df.Country.nunique():,}")
    c3.metric('Median Rank', f"{int(df.Rank.median())}")
    c4.metric('Mean Score', f'{df["Overall Score"].mean():.1f}')
else:
    c1.metric('Universities', "0")
    c2.metric('Countries', "0")
    st.warning("No data matches the current filter settings. Please adjust the filters in the sidebar.")

# --- 6. Tabs ---
tab_titles = ['Overview', 'Country & Continent', 'Animated World Map', 'Diversity', 
              'Research & Industry', 'Pairwise Analysis', 'K-Means Clusters', 'Advanced Insights', 
              'University Comparer','Conclusions','View Data','EDA']
tabs = st.tabs(tab_titles)

selected_vars = ['Overall Score', 'Teaching', 'Research Environment', 'Research Quality', 'Industry Impact']

with tabs[0]:
    render_overview_tab(df, DF)
with tabs[1]:
    render_geo_tab(DF)
with tabs[2]:
    render_map_tab(DF)
with tabs[3]:
    render_diversity_tab(df, DF)
with tabs[4]:
    render_research_tab(df, DF, selected_vars)
with tabs[5]:
    render_pairwise_tab(df, selected_vars)
with tabs[6]:
    render_cluster_tab(df, selected_vars)
with tabs[7]:
    render_advanced_insights_tab(df, DF, selected_vars)
with tabs[8]:
    render_comparer_tab(DF, selected_vars)
with tabs[9]:
    render_conclusions_tab()
with tabs[10]:
    render_data_view_tab(DF)
with tabs[11]:
    render_eda_tab(DF)

st.caption('Dashboard created by Hritik Chouhan. Data source: Times Higher Education 2016-2025.')