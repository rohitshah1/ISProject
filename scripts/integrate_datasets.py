"""
integrate_datasets.py

Merges cleaned NOAA weather data with USDA crop yield data.
Creates the final integrated dataset for analysis.

Author: Dev Rishi Udata & Rohit Shah
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


def load_cleaned_data(noaa_path: str, usda_path: str):
    """Load the cleaned datasets."""
    logger.info("Loading cleaned datasets...")
    
    if not Path(noaa_path).exists():
        raise FileNotFoundError(f"NOAA data not found: {noaa_path}")
    if not Path(usda_path).exists():
        raise FileNotFoundError(f"USDA data not found: {usda_path}")
    
    noaa_df = pd.read_csv(noaa_path)
    usda_df = pd.read_csv(usda_path)
    
    logger.info(f"NOAA: {len(noaa_df):,} rows")
    logger.info(f"USDA: {len(usda_df):,} rows")
    
    return noaa_df, usda_df


def validate_merge_keys(noaa_df: pd.DataFrame, usda_df: pd.DataFrame):
    """Check that merge keys are compatible."""
    logger.info("Validating merge keys...")
    
    # Make sure we have the columns we need
    if 'county_fips' not in noaa_df.columns or 'year' not in noaa_df.columns:
        raise ValueError("NOAA data missing county_fips or year")
    if 'county_fips' not in usda_df.columns or 'year' not in usda_df.columns:
        raise ValueError("USDA data missing county_fips or year")
    
    # Standardize formats
    noaa_df['county_fips'] = noaa_df['county_fips'].astype(str).str.zfill(5)
    usda_df['county_fips'] = usda_df['county_fips'].astype(str).str.zfill(5)
    
    noaa_df['year'] = noaa_df['year'].astype(int)
    usda_df['year'] = usda_df['year'].astype(int)
    
    # Check overlap
    noaa_years = set(noaa_df['year'].unique())
    usda_years = set(usda_df['year'].unique())
    overlap_years = noaa_years.intersection(usda_years)
    
    noaa_counties = set(noaa_df['county_fips'].unique())
    usda_counties = set(usda_df['county_fips'].unique())
    overlap_counties = noaa_counties.intersection(usda_counties)
    
    logger.info(f"Year overlap: {min(overlap_years)} to {max(overlap_years)} ({len(overlap_years)} years)")
    logger.info(f"County overlap: {len(overlap_counties)} counties")
    
    if len(overlap_years) == 0:
        logger.warning("No overlapping years!")
    if len(overlap_counties) == 0:
        logger.warning("No overlapping counties!")


def merge_datasets(noaa_df: pd.DataFrame, usda_df: pd.DataFrame):
    """Merge weather and yield data."""
    logger.info("Merging datasets...")
    
    # Inner join on county and year
    merged = pd.merge(
        usda_df,
        noaa_df,
        on=['county_fips', 'year'],
        how='inner',
        indicator=True
    )
    
    # Log merge stats
    merge_counts = merged['_merge'].value_counts()
    logger.info(f"Matched records: {merge_counts.get('both', 0):,}")
    
    # Keep only matched records
    merged = merged[merged['_merge'] == 'both'].drop('_merge', axis=1)
    
    logger.info(f"Integrated dataset: {len(merged):,} rows")
    
    return merged


def prepare_analysis_dataset(df: pd.DataFrame):
    """Prepare final dataset for analysis."""
    logger.info("Preparing analysis dataset...")
    
    # Select columns we need
    core_cols = ['county_fips', 'year', 'commodity', 'yield']
    climate_cols = ['mean_temp', 'temp_sd', 'annual_prcp']
    
    # Add optional columns if they exist
    optional_cols = []
    if 'county_name' in df.columns:
        optional_cols.append('county_name')
    if 'mean_tmax' in df.columns:
        climate_cols.append('mean_tmax')
    if 'mean_tmin' in df.columns:
        climate_cols.append('mean_tmin')
    
    # Build final column list
    final_cols = [core_cols[0]] + optional_cols + core_cols[1:] + climate_cols
    final_cols = [col for col in final_cols if col in df.columns]
    
    df = df[final_cols].copy()
    
    # Check for missing values
    missing = df.isnull().sum()
    if missing.sum() > 0:
        logger.warning("Missing values detected:")
        for col in missing[missing > 0].index:
            logger.warning(f"  {col}: {missing[col]:,} ({missing[col]/len(df)*100:.1f}%)")
        
        # Drop rows with missing critical values
        before = len(df)
        df = df.dropna(subset=['yield', 'mean_temp', 'temp_sd'])
        logger.info(f"Dropped {before - len(df):,} rows with missing data")
    
    # Sort by county and year
    df = df.sort_values(['county_fips', 'year', 'commodity'])
    
    logger.info(f"Final dataset: {df.shape[0]:,} rows x {df.shape[1]} columns")
    
    return df


def generate_summary_stats(df: pd.DataFrame):
    """Generate summary statistics."""
    logger.info("\n" + "="*60)
    logger.info("INTEGRATED DATASET SUMMARY")
    logger.info("="*60)
    
    logger.info(f"\nTotal observations: {len(df):,}")
    logger.info(f"Years: {df['year'].min()} to {df['year'].max()}")
    logger.info(f"Counties: {df['county_fips'].nunique()}")
    
    # By commodity
    if 'commodity' in df.columns:
        logger.info("\nBy Commodity:")
        for commodity in df['commodity'].unique():
            subset = df[df['commodity'] == commodity]
            logger.info(f"\n  {commodity}:")
            logger.info(f"    Observations: {len(subset):,}")
            logger.info(f"    Mean yield: {subset['yield'].mean():.1f} bu/acre")
            logger.info(f"    Yield std: {subset['yield'].std():.1f}")
            
            if 'mean_temp' in df.columns:
                logger.info(f"    Mean temp: {subset['mean_temp'].mean():.1f}°C")
            if 'temp_sd' in df.columns:
                logger.info(f"    Mean volatility: {subset['temp_sd'].mean():.1f}°C")
    
    # Correlations
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if 'yield' in numeric_cols and len(numeric_cols) > 2:
        logger.info("\nCorrelations with Yield:")
        correlations = df[numeric_cols].corr()['yield'].sort_values(ascending=False)
        for col, corr in correlations.items():
            if col != 'yield' and abs(corr) > 0.01:
                logger.info(f"  {col}: {corr:.3f}")


def save_integrated_data(df: pd.DataFrame, output_path: str):
    """Save the integrated dataset."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    df.to_csv(output_path, index=False)
    logger.info(f"\nSaved to: {output_path}")


def main():
    """Run integration pipeline."""
    noaa_path = "/Users/dru/ISProject/data/processed/noaa_clean.csv"
    usda_path = "/Users/dru/ISProject/data/processed/usda_clean.csv"
    output_path = "/Users/dru/ISProject/data/processed/integrated.csv"
    
    try:
        # Load data
        noaa_df, usda_df = load_cleaned_data(noaa_path, usda_path)
        
        # Validate
        validate_merge_keys(noaa_df, usda_df)
        
        # Merge
        merged = merge_datasets(noaa_df, usda_df)
        
        # Prepare
        final_df = prepare_analysis_dataset(merged)
        
        # Stats
        generate_summary_stats(final_df)
        
        # Save
        save_integrated_data(final_df, output_path)
        
        logger.info("\n" + "="*60)
        logger.info("Integration complete!")
        logger.info("="*60)
        
    except Exception as e:
        logger.error(f"Integration failed: {e}")
        raise


if __name__ == "__main__":
    main()

