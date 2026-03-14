import pandas as pd

def load_data(file):
    """Detect file extension and load into a Pandas DataFrame."""
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    return pd.read_excel(file)

def clean_data(df):
    """
    Perform automated data cleaning:
    1. Remove empty columns.
    2. Auto-detect and convert date strings.
    3. Fill missing numerical values with median.
    4. Fill missing categorical values with 'Unknown'.
    """
    # Drop columns where all values are NaN
    df = df.dropna(axis=1, how='all')
    
    # Auto-detect date columns by name pattern
    for col in df.columns:
        if 'date' in col.lower() or 'time' in col.lower():
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Fill missing numerical values
    num_cols = df.select_dtypes(include=['number']).columns
    df[num_cols] = df[num_cols].fillna(df[num_cols].median())
    
    # Fill missing categorical values
    cat_cols = df.select_dtypes(exclude=['number']).columns
    df[cat_cols] = df[cat_cols].fillna("Unknown")
    
    return df