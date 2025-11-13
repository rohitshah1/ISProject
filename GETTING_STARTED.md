# Getting Started

Quick guide for Weeks 4-5: Data cleaning and processing.

## Installation

1. Install dependencies:

```bash
cd /Users/dru/ISProject
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configure API Keys

You need API keys from:
- NOAA: https://www.ncdc.noaa.gov/cdo-web/token
- USDA: https://quickstats.nass.usda.gov/api

Once you have them:

```bash
python setup_api_keys.py
```

Or manually edit `config.py` with your keys.

## Run the Pipeline

### Option 1: Automated (recommended)

```bash
./workflow/run_all.sh
```

This runs the data acquisition and cleaning scripts.

### Option 2: Step by step

```bash
# Download data (if needed)
python scripts/get_noaa_data.py
python scripts/get_usda_data.py

# Clean data (Weeks 4-5)
python scripts/clean_noaa.py
python scripts/clean_usda.py
```

## Expected Output

After running the pipeline, you will have:

- `data/processed/noaa_clean.csv` - County-year aggregated weather
- `data/processed/usda_clean.csv` - Cleaned crop yields

These files contain:
- County-level data with 5-digit FIPS codes
- Annual observations
- Corn and soybean yields (bushels per acre)
- Weather metrics (temperature, precipitation)
- Temperature volatility (standard deviation)

## Troubleshooting

**API key errors:** Run `python config.py` to verify configuration

**Missing files:** Check that data files are in `data/raw/`

**Download takes long:** NOAA has lots of data, 10-30 minutes is normal

## Documentation

- Project overview: `README.md`
- Scripts details: `scripts/README.md`
- API setup help: `docs/API_SETUP_GUIDE.md`
- Quick start guide: `docs/QUICKSTART.md`
- Variable definitions: `data/metadata/data_dictionary.md`

