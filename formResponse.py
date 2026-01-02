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
