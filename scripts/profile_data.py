"""
profile_data.py

Profiles and assesses data quality for all datasets in the pipeline.
Generates quality reports and identifies potential issues.

Author: Rohit Shah
Project: Climate Variability and Agricultural Productivity in Illinois
Course: IS477
"""

import pandas as pd
import numpy as np
import logging
from pathlib import Path
import json
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def profile_dataset(filepath: str, dataset_name: str):
    """Generate comprehensive data profile."""
    logger.info(f"\nProfiling {dataset_name}...")
    logger.info("="*60)
    
    if not Path(filepath).exists():
        logger.warning(f"File not found: {filepath}")
        return None
    
    df = pd.read_csv(filepath)
    
    profile = {
        'dataset_name': dataset_name,
        'filepath': filepath,
        'profiled_at': datetime.now().isoformat(),
        'basic_info': {
            'rows': len(df),
            'columns': len(df.columns),
            'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2
        },
        'columns': {}
    }
    
    logger.info(f"Rows: {len(df):,}")
    logger.info(f"Columns: {len(df.columns)}")
    logger.info(f"Memory: {profile['basic_info']['memory_usage_mb']:.2f} MB")
    
    # Profile each column
    for col in df.columns:
        col_profile = {
            'dtype': str(df[col].dtype),
            'missing_count': int(df[col].isnull().sum()),
            'missing_percent': float(df[col].isnull().sum() / len(df) * 100),
            'unique_count': int(df[col].nunique())
        }
        
        if df[col].dtype in ['int64', 'float64']:
            col_profile['stats'] = {
                'mean': float(df[col].mean()),
                'std': float(df[col].std()),
                'min': float(df[col].min()),
                'max': float(df[col].max()),
                'q25': float(df[col].quantile(0.25)),
                'median': float(df[col].median()),
                'q75': float(df[col].quantile(0.75))
            }
            
            # Check for outliers (IQR method)
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = ((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))).sum()
            col_profile['outlier_count'] = int(outliers)
            col_profile['outlier_percent'] = float(outliers / len(df) * 100)
        
        profile['columns'][col] = col_profile
        
        # Log important findings
        if col_profile['missing_percent'] > 5:
            logger.warning(f"  {col}: {col_profile['missing_percent']:.1f}% missing")
        if col_profile.get('outlier_percent', 0) > 5:
            logger.warning(f"  {col}: {col_profile['outlier_percent']:.1f}% outliers")
    
    return profile


def assess_data_quality(df: pd.DataFrame, dataset_name: str):
    """Assess overall data quality."""
    logger.info(f"\nQuality Assessment: {dataset_name}")
    logger.info("-"*60)
    
    quality_score = 100
    issues = []
    
    # Check missing data
    missing_pct = df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100
    if missing_pct > 10:
        quality_score -= 20
        issues.append(f"High missing data: {missing_pct:.1f}%")
    elif missing_pct > 5:
        quality_score -= 10
        issues.append(f"Moderate missing data: {missing_pct:.1f}%")
    
    # Check for duplicate rows
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        dup_pct = duplicates / len(df) * 100
        quality_score -= min(20, int(dup_pct * 2))
        issues.append(f"Duplicate rows: {duplicates} ({dup_pct:.1f}%)")
    
    # Check for constant columns
    constant_cols = [col for col in df.columns if df[col].nunique() == 1]
    if constant_cols:
        quality_score -= 5 * len(constant_cols)
        issues.append(f"Constant columns: {', '.join(constant_cols)}")
    
    logger.info(f"Quality Score: {max(0, quality_score)}/100")
    if issues:
        logger.info("Issues Found:")
        for issue in issues:
            logger.info(f"  - {issue}")
    else:
        logger.info("No major quality issues detected")
    
    return {'score': max(0, quality_score), 'issues': issues}


def compare_datasets():
    """Compare data before and after cleaning."""
    logger.info("\n" + "="*60)
    logger.info("DATASET COMPARISON")
    logger.info("="*60)
    
    # Compare NOAA
    raw_noaa = "/Users/dru/ISProject/data/raw/noaa_full.csv"
    clean_noaa = "/Users/dru/ISProject/data/processed/noaa_clean.csv"
    
    if Path(raw_noaa).exists() and Path(clean_noaa).exists():
        logger.info("\nNOAA Dataset:")
        raw_df = pd.read_csv(raw_noaa)
        clean_df = pd.read_csv(clean_noaa)
        
        logger.info(f"  Raw: {len(raw_df):,} rows")
        logger.info(f"  Cleaned: {len(clean_df):,} rows")
        logger.info(f"  Reduction: {(1 - len(clean_df)/len(raw_df)) * 100:.1f}%")
        logger.info(f"  Aggregation: {len(raw_df) / len(clean_df):.1f}:1")
    
    # Compare USDA
    raw_usda = "/Users/dru/ISProject/data/raw/usda_yields.csv"
    clean_usda = "/Users/dru/ISProject/data/processed/usda_clean.csv"
    
    if Path(raw_usda).exists() and Path(clean_usda).exists():
        logger.info("\nUSDA Dataset:")
        raw_df = pd.read_csv(raw_usda)
        clean_df = pd.read_csv(clean_usda)
        
        logger.info(f"  Raw: {len(raw_df):,} rows")
        logger.info(f"  Cleaned: {len(clean_df):,} rows")
        logger.info(f"  Retention: {(len(clean_df)/len(raw_df)) * 100:.1f}%")


def main():
    """Run data profiling pipeline."""
    output_file = "/Users/dru/ISProject/results/data_profile.json"
    
    try:
        profiles = {}
        
        # Profile all datasets
        datasets = [
            ("/Users/dru/ISProject/data/raw/noaa_full.csv", "NOAA Raw"),
            ("/Users/dru/ISProject/data/raw/usda_yields.csv", "USDA Raw"),
            ("/Users/dru/ISProject/data/processed/noaa_clean.csv", "NOAA Cleaned"),
            ("/Users/dru/ISProject/data/processed/usda_clean.csv", "USDA Cleaned"),
            ("/Users/dru/ISProject/data/processed/integrated.csv", "Integrated")
        ]
        
        for filepath, name in datasets:
            profile = profile_dataset(filepath, name)
            if profile:
                profiles[name] = profile
                
                # Quality assessment
                df = pd.read_csv(filepath)
                quality = assess_data_quality(df, name)
                profiles[name]['quality'] = quality
        
        # Compare datasets
        compare_datasets()
        
        # Save profiles
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(profiles, f, indent=2)
        
        logger.info(f"\nData profiles saved to: {output_file}")
        logger.info("\n" + "="*60)
        logger.info("Data profiling complete!")
        logger.info("="*60)
        
    except Exception as e:
        logger.error(f"Profiling failed: {e}")
        raise


if __name__ == "__main__":
    main()

