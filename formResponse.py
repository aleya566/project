import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Exploration Dashboard: Academic Stress and Sleep Patterns", 
    layout="wide"
)

# ==========================================
# 2. DATA LOADING & PRE-PROCESSING
# ==========================================
@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/aleya566/project/refs/heads/main/final_processed_data%20(8).csv'
    df = pd.read_csv(url)
    
    # Define global category orders for consistency
    academic_order = ['Below average', 'Average', 'Good', 'Very good', 'Excellent']
    insomnia_order = ['Low / No Insomnia', 'Moderate Insomnia', 'Severe Insomnia']
    frequency_order = ['Never', 'Rarely', 'Sometimes', 'Often', 'Always']
    impact_order = ['No impact', 'Minor impact', 'Moderate impact', 'Major impact', 'Severe impact']
    
    # Apply categorical ordering to the dataframe
    df['AcademicPerformance'] = pd.Categorical(df['AcademicPerformance'], categories=academic_order, ordered=True)
    df['Insomnia_Category'] = pd.Categorical(df['Insomnia_Category'], categories=insomnia_order, ordered=True)
    df['ConcentrationDifficulty'] = pd.Categorical(df['ConcentrationDifficulty'], categories=frequency_order, ordered=True)
    df['AssignmentImpact'] = pd.Categorical(df['AssignmentImpact'], categories=impact_order, ordered=True)
    df['DaytimeFatigue'] = pd.Categorical(df['DaytimeFatigue'], categories=frequency_order, ordered=True)
    
    return df, academic_order, insomnia_order, frequency_order, impact_order

df, academic_order, insomnia_order, frequency_order, impact_order = load_data()

# ==========================================
# 3. HEADER & NAVIGATION STRUCTURE
# ==========================================
st.title("📊 Student Health & Academic Analysis")
st.markdown("Exploring the relationship between sleep quality (Insomnia) and academic outcomes.")

# Using Tabs to keep the dashboard organized and scannable
tab1, tab2, tab3 = st.tabs(["📉 Academic Analysis", "😴 Sleep & Fatigue Patterns", "🔗 Overall Correlations"])

# ==========================================
# TAB 1: ACADEMIC ANALYSIS
# ==========================================
with tab1:
    col1, col2 = st.columns(2)

    with col1:
        # Box Plot: Academic Performance vs Insomnia
        fig_ac = px.box(
            df, x='Insomnia_Category', y='AcademicPerformance', color='Insomnia_Category',
            title="Academic Performance by Insomnia Severity",
            category_orders={"AcademicPerformance": academic_order, "Insomnia_Category": insomnia_order},
            color_discrete_sequence=px.colors.sequential.Sunset,
            points="outliers"
        )
        # Use reversed autorange so 'Excellent' stays at the top of the Y-axis
        fig_ac.update_layout(yaxis=dict(autorange="reversed"), showlegend=False)
        st.plotly_chart(fig_ac, use_container_width=True)

    with col2:
        # Box Plot: Insomnia Index vs GPA
        gpa_order = sorted(df['GPA'].unique())
        fig_gpa = px.box(
            df, x="GPA", y="InsomniaSeverity_index", color="GPA",
            title="Insomnia Severity Index Across GPA Categories",
            category_orders={"GPA": gpa_order},
            color_discrete_sequence=px.colors.sequential.Sunset,
            points="outliers"
        )
        fig_gpa.update_layout(showlegend=False)
        st.plotly_chart(fig_gpa, use_container_width=True)

# ==========================================
# TAB 2: SLEEP & FATIGUE PATTERNS
# ==========================================
with tab2:
    col3, col4 = st.columns(2)

    with col3:
        # Grouped Bar: Concentration Difficulty
        conc_data = pd.crosstab(df['Insomnia_Category'], df['ConcentrationDifficulty'], dropna=False).reset_index().melt(id_vars='Insomnia_Category')
        fig_conc = px.bar(
            conc_data, x='Insomnia_Category', y='value', color='ConcentrationDifficulty',
            barmode='group', title='Concentration Difficulty by Insomnia Category',
            category_orders={"ConcentrationDifficulty": frequency_order, "Insomnia_Category": insomnia_order},
            color_discrete_sequence=px.colors.sequential.Sunset,
            labels={'value': 'Number of Students'}
        )
        st.plotly_chart(fig_conc, use_container_width=True)

    with col4:
        # Stacked Bar: Daytime Fatigue
        fatigue_data = pd.crosstab(df['Insomnia_Category'], df['DaytimeFatigue'], dropna=False).reset_index().melt(id_vars='Insomnia_Category')
        fig_fatigue = px.bar(
            fatigue_data, x='Insomnia_Category', y='value', color='DaytimeFatigue',
            barmode='stack', title="Fatigue Level by Insomnia Severity",
            category_orders={"DaytimeFatigue": frequency_order, "Insomnia_Category": insomnia_order},
            color_discrete_sequence=px.colors.sequential.Sunset,
            labels={'value': 'Number of Students'}
        )
        st.plotly_chart(fig_fatigue, use_container_width=True)

    # Assignment Impact (Full Width Stacked Bar)
    assign_data = pd.crosstab(df["Insomnia_Category"], df["AssignmentImpact"], dropna=False).reset_index().melt(id_vars='Insomnia_Category')
    fig_assign = px.bar(
        assign_data, x='Insomnia_Category', y='value', color='AssignmentImpact',
        barmode='stack', title="Assignment Impact by Insomnia Category",
        category_orders={"AssignmentImpact": impact_order, "Insomnia_Category": insomnia_order},
        color_discrete_sequence=px.colors.sequential.Sunset,
        labels={'value': 'Number of Students'}
    )
    st.plotly_chart(fig_assign, use_container_width=True)

# ==========================================
# TAB 3: CORRELATIONS
# ==========================================
with tab3:
    st.subheader("Statistical Correlation")
    # Identify numerical columns for correlation matrix
    corr_columns = [
        'SleepHours_est', 'InsomniaSeverity_index', 'DaytimeFatigue_numeric',
        'ConcentrationDifficulty_numeric', 'MissedClasses_numeric',
        'AcademicPerformance_numeric', 'GPA_numeric', 'CGPA_numeric'
    ]
    existing_cols = [c for c in corr_columns if c in df.columns]
    corr_matrix = df[existing_cols].corr()

    # Heatmap visualization
    fig_heat = px.imshow(
        corr_matrix, text_auto=".2f", aspect="auto",
        color_continuous_scale='Sunset',
        title="Correlation Heatmap: Sleep Issues vs. Academic Outcomes"
    )
    st.plotly_chart(fig_heat, use_container_width=True)
