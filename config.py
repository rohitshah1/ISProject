"""
config.py

Configuration file for API keys and project settings.
Store your API keys here and import into data acquisition scripts.

IMPORTANT: This file should NOT be committed to Git if it contains real API keys.
Add config.py to .gitignore if using real keys.

For this project, you can either:
1. Edit this file directly with your keys
2. Use environment variables (more secure)
"""

import os

# NOAA Climate Data Online API Token
# Get your token at: https://www.ncdc.noaa.gov/cdo-web/token
NOAA_API_TOKEN = os.getenv('NOAA_API_TOKEN', 'YOUR_NOAA_TOKEN_HERE')

# USDA NASS QuickStats API Key
# Get your key at: https://quickstats.nass.usda.gov/api
USDA_API_KEY = os.getenv('USDA_API_KEY', 'YOUR_USDA_KEY_HERE')

# Data acquisition parameters
DATA_START_YEAR = 1990
DATA_END_YEAR = 2023
TARGET_STATE = "ILLINOIS"
TARGET_CROPS = ["CORN", "SOYBEANS"]

# File paths
PROJECT_ROOT = "/Users/dru/ISProject"
RAW_DATA_DIR = f"{PROJECT_ROOT}/data/raw"
PROCESSED_DATA_DIR = f"{PROJECT_ROOT}/data/processed"

# API settings
REQUEST_DELAY = 1  # seconds between API requests
MAX_RETRIES = 3


def validate_api_keys():
    """
    Check if API keys are configured.
    
    Returns:
        tuple: (noaa_valid, usda_valid)
    """
    noaa_valid = NOAA_API_TOKEN != 'YOUR_NOAA_TOKEN_HERE'
    usda_valid = USDA_API_KEY != 'YOUR_USDA_KEY_HERE'
    
    return noaa_valid, usda_valid


def print_config_status():
    """
    Print configuration status for debugging.
    """
    noaa_valid, usda_valid = validate_api_keys()
    
    print("="*60)
    print("Configuration Status")
    print("="*60)
    print(f"NOAA API Token: {'Set' if noaa_valid else 'Not set'}")
    print(f"USDA API Key:   {'Set' if usda_valid else 'Not set'}")
    print(f"Data years:     {DATA_START_YEAR} - {DATA_END_YEAR}")
    print(f"Target state:   {TARGET_STATE}")
    print(f"Target crops:   {', '.join(TARGET_CROPS)}")
    print("="*60)
    
    if not noaa_valid:
        print("\nNOAA API token not set!")
        print("Get one at: https://www.ncdc.noaa.gov/cdo-web/token")
    
    if not usda_valid:
        print("\nUSDA API key not set!")
        print("Get one at: https://quickstats.nass.usda.gov/api")
    
    print()


if __name__ == "__main__":
    print_config_status()

