import streamlit as st
import pandas as pd
import plotly.express as px

def render_geo_tab(DF):
    """
    Renders the Geographic Analysis tab.
    
    Args:
        DF (pd.DataFrame): The original, unfiltered DataFrame.
    """
    year_min, year_max = int(DF.Year.min()), int(DF.Year.max())
    # Default to the single latest year for a cleaner initial view
    year_range = st.slider('Select Year Range for this Tab', year_min, year_max, (year_max, year_max))
    df_country = DF[(DF.Year >= year_range[0]) & (DF.Year <= year_range[1])]

    st.subheader(f'Continent & Country Analysis for {year_range[0]}-{year_range[1]}')

    # --- Sunburst Charts ---
    continent_avg = df_country.groupby('Continent')['Overall Score'].mean().reset_index()
    fig_sun = px.sunburst(continent_avg, path=['Continent'], values='Overall Score', title='Average Score by Continent')
    fig_sun.update_traces(insidetextorientation='radial')

    TOP_N = 5
    continent_avg['Country'] = ''
    continent_avg['University'] = ''

    country_avg = df_country.groupby(['Continent','Country'])['Overall Score'].mean().reset_index()
    country_avg['University'] = ''

    uni_topn = (
        df_country
        .sort_values('Overall Score', ascending=False)
        .groupby('Country')
        .head(TOP_N)
        .loc[:, ['Continent','Country','Name','Overall Score']]
        .rename(columns={'Name':'University'})
    )

    sun_df3 = pd.concat([continent_avg, country_avg, uni_topn], ignore_index=True)
    fig3 = px.sunburst(
        sun_df3,
        path=['Continent','Country','University'],
        values='Overall Score',
        branchvalues='total',
        title=f'Overall Score: Continent → Country → Top {TOP_N} Universities'
    )
    fig3.update_traces(maxdepth=2, insidetextorientation='radial')
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_sun, use_container_width=True)
    with col2:
        st.plotly_chart(fig3, use_container_width=True)
    
    st.markdown("---")

    # --- Top 10 Charts ---
    st.subheader(f'Top 10 Country Rankings for {year_range[0]}-{year_range[1]}')

    c1, c2 = st.columns(2)
    with c1:
        # Top 10 by count
        ct = df_country.Country.value_counts().nlargest(10).reset_index()
        ct.columns = ['Country', 'Count']
        fig2 = px.bar(ct, x='Count', y='Country', orientation='h', title='Top 10 Countries by University Count')
        fig2.update_yaxes(dtick=1, autorange='reversed')
        st.plotly_chart(fig2, use_container_width=True)

        # Top 10 by Industry Impact
        ii = df_country.groupby('Country')['Industry Impact'].mean().nlargest(10).reset_index()
        fig_ii = px.bar(ii, x='Industry Impact', y='Country', orientation='h', title='Top 10 Countries by Industry Impact')
        fig_ii.update_yaxes(autorange='reversed')
        st.plotly_chart(fig_ii, use_container_width=True)

    with col2:
        # Avg Overall Score horizontal bar
        cs = df_country.groupby('Country')['Overall Score'].mean().nlargest(10).reset_index()
        fig_avg_score = px.bar(cs, x='Overall Score', y='Country', orientation='h', title='Top 10 Countries by Avg Overall Score')
        fig_avg_score.update_yaxes(dtick=1, autorange='reversed')
        st.plotly_chart(fig_avg_score, use_container_width=True)

        # Top 10 by Student Population
        sp = df_country.groupby('Country')['Student Population'].mean().nlargest(10).reset_index()
        fig_sp = px.bar(sp, x='Student Population', y='Country', orientation='h', title='Top 10 Countries by Avg Student Population')
        fig_sp.update_yaxes(autorange='reversed')
        st.plotly_chart(fig_sp, use_container_width=True)