import streamlit as st
import pandas as pd

def render_data_view_tab(DF):
    """
    Renders the Data Explorer tab.

    Args:
        DF (pd.DataFrame): The original, unfiltered DataFrame.
    """
    st.subheader("Dataset Explorer")

    # --- Filters for the data view ---
    query = st.text_input("🔍 Search University Name (substring match)", key="data_view_search")

    years = sorted(DF['Year'].unique())
    sel_years = st.multiselect("Filter Years", years, default=years, key="data_view_years")
    
    countries = sorted(DF['Country'].unique())
    sel_countries = st.multiselect("Filter Countries", countries, default=countries, key="data_view_countries")

    all_cols = DF.columns.tolist()
    sel_cols = st.multiselect("Select Columns to Display", all_cols, default=all_cols, key="data_view_cols")

    # --- Apply filters ---
    df_view = DF[
        (DF['Year'].isin(sel_years)) &
        (DF['Country'].isin(sel_countries))
    ]
    if query:
        df_view = df_view[df_view['Name'].str.contains(query, case=False, na=False)]

    # --- Display DataFrame ---
    if not sel_cols:
        st.warning("Please select at least one column to display.")
    else:
        st.dataframe(df_view[sel_cols], use_container_width=True)