

import requests
import pandas as pd
import time
import logging
from pathlib import Path


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class USDADataDownloader:
    
    
    def __init__(self, api_key: str):
        
        self.api_key = api_key
        self.base_url = "http://quickstats.nass.usda.gov/api/api_GET/"
        
    def get_crop_yields(self, commodity: str, start_year: int = 1990, 
                       end_year: int = 2023, state: str = "ILLINOIS") -> pd.DataFrame:
       
        logger.info(f"Downloading {commodity} yield data for {state}, {start_year}-{end_year}")
        
        params = {
            'key': self.api_key,
            'source_desc': 'SURVEY',
            'sector_desc': 'CROPS',
            'group_desc': 'FIELD CROPS',
            'commodity_desc': commodity,
            'statisticcat_desc': 'YIELD',
            'unit_desc': 'BU / ACRE',
            'agg_level_desc': 'COUNTY',
            'state_name': state,
            'year__GE': start_year,
            'year__LE': end_year,
            'format': 'JSON'
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if 'data' in data:
                df = pd.DataFrame(data['data'])
                logger.info(f"Downloaded {len(df):,} records for {commodity}")
                return df
            else:
                logger.warning(f"No data returned for {commodity}")
                return pd.DataFrame()
        
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error downloading {commodity} data: {e}")
            if hasattr(e.response, 'text'):
                logger.error(f"Response: {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Error downloading {commodity} data: {e}")
            raise
    
    def download_all_crops(self, crops: list = None, start_year: int = 1990,
                          end_year: int = 2023, state: str = "ILLINOIS") -> pd.DataFrame:
       
        if crops is None:
            crops = ["CORN", "SOYBEANS"]
        
        all_data = []
        
        for crop in crops:
            logger.info(f"\nFetching {crop} data...")
            
            try:
                df = self.get_crop_yields(
                    commodity=crop,
                    start_year=start_year,
                    end_year=end_year,
                    state=state
                )
                
                if not df.empty:
                    all_data.append(df)
                    
               
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Failed to download {crop} data: {e}")
                continue
        
        if all_data:
            combined = pd.concat(all_data, ignore_index=True)
            logger.info(f"\nTotal records downloaded: {len(combined):,}")
            return combined
        else:
            logger.warning("No data downloaded for any crops")
            return pd.DataFrame()
    
    def save_data(self, df: pd.DataFrame, output_path: str) -> None:
       
        if df.empty:
            logger.error("No data to save")
            return
        
       
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
      
        df.to_csv(output_path, index=False)
        logger.info(f"Data saved to {output_path}")
        logger.info(f"Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
        
     
        logger.info("\nData Summary:")
        if 'commodity_desc' in df.columns:
            logger.info("\nRecords by crop:")
            logger.info(df['commodity_desc'].value_counts())
        
        if 'year' in df.columns:
            logger.info(f"\nYear range: {df['year'].min()} to {df['year'].max()}")
        
        if 'county_name' in df.columns:
            logger.info(f"Number of counties: {df['county_name'].nunique()}")
        
        logger.info("\nFirst few rows:")
        logger.info(df.head())


def main():
   
    import sys
    sys.path.append('/Users/dru/ISProject')
    import config
    
    API_KEY = config.USDA_API_KEY
    
   
    if API_KEY == "YOUR_USDA_KEY_HERE":
        logger.error("Please set your USDA NASS API key in config.py or as environment variable")
        logger.error("Get an API key at: https://quickstats.nass.usda.gov/api")
        logger.error("\nTo set via environment variable:")
        logger.error("  export USDA_API_KEY='your_key_here'")
        return
    
    
    START_YEAR = config.DATA_START_YEAR
    END_YEAR = config.DATA_END_YEAR
    STATE = config.TARGET_STATE
    CROPS = config.TARGET_CROPS
    
   
    OUTPUT_FILE = f"{config.RAW_DATA_DIR}/usda_yields.csv"
    
    try:
        logger.info("="*60)
        logger.info("USDA NASS Crop Yield Data Download")
        logger.info("="*60)
        logger.info(f"State: {STATE}")
        logger.info(f"Crops: {', '.join(CROPS)}")
        logger.info(f"Years: {START_YEAR}-{END_YEAR}")
        logger.info("")
        
        
        downloader = USDADataDownloader(API_KEY)
        
        
        data = downloader.download_all_crops(
            crops=CROPS,
            start_year=START_YEAR,
            end_year=END_YEAR,
            state=STATE
        )
        
        
        if not data.empty:
            downloader.save_data(data, OUTPUT_FILE)
            
            logger.info("\n" + "="*60)
            logger.info("Download completed successfully!")
            logger.info("="*60)
            logger.info(f"Output file: {OUTPUT_FILE}")
            logger.info("\nNext step: Run clean_usda.py to process this data")
        else:
            logger.error("No data was downloaded")
    
    except Exception as e:
        logger.error(f"Download failed: {e}")
        raise


if __name__ == "__main__":
    main()

