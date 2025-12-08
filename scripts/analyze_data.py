"""
analyze_data.py

Performs statistical analysis on the integrated dataset.
Runs regression models to analyze temperature volatility impacts on crop yields.

Author: Rohit Shah
Project: Climate Variability and Agricultural Productivity in Illinois
Course: IS477
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats
import logging
from pathlib import Path
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_data(filepath: str):
    """Load the integrated dataset."""
    logger.info(f"Loading data from {filepath}")
    
    if not Path(filepath).exists():
        raise FileNotFoundError(f"Data file not found: {filepath}")
    
    df = pd.read_csv(filepath)
    logger.info(f"Loaded {len(df):,} observations")
    
    return df


def exploratory_analysis(df: pd.DataFrame):
    """Run basic exploratory analysis."""
    logger.info("\n" + "="*60)
    logger.info("EXPLORATORY ANALYSIS")
    logger.info("="*60)
    
    # Descriptive stats
    logger.info("\nDescriptive Statistics:")
    logger.info(df[['yield', 'mean_temp', 'temp_sd', 'annual_prcp']].describe())
    
    # By crop
    logger.info("\nBy Crop Type:")
    for crop in df['commodity'].unique():
        subset = df[df['commodity'] == crop]
        logger.info(f"\n{crop}:")
        logger.info(f"  N: {len(subset)}")
        logger.info(f"  Yield mean: {subset['yield'].mean():.2f}")
        logger.info(f"  Yield std: {subset['yield'].std():.2f}")
        logger.info(f"  Temp volatility mean: {subset['temp_sd'].mean():.2f}")


def run_regression_analysis(df: pd.DataFrame):
    """Run regression models."""
    logger.info("\n" + "="*60)
    logger.info("REGRESSION ANALYSIS")
    logger.info("="*60)
    
    results = {}
    
    # Model 1: Simple regression - yield on temperature volatility
    logger.info("\nModel 1: Yield ~ Temperature Volatility")
    model1 = smf.ols('yield ~ temp_sd', data=df).fit()
    logger.info(model1.summary())
    results['model1'] = {
        'formula': 'yield ~ temp_sd',
        'r_squared': model1.rsquared,
        'adj_r_squared': model1.rsquared_adj,
        'coef_temp_sd': model1.params.get('temp_sd', None),
        'pval_temp_sd': model1.pvalues.get('temp_sd', None)
    }
    
    # Model 2: Multiple regression
    logger.info("\n\nModel 2: Yield ~ Temperature + Volatility + Precipitation")
    model2 = smf.ols('yield ~ mean_temp + temp_sd + annual_prcp', data=df).fit()
    logger.info(model2.summary())
    results['model2'] = {
        'formula': 'yield ~ mean_temp + temp_sd + annual_prcp',
        'r_squared': model2.rsquared,
        'adj_r_squared': model2.rsquared_adj,
        'coef_temp_sd': model2.params.get('temp_sd', None),
        'pval_temp_sd': model2.pvalues.get('temp_sd', None)
    }
    
    # Model 3: Separate by crop
    logger.info("\n\nModel 3: By Crop Type")
    for crop in df['commodity'].unique():
        logger.info(f"\n{crop}:")
        crop_df = df[df['commodity'] == crop]
        model_crop = smf.ols('yield ~ mean_temp + temp_sd + annual_prcp', 
                             data=crop_df).fit()
        logger.info(model_crop.summary())
        
        results[f'model3_{crop.lower()}'] = {
            'formula': f'yield ~ mean_temp + temp_sd + annual_prcp (for {crop})',
            'r_squared': model_crop.rsquared,
            'adj_r_squared': model_crop.rsquared_adj,
            'coef_temp_sd': model_crop.params.get('temp_sd', None),
            'pval_temp_sd': model_crop.pvalues.get('temp_sd', None),
            'n': len(crop_df)
        }
    
    return results


def test_volatility_thresholds(df: pd.DataFrame):
    """Test for threshold effects in temperature volatility."""
    logger.info("\n" + "="*60)
    logger.info("THRESHOLD ANALYSIS")
    logger.info("="*60)
    
    # Create volatility quartiles
    df['volatility_quartile'] = pd.qcut(df['temp_sd'], q=4, labels=['Q1', 'Q2', 'Q3', 'Q4'])
    
    logger.info("\nMean Yield by Volatility Quartile:")
    quartile_means = df.groupby('volatility_quartile')['yield'].agg(['mean', 'std', 'count'])
    logger.info(quartile_means)
    
    # ANOVA test
    groups = [df[df['volatility_quartile'] == q]['yield'].values 
              for q in ['Q1', 'Q2', 'Q3', 'Q4']]
    f_stat, p_value = stats.f_oneway(*groups)
    
    logger.info(f"\nANOVA Test:")
    logger.info(f"  F-statistic: {f_stat:.4f}")
    logger.info(f"  P-value: {p_value:.4f}")
    
    if p_value < 0.05:
        logger.info("  Result: Significant differences across volatility quartiles")
    else:
        logger.info("  Result: No significant differences")


def analyze_temporal_trends(df: pd.DataFrame):
    """Analyze trends over time."""
    logger.info("\n" + "="*60)
    logger.info("TEMPORAL TRENDS")
    logger.info("="*60)
    
    # Yield trends by crop
    logger.info("\nYield Trends:")
    for crop in df['commodity'].unique():
        crop_df = df[df['commodity'] == crop]
        yearly_avg = crop_df.groupby('year')['yield'].mean()
        
        # Simple linear trend
        X = yearly_avg.index.values.reshape(-1, 1)
        y = yearly_avg.values
        from sklearn.linear_model import LinearRegression
        model = LinearRegression().fit(X, y)
        
        logger.info(f"\n{crop}:")
        logger.info(f"  Slope: {model.coef_[0]:.3f} bu/acre per year")
        logger.info(f"  Intercept: {model.intercept_:.2f}")
    
    # Temperature volatility trends
    logger.info("\nTemperature Volatility Trends:")
    yearly_volatility = df.groupby('year')['temp_sd'].mean()
    X = yearly_volatility.index.values.reshape(-1, 1)
    y = yearly_volatility.values
    from sklearn.linear_model import LinearRegression
    model = LinearRegression().fit(X, y)
    
    logger.info(f"  Slope: {model.coef_[0]:.4f}°C per year")
    logger.info(f"  Intercept: {model.intercept_:.2f}")


def save_results(results: dict, output_path: str):
    """Save analysis results."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Convert numpy types to native Python types
    def convert_types(obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {key: convert_types(value) for key, value in obj.items()}
        return obj
    
    results_clean = convert_types(results)
    
    with open(output_path, 'w') as f:
        json.dump(results_clean, f, indent=2)
    
    logger.info(f"\nResults saved to: {output_path}")


def main():
    """Run analysis pipeline."""
    input_file = "/Users/dru/ISProject/data/processed/integrated.csv"
    output_file = "/Users/dru/ISProject/results/analysis_results.json"
    
    try:
        # Load data
        df = load_data(input_file)
        
        # Exploratory analysis
        exploratory_analysis(df)
        
        # Regression analysis
        results = run_regression_analysis(df)
        
        # Threshold analysis
        test_volatility_thresholds(df)
        
        # Temporal trends
        analyze_temporal_trends(df)
        
        # Save results
        save_results(results, output_file)
        
        logger.info("\n" + "="*60)
        logger.info("Analysis complete!")
        logger.info("="*60)
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise


if __name__ == "__main__":
    main()

