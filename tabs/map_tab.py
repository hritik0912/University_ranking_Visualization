import streamlit as st
import plotly.express as px

def render_map_tab(DF):
    """
    Renders the Animated World Map tab with various choropleth maps.

    Args:
        DF (pd.DataFrame): The original, unfiltered DataFrame.
    """
    st.subheader('Global Choropleth Maps')

    # --- Animated map for University Count ---
    uni_year = (
        DF
        .groupby(['Year','Country'])
        .size()
        .reset_index(name='Universities')
    )
    map_anim1 = px.choropleth(
        uni_year,
        locations='Country',
        locationmode='country names',
        color='Universities',
        projection='natural earth',
        animation_frame='Year',
        title='Count of Universities Over Time'
    )
    map_anim1.update_layout(
        geo=dict(showcoastlines=True),
        height=600, width=800
    )
    st.plotly_chart(map_anim1, use_container_width=True)
    st.markdown("---")

    # --- Animated map for International Students ---
    intl_year = (
        DF
        .groupby(['Year','Country'])['International Students']
        .mean()
        .reset_index()
    )
    map_anim2 = px.choropleth(
        intl_year,
        locations='Country',
        locationmode='country names',
        color='International Students',
        projection='natural earth',
        animation_frame='Year',
        title='Avg % International Students Over Time'
    )
    map_anim2.update_layout(
        geo=dict(showcoastlines=True),
        height=600, width=800
    )
    st.plotly_chart(map_anim2, use_container_width=True)
    st.markdown("---")
    
    # --- Animated map for Female Student Percentage ---
    female_year = (
        DF
        .groupby(['Year','Country'])['Female %']
        .mean()
        .reset_index()
    )
    map_anim3 = px.choropleth(
        female_year,
        locations='Country',
        locationmode='country names',
        color='Female %',
        projection='natural earth',
        animation_frame='Year',
        title='Avg % Female Students Over Time'
    )
    map_anim3.update_layout(
        geo=dict(showcoastlines=True),
        height=600, width=800
    )
    st.plotly_chart(map_anim3, use_container_width=True)