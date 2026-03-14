import pandas as pd

def get_correlations(df):
    """Extract top 3 strongest numerical correlations (excluding self-correlation)."""
    num_df = df.select_dtypes(include=['number'])
    if num_df.shape[1] < 2:
        return None
    
    # Calculate correlation matrix and unstack
    corr_matrix = num_df.corr().unstack().sort_values(ascending=False)
    # Filter out 1.0 (self-correlation) and take top unique pairs
    top_corr = corr_matrix[corr_matrix < 1].head(6) 
    return top_corr.iloc[::2] # Keep one entry per pair

def get_outliers(df):
    """Detect statistical outliers using the Interquartile Range (IQR) method."""
    outliers_report = {}
    num_cols = df.select_dtypes(include=['number']).columns
    
    for col in num_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        count = df[(df[col] < lower_bound) | (df[col] > upper_bound)].shape[0]
        if count > 0:
            outliers_report[col] = count
    return outliers_report