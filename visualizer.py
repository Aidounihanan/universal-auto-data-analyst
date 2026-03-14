import plotly.express as px

def create_chart(df, chart_type, x, y, color=None):
    """Generate dynamic Plotly charts based on user selection."""
    if chart_type == "Scatter Plot":
        return px.scatter(df, x=x, y=y, color=color, template="plotly_white", 
                          title=f"{y} vs {x}")
    elif chart_type == "Bar Chart":
        return px.bar(df, x=x, y=y, color=color, template="plotly_dark",
                      title=f"Total {y} grouped by {x}")
    elif chart_type == "Histogram":
        return px.histogram(df, x=x, color=color, template="ggplot2",
                            title=f"Distribution of {x}")
    elif chart_type == "Box Plot":
        return px.box(df, x=x, y=y, color=color, template="presentation",
                      title=f"Statistical Spread of {y} by {x}")