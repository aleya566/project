import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- Streamlit Page Config ---
st.set_page_config(page_title="Exploration Dashboard: Academic Stress and Sleep Patterns Among Students", layout="wide")

# --- Load Data ---
@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/aleya566/project/refs/heads/main/final_processed_data%20(8).csv'
    df = pd.read_csv(url)
    return df

df = load_data()
# Title for the Streamlit App
st.title("Student Health Analysis")

# Create the Plotly figure
# 'flare' is a sequential palette; px.colors.sequential.Sunset or RdPu are close matches
fig = px.histogram(
    df, 
    x='Insomnia_Category', 
    color='Insomnia_Category',
    title="Distribution of Insomnia Severity among Students",
    labels={'Insomnia_Category': 'Insomnia Severity', 'count': 'Number of Students'},
    color_discrete_sequence=px.colors.sequential.Sunset  # Matches the 'flare' aesthetic
)

# Optional: Improve layout to match Seaborn's default clean look
fig.update_layout(
    xaxis_title="Insomnia Severity",
    yaxis_title="Number of Students",
    showlegend=False
)

# Display in Streamlit
st.plotly_chart(fig, use_container_width=True)


import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Prepare the Data (Ensure categories are ordered)
concentration_difficulty_order = ['Never', 'Rarely', 'Sometimes', 'Often', 'Always']
insomnia_category_order = ['Low / No Insomnia', 'Moderate Insomnia', 'Severe Insomnia']

df['ConcentrationDifficulty'] = pd.Categorical(
    df['ConcentrationDifficulty'], 
    categories=concentration_difficulty_order, 
    ordered=True
)
df['Insomnia_Category'] = pd.Categorical(
    df['Insomnia_Category'], 
    categories=insomnia_category_order, 
    ordered=True
)

# 2. Create the Cross-tab and Melt (Just like your original code)
concentration_crosstab = pd.crosstab(
    df['Insomnia_Category'], 
    df['ConcentrationDifficulty'], 
    dropna=False
)
concentration_melted = concentration_crosstab.reset_index().melt(
    id_vars='Insomnia_Category', 
    var_name='ConcentrationDifficulty', 
    value_name='Count'
)

# 3. Create the Plotly Grouped Bar Chart
fig2 = px.bar(
    concentration_melted,
    x='Insomnia_Category',
    y='Count',
    color='ConcentrationDifficulty',
    barmode='group',  # This creates the "grouped" effect instead of stacked
    title='Concentration Difficulty by Insomnia Category',
    category_orders={
        "ConcentrationDifficulty": concentration_difficulty_order,
        "Insomnia_Category": insomnia_category_order
    },
    color_discrete_sequence=px.colors.sequential.Sunset,
    labels={'Count': 'Number of Students', 'Insomnia_Category': 'Insomnia Level'}
)

fig2.update_layout(
    legend_title_text='Concentration Difficulty',
    xaxis_title="Insomnia Category",
    yaxis_title="Number of Students"
)

# 4. Display in Streamlit
st.plotly_chart(fig2, use_container_width=True)
