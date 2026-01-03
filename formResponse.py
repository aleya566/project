import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="🧠 Interpretation Dashboard: Impact of Sleep Related Issues on Academic Performance", 
    layout="wide"
)

# ==========================================
# 2. DATA LOADING & PRE-PROCESSING
# ==========================================
@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/aleya566/project/refs/heads/main/final_processed_data%20(8).csv'
    df = pd.read_csv(url)
    
    # Define category orders (Used across all charts)
    academic_order = ['Below average', 'Average', 'Good', 'Very good', 'Excellent']
    insomnia_order = ['Low / No Insomnia', 'Moderate Insomnia', 'Severe Insomnia']
    freq_order = ['Never', 'Rarely', 'Sometimes', 'Often', 'Always']
    impact_order = ['No impact', 'Minor impact', 'Moderate impact', 'Major impact', 'Severe impact']
    
    # Convert columns to categorical type to ensure correct ordering in plots
    df['AcademicPerformance'] = pd.Categorical(df['AcademicPerformance'], categories=academic_order, ordered=True)
    df['Insomnia_Category'] = pd.Categorical(df['Insomnia_Category'], categories=insomnia_order, ordered=True)
    df['ConcentrationDifficulty'] = pd.Categorical(df['ConcentrationDifficulty'], categories=freq_order, ordered=True)
    df['AssignmentImpact'] = pd.Categorical(df['AssignmentImpact'], categories=impact_order, ordered=True)
    df['DaytimeFatigue'] = pd.Categorical(df['DaytimeFatigue'], categories=freq_order, ordered=True)
    
    return df, academic_order, insomnia_order, freq_order, impact_order

df, academic_order, insomnia_order, freq_order, impact_order = load_data()

# ==========================================
# 3. DASHBOARD CONTENT (ORIGINAL LAYOUT)
# ==========================================
st.title("Interpretation Dashboard: Impact of Sleep Related Issues on Academic Performance")

# --- CHART 1: Concentration Difficulty (Grouped Bar) ---
concentration_crosstab = pd.crosstab(df['Insomnia_Category'], df['ConcentrationDifficulty'], dropna=False)
concentration_melted = concentration_crosstab.reset_index().melt(id_vars='Insomnia_Category', var_name='ConcentrationDifficulty', value_name='Count')

fig2 = px.bar(
    concentration_melted, x='Insomnia_Category', y='Count', color='ConcentrationDifficulty',
    barmode='group', title='Concentration Difficulty by Insomnia Category',
    category_orders={"ConcentrationDifficulty": freq_order, "Insomnia_Category": insomnia_order},
    color_discrete_sequence=px.colors.sequential.Sunset,
    labels={'Count': 'Number of Students', 'Insomnia_Category': 'Insomnia Level'}
)
st.plotly_chart(fig2, use_container_width=True)

# --- CHART 2: GPA vs Insomnia Index (Box Plot) ---
gpa_order = sorted(df['GPA'].unique()) 
fig3 = px.box(
    df, x="GPA", y="InsomniaSeverity_index", color="GPA",
    title="Insomnia Severity Index Across GPA Categories",
    category_orders={"GPA": gpa_order},
    color_discrete_sequence=px.colors.sequential.Sunset,
    points="outliers"
)
fig3.update_layout(xaxis_title="GPA Category", yaxis_title="Insomnia Severity Index", showlegend=False, plot_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig3, use_container_width=True)

# --- CHART 3: Assignment Impact (Stacked Bar) ---
assignment_table = pd.crosstab(df["Insomnia_Category"], df["AssignmentImpact"], dropna=False)
assignment_melted = assignment_table.reset_index().melt(id_vars='Insomnia_Category', var_name='AssignmentImpact', value_name='Student_Count')

fig4 = px.bar(
    assignment_melted, x='Insomnia_Category', y='Student_Count', color='AssignmentImpact',
    title="Assignment Impact by Insomnia Category",
    category_orders={"AssignmentImpact": impact_order, "Insomnia_Category": insomnia_order},
    color_discrete_sequence=px.colors.sequential.Sunset,
    labels={'Student_Count': 'Number of Students'}
)
fig4.update_layout(barmode='stack', xaxis_title="Insomnia Category", yaxis_title="Number of Students")
st.plotly_chart(fig4, use_container_width=True)

# --- CHART 4: Daytime Fatigue (Stacked Bar) ---
fatigue_table = pd.crosstab(df['Insomnia_Category'], df['DaytimeFatigue'], dropna=False)
fatigue_melted = fatigue_table.reset_index().melt(id_vars='Insomnia_Category', var_name='DaytimeFatigue', value_name='Count')

fig5 = px.bar(
    fatigue_melted, x='Insomnia_Category', y='Count', color='DaytimeFatigue',
    title="Fatigue Level by Insomnia Severity",
    category_orders={"DaytimeFatigue": freq_order, "Insomnia_Category": insomnia_order},
    color_discrete_sequence=px.colors.sequential.Sunset,
    barmode='stack'
)
st.plotly_chart(fig5, use_container_width=True)

# --- CHART 5: Academic Performance (Box Plot) ---
fig6 = px.box(
    df, x='Insomnia_Category', y='AcademicPerformance', color='Insomnia_Category',
    title="Academic Performance by Insomnia Severity",
    category_orders={"AcademicPerformance": academic_order, "Insomnia_Category": insomnia_order},
    color_discrete_sequence=px.colors.sequential.Sunset,
    points="outliers" 
)
fig6.update_layout(xaxis_title="Insomnia Severity", yaxis_title="Academic Performance (GPA / Self-rated)", showlegend=False, yaxis=dict(autorange="reversed"))
st.plotly_chart(fig6, use_container_width=True)

# --- CHART 6: Correlation Heatmap ---
corr_columns = ['SleepHours_est', 'InsomniaSeverity_index', 'DaytimeFatigue_numeric', 'ConcentrationDifficulty_numeric', 'MissedClasses_numeric', 'AcademicPerformance_numeric', 'GPA_numeric', 'CGPA_numeric']
existing_cols = [c for c in corr_columns if c in df.columns]
corr_matrix = df[existing_cols].corr()

fig7 = px.imshow(
    corr_matrix, text_auto=".2f", aspect="auto",
    color_continuous_scale='Sunset',
    title="Correlation Heatmap: Sleep Issues vs. Academic Outcomes"
)
st.plotly_chart(fig7, use_container_width=True)
