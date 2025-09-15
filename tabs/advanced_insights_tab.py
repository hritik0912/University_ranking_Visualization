import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import umap
import hdbscan
import networkx as nx
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

def render_advanced_insights_tab(df, DF, selected_vars):
    """
    Renders the Advanced Insights tab with UMAP, HDBSCAN, and similarity networks.
    
    Args:
        df (pd.DataFrame): The filtered DataFrame based on sidebar selections.
        DF (pd.DataFrame): The original, unfiltered DataFrame.
        selected_vars (list): List of core metric column names.
    """
    st.header('Advanced Clustering & Networks (respects sidebar filters)')

    # --- UMAP + HDBSCAN Clustering ---
    st.subheader('🔹 UMAP + HDBSCAN Clustering')
    
    umap_metrics = st.multiselect(
        'Select Metrics for UMAP & HDBSCAN Clustering',
        selected_vars,
        default=selected_vars,
        key='umap_hdbscan_metrics'
    )

    if umap_metrics:
        data_umap = df.dropna(subset=umap_metrics)
        if data_umap.shape[0] < 15: # UMAP default n_neighbors is 15
            st.warning(f"Not enough data ({data_umap.shape[0]} universities) for robust UMAP/HDBSCAN. Please broaden filters.")
        else:
            X_umap_scaled = StandardScaler().fit_transform(data_umap[umap_metrics])

            reducer = umap.UMAP(random_state=42, n_neighbors=15, min_dist=0.1)
            X_embedded = reducer.fit_transform(X_umap_scaled)

            clusterer = hdbscan.HDBSCAN(min_cluster_size=10, prediction_data=True)
            labels = clusterer.fit_predict(X_embedded)

            data_umap['UMAP1'] = X_embedded[:, 0]
            data_umap['UMAP2'] = X_embedded[:, 1]
            data_umap['Cluster'] = labels.astype(str)

            fig_umap = px.scatter(
                data_umap, x='UMAP1', y='UMAP2', color='Cluster',
                hover_data=['Name', 'Country', 'Overall Score'],
                title='UMAP + HDBSCAN Clustering of Universities',
                height=600
            )
            st.plotly_chart(fig_umap, use_container_width=True)
    else:
        st.warning('Please select at least one metric to perform UMAP + HDBSCAN clustering.')
    st.markdown("---")

    # --- Cosine Similarity Network ---
    st.subheader('🔹 University Similarity Network (Academic Twins)')
    st.markdown("Find universities in one country that are most similar to a selected university from another, based on their performance metrics.")

    if umap_metrics and not data_umap.empty:
        col1, col2 = st.columns(2)
        with col1:
            # Use the full, unfiltered dataframe for the source university list
            uni_list = sorted(DF['Name'].unique())
            selected_uni = st.selectbox('Select a University:', uni_list, key='selected_uni_real')
        with col2:
            country_list = sorted(DF['Country'].unique())
            selected_country = st.selectbox('Select a Country to Compare Against:', country_list, index=country_list.index("United States"), key='selected_country_real')

        sim_threshold = st.slider(
            'Similarity Threshold (%)', min_value=70, max_value=99, value=90,
            help="Higher threshold means stronger similarity required to draw a link."
        )
        
        # Prepare data for similarity calculation from the full dataset
        data_real = DF.dropna(subset=umap_metrics).copy()
        X_real = StandardScaler().fit_transform(data_real[umap_metrics])
        
        # Create a mapping from name to index for quick lookup
        name_to_idx = {name: i for i, name in enumerate(data_real['Name'])}

        if selected_uni not in name_to_idx:
            st.warning(f"'{selected_uni}' not found in the dataset after filtering for metric calculations. It may have missing values in the selected metrics.")
        else:
            G = nx.Graph()
            idx_main = name_to_idx[selected_uni]
            main_uni_data = data_real.iloc[idx_main]
            
            G.add_node(selected_uni, country=main_uni_data['Country'], score=main_uni_data['Overall Score'])

            # Filter for universities in the target country
            target_country_df = data_real[data_real['Country'] == selected_country]
            
            for idx, row in target_country_df.iterrows():
                univ = row['Name']
                if univ != selected_uni:
                    idx_target = name_to_idx[univ]
                    sim = cosine_similarity(X_real[idx_main].reshape(1, -1), X_real[idx_target].reshape(1, -1))[0][0] * 100
                    if sim >= sim_threshold:
                        G.add_node(univ, country=row['Country'], score=row['Overall Score'])
                        G.add_edge(selected_uni, univ, weight=sim)

            if len(G.nodes()) > 1:
                pos = nx.spring_layout(G, seed=42)
                edge_x, edge_y = [], []
                for edge in G.edges():
                    x0, y0 = pos[edge[0]]
                    x1, y1 = pos[edge[1]]
                    edge_x.extend([x0, x1, None])
                    edge_y.extend([y0, y1, None])

                edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=0.5, color='#888'), hoverinfo='none', mode='lines')
                
                node_x, node_y, node_color, node_text = [], [], [], []
                for node in G.nodes():
                    x, y = pos[node]
                    node_x.append(x)
                    node_y.append(y)
                    node_color.append(G.nodes[node]['score'])
                    node_text.append(f"{node}<br>Score: {G.nodes[node]['score']:.2f}")

                node_trace = go.Scatter(
                    x=node_x, y=node_y, mode='markers+text', textposition="top center",
                    textfont=dict(size=9), hoverinfo='text', text=list(G.nodes()),
                    marker=dict(showscale=True, colorscale='YlGnBu', reversescale=True, color=node_color, size=10,
                                colorbar=dict(thickness=15, title='Overall Score', xanchor='left'), line_width=2)
                )
                fig_network = go.Figure(data=[edge_trace, node_trace],
                                        layout=go.Layout(
                                            title=f'Similarity Network: {selected_uni} vs Universities in {selected_country}',
                                            showlegend=False, hovermode='closest',
                                            margin=dict(b=20,l=5,r=5,t=40),
                                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                                       )
                st.plotly_chart(fig_network, use_container_width=True)
            else:
                st.info(f"No universities in {selected_country} met the {sim_threshold}% similarity threshold with {selected_uni}.")
    else:
        st.warning('Please select metrics to build the similarity network.')