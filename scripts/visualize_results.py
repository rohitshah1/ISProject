"""
visualize_results.py

Creates visualizations for the climate and agriculture analysis.
Generates plots showing relationships between temperature volatility and yields.

Author: Dev Rishi Udata
Project: Climate Variability and Agricultural Productivity in Illinois
Course: IS477
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)


def load_data(filepath: str):
    """Load integrated dataset."""
    logger.info(f"Loading data from {filepath}")
    
    if not Path(filepath).exists():
        raise FileNotFoundError(f"Data file not found: {filepath}")
    
    df = pd.read_csv(filepath)
    logger.info(f"Loaded {len(df):,} observations")
    
    return df


def plot_yield_vs_volatility(df: pd.DataFrame, output_dir: str):
    """Scatter plot of yield vs temperature volatility."""
    logger.info("Creating yield vs volatility plot...")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    for idx, crop in enumerate(df['commodity'].unique()):
        crop_df = df[df['commodity'] == crop]
        
        axes[idx].scatter(crop_df['temp_sd'], crop_df['yield'], alpha=0.3)
        
        # Add trend line
        z = np.polyfit(crop_df['temp_sd'], crop_df['yield'], 1)
        p = np.poly1d(z)
        x_line = np.linspace(crop_df['temp_sd'].min(), crop_df['temp_sd'].max(), 100)
        axes[idx].plot(x_line, p(x_line), "r--", linewidth=2)
        
        axes[idx].set_xlabel('Temperature Volatility (°C SD)')
        axes[idx].set_ylabel('Yield (bu/acre)')
        axes[idx].set_title(f'{crop}')
        axes[idx].grid(True, alpha=0.3)
    
    plt.tight_layout()
    output_path = Path(output_dir) / 'yield_vs_volatility.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    logger.info(f"Saved: {output_path}")


def plot_temporal_trends(df: pd.DataFrame, output_dir: str):
    """Plot yield and volatility trends over time."""
    logger.info("Creating temporal trends plot...")
    
    fig, axes = plt.subplots(2, 1, figsize=(12, 10))
    
    # Yield trends by crop
    for crop in df['commodity'].unique():
        crop_df = df[df['commodity'] == crop]
        yearly_avg = crop_df.groupby('year')['yield'].mean()
        axes[0].plot(yearly_avg.index, yearly_avg.values, marker='o', label=crop)
    
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Mean Yield (bu/acre)')
    axes[0].set_title('Crop Yield Trends Over Time')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Temperature volatility trend
    yearly_volatility = df.groupby('year')['temp_sd'].mean()
    axes[1].plot(yearly_volatility.index, yearly_volatility.values, 
                 marker='o', color='red', linewidth=2)
    axes[1].set_xlabel('Year')
    axes[1].set_ylabel('Mean Temperature Volatility (°C SD)')
    axes[1].set_title('Temperature Volatility Trend Over Time')
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    output_path = Path(output_dir) / 'temporal_trends.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    logger.info(f"Saved: {output_path}")


def plot_volatility_distributions(df: pd.DataFrame, output_dir: str):
    """Plot distributions of temperature volatility by crop."""
    logger.info("Creating volatility distribution plot...")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    for crop in df['commodity'].unique():
        crop_df = df[df['commodity'] == crop]
        ax.hist(crop_df['temp_sd'], bins=30, alpha=0.5, label=crop)
    
    ax.set_xlabel('Temperature Volatility (°C SD)')
    ax.set_ylabel('Frequency')
    ax.set_title('Distribution of Temperature Volatility')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    output_path = Path(output_dir) / 'volatility_distribution.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    logger.info(f"Saved: {output_path}")


def plot_correlation_matrix(df: pd.DataFrame, output_dir: str):
    """Create correlation matrix heatmap."""
    logger.info("Creating correlation matrix...")
    
    # Select numeric columns
    numeric_cols = ['yield', 'mean_temp', 'temp_sd', 'annual_prcp']
    if 'mean_tmax' in df.columns:
        numeric_cols.append('mean_tmax')
    if 'mean_tmin' in df.columns:
        numeric_cols.append('mean_tmin')
    
    corr_matrix = df[numeric_cols].corr()
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='coolwarm', 
                center=0, square=True, linewidths=1)
    plt.title('Correlation Matrix')
    plt.tight_layout()
    
    output_path = Path(output_dir) / 'correlation_matrix.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    logger.info(f"Saved: {output_path}")


def plot_yield_by_volatility_quartile(df: pd.DataFrame, output_dir: str):
    """Box plot of yields by volatility quartiles."""
    logger.info("Creating yield by quartile plot...")
    
    # Create quartiles
    df['volatility_quartile'] = pd.qcut(df['temp_sd'], q=4, labels=['Q1 (Low)', 'Q2', 'Q3', 'Q4 (High)'])
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    for idx, crop in enumerate(df['commodity'].unique()):
        crop_df = df[df['commodity'] == crop]
        
        crop_df.boxplot(column='yield', by='volatility_quartile', ax=axes[idx])
        axes[idx].set_xlabel('Temperature Volatility Quartile')
        axes[idx].set_ylabel('Yield (bu/acre)')
        axes[idx].set_title(f'{crop} Yield by Volatility Quartile')
        axes[idx].get_figure().suptitle('')  # Remove automatic title
    
    plt.tight_layout()
    output_path = Path(output_dir) / 'yield_by_quartile.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    logger.info(f"Saved: {output_path}")


def plot_geographic_summary(df: pd.DataFrame, output_dir: str):
    """Create summary statistics by county."""
    logger.info("Creating geographic summary plot...")
    
    # Mean yield by county
    county_means = df.groupby(['county_fips', 'commodity'])['yield'].mean().unstack()
    
    # Top 10 and bottom 10 counties for each crop
    fig, axes = plt.subplots(1, 2, figsize=(14, 8))
    
    for idx, crop in enumerate(df['commodity'].unique()):
        if crop in county_means.columns:
            top10 = county_means[crop].nlargest(10)
            
            axes[idx].barh(range(len(top10)), top10.values)
            axes[idx].set_yticks(range(len(top10)))
            axes[idx].set_yticklabels(top10.index)
            axes[idx].set_xlabel('Mean Yield (bu/acre)')
            axes[idx].set_title(f'Top 10 Counties - {crop}')
            axes[idx].grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    output_path = Path(output_dir) / 'geographic_summary.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    logger.info(f"Saved: {output_path}")


def main():
    """Generate all visualizations."""
    input_file = "/Users/dru/ISProject/data/processed/integrated.csv"
    output_dir = "/Users/dru/ISProject/results"
    
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    try:
        # Load data
        df = load_data(input_file)
        
        # Generate plots
        plot_yield_vs_volatility(df, output_dir)
        plot_temporal_trends(df, output_dir)
        plot_volatility_distributions(df, output_dir)
        plot_correlation_matrix(df, output_dir)
        plot_yield_by_volatility_quartile(df, output_dir)
        plot_geographic_summary(df, output_dir)
        
        logger.info("\n" + "="*60)
        logger.info("All visualizations created successfully!")
        logger.info(f"Saved to: {output_dir}")
        logger.info("="*60)
        
    except Exception as e:
        logger.error(f"Visualization failed: {e}")
        raise


if __name__ == "__main__":
    main()

