import streamlit as st
import plotly.express as px

def render_research_tab(df, DF, selected_vars):
    """
    Renders the Research & Industry tab with analysis on research and industry metrics.

    Args:
        df (pd.DataFrame): The filtered DataFrame based on sidebar selections.
        DF (pd.DataFrame): The original, unfiltered DataFrame.
        selected_vars (list): List of core metric column names.
    """
    # This chart uses the original unfiltered DF to show the global trend
    st.subheader('Average Metrics Over Time Worldwide (2016-2025)')
    time_df = DF.groupby('Year')[selected_vars].mean().reset_index()
    fig17 = px.area(time_df, x='Year', y=selected_vars)
    st.plotly_chart(fig17, use_container_width=True)
    st.markdown("---")

    st.subheader('Analysis Based on Sidebar Filters')

    col1, col2 = st.columns(2)
    with col1:
        st.write('Research Quality vs Overall Score')
        fig6 = px.scatter(df, x='Research Quality', y='Overall Score', trendline='ols', hover_name='Name')
        st.plotly_chart(fig6, use_container_width=True)
        
    with col2:
        st.write('Industry Impact vs Research Environment')
        fig7 = px.scatter(df, x='Industry Impact', y='Research Environment', size='Overall Score', hover_name='Name', trendline='ols')
        st.plotly_chart(fig7, use_container_width=True)

    st.markdown('---')

    # This bar chart now respects the sidebar filters by using 'df'
    st.subheader('Top 10 Countries by Average Research Quality')
    rq = df.groupby('Country')['Research Quality'].mean().nlargest(10).reset_index()
    fig_rq = px.bar(rq, x='Research Quality', y='Country', orientation='h', title='Avg Research Quality by Country (for selection)')
    fig_rq.update_yaxes(autorange='reversed')
    st.plotly_chart(fig_rq, use_container_width=True)
    st.markdown('---')

    st.subheader('Distribution of Core Metrics')
    selm = st.multiselect(
        'Choose Metrics for Violin Plot', 
        selected_vars, 
        default=['Overall Score', 'Teaching', 'Research Environment', 'Research Quality', 'Industry Impact']
    )
    if selm:
        melt2 = df[['Name'] + selm].melt(id_vars='Name', var_name='Metric', value_name='Value')
        fig10 = px.violin(melt2, x='Metric', y='Value', box=True, points='all', hover_name='Name')
        st.plotly_chart(fig10, use_container_width=True)