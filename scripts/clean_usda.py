"""
clean_usda.py

Cleans and standardizes USDA NASS QuickStats crop yield data for Illinois.
Filters for corn and soybeans, normalizes county codes, and prepares data for integration.

Author: Rohit Shah
Project: Climate Variability and Agricultural Productivity in Illinois
Course: IS477
"""

import pandas as pd
import numpy as np
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_usda(filepath: str) -> pd.DataFrame:
    """
    Load USDA NASS crop yield data from CSV file.
    
    Args:
        filepath: Path to raw USDA CSV file
        
    Returns:
        DataFrame with loaded USDA data
    """
    logger.info(f"Loading USDA data from {filepath}")
    
    if not Path(filepath).exists():
        raise FileNotFoundError(f"USDA data file not found: {filepath}")
    
    try:
        df = pd.read_csv(filepath, low_memory=False)
        logger.info(f"Successfully loaded {len(df):,} rows")
        logger.info(f"Columns: {list(df.columns)}")
        return df
        
    except Exception as e:
        logger.error(f"Error loading USDA data: {e}")
        raise


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize column names to snake_case for consistency.
    
    Args:
        df: Raw USDA DataFrame
        
    Returns:
        DataFrame with normalized column names
    """
    logger.info("Normalizing column names to snake_case...")
    
    # Convert to snake_case
    df.columns = (df.columns
                  .str.lower()
                  .str.replace(' ', '_')
                  .str.replace('-', '_')
                  .str.replace('(', '')
                  .str.replace(')', ''))
    
    logger.info(f"Normalized columns: {list(df.columns)}")
    return df


def clean_usda(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and filter USDA crop yield data.
    Extracts relevant columns, filters for corn and soybeans, and handles missing values.
    
    Args:
        df: Raw USDA DataFrame
        
    Returns:
        Cleaned DataFrame with corn and soybean yields
    """
    logger.info("Cleaning USDA data...")
    initial_rows = len(df)
    
    # Identify key columns (NASS uses various naming conventions)
    # Common column names: 'Year', 'County', 'County Code', 'Commodity', 'Value'
    year_col = next((col for col in df.columns if 'year' in col.lower()), None)
    county_col = next((col for col in df.columns if 'county' in col.lower() and 'code' not in col.lower()), None)
    county_code_col = next((col for col in df.columns if 'county' in col.lower() and ('code' in col.lower() or 'ansi' in col.lower())), None)
    commodity_col = next((col for col in df.columns if 'commodity' in col.lower()), None)
    value_col = next((col for col in df.columns if 'value' in col.lower()), None)
    state_col = next((col for col in df.columns if 'state' in col.lower() and 'ansi' in col.lower()), None)
    
    logger.info(f"Identified columns - Year: {year_col}, County: {county_col}, "
                f"County Code: {county_code_col}, Commodity: {commodity_col}, Value: {value_col}")
    
    # Select relevant columns
    cols_to_keep = []
    col_mapping = {}
    
    if year_col:
        cols_to_keep.append(year_col)
        col_mapping[year_col] = 'year'
    if county_col:
        cols_to_keep.append(county_col)
        col_mapping[county_col] = 'county_name'
    if county_code_col:
        cols_to_keep.append(county_code_col)
        col_mapping[county_code_col] = 'county_code'
    if commodity_col:
        cols_to_keep.append(commodity_col)
        col_mapping[commodity_col] = 'commodity'
    if value_col:
        cols_to_keep.append(value_col)
        col_mapping[value_col] = 'yield'
    if state_col:
        cols_to_keep.append(state_col)
        col_mapping[state_col] = 'state_code'
    
    df = df[cols_to_keep].copy()
    df = df.rename(columns=col_mapping)
    
    # Filter for Illinois (FIPS code 17) if state_code exists
    if 'state_code' in df.columns:
        df = df[df['state_code'] == 17]
        logger.info(f"Filtered for Illinois: {len(df):,} rows")
    
    # Filter for CORN and SOYBEANS
    if 'commodity' in df.columns:
        df['commodity'] = df['commodity'].str.upper().str.strip()
        df = df[df['commodity'].isin(['CORN', 'SOYBEANS', 'CORN, GRAIN', 'SOYBEANS, ALL'])]
        logger.info(f"Filtered for corn and soybeans: {len(df):,} rows")
        
        # Standardize commodity names
        df['commodity'] = df['commodity'].replace({
            'CORN, GRAIN': 'CORN',
            'SOYBEANS, ALL': 'SOYBEANS'
        })
    
    # Convert year to integer
    if 'year' in df.columns:
        df['year'] = pd.to_numeric(df['year'], errors='coerce')
        df = df.dropna(subset=['year'])
        df['year'] = df['year'].astype(int)
    
    # Handle yield values
    if 'yield' in df.columns:
        # NASS often includes non-numeric values like "(D)" for suppressed data
        df['yield'] = pd.to_numeric(df['yield'], errors='coerce')
        
        # Remove rows with missing yields
        before = len(df)
        df = df.dropna(subset=['yield'])
        logger.info(f"Removed {before - len(df):,} rows with missing or suppressed yields")
        
        # Remove unrealistic yield values (outliers/data errors)
        # Typical corn yields: 50-250 bu/acre, soybeans: 20-80 bu/acre
        df = df[df['yield'] > 0]
        df = df[df['yield'] < 500]  # Conservative upper bound
    
    # Normalize county FIPS codes to 5-digit format (state + county)
    if 'county_code' in df.columns and 'state_code' in df.columns:
        # Combine state code (17 for IL) with county code
        df['county_fips'] = (df['state_code'].astype(str).str.zfill(2) + 
                            df['county_code'].astype(str).str.zfill(3))
    elif 'county_code' in df.columns:
        # Assume Illinois (17) if state code not available
        df['county_fips'] = '17' + df['county_code'].astype(str).str.zfill(3)
    
    # Remove any rows with invalid FIPS codes
    if 'county_fips' in df.columns:
        df = df[df['county_fips'].str.len() == 5]
    
    # Select final columns
    final_cols = ['year', 'county_fips', 'commodity', 'yield']
    if 'county_name' in df.columns:
        final_cols.insert(2, 'county_name')
    
    df = df[[col for col in final_cols if col in df.columns]]
    
    logger.info(f"Cleaning complete. {len(df):,} rows remaining ({initial_rows - len(df):,} removed)")
    logger.info(f"Date range: {df['year'].min()} to {df['year'].max()}")
    logger.info(f"Number of unique counties: {df['county_fips'].nunique()}")
    logger.info(f"Commodities: {df['commodity'].unique().tolist()}")
    
    return df


def save_output(df: pd.DataFrame, output_path: str) -> None:
    """
    Save cleaned USDA data to CSV file.
    
    Args:
        df: Cleaned DataFrame
        output_path: Path where CSV should be saved
    """
    # Create output directory if it doesn't exist
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Save to CSV
    df.to_csv(output_path, index=False)
    logger.info(f"Data saved to {output_path}")
    logger.info(f"Output shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
    
    # Log summary statistics by commodity
    logger.info("\nSummary Statistics by Commodity:")
    for commodity in df['commodity'].unique():
        subset = df[df['commodity'] == commodity]
        logger.info(f"\n{commodity}:")
        logger.info(f"  Mean yield: {subset['yield'].mean():.2f} bu/acre")
        logger.info(f"  Median yield: {subset['yield'].median():.2f} bu/acre")
        logger.info(f"  Std deviation: {subset['yield'].std():.2f} bu/acre")
        logger.info(f"  Observations: {len(subset):,}")


def main():
    """
    Main execution function for USDA data cleaning pipeline.
    """
    # Define file paths
    input_file = "/Users/dru/ISProject/data/raw/usda_yields.csv"
    output_file = "/Users/dru/ISProject/data/processed/usda_clean.csv"
    
    try:
        # Step 1: Load data
        df = load_usda(input_file)
        
        # Step 2: Normalize column names
        df = normalize_column_names(df)
        
        # Step 3: Clean data
        df_clean = clean_usda(df)
        
        # Step 4: Save output
        save_output(df_clean, output_file)
        
        logger.info("USDA data cleaning pipeline completed successfully!")
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise


if __name__ == "__main__":
    main()

