

import os


NOAA_API_TOKEN = os.getenv('NOAA_API_TOKEN', 'YOUR_NOAA_TOKEN_HERE')


USDA_API_KEY = os.getenv('USDA_API_KEY', 'YOUR_USDA_KEY_HERE')


DATA_START_YEAR = 1990
DATA_END_YEAR = 2023
TARGET_STATE = "ILLINOIS"
TARGET_CROPS = ["CORN", "SOYBEANS"]


PROJECT_ROOT = "/Users/dru/ISProject"
RAW_DATA_DIR = f"{PROJECT_ROOT}/data/raw"
PROCESSED_DATA_DIR = f"{PROJECT_ROOT}/data/processed"


REQUEST_DELAY = 1  # seconds between API requests
MAX_RETRIES = 3


def validate_api_keys():
   
    noaa_valid = NOAA_API_TOKEN != 'YOUR_NOAA_TOKEN_HERE'
    usda_valid = USDA_API_KEY != 'YOUR_USDA_KEY_HERE'
    
    return noaa_valid, usda_valid


def print_config_status():
  
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

