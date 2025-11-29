

import requests
import pandas as pd
import time
import logging
from pathlib import Path
from datetime import datetime, timedelta
import json


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NOAADataDownloader:
   
    
    def __init__(self, api_token: str):
       
        self.api_token = api_token
        self.base_url = "https://www.ncdc.noaa.gov/cdo-web/api/v2"
        self.headers = {'token': api_token}
        
    def get_stations(self, location_id: str = "FIPS:17") -> pd.DataFrame:
       
        logger.info(f"Fetching stations for {location_id}...")
        
        url = f"{self.base_url}/stations"
        params = {
            'locationid': location_id,
            'datasetid': 'GHCND', 
            'limit': 1000
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            if 'results' in data:
                stations_df = pd.json_normalize(data['results'])
                logger.info(f"Found {len(stations_df)} stations")
                return stations_df
            else:
                logger.warning("No stations found")
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"Error fetching stations: {e}")
            raise
    
    def get_daily_data(self, start_date: str, end_date: str, 
                       location_id: str = "FIPS:17",
                       datatypes: list = None) -> pd.DataFrame:
        
        if datatypes is None:
            datatypes = ['TMAX', 'TMIN', 'TAVG', 'PRCP']
        
        logger.info(f"Downloading data from {start_date} to {end_date}")
        logger.info(f"Data types: {', '.join(datatypes)}")
        
        all_data = []
        
        
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        
       
        current = start
        chunk_size = timedelta(days=180)
        
        while current < end:
            chunk_end = min(current + chunk_size, end)
            
            logger.info(f"Fetching data for {current.strftime('%Y-%m-%d')} to {chunk_end.strftime('%Y-%m-%d')}")
            
            for datatype in datatypes:
                offset = 1
                has_more = True
                
                while has_more:
                    url = f"{self.base_url}/data"
                    params = {
                        'datasetid': 'GHCND',
                        'locationid': location_id,
                        'startdate': current.strftime('%Y-%m-%d'),
                        'enddate': chunk_end.strftime('%Y-%m-%d'),
                        'datatypeid': datatype,
                        'units': 'metric',
                        'limit': 1000,
                        'offset': offset
                    }
                    
                    try:
                        response = requests.get(url, headers=self.headers, params=params)
                        response.raise_for_status()
                        
                        data = response.json()
                        
                        if 'results' in data:
                            df = pd.json_normalize(data['results'])
                            all_data.append(df)
                            logger.info(f"  Retrieved {len(df)} records for {datatype} (offset {offset})")
                            
                            # Check if there are more pages
                            metadata = data.get('metadata', {})
                            resultset = metadata.get('resultset', {})
                            offset_val = resultset.get('offset', 0)
                            count = resultset.get('count', 0)
                            limit = resultset.get('limit', 1000)
                            
                            if offset_val + limit >= count:
                                has_more = False
                            else:
                                offset += 1000
                        else:
                            has_more = False
                        
                        # Respect API rate limits
                        time.sleep(0.2)
                        
                    except requests.exceptions.HTTPError as e:
                        if e.response.status_code == 429:
                            logger.warning("Rate limit hit, waiting 60 seconds...")
                            time.sleep(60)
                        else:
                            logger.error(f"HTTP error: {e}")
                            has_more = False
                    except Exception as e:
                        logger.error(f"Error fetching data: {e}")
                        has_more = False
            
            current = chunk_end + timedelta(days=1)
        
        if all_data:
            combined_df = pd.concat(all_data, ignore_index=True)
            logger.info(f"Total records downloaded: {len(combined_df):,}")
            return combined_df
        else:
            logger.warning("No data downloaded")
            return pd.DataFrame()
    
    def process_and_save(self, df: pd.DataFrame, output_path: str) -> None:
       
        if df.empty:
            logger.error("No data to process")
            return
        
        logger.info("Processing downloaded data...")
        
       
        processed = df.copy()
        
       
        if 'station' in processed.columns:
            processed['station'] = processed['station']
        
        # Rename columns for consistency
        column_mapping = {
            'date': 'date',
            'station': 'station',
            'datatype': 'datatype',
            'value': 'value'
        }
        
        processed = processed.rename(columns=column_mapping)
        
       
        if 'datatype' in processed.columns:
            processed_pivot = processed.pivot_table(
                index=['date', 'station'],
                columns='datatype',
                values='value',
                aggfunc='first'
            ).reset_index()
            
           
            processed_pivot.columns.name = None
            
           
            processed_pivot['county_fips'] = None
            
            processed = processed_pivot
        
       
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        
        processed.to_csv(output_path, index=False)
        logger.info(f"Data saved to {output_path}")
        logger.info(f"Shape: {processed.shape[0]:,} rows × {processed.shape[1]} columns")
        
       
        logger.info("\nFirst few rows:")
        logger.info(processed.head())


def main():
   
    import sys
    sys.path.append('/Users/dru/ISProject')
    import config
    
    API_TOKEN = config.NOAA_API_TOKEN
    
   
    if API_TOKEN == "YOUR_NOAA_TOKEN_HERE":
        logger.error("Please set your NOAA API token in config.py or as environment variable")
        logger.error("Get a token at: https://www.ncdc.noaa.gov/cdo-web/token")
        logger.error("\nTo set via environment variable:")
        logger.error("  export NOAA_API_TOKEN='your_token_here'")
        return
    
    
    START_DATE = f"{config.DATA_START_YEAR}-01-01"
    END_DATE = f"{config.DATA_END_YEAR}-12-31"
    
   
    OUTPUT_FILE = f"{config.RAW_DATA_DIR}/noaa_full.csv"
    
    try:
       
        logger.info("="*60)
        logger.info("NOAA Climate Data Download")
        logger.info("="*60)
        
        downloader = NOAADataDownloader(API_TOKEN)
        
        
        logger.info("\nStep 1: Fetching station information...")
        stations = downloader.get_stations(location_id="FIPS:17")
        if not stations.empty:
            logger.info(f"Found {len(stations)} stations in Illinois")
            
            stations.to_csv(OUTPUT_FILE.replace('noaa_full.csv', 'noaa_stations.csv'), index=False)
        
       
        logger.info("\nStep 2: Downloading daily weather data...")
        logger.info("This may take 10-30 minutes depending on date range...")
        
        data = downloader.get_daily_data(
            start_date=START_DATE,
            end_date=END_DATE,
            location_id="FIPS:17",
            datatypes=['TMAX', 'TMIN', 'TAVG', 'PRCP']
        )
        
      
        if not data.empty:
            logger.info("\nStep 3: Processing and saving data...")
            downloader.process_and_save(data, OUTPUT_FILE)
            
            logger.info("\n" + "="*60)
            logger.info("Download completed successfully!")
            logger.info("="*60)
            logger.info(f"Output file: {OUTPUT_FILE}")
            logger.info("\nNote: You may need to map stations to county FIPS codes.")
            logger.info("The clean_noaa.py script will handle further processing.")
        else:
            logger.error("No data was downloaded")
    
    except Exception as e:
        logger.error(f"Download failed: {e}")
        raise


if __name__ == "__main__":
    main()

