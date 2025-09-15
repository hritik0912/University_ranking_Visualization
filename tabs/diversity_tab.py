import streamlit as st
import plotly.express as px

def render_diversity_tab(df, DF):
    """
    Renders the Diversity tab, showing gender and international student data.

    Args:
        df (pd.DataFrame): The filtered DataFrame based on sidebar selections.
        DF (pd.DataFrame): The original, unfiltered DataFrame.
    """
    st.subheader('Mean Gender Diversity Over Time Worldwide')
    dfem = DF.groupby('Year')[['Female %', 'Male %']].mean().reset_index()
    fig4 = px.line(dfem, x='Year', y=['Female %', 'Male %'], title='Global Gender Balance Trend (2016-2025)')
    fig4.update_yaxes(range=[45, 55]) # Adjusted range for better visibility
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('---')

    st.subheader('Evolution in Diversity by Country')

    col1, col2 = st.columns(2)

    with col1:
        # Top 10 countries by historical Female %
        top10_gender = (
            DF.groupby('Country')['Female %']
            .mean()
            .nlargest(10)
            .index
            .tolist()
        )
        # Evolution of Female % in those top 10
        dfem_top10 = (
            DF[DF['Country'].isin(top10_gender)]
            .groupby(['Year','Country'])['Female %']
            .mean()
            .reset_index()
        )
        fig_top10_gender = px.line(
            dfem_top10, x='Year', y='Female %', color='Country',
            markers=True, title='Top 10 Countries by Average Female %: Yearly Trend'
        )
        st.plotly_chart(fig_top10_gender, use_container_width=True)

    with col2:
        # Top 10 Countries Hosting International Students
        top_ci = DF.groupby('Country')['International Students'].mean().nlargest(10).index
        grouped_ci = DF[DF['Country'].isin(top_ci)].groupby(['Country', 'Year'])['International Students'].mean().reset_index()
        fig_topci = px.line(
            grouped_ci, x='Year', y='International Students', color='Country',
            markers=True, title='Top 10 Countries by Avg. International Students %'
        )
        st.plotly_chart(fig_topci, use_container_width=True)

    st.markdown('---')
    
    st.subheader('Metrics vs. Scores (respects sidebar filters)')

    c1, c2 = st.columns(2)
    with c1:
        # Students to Staff Ratio vs Teaching Score
        st.write('Students to Staff Ratio vs Teaching Score')
        fig5 = px.scatter(df, x='Students to Staff Ratio', y='Teaching', trendline='ols',
                          hover_name='Name')
        st.plotly_chart(fig5, use_container_width=True)
        
    with c2:
        # Student Population vs Rank
        st.write('Student Population vs Rank')
        fig8 = px.scatter(df, x='Student Population', y='Rank', color='Country', size='Overall Score', hover_name='Name')
        fig8.update_yaxes(autorange='reversed')
        st.plotly_chart(fig8, use_container_width=True)