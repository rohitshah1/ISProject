## Reproducibility Guide

This document provides complete instructions for reproducing the Climate Variability and Agricultural Productivity in Illinois analysis.

### Prerequisites

**Software Requirements:**
- Python 3.8 or higher
- pip (Python package manager)
- Git
- 8GB RAM minimum (16GB recommended for full dataset)

**Hardware Requirements:**
- ~2GB disk space for raw data
- ~500MB for processed data and results

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/climate-agriculture-il.git
cd climate-agriculture-il
```

### Step 2: Set Up Python Environment

We recommend using a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

Expected packages:
- pandas, numpy (data manipulation)
- matplotlib, seaborn (visualization)
- statsmodels, scikit-learn (statistical analysis)
- snakemake (workflow automation)

Verify installation:
```bash
pip freeze > installed_packages.txt
```

### Step 4: Data Acquisition

#### Option A: Download from Box (Recommended)

We have hosted all raw and processed data on Box for easy access:

**Box Link:** [INSERT YOUR BOX LINK HERE]

1. Download the `data.zip` file from Box
2. Extract it in the project root:
   ```bash
   unzip data.zip
   ```
3. Verify checksums:
   ```bash
   python scripts/verify_data.py verify
   ```

The data directory should contain:
```
data/
├── raw/
│   ├── noaa_full.csv (~200MB)
│   └── usda_yields.csv (~2MB)
└── processed/
    ├── noaa_clean.csv (~5MB)
    ├── usda_clean.csv (~500KB)
    └── integrated.csv (~8MB)
```

#### Option B: Acquire Data Programmatically

If you want to download fresh data:

1. Get API keys:
   - NOAA: https://www.ncdc.noaa.gov/cdo-web/token
   - USDA: https://quickstats.nass.usda.gov/api

2. Configure keys:
   ```bash
   python setup_api_keys.py
   ```

3. Download data:
   ```bash
   python scripts/get_noaa_data.py
   python scripts/get_usda_data.py
   ```

Note: NOAA download may take 10-30 minutes.

### Step 5: Run the Analysis

#### Option A: Complete Workflow (Recommended)

Run the entire analysis pipeline:

```bash
./workflow/run_all.sh
```

This will:
1. Verify/download raw data
2. Clean NOAA weather data
3. Clean USDA crop yield data
4. Integrate datasets
5. Profile data quality
6. Run statistical analysis
7. Generate visualizations
8. Compute checksums

Expected runtime: 15-30 minutes (depending on whether data needs downloading)

#### Option B: Using Snakemake

For more control, use Snakemake:

```bash
# Dry run to see what will be executed
snakemake --dry-run

# Run with 4 cores
snakemake --cores 4

# Generate workflow diagram
snakemake --dag | dot -Tpng > workflow_dag.png
```

#### Option C: Step-by-Step Execution

Run scripts individually:

```bash
# Data cleaning
python scripts/clean_noaa.py
python scripts/clean_usda.py

# Integration
python scripts/integrate_datasets.py

# Analysis
python scripts/profile_data.py
python scripts/analyze_data.py
python scripts/visualize_results.py

# Verification
python scripts/verify_data.py
```

### Step 6: Verify Results

Expected outputs:

**Processed Data:**
- `data/processed/noaa_clean.csv` - County-year weather aggregates
- `data/processed/usda_clean.csv` - Cleaned crop yields
- `data/processed/integrated.csv` - Final integrated dataset

**Analysis Results:**
- `results/analysis_results.json` - Regression results and statistics
- `results/data_profile.json` - Data quality assessment

**Visualizations:**
- `results/yield_vs_volatility.png` - Scatter plots of yield vs volatility
- `results/temporal_trends.png` - Time series of yields and volatility
- `results/correlation_matrix.png` - Variable correlations
- `results/yield_by_quartile.png` - Yield distributions by volatility
- `results/geographic_summary.png` - County-level summaries
- `results/volatility_distribution.png` - Temperature volatility distributions

**Verification:**
- `data/checksums.json` - SHA-256 checksums for data integrity

Compare your results with our checksums:
```bash
python scripts/verify_data.py verify
```

### Step 7: Examine Results

View analysis results:
```bash
# Summary statistics
cat results/analysis_results.json | python -m json.tool

# Data quality report
cat results/data_profile.json | python -m json.tool

# View visualizations
open results/*.png  # macOS
xdg-open results/*.png  # Linux
start results/*.png  # Windows
```

### Expected Key Findings

If you've reproduced the analysis correctly, you should see:

1. **Temperature Volatility Effect:**
   - Negative correlation between temp_sd and yield
   - Coefficient approximately -2 to -5 bu/acre per °C SD
   - Statistically significant (p < 0.05)

2. **Crop Differences:**
   - Corn shows stronger volatility sensitivity than soybeans
   - Different optimal temperature ranges

3. **Temporal Trends:**
   - Yields generally increasing over time
   - Temperature volatility shows slight increase

4. **Data Quality:**
   - ~10,000-25,000 observations in integrated dataset
   - ~100 Illinois counties represented
   - ~30 years of data (1990s-2020s)

### Troubleshooting

**Problem: Missing data files**
- Solution: Download from Box or run acquisition scripts

**Problem: Import errors**
- Solution: Verify all packages installed: `pip install -r requirements.txt`

**Problem: Memory errors**
- Solution: Close other applications, or reduce chunksize in clean_noaa.py

**Problem: Checksums don't match**
- Solution: This is expected if you downloaded fresh data. Original checksums are for our specific download date.

**Problem: Snakemake errors**
- Solution: Try run_all.sh instead, or run scripts individually

### System Information

Document your system for reproducibility:

```bash
# Python version
python --version > system_info.txt

# Installed packages
pip freeze >> system_info.txt

# System info
uname -a >> system_info.txt  # Unix/Mac
systeminfo >> system_info.txt  # Windows
```

### Computing Environment

This analysis was developed and tested on:
- macOS 14.0 (also tested on Ubuntu 22.04)
- Python 3.10.12
- 16GB RAM
- See `installed_packages.txt` for exact package versions

### Data Provenance

All data sources are documented in DATA_LICENSE:
- NOAA data: Public domain (U.S. Government)
- USDA data: Public domain (U.S. Government)
- Derived data: CC0 1.0 (Public Domain Dedication)

### Questions or Issues?

If you encounter problems reproducing this analysis:

1. Check that all prerequisites are installed
2. Verify data files match checksums (if using Box data)
3. Review log files in `logs/` directory
4. Check GitHub issues page
5. Contact authors:
   - Dev Rishi Udata: dudata2@illinois.edu
   - Rohit Shah: rohitps2@illinois.edu

### Citation

If you use this work, please cite:

```
Udata, D. R., & Shah, R. (2024). Climate Variability and Agricultural 
Productivity in Illinois. University of Illinois at Urbana-Champaign. 
IS477 Data Lifecycle Project.
```

See CITATION.cff for machine-readable citation information.

### License

- Code: MIT License (see LICENSE)
- Data: Public Domain / CC0 (see DATA_LICENSE)

---

Last Updated: November 2024

