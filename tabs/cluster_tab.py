import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

def render_cluster_tab(df, selected_vars):
    """
    Renders the Clustering and PCA tab.

    Args:
        df (pd.DataFrame): The filtered DataFrame based on sidebar selections.
        selected_vars (list): List of core metric column names.
    """
    st.subheader('K-Means Clustering & PCA Analysis (respects sidebar filters)')

    cols = st.multiselect(
        'Choose Metrics for Clustering',
        selected_vars,
        default=selected_vars,
        key='cluster_choose_metrics'
    )

    if not cols:
        st.warning("Please select at least one metric for clustering.")
        return

    data_c = df.dropna(subset=cols)
    if data_c.shape[0] < 2:
        st.warning("Not enough data to perform clustering with the current filters. Please select more data.")
        return
        
    X = StandardScaler().fit_transform(data_c[cols])

    # --- Elbow Method ---
    inertias = []
    k_range = range(2, min(11, data_c.shape[0])) # Ensure k is not larger than sample size
    if len(k_range) > 0:
        for i in k_range:
            km = KMeans(n_clusters=i, random_state=0, n_init='auto')
            km.fit(X)
            inertias.append(km.inertia_)

        fig_elbow = px.line(
            x=list(k_range), y=inertias, markers=True,
            title='Elbow Method: Inertia vs. Number of Clusters (k)'
        )
        fig_elbow.update_layout(xaxis_title='Number of Clusters (k)', yaxis_title='Inertia')
        st.plotly_chart(fig_elbow, use_container_width=True)
        st.markdown('---')
    
    # --- Clustering & Visualization ---
    k = st.slider(
        'Select number of clusters (k) based on the Elbow plot above',
        min_value=2, max_value=10, value=6, key='cluster_k'
    )
    if data_c.shape[0] < k:
        st.error(f"❗ Not enough universities ({data_c.shape[0]}) to create {k} clusters. Please lower k or adjust filters.")
    else:
        st.write(f"🔹 **Running K-Means with k = {k}**")
        kmeans = KMeans(n_clusters=k, random_state=0, n_init='auto').fit(X)
        data_c = data_c.copy()
        data_c['Cluster'] = kmeans.labels_.astype(str)

        # --- Cluster Sizes ---
        cluster_counts = data_c['Cluster'].value_counts().sort_index()
        fig_counts = px.bar(
            y=cluster_counts.index, x=cluster_counts.values,
            labels={'x':'Count of Universities', 'y':'Cluster Label'},
            title=f'Cluster Sizes (k={k})', orientation='h'
        )
        st.plotly_chart(fig_counts, use_container_width=True)

        # --- PCA Visualization ---
        pca = PCA(n_components=3)
        X_pca = pca.fit_transform(X)
        data_c['PC1'] = X_pca[:, 0]
        data_c['PC2'] = X_pca[:, 1]
        data_c['PC3'] = X_pca[:, 2]

        st.subheader('2D PCA Cluster Visualization')
        fig_pca2 = px.scatter(
            data_c, x='PC1', y='PC2', color='Cluster',
            title=f'2D PCA Cluster Assignment (k={k})',
            hover_data=['Name', 'Country', 'Rank', 'Overall Score']
        )
        st.plotly_chart(fig_pca2, use_container_width=True)

        st.subheader('3D PCA Cluster Visualization')
        fig_pca3 = px.scatter_3d(
            data_c, x='PC1', y='PC2', z='PC3', color='Cluster',
            title=f'3D PCA Cluster Assignment (k={k})',
            hover_data=['Name', 'Country']
        )
        st.plotly_chart(fig_pca3, use_container_width=True)
        st.markdown('---')

        # --- Cluster Profiles ---
        st.subheader('📊 Cluster Profiles: Average Metrics')
        cluster_profile = data_c.groupby('Cluster')[cols + ['Rank', 'International Students']].mean().round(2)
        st.dataframe(cluster_profile, use_container_width=True)