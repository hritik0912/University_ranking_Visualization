import streamlit as st

def render_conclusions_tab():
    """
    Renders the Conclusions & Story tab with a summary of the analysis.
    """
    st.header('Conclusions & Story')
    st.markdown('''
    Over a decade, higher education has undergone substantial transformations. Our visual analytics journey reveals that while the United States and Europe maintain dominance, Asian institutions are significantly improving, particularly in research quality and international appeal.

    We observe progressive gender diversity improvements, with female student participation rising consistently, demonstrating effective global policies for inclusivity. However, certain regions still lag behind, emphasizing the need for targeted diversity strategies.

    Resource allocation emerges as a critical performance driver. Institutions with lower student-to-staff ratios consistently demonstrate superior teaching quality, urging policymakers to reconsider faculty investments strategically.

    Through PCA Loadings, we discover that PC1 acts as a 'University Strength' axis blending teaching, research, and industry outreach, while PC2 distinguishes universities highly focused on research impact. This two-axis structure explains over 90% of the variance, validating the use of PCA scatter plots for meaningful clustering and interpretation of global university profiles.

    Techniques like Principal Component Analysis (PCA) and KMeans helped us capture broader patterns and clusters among institutions worldwide. To uncover deeper, non-linear relationships, we applied UMAP and HDBSCAN, which allowed us to isolate hidden clusters and detect outliers with greater accuracy. By constructing similarity networks based on true cosine similarities, we also introduced a new perspective: identifying academic “twins” across different countries and continents, something traditional ranking lists cannot easily reveal.

    Our clustering analysis notably reveals six distinct university profiles:

    | **Cluster** | **University Type** | **Key Characteristics** |
    |:------------|:----------------------------------|:-------------------------|
    | **0** | Emerging Institutions             | Low scores in teaching, research, and international outlook; limited global presence. |
    | **1** | Research-Driven Universities      | Strong research quality and industry collaborations; moderate teaching focus; growing internationalization. |
    | **2** | Specialized Research Centers      | Moderate research excellence; weaker teaching and industry engagement; emerging in visibility. |
    | **3** | Developing Universities           | Weak across all metrics; very low internationalization; needs significant improvement. |
    | **4** | Balanced Mid-Tier Universities    | Moderate scores in teaching, research, and industry impact; on a steady path toward global competitiveness. |
    | **5** | World-Class Elite Universities    | Exceptional across all dimensions: teaching, research, industry impact, and international diversity. |

    Interactive comparisons between institutions illuminate competitive dynamics, crucial for stakeholders aiming at strategic improvements or partnerships.

    Overall, this project goes beyond simply reporting which universities rank highest. It sheds light on how and why certain patterns emerge, evolve, and sometimes diverge over time. The final system offers an educational intelligence framework that is not only informative but also actionable --- serving students, researchers, policymakers, and institutional leaders aiming to better understand and shape the future of higher education.
    ''')