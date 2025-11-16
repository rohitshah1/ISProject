# Quick Start Guide - Weeks 4-5

This guide walks you through setting up and running the data cleaning pipeline.

## Setup

### 1. Install Dependencies

```bash
cd /Users/dru/ISProject
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure API Keys

You need two API keys:
- NOAA Climate Data Online token: https://www.ncdc.noaa.gov/cdo-web/token
- USDA NASS QuickStats key: https://quickstats.nass.usda.gov/api

Once you have them, run:

```bash
python setup_api_keys.py
```

Or manually edit `config.py` and replace the placeholder values with your actual keys.

### 3. Download Data

```bash
python scripts/get_noaa_data.py
python scripts/get_usda_data.py
```

Note: NOAA download may take 10-30 minutes depending on the date range.

## Running the Pipeline

### Automated workflow

```bash
./workflow/run_all.sh
```

This checks for raw data and runs the cleaning scripts.

### Running manually

```bash
# Clean the downloaded data
python scripts/clean_noaa.py
python scripts/clean_usda.py
```

## Output Files

After running the pipeline, you'll have these files in `data/processed/`:

- `noaa_clean.csv` - County-year aggregated weather data
- `usda_clean.csv` - Cleaned crop yield data

The cleaned datasets have these features:

**noaa_clean.csv:**
- county_fips - 5-digit county identifier
- year - Year
- mean_temp - Annual mean temperature (Celsius)
- temp_sd - Temperature volatility (standard deviation)
- annual_prcp - Total annual precipitation (mm)
- Additional temperature metrics

**usda_clean.csv:**
- year - Year
- county_fips - 5-digit county identifier
- commodity - CORN or SOYBEANS
- yield - Crop yield in bushels per acre

## Troubleshooting

**Problem: API key errors**
- Make sure you've configured your keys in `config.py` or run `setup_api_keys.py`
- Verify keys are correct (no extra spaces)

**Problem: Download takes too long**
- This is normal for NOAA data. It has millions of daily records.
- You can reduce the date range by editing `DATA_START_YEAR` in `config.py`

**Problem: "No data downloaded"**
- Check your internet connection
- Verify API keys are valid
- Make sure the API services are online

**Problem: Missing files**
- Check that raw data files exist in `data/raw/`
- Re-run the download scripts if needed

## Next Steps (Week 6+)

Once you have the cleaned datasets:

1. Examine the cleaned data
   ```bash
   head data/processed/noaa_clean.csv
   head data/processed/usda_clean.csv
   ```

2. Check summary statistics (logged during cleaning)

3. Prepare for Week 6:
   - Integrate NOAA and USDA datasets
   - Merge on county_fips and year
   - Calculate final volatility metrics
   
4. Future work (Weeks 7-8):
   - Exploratory data analysis
   - Regression modeling
   - Visualizations

## Data Quality Notes

The scripts handle several data quality issues:
- Missing temperature/precipitation values (removed or interpolated)
- Suppressed USDA data marked as "(D)" (filtered out)
- Inconsistent FIPS codes (standardized to 5 digits)
- Unrealistic yield outliers (filtered)

All data cleaning decisions are logged during script execution.

## Additional Documentation

- Full project documentation: `README.md`
- Data variable definitions: `data/metadata/data_dictionary.md`
- Script details: `scripts/README.md`
- API setup help: `docs/API_SETUP_GUIDE.md`
