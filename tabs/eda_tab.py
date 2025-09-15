import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

def render_eda_tab(DF):
    """
    Renders the Exploratory Data Analysis (EDA) tab.

    Args:
        DF (pd.DataFrame): The original, unfiltered DataFrame.
    """
    st.header("Exploratory Data Analysis")

    st.subheader("Dataset Columns and Description of original data")
    columns_info = {
        "Rank": "The global ranking of institutions",
        "Name": "The name of institutions",
        "Country": "The country of each university",
        "Student Population": "Total number of students enrolled",
        "Student-to-Staff Ratio": "Faculty availability for students",
        "International Students": "Percentage of international students",
        "Female-to-Male Ratio": "Gender distribution of students",
        "Overall Score": "Composite ranking score",
        "Teaching Score": "Rating based on teaching quality",
        "Research Environment Score": "Research facilities & output",
        "Research Quality Score": "Research impact in citations",
        "Industry Impact Score": "University collaboration with industries",
        "International Outlook Score": "Diversity in faculty & students",
        "Year (2016-2025)": "Year-wise rankings"
    }
    description_df = pd.DataFrame(list(columns_info.items()), columns=["Attribute", "Description"])
    st.dataframe(description_df, use_container_width=True)

    st.subheader("Columns Present in Cleaned Data (DF)")
    st.write(f"Total Columns: {len(DF.columns)}")
    columns_list = ", ".join(DF.columns)
    st.write(f" {columns_list}")

    st.subheader("Missing Values Summary")
    missing = DF.isna().sum()
    missing_percent = (missing / len(DF)) * 100
    missing_df = pd.DataFrame({'Missing Count': missing, 'Missing Percentage': missing_percent})
    missing_df = missing_df[missing_df['Missing Count'] > 0].sort_values('Missing Count', ascending=False)
    st.dataframe(missing_df)

    st.subheader("Descriptive Statistics")
    st.dataframe(DF.describe(), use_container_width=True)

    st.subheader("Key Data Points")
    c1, c2 = st.columns(2)
    with c1:
        st.metric(label="Total Unique Universities", value=DF['Name'].nunique())
        max_score_row = DF.loc[DF['Overall Score'].idxmax()]
        st.metric(label="Highest Overall Score Achieved", value=f"{max_score_row['Name']} ({max_score_row['Year']})", delta=f"{max_score_row['Overall Score']:.2f}")
    with c2:
        country_avg_score = DF.groupby('Country')['Overall Score'].mean().sort_values(ascending=False).reset_index()
        st.metric(label="Top Country by Mean Score", value=country_avg_score.iloc[0]['Country'], delta=f"{country_avg_score.iloc[0]['Overall Score']:.2f}")
        min_score_row = DF.loc[DF['Overall Score'].idxmin()]
        st.metric(label="Lowest Overall Score Achieved", value=f"{min_score_row['Name']} ({min_score_row['Year']})", delta=f"{min_score_row['Overall Score']:.2f}")

    st.markdown("---")
    st.subheader("Data Distributions")
    
    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.histplot(DF['Overall Score'].dropna(), kde=True, ax=ax, bins=30)
        ax.set_title("Overall Score Distribution")
        st.pyplot(fig)

        fig, ax = plt.subplots(figsize=(6, 4))
        sns.histplot(DF['Student Population'].dropna(), kde=True, ax=ax, bins=30)
        ax.set_title("Student Population Distribution")
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.histplot(DF['International Students'].dropna(), kde=True, ax=ax, bins=30)
        ax.set_title("International Students % Distribution")
        st.pyplot(fig)

        fig, ax = plt.subplots(figsize=(6, 4))
        sns.histplot(DF['Students to Staff Ratio'].dropna(), kde=True, ax=ax, bins=30)
        ax.set_title("Students to Staff Ratio Distribution")
        st.pyplot(fig)