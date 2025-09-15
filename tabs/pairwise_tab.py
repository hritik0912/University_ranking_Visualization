import streamlit as st
import plotly.express as px
import pandas as pd

def render_pairwise_tab(df, selected_vars):
    """
    Renders the Pairwise analysis tab with scatter matrix and heatmaps.

    Args:
        df (pd.DataFrame): The filtered DataFrame based on sidebar selections.
        selected_vars (list): List of core metric column names.
    """
    st.subheader('Pair Plot of Core Metrics')
    st.markdown("This plot shows the relationship between each pair of the core metrics. The diagonal shows the distribution of each metric.")
    
    fig11 = px.scatter_matrix(
        df, 
        dimensions=selected_vars, 
        title='Pair Plot of Metrics (respects filters)', 
        height=800, 
        hover_name='Name'
    )
    fig11.update_traces(marker=dict(size=3, opacity=0.7))
    fig11.update_layout(
        font=dict(size=9), 
        margin=dict(l=40, r=40, t=100, b=40)
    )
    st.plotly_chart(fig11, use_container_width=True)
    st.markdown('---')

    st.subheader('Correlation Heatmap')
    numeric_cols = selected_vars + ['Rank', 'Student Population', 'Students to Staff Ratio', 'International Students', 'Female %']
    
    # Ensure only numeric columns that exist in df are used
    existing_numeric_cols = [col for col in numeric_cols if col in df.columns and pd.api.types.is_numeric_dtype(df[col])]
    
    if not existing_numeric_cols:
        st.warning("No numeric data available for correlation based on current filters.")
        return

    corr = df[existing_numeric_cols].corr()
    fig12 = px.imshow(
        corr, 
        text_auto=True, 
        title='Correlation Heatmap (respects filters)', 
        color_continuous_scale='RdBu_r', 
        zmin=-1, zmax=1, 
        aspect='auto'
    )
    fig12.update_layout(
        height=700, 
        margin=dict(l=100, r=100, t=100, b=100), 
        font=dict(size=10), 
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig12, use_container_width=True)