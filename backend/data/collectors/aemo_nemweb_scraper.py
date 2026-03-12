#!/usr/bin/env python3
"""
AEMO NEMWeb Data Scraper for Real Electricity Price Data
"""

import requests
import zipfile
import io
import csv
import json
from datetime import datetime, timedelta
import time
import logging
import re

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AEMONEMWebScraper:
    """Scraper for AEMO NEMWeb dispatch data"""
    
    def __init__(self):
        self.base_url = "https://nemweb.com.au/Reports/Current/DispatchIS_Reports/"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def get_latest_dispatch_files(self, limit=3):
        """Get the latest dispatch file URLs by scraping the directory"""
        
        import re
        
        try:
            # Fetch the directory listing page
            response = self.session.get(self.base_url, timeout=30)
            response.raise_for_status()
            
            # Extract file links - pattern: PUBLIC_DISPATCHIS_YYYYMMDDHHMM_*.zip
            pattern = r'(PUBLIC_DISPATCHIS_\d{12}_\d+\.zip)'
            matches = re.findall(pattern, response.text)
            
            if matches:
                # Get unique filenames and sort by timestamp (newest first)
                unique_files = list(set(matches))
                unique_files.sort(reverse=True)
                
                # Return full URLs for the latest files
                file_urls = [self.base_url + f for f in unique_files[:limit]]
                logger.info(f"Found {len(unique_files)} dispatch files, using latest: {unique_files[:limit]}")
                return file_urls
            
            logger.warning("No dispatch files found in directory listing")
            return []
            
        except Exception as e:
            logger.error(f"Error fetching directory listing: {e}")
            # Fallback: try to use current time to construct likely filename
            now = datetime.now()
            filename = now.strftime('PUBLIC_DISPATCHIS_%Y%m%d%H%M_0000000.zip')
            return [self.base_url + filename]
    
    def download_and_extract_file(self, url):
        """Download and extract a NEMWeb ZIP file"""
        
        try:
            logger.info(f"Downloading: {url}")
            response = self.session.get(url, timeout=30)
            
            if response.status_code == 200:
                with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
                    csv_files = [f for f in zip_file.namelist() if f.upper().endswith('.CSV')]
                    
                    if csv_files:
                        csv_file = csv_files[0]
                        with zip_file.open(csv_file) as csv_data:
                            content = csv_data.read().decode('utf-8', errors='ignore')
                            return content
            
            return None
            
        except Exception as e:
            logger.error(f"Error downloading {url}: {e}")
            return None
    
    def extract_price_data(self, content):
        """Extract price data from dispatch content"""
        
        if not content:
            return {}
        
        price_data = {}
        csv_reader = csv.reader(io.StringIO(content))
        rows = list(csv_reader)
        
        # Look for the PRICE table
        price_rows = []
        in_price_section = False
        
        for row in rows:
            if row and len(row) > 0:
                # Check if this is the start of the PRICE table
                if (len(row) > 2 and 
                    row[1] == 'DISPATCH' and 
                    row[2] == 'PRICE' and 
                    row[0] == 'I'):  # 'I' indicates header row
                    in_price_section = True
                    continue
                
                # Check if we're in the price section and this is data
                if in_price_section and row[0] == 'D' and len(row) > 9:
                    # Extract region and price
                    region = row[6]  # REGIONID column (index 6)
                    price = row[9]   # RRP (Regional Reference Price) column (index 9)
                    
                    if region and price and region in ['NSW1', 'VIC1', 'QLD1', 'SA1', 'TAS1']:
                        try:
                            price_value = float(price)
                            price_data[region] = price_value
                            logger.info(f"Found price for {region}: ${price_value}/MWh")
                        except ValueError:
                            logger.warning(f"Invalid price value for {region}: {price}")
                
                # Check if we've moved to a different table
                elif in_price_section and row[0] == 'I' and row[2] != 'PRICE':
                    in_price_section = False
        
        return price_data
    
    def scrape_current_prices(self):
        """Scrape current electricity prices"""
        
        logger.info("Scraping current electricity prices from AEMO NEMWeb...")
        
        # Get latest files
        file_urls = self.get_latest_dispatch_files()
        
        for url in file_urls:
            content = self.download_and_extract_file(url)
            if content:
                price_data = self.extract_price_data(content)
                if price_data:
                    logger.info(f"Successfully extracted price data from {url}")
                    
                    # Keep region codes as they are (NSW1, VIC1, etc.) for database compatibility
                    formatted_data = price_data
                    
                    formatted_data['source'] = 'AEMO NEMWeb'
                    formatted_data['timestamp'] = datetime.now().isoformat()
                    formatted_data['data_quality'] = 'REAL'
                    
                    return formatted_data
            
            time.sleep(1)  # Be respectful to the server
        
        logger.warning("No price data found in any dispatch files")
        return {
            'NSW': 0,
            'VIC': 0,
            'QLD': 0,
            'SA': 0,
            'TAS': 0,
            'source': 'AEMO NEMWeb',
            'timestamp': datetime.now().isoformat(),
            'data_quality': 'UNAVAILABLE'
        }

def scrape_aemo_prices():
    """Main function to scrape AEMO prices"""
    
    scraper = AEMONEMWebScraper()
    return scraper.scrape_current_prices()

if __name__ == "__main__":
    prices = scrape_aemo_prices()
    print(json.dumps(prices, indent=2))
