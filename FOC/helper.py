

def parse_price(price_str):
    # Remove dollar sign and convert to float
    return float(price_str.replace('$', '').strip()) if price_str else None

def parse_volume(volume_str):
    # Convert volume to float
    return float(volume_str) if volume_str else None

def cast_columns(df, null_placeholder='--'):
    """
    Casts columns of a DataFrame to specified types, replacing placeholder values.
    
    Parameters:
    df (pd.DataFrame): The DataFrame to operate on.
    placeholder (str, optional): A placeholder value to replace before casting. Default is '--'.
    
    Returns:
    pd.DataFrame: The DataFrame with columns cast to the specified types.
    """
    column_types = {
    'c_Openinterest': int,
    'p_Openinterest': int,
    'c_Volume': int,
    'p_Volume': int,
    'strike': float,
    'p_Last': float,
    'c_Last': float,
    'c_Change': float,
    'p_Change': float,
    'c_Bid': float,
    'c_Ask': float,
    'p_Bid': float,
    'p_Ask': float,
    'c_Delta': float,
    'c_Gamma': float,
    'c_Rho': float,
    'c_Theta': float,
    'c_Vega': float,
    'c_Impvol': float,
    'p_Delta': float,
    'p_Gamma': float,
    'p_Rho': float,
    'p_Theta': float,
    'p_Vega': float,
    'p_Impvol': float
}
    
    # Make a copy of the DataFrame to avoid SettingWithCopyWarning
    df_casted = df.copy()
    
    for column, dtype in column_types.items():
        # Check if the column exists in the DataFrame
        if column not in df_casted.columns:
            continue
        # Replace placeholder and cast the column
        if dtype == int:
            df_casted.loc[df_casted[column] == null_placeholder, column] = 0
            df_casted[column] = df_casted[column].astype(int)
        elif dtype == float:
            df_casted.loc[df_casted[column] == null_placeholder, column] = 0.0
            df_casted[column] = df_casted[column].astype(float)
        # Add more elif blocks here for other data types as needed
        else:
            raise ValueError(f"Type '{dtype}' is not supported for casting.")
            
    return df_casted