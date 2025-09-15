import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def render_comparer_tab(DF, selected_vars):
    """
    Renders the University Comparer tab.

    Args:
        DF (pd.DataFrame): The original, unfiltered DataFrame.
        selected_vars (list): List of core metric column names for the radar chart.
    """
    st.subheader('University Comparer')
    st.markdown('Select two universities to compare them across different metrics.')

    universities = sorted(DF['Name'].unique())
    # Default to two well-known universities for a good initial example
    default_unis = []
    if "University of Oxford" in universities and "Harvard University" in universities:
        default_unis = ["University of Oxford", "Harvard University"]
    elif len(universities) >= 2:
        default_unis = universities[:2]

    selected_unis = st.multiselect(
        'Select two universities:',
        universities,
        default=default_unis,
        max_selections=2,
        key="compare_universities"
    )

    if len(selected_unis) == 2:
        u_df = DF[DF['Name'].isin(selected_unis)].sort_values('Year')

        # Get latest data for radar plot
        latest_year = u_df['Year'].max()
        latest_u1_df = u_df[(u_df['Name'] == selected_unis[0]) & (u_df['Year'] == latest_year)]
        latest_u2_df = u_df[(u_df['Name'] == selected_unis[1]) & (u_df['Year'] == latest_year)]

        if latest_u1_df.empty or latest_u2_df.empty:
            st.warning(f"One of the selected universities does not have data for the latest year ({latest_year}).")
            return

        latest_u1 = latest_u1_df.iloc[0]
        latest_u2 = latest_u2_df.iloc[0]

        # --- Radar Chart ---
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=[latest_u1[m] for m in selected_vars],
            theta=selected_vars,
            fill='toself',
            name=selected_unis[0]
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=[latest_u2[m] for m in selected_vars],
            theta=selected_vars,
            fill='toself',
            name=selected_unis[1]
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=True,
            title=f"Metric Comparison ({latest_year})"
        )
        st.plotly_chart(fig_radar, use_container_width=True)

        # --- Rank Over Time ---
        fig_s1 = px.line(
            u_df, x='Year', y='Rank', color='Name', markers=True,
            title='Rank Over Time'
        )
        fig_s1.update_yaxes(autorange='reversed')
        st.plotly_chart(fig_s1, use_container_width=True)

        # --- Overall Score Over Time ---
        fig_s2 = px.bar(
            u_df, x='Year', y='Overall Score', color='Name',
            barmode='group', title='Overall Score Over Time', range_y=[0, 100]
        )
        st.plotly_chart(fig_s2, use_container_width=True)
    else:
        st.info('Please select exactly two universities to compare.')