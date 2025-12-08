# Project Summary

## Climate Variability and Agricultural Productivity in Illinois

This repository contains a complete data analysis pipeline examining the relationship between temperature volatility and crop yields in Illinois (2018-2023).

## Repository Structure

```
ISProject/
├── scripts/                    # Python analysis scripts (9 total)
│   ├── get_noaa_data.py       # NOAA weather data acquisition
│   ├── get_usda_data.py       # USDA crop yield acquisition
│   ├── clean_noaa.py          # Weather data cleaning
│   ├── clean_usda.py          # Crop yield data cleaning
│   ├── integrate_datasets.py  # Dataset merging
│   ├── profile_data.py        # Data quality assessment
│   ├── analyze_data.py        # Statistical regression analysis
│   ├── visualize_results.py   # Visualization generation
│   └── verify_data.py         # Data integrity verification
│
├── workflow/                   # Automation scripts
│   └── run_all.sh             # Complete pipeline executor
│
├── data/
│   ├── raw/                   # Downloaded source data
│   ├── processed/             # Cleaned and integrated data
│   └── metadata/              # Data dictionary and schemas
│
├── results/                    # Analysis outputs
│   ├── *.png                  # Visualizations (6 plots)
│   ├── analysis_results.json  # Regression model results
│   └── data_profile.json      # Quality assessment
│
├── docs/                       # Documentation
│   ├── API_SETUP_GUIDE.md     # API configuration guide
│   ├── QUICKSTART.md          # Quick start instructions
│   └── REPRODUCING.md         # Detailed reproduction steps
│
└── config/
    ├── Snakefile              # Snakemake workflow definition
    ├── config.yaml            # Workflow parameters
    ├── config.py              # API keys and settings
    └── requirements.txt       # Python dependencies
```

## Analysis Pipeline

The complete workflow performs these steps:

1. **Data Acquisition** - Downloads weather data from NOAA CDO API and crop yields from USDA NASS
2. **Data Cleaning** - Standardizes formats, handles missing values, aggregates to county-year level
3. **Data Integration** - Merges datasets on county and year keys
4. **Quality Profiling** - Generates data quality reports and statistics
5. **Statistical Analysis** - Runs regression models examining temperature volatility effects
6. **Visualization** - Creates 6 plots showing climate-yield relationships
7. **Verification** - Computes SHA-256 checksums for data integrity

## Key Findings

- **Corn yields** decline 6.5 bushels/acre per degree Celsius increase in temperature volatility (p<0.001, R²=0.19)
- **Soybean yields** decline 2.0 bushels/acre per degree Celsius increase in temperature volatility (p<0.001, R²=0.12)
- Temperature volatility shows negative correlation with yields even when controlling for mean temperature and precipitation
- Analysis covers 1,085 county-year observations across 103 Illinois counties

## Running the Analysis

### Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set up API keys
cp config.py.template config.py
# Edit config.py with your NOAA and USDA API keys

# Run complete pipeline
./workflow/run_all.sh
```

### Using Snakemake

```bash
snakemake --cores 1
```

## Data Sources

- **NOAA Climate Data Online**: Daily weather observations from Illinois stations (1990-2023)
- **USDA NASS QuickStats**: County-level annual crop yields for corn and soybeans (2018-2024)

Both datasets are public domain and accessed programmatically via official APIs.

## Requirements

- Python 3.8+
- pandas, numpy, statsmodels, matplotlib, seaborn
- API tokens from NOAA and USDA (free registration)
- ~500MB disk space

## Documentation

- `REPRODUCIBILITY.md` - Complete reproduction instructions
- `GETTING_STARTED.md` - Quick setup guide  
- `docs/API_SETUP_GUIDE.md` - API configuration steps
- `data/metadata/data_dictionary.md` - Variable definitions and schemas

## Licenses

- Code: MIT License
- Data: Public Domain (CC0)
- Original data: NOAA and USDA public domain works

## Citation

See `CITATION.cff` for citation metadata in Citation File Format.

## Course Context

IS477 - Data Management, Curation, and Reproducibility  
School of Information Sciences  
University of Illinois at Urbana-Champaign  
Fall 2024
