# Scripts Documentation

This directory contains Python scripts for data acquisition and cleaning (Weeks 2-5).

## Overview

The current pipeline consists of four scripts:

1. `get_noaa_data.py` - Downloads NOAA weather data via API (Weeks 2-3)
2. `get_usda_data.py` - Downloads USDA crop yield data via API (Weeks 2-3)
3. `clean_noaa.py` - Cleans and aggregates weather data (Weeks 4-5)
4. `clean_usda.py` - Cleans and standardizes crop yield data (Weeks 4-5)

## Prerequisites

Install required packages:

```bash
pip install -r ../requirements.txt
```

Main dependencies:
- pandas - Data manipulation
- numpy - Numerical operations
- requests - API calls
- logging - Progress tracking

## Data Acquisition Scripts

### get_noaa_data.py

Downloads daily weather observations from NOAA Climate Data Online API.

**Configuration:**
- Reads API token from `config.py`
- Date range: 1990-2023 (configurable)
- Target: Illinois weather stations

**Output:** `data/raw/noaa_full.csv`

**Usage:**
```bash
python get_noaa_data.py
```

**Note:** Download may take 10-30 minutes due to large dataset size.

### get_usda_data.py

Downloads county-level crop yields from USDA NASS QuickStats API.

**Configuration:**
- Reads API key from `config.py`
- Commodities: CORN and SOYBEANS
- Geographic level: County
- State: Illinois

**Output:** `data/raw/usda_yields.csv`

**Usage:**
```bash
python get_usda_data.py
```

**Note:** Usually completes in 1-2 minutes.

## Data Cleaning Scripts

### clean_noaa.py

Processes raw NOAA weather data and aggregates to county-year level.

**Input:** `data/raw/noaa_full.csv`
**Output:** `data/processed/noaa_clean.csv`

**Processing steps:**
- Loads data in chunks for memory efficiency
- Converts temperatures from tenths of degrees Celsius to actual degrees
- Converts precipitation from tenths of mm to mm
- Handles missing values
- Aggregates daily observations to annual county-level
- Computes temperature volatility (standard deviation)

**Output columns:**
- county_fips - 5-digit FIPS code
- year - Year
- mean_temp - Annual mean temperature (Celsius)
- temp_sd - Temperature volatility (standard deviation)
- mean_tmax - Mean maximum temperature
- mean_tmin - Mean minimum temperature
- annual_prcp - Total annual precipitation (mm)
- mean_daily_prcp - Mean daily precipitation

**Usage:**
```bash
python clean_noaa.py
```

### clean_usda.py

Cleans and standardizes USDA crop yield data.

**Input:** `data/raw/usda_yields.csv`
**Output:** `data/processed/usda_clean.csv`

**Processing steps:**
- Normalizes column names
- Filters for Illinois counties
- Filters for corn and soybeans
- Removes suppressed data marked as "(D)"
- Standardizes FIPS codes to 5 digits
- Removes unrealistic outliers

**Output columns:**
- year - Year
- county_fips - 5-digit FIPS code
- county_name - County name
- commodity - CORN or SOYBEANS
- yield - Yield in bushels per acre

**Usage:**
```bash
python clean_usda.py
```

## Running the Pipeline

### Individual Scripts

Run in order:
```bash
# Data acquisition (Weeks 2-3)
python get_noaa_data.py
python get_usda_data.py

# Data cleaning (Weeks 4-5)
python clean_noaa.py
python clean_usda.py
```

### Automated Workflow

Run data cleaning workflow:
```bash
cd ../workflow
./run_all.sh
```

Note: This currently runs only the cleaning scripts (weeks 4-5 work).

## Output Files

Expected file sizes after processing (Weeks 4-5):

| File | Size | Description |
|------|------|-------------|
| data/raw/noaa_full.csv | 100-500 MB | Raw weather data |
| data/raw/usda_yields.csv | 1-5 MB | Raw yield data |
| data/processed/noaa_clean.csv | 1-10 MB | Cleaned aggregated weather |
| data/processed/usda_clean.csv | <1 MB | Cleaned yields |

## Logging

All scripts log progress to console. Typical log output includes:
- Number of rows processed
- Data quality warnings
- Summary statistics
- Execution time

To save logs to file:
```bash
python clean_noaa.py 2>&1 | tee logs/noaa.log
```

## Troubleshooting

**FileNotFoundError**
- Check that raw data files exist in data/raw/
- Run download scripts first

**MemoryError**
- Reduce chunksize parameter in clean_noaa.py
- Default is 50,000 rows, try 25,000

**No overlapping data**
- Verify FIPS codes are standardized
- Check year ranges overlap
- Review data quality logs

**API errors**
- Verify API keys in config.py
- Check internet connection
- Confirm API services are online

## Customization

You can modify the scripts to:
- Change date ranges (edit config.py)
- Add more climate variables (edit clean_noaa.py)
- Include additional crops (edit get_usda_data.py)
- Change aggregation methods (edit clean_noaa.py)
- Modify merge logic (edit integrate_datasets.py)

## Notes

- clean_noaa.py uses chunked processing for large files
- All scripts have extensive error handling
- Data quality checks are performed at each step
- Missing data is handled appropriately for each variable

## Authors

Dev Rishi Udata - NOAA data pipeline  
Rohit Shah - USDA data pipeline

