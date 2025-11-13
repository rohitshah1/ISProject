"""
clean_noaa.py

Cleans and aggregates NOAA weather data from daily observations to county-year level.
Computes temperature volatility metrics and prepares data for integration with crop yields.

Author: Dev Rishi Udata
Project: Climate Variability and Agricultural Productivity in Illinois
Course: IS477
"""

import pandas as pd
import numpy as np
import logging
from pathlib import Path
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_noaa(filepath: str, chunksize: int = 50000) -> pd.DataFrame:
    """
    Load NOAA weather data in chunks to handle large files efficiently.
    
    Args:
        filepath: Path to raw NOAA CSV file
        chunksize: Number of rows to process at once
        
    Returns:
        DataFrame with loaded NOAA data
    """
    logger.info(f"Loading NOAA data from {filepath}")
    
    if not Path(filepath).exists():
        raise FileNotFoundError(f"NOAA data file not found: {filepath}")
    
    # Columns we need from NOAA data
    required_columns = ['date', 'station', 'county_fips', 'tmax', 'tmin', 'tavg', 'prcp']
    
    chunks = []
    total_rows = 0
    
    try:
        # Read CSV in chunks
        for chunk in pd.read_csv(filepath, chunksize=chunksize, low_memory=False):
            # Select only required columns if they exist
            available_cols = [col for col in required_columns if col in chunk.columns]
            chunk = chunk[available_cols]
            chunks.append(chunk)
            total_rows += len(chunk)
            
            if total_rows % 100000 == 0:
                logger.info(f"Processed {total_rows:,} rows...")
        
        # Combine all chunks
        df = pd.concat(chunks, ignore_index=True)
        logger.info(f"Successfully loaded {len(df):,} total rows")
        return df
        
    except Exception as e:
        logger.error(f"Error loading NOAA data: {e}")
        raise


def clean_noaa(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean NOAA weather data by handling missing values and converting units.
    
    Args:
        df: Raw NOAA DataFrame
        
    Returns:
        Cleaned DataFrame with standardized temperature and precipitation values
    """
    logger.info("Cleaning NOAA data...")
    initial_rows = len(df)
    
    # Convert date to datetime
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    
    # Drop rows with invalid dates
    df = df.dropna(subset=['date'])
    logger.info(f"Dropped {initial_rows - len(df):,} rows with invalid dates")
    
    # Extract year for grouping
    df['year'] = df['date'].dt.year
    
    # NOAA temperatures are stored in tenths of degrees Celsius
    # Convert to actual degrees Celsius
    temp_columns = ['tmax', 'tmin', 'tavg']
    for col in temp_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce') / 10.0
    
    # NOAA precipitation is in tenths of mm, convert to mm
    if 'prcp' in df.columns:
        df['prcp'] = pd.to_numeric(df['prcp'], errors='coerce') / 10.0
    
    # Drop rows where ALL temperature fields are missing
    if all(col in df.columns for col in temp_columns):
        before = len(df)
        df = df.dropna(subset=temp_columns, how='all')
        logger.info(f"Dropped {before - len(df):,} rows with all temperature values missing")
    
    # Standardize county FIPS codes (ensure 5-digit format)
    if 'county_fips' in df.columns:
        df['county_fips'] = df['county_fips'].astype(str).str.zfill(5)
    
    logger.info(f"Cleaning complete. {len(df):,} rows remaining")
    return df


def aggregate_noaa(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate daily NOAA data to county-year level.
    Computes annual means and temperature volatility metrics.
    
    Args:
        df: Cleaned NOAA DataFrame with daily observations
        
    Returns:
        DataFrame aggregated to county-year level with volatility metrics
    """
    logger.info("Aggregating NOAA data to county-year level...")
    
    # Group by county and year
    group_cols = ['county_fips', 'year']
    
    # Define aggregation functions
    agg_dict = {}
    
    if 'tmax' in df.columns:
        agg_dict['tmax'] = ['mean', 'std']
    if 'tmin' in df.columns:
        agg_dict['tmin'] = ['mean', 'std']
    if 'tavg' in df.columns:
        agg_dict['tavg'] = ['mean', 'std']
    if 'prcp' in df.columns:
        agg_dict['prcp'] = ['sum', 'mean']  # Total annual precip + mean daily
    
    # Perform aggregation
    df_agg = df.groupby(group_cols).agg(agg_dict).reset_index()
    
    # Flatten column names
    df_agg.columns = ['_'.join(col).strip('_') if col[1] else col[0] 
                      for col in df_agg.columns.values]
    
    # Rename columns for clarity
    rename_dict = {
        'tavg_mean': 'mean_temp',
        'tavg_std': 'temp_sd',  # Temperature volatility (standard deviation)
        'tmax_mean': 'mean_tmax',
        'tmin_mean': 'mean_tmin',
        'prcp_sum': 'annual_prcp',
        'prcp_mean': 'mean_daily_prcp'
    }
    
    df_agg = df_agg.rename(columns=rename_dict)
    
    logger.info(f"Aggregated to {len(df_agg):,} county-year observations")
    logger.info(f"Date range: {df_agg['year'].min()} to {df_agg['year'].max()}")
    logger.info(f"Number of unique counties: {df_agg['county_fips'].nunique()}")
    
    return df_agg


def save_output(df: pd.DataFrame, output_path: str) -> None:
    """
    Save cleaned and aggregated data to CSV file.
    
    Args:
        df: Processed DataFrame
        output_path: Path where CSV should be saved
    """
    # Create output directory if it doesn't exist
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Save to CSV
    df.to_csv(output_path, index=False)
    logger.info(f"Data saved to {output_path}")
    logger.info(f"Output shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
    
    # Log summary statistics
    logger.info("\nSummary Statistics:")
    logger.info(f"Mean annual temperature: {df['mean_temp'].mean():.2f}°C" if 'mean_temp' in df.columns else "")
    logger.info(f"Mean temperature volatility (SD): {df['temp_sd'].mean():.2f}°C" if 'temp_sd' in df.columns else "")
    logger.info(f"Mean annual precipitation: {df['annual_prcp'].mean():.2f} mm" if 'annual_prcp' in df.columns else "")


def main():
    """
    Main execution function for NOAA data cleaning pipeline.
    """
    # Define file paths
    input_file = "/Users/dru/ISProject/data/raw/noaa_full.csv"
    output_file = "/Users/dru/ISProject/data/processed/noaa_clean.csv"
    
    try:
        # Step 1: Load data
        df = load_noaa(input_file, chunksize=50000)
        
        # Step 2: Clean data
        df_clean = clean_noaa(df)
        
        # Step 3: Aggregate to county-year
        df_agg = aggregate_noaa(df_clean)
        
        # Step 4: Save output
        save_output(df_agg, output_file)
        
        logger.info("NOAA data cleaning pipeline completed successfully!")
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise


if __name__ == "__main__":
    main()

