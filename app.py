import streamlit as st
from data_processor import load_data, clean_data
from visualizer import create_chart

# Page Configuration
st.set_page_config(page_title="Universal Data Explorer", layout="wide")

st.title("📊 Universal Data Explorer")
st.markdown("Upload any dataset to visualize insights instantly.")

# File Uploader
uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    # 1. Processing Pipeline
    df_raw = load_data(uploaded_file)
    df = clean_data(df_raw)
    
    st.sidebar.header("Chart Configuration")
    
    # 2. Automated Type Detection
    all_cols = df.columns.tolist()
    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    cat_cols = [None] + df.select_dtypes(exclude=['number']).columns.tolist()

    # 3. Streamlit Widgets (Input)
    chart_options = ["Scatter Plot", "Bar Chart", "Histogram"]
    chart_type = st.sidebar.selectbox("Select Chart Type", chart_options)
    
    x_axis = st.sidebar.selectbox("Select X Axis", all_cols)
    y_axis = st.sidebar.selectbox("Select Y Axis (Numerical)", num_cols)
    color_choice = st.sidebar.selectbox("Segment by (Color)", cat_cols)

    # 4. Display Logic
    st.subheader(f"Analysis: {x_axis} vs {y_axis}")
    
    # Generate chart using the modular visualizer
    fig = create_chart(df, chart_type, x_axis, y_axis, color_choice)
    st.plotly_chart(fig, use_container_width=True)

    # 5. Data Preview
    with st.expander("View Cleaned Data Preview"):
        st.dataframe(df.head(10))