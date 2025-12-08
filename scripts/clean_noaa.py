"""
clean_noaa.py

Cleans and aggregates NOAA weather data from daily observations to annual level.
Computes temperature volatility metrics and prepares data for integration with crop yields.

Author: Dev Rishi Udata
Project: Climate Variability and Agricultural Productivity in Illinois
Course: IS477
"""

import pandas as pd
import numpy as np
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_noaa(filepath: str, chunksize: int = 50000) -> pd.DataFrame:
    """Load NOAA weather data in chunks since the file is huge."""
    logger.info(f"Loading NOAA data from {filepath}")
    
    if not Path(filepath).exists():
        raise FileNotFoundError(f"NOAA data file not found: {filepath}")
    
    chunks = []
    total_rows = 0
    
    try:
        for chunk in pd.read_csv(filepath, chunksize=chunksize, low_memory=False):
            chunks.append(chunk)
            total_rows += len(chunk)
            
            if total_rows % 100000 == 0:
                logger.info(f"Processed {total_rows:,} rows...")
        
        df = pd.concat(chunks, ignore_index=True)
        logger.info(f"Successfully loaded {len(df):,} total rows")
        return df
        
    except Exception as e:
        logger.error(f"Error loading NOAA data: {e}")
        raise


def clean_noaa(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the raw NOAA data and convert units."""
    logger.info("Cleaning NOAA data...")
    initial_rows = len(df)
    
    # Normalize column names
    df.columns = df.columns.str.lower().str.strip()
    
    # Convert date
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date'])
    logger.info(f"Dropped {initial_rows - len(df):,} rows with invalid dates")
    
    # Extract year
    df['year'] = df['date'].dt.year
    
    # Convert numeric columns
    for col in ['tmax', 'tmin', 'tavg', 'prcp']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Drop rows missing all temperature data
    temp_cols = [c for c in ['tmax', 'tmin', 'tavg'] if c in df.columns]
    if temp_cols:
        before = len(df)
        df = df.dropna(subset=temp_cols, how='all')
        logger.info(f"Dropped {before - len(df):,} rows with all temps missing")
    
    logger.info(f"Cleaning complete. {len(df):,} rows remaining")
    return df


def aggregate_noaa(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate daily data to annual level (state-wide for Illinois)."""
    logger.info("Aggregating NOAA data to annual level...")
    
    # Since we don't have reliable county_fips, aggregate to state-year level
    # This will give us one set of climate metrics per year for Illinois
    group_cols = ['year']
    
    agg_dict = {}
    
    if 'tmax' in df.columns:
        agg_dict['tmax'] = ['mean', 'std']
    if 'tmin' in df.columns:
        agg_dict['tmin'] = ['mean', 'std']
    if 'tavg' in df.columns:
        agg_dict['tavg'] = ['mean', 'std']
    if 'prcp' in df.columns:
        agg_dict['prcp'] = ['sum', 'mean']
    
    if not agg_dict:
        raise ValueError("No temperature or precipitation columns found")
    
    df_agg = df.groupby(group_cols).agg(agg_dict).reset_index()
    
    # Flatten column names
    df_agg.columns = ['_'.join(col).strip('_') if col[1] else col[0] 
                      for col in df_agg.columns.values]
    
    # Rename for clarity
    rename_dict = {
        'tavg_mean': 'mean_temp',
        'tavg_std': 'temp_sd',
        'tmax_mean': 'mean_tmax',
        'tmin_mean': 'mean_tmin',
        'prcp_sum': 'annual_prcp',
        'prcp_mean': 'mean_daily_prcp'
    }
    
    df_agg = df_agg.rename(columns=rename_dict)
    
    logger.info(f"Aggregated to {len(df_agg):,} annual observations")
    logger.info(f"Year range: {df_agg['year'].min()} to {df_agg['year'].max()}")
    
    return df_agg


def save_output(df: pd.DataFrame, output_path: str) -> None:
    """Save the processed data to CSV."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    df.to_csv(output_path, index=False)
    logger.info(f"Data saved to {output_path}")
    logger.info(f"Output shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
    
    # Log summary stats
    logger.info("\nSummary Statistics:")
    if 'mean_temp' in df.columns:
        logger.info(f"Mean annual temperature: {df['mean_temp'].mean():.2f}°C")
    if 'temp_sd' in df.columns:
        logger.info(f"Mean temperature volatility: {df['temp_sd'].mean():.2f}°C")
    if 'annual_prcp' in df.columns:
        logger.info(f"Mean annual precipitation: {df['annual_prcp'].mean():.2f} mm")


def main():
    """Run the NOAA cleaning pipeline."""
    input_file = "/Users/dru/ISProject/data/raw/noaa_full.csv"
    output_file = "/Users/dru/ISProject/data/processed/noaa_clean.csv"
    
    try:
        # Load the raw data
        df = load_noaa(input_file, chunksize=50000)
        
        # Clean it
        df_clean = clean_noaa(df)
        
        # Aggregate to annual level
        df_agg = aggregate_noaa(df_clean)
        
        # Save results
        save_output(df_agg, output_file)
        
        logger.info("NOAA cleaning done!")
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise


if __name__ == "__main__":
    main()
