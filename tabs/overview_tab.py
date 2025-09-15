import streamlit as st
import plotly.express as px

def render_overview_tab(df, DF):
    """
    Renders the Overview tab with top/bottom universities and rank trajectories.
    
    Args:
        df (pd.DataFrame): The filtered DataFrame based on sidebar selections.
        DF (pd.DataFrame): The original, unfiltered DataFrame.
    """
    st.subheader('Top 20 Universities by Rank')
    top20 = df.nsmallest(20, 'Rank').sort_values('Rank')
    fig0 = px.bar(top20, x='Rank', y='Name', orientation='h',
                  hover_data=['Overall Score'], title='Top 20 Universities (respects filters)')
    fig0.update_yaxes(dtick=1, autorange='reversed')
    st.plotly_chart(fig0, use_container_width=True)
    st.markdown('---')

    st.subheader('Bottom 10 Universities by Rank')
    bottom10 = df.nlargest(10, 'Rank')
    fig_bottom10 = px.bar(bottom10, x='Overall Score', y='Name', orientation='h',
                          hover_data=['Rank'], title='Bottom 10 Universities (respects filters)')
    fig_bottom10.update_yaxes(dtick=1, autorange='reversed')
    st.plotly_chart(fig_bottom10, use_container_width=True)
    st.markdown('---')
    
    st.subheader('Rank Trajectories (2016-2025)')
    # Use the original unfiltered DF for trajectories but default selection to filtered top 20
    all_unis = sorted(DF['Name'].unique())
    sel_uni = st.multiselect('Select universities for trajectory', all_unis, default=top20['Name'].tolist())
    if sel_uni:
        tra = DF[DF.Name.isin(sel_uni)].sort_values(['Name', 'Year'])
        fig1 = px.line(tra, x='Year', y='Rank', color='Name', markers=True, title='Rank Trajectories of Selected Universities')
        fig1.update_yaxes(autorange='reversed')
        st.plotly_chart(fig1, use_container_width=True)
    st.markdown('---')

    st.subheader('Animated Top 20 Universities by Score (2016-2025)')
    df_anim = (
        DF.sort_values(['Year','Overall Score'], ascending=[True, False])
          .groupby('Year', group_keys=False)
          .head(20)
          .reset_index(drop=True)
    )
    fig_anim = px.bar(
        df_anim.sort_values(['Year','Overall Score']), x='Overall Score', y='Name',
        orientation='h', animation_frame='Year', animation_group='Name',
        range_x=[0,100], title='Top 20 Universities by Overall Score Worldwide', height=600
    )
    fig_anim.update_layout(yaxis={'categoryorder':'total ascending'}, updatemenus=[])
    st.plotly_chart(fig_anim, use_container_width=True)