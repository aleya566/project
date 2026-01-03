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


import streamlit as st
import plotly.express as px

# 1. Define the GPA order (if your GPA column contains categories like '2.0-2.5', etc.)
# If GPA is a number, you can skip the 'category_orders' part.
gpa_order = sorted(df['GPA'].unique()) 

# 2. Create the Plotly Box Plot

fig3 = px.box(
    df,
    x="GPA",
    y="InsomniaSeverity_index",
    color="GPA", # Gives each box a different color from the palette
    title="Insomnia Severity Index Across GPA Categories",
    category_orders={"GPA": gpa_order},
    color_discrete_sequence=px.colors.sequential.Sunset, # Matches 'flare'
    points="outliers" # Show outliers specifically (default) or use "all"
)

# 3. Clean up labels and layout
fig3.update_layout(
    xaxis_title="GPA Category",
    yaxis_title="Insomnia Severity Index",
    showlegend=False, # Hide legend since the X-axis already identifies the GPA
    plot_bgcolor="rgba(0,0,0,0)" # Transparent background for a cleaner look
)

# 4. Display in Streamlit
st.plotly_chart(fig3, use_container_width=True)

import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Define the ordering logic
assignment_impact_order = ['No impact', 'Minor impact', 'Moderate impact', 'Major impact', 'Severe impact']
insomnia_category_order = ['Low / No Insomnia', 'Moderate Insomnia', 'Severe Insomnia']

# 2. Prepare the data (Crosstab to Melted format)
assignment_table = pd.crosstab(
    df["Insomnia_Category"], 
    df["AssignmentImpact"],
    dropna=False
)
assignment_melted = assignment_table.reset_index().melt(
    id_vars='Insomnia_Category', 
    var_name='AssignmentImpact', 
    value_name='Student_Count'
)

# 3. Create the Plotly Stacked Bar Chart
fig4 = px.bar(
    assignment_melted,
    x='Insomnia_Category',
    y='Student_Count',
    color='AssignmentImpact',
    title="Assignment Impact by Insomnia Category",
    category_orders={
        "AssignmentImpact": assignment_impact_order,
        "Insomnia_Category": insomnia_category_order
    },
    color_discrete_sequence=px.colors.sequential.Sunset, # Closest match to 'flare'
    labels={'Student_Count': 'Number of Students', 'Insomnia_Category': 'Insomnia Level'}
)

# 4. Refine layout (matches your plt.legend logic)
fig4.update_layout(
    barmode='stack', # This ensures the bars are stacked
    xaxis_title="Insomnia Category",
    yaxis_title="Number of Students",
    legend_title_text='Assignment Impact'
)

# 5. Display in Streamlit
st.plotly_chart(fig4, use_container_width=True)

# Prepare Data
daytime_fatigue_order = ['Never', 'Rarely', 'Sometimes', 'Often', 'Always']
fatigue_table = pd.crosstab(df['Insomnia_Category'], df['DaytimeFatigue'], dropna=False)
fatigue_melted = fatigue_table.reset_index().melt(id_vars='Insomnia_Category', var_name='DaytimeFatigue', value_name='Count')

# Plot
fig5 = px.bar(
    fatigue_melted,
    x='Insomnia_Category',
    y='Count',
    color='DaytimeFatigue',
    title="Fatigue Level by Insomnia Severity",
    category_orders={"DaytimeFatigue": daytime_fatigue_order},
    color_discrete_sequence=px.colors.sequential.Sunset,
    barmode='stack'
)
st.plotly_chart(fig5, use_container_width=True)

import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Pastikan urutan kategori adalah tepat (Excellent di atas, Below Average di bawah)
# Kita susun begini supaya dalam graf, Excellent berada di kedudukan tertinggi paksi-Y
academic_order = ['Below average', 'Average', 'Good', 'Very good', 'Excellent']
insomnia_order = ['Low / No Insomnia', 'Moderate Insomnia', 'Severe Insomnia']

# 2. Tukar data kepada kategori (Penting untuk susunan paksi)
df['AcademicPerformance'] = pd.Categorical(
    df['AcademicPerformance'], 
    categories=academic_order, 
    ordered=True
)

# 3. Gunakan px.box (BUKAN px.histogram atau px.bar)
fig = px.box(
    df,
    x='Insomnia_Category',
    y='AcademicPerformance',
    color='Insomnia_Category',
    title="Academic Performance by Insomnia Severity",
    # category_orders memastikan Excellent di atas dan Below Average di bawah
    category_orders={
        "AcademicPerformance": academic_order,
        "Insomnia_Category": insomnia_order
    },
    color_discrete_sequence=px.colors.sequential.Sunset,
    points="outliers" 
)

# 4. Laraskan Layout supaya serupa dengan Colab
fig.update_layout(
    xaxis_title="Insomnia Severity",
    yaxis_title="Academic Performance (GPA / Self-rated)",
    showlegend=False,
    # Memaksa paksi-Y mengikut urutan kategori yang kita tetapkan
    yaxis=dict(autorange="reversed") 
)

st.plotly_chart(fig, use_container_width=True)

# Select columns and calculate matrix
corr_columns = [
    'SleepHours_est', 'InsomniaSeverity_index', 'DaytimeFatigue_numeric',
    'ConcentrationDifficulty_numeric', 'MissedClasses_numeric',
    'AcademicPerformance_numeric', 'GPA_numeric', 'CGPA_numeric'
]
# Ensure we only use columns that exist in df
existing_cols = [c for c in corr_columns if c in df.columns]
corr_matrix = df[existing_cols].corr()

# Create Heatmap
fig7 = px.imshow(
    corr_matrix,
    text_auto=".2f", # Adds the numbers inside the squares
    aspect="auto",
    color_continuous_scale='Sunset', # Matches 'flare'
    title="Correlation Heatmap: Sleep Issues vs. Academic Outcomes"
)
st.plotly_chart(fig7, use_container_width=True)
