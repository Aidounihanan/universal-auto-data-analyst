import streamlit as st
from data_processor import load_data, clean_data
from visualizer import create_chart
from analyzer import get_correlations, get_outliers

# Page Configuration
st.set_page_config(page_title="Universal Auto-Data Analyst", layout="wide")

st.title("📊 Universal Auto-Data Analyst")
st.markdown("Upload any CSV or Excel file to get instant insights and visualizations.")

# File Uploader
uploaded_file = st.file_uploader("Upload your dataset", type=["csv", "xlsx"])

if uploaded_file:
    # Processing pipeline
    df_raw = load_data(uploaded_file)
    df = clean_data(df_raw)
    
    # Sidebar Configuration
    st.sidebar.header("Chart Settings")
    all_cols = df.columns.tolist()
    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    cat_cols = [None] + df.select_dtypes(exclude=['number']).columns.tolist()

    chart_type = st.sidebar.selectbox("Select Chart Type", ["Scatter Plot", "Bar Chart", "Histogram", "Box Plot"])
    x_axis = st.sidebar.selectbox("Select X-Axis", all_cols)
    y_axis = st.sidebar.selectbox("Select Y-Axis (Numerical)", num_cols)
    color_choice = st.sidebar.selectbox("Color Segment (Optional)", cat_cols)

    # Main Display: Visuals
    st.subheader("📈 Dynamic Visualization")
    fig = create_chart(df, chart_type, x_axis, y_axis, color_choice)
    st.plotly_chart(fig, use_container_width=True)

    # Main Display: Automated Insights
    st.divider()
    st.subheader("🚀 Smart Automated Insights")
    col1, col2 = st.columns(2)

    with col1:
        st.write("🔗 **Key Correlations**")
        top_corrs = get_correlations(df)
        if top_corrs is not None:
            for (v1, v2), val in top_corrs.items():
                st.info(f"**{v1}** & **{v2}**: `{val:.2f}`")
        else:
            st.write("No sufficient numerical data.")

    with col2:
        st.write("⚠️ **Anomaly Detection (Outliers)**")
        outliers = get_outliers(df)
        if outliers:
            for col, count in outliers.items():
                st.warning(f"**{col}**: {count} outliers found")
        else:
            st.success("No significant outliers detected!")

    # Data Preview
    with st.expander("View Cleaned Data Preview"):
        st.dataframe(df.head(20))