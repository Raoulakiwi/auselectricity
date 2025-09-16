#!/usr/bin/env python3
"""
Test script to investigate all data sources and determine which can provide real data
"""

import requests
import json
import time
from bs4 import BeautifulSoup
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataSourceTester:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.results = {}
    
    def test_aemo_data(self):
        """Test AEMO data access"""
        logger.info("Testing AEMO data access...")
        
        # Test AEMO's public data portal
        try:
            url = "https://aemo.com.au/energy-systems/electricity/national-electricity-market-nem/data-nem/price-and-demand"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                logger.info("✅ AEMO website accessible")
                # Check if there's any downloadable data
                soup = BeautifulSoup(response.content, 'html.parser')
                data_links = soup.find_all('a', href=True)
                downloadable_data = [link for link in data_links if any(ext in link.get('href', '').lower() for ext in ['.csv', '.xlsx', '.json', 'api'])]
                
                if downloadable_data:
                    logger.info(f"✅ Found {len(downloadable_data)} potential data links")
                    self.results['aemo'] = {'status': 'accessible', 'data_links': len(downloadable_data)}
                else:
                    logger.warning("⚠️ AEMO accessible but no obvious data downloads found")
                    self.results['aemo'] = {'status': 'accessible_no_data', 'data_links': 0}
            else:
                logger.error(f"❌ AEMO returned status {response.status_code}")
                self.results['aemo'] = {'status': 'inaccessible', 'error': f'HTTP {response.status_code}'}
                
        except Exception as e:
            logger.error(f"❌ AEMO test failed: {e}")
            self.results['aemo'] = {'status': 'error', 'error': str(e)}
    
    def test_opennem_data(self):
        """Test OpenNEM data access"""
        logger.info("Testing OpenNEM data access...")
        
        try:
            # Test OpenNEM API
            url = "https://api.opennem.org.au/stats/energy/nem/7d"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                logger.info("✅ OpenNEM API accessible")
                logger.info(f"✅ Found {len(data.get('data', []))} data points")
                self.results['opennem'] = {'status': 'accessible', 'data_points': len(data.get('data', []))}
            else:
                logger.error(f"❌ OpenNEM API returned status {response.status_code}")
                self.results['opennem'] = {'status': 'inaccessible', 'error': f'HTTP {response.status_code}'}
                
        except Exception as e:
            logger.error(f"❌ OpenNEM test failed: {e}")
            self.results['opennem'] = {'status': 'error', 'error': str(e)}
    
    def test_seqwater_data(self):
        """Test Seqwater data access"""
        logger.info("Testing Seqwater data access...")
        
        try:
            # Test main dam levels page
            url = "https://www.seqwater.com.au/dam-levels"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for capacity data
                capacity_elements = soup.find_all(text=lambda text: text and '%' in text and any(char.isdigit() for char in text))
                logger.info(f"✅ Seqwater accessible, found {len(capacity_elements)} potential capacity elements")
                
                # Test specific dam page
                hinze_url = "https://www.seqwater.com.au/dams/hinze"
                hinze_response = self.session.get(hinze_url, timeout=10)
                
                if hinze_response.status_code == 200:
                    hinze_soup = BeautifulSoup(hinze_response.content, 'html.parser')
                    hinze_capacity = hinze_soup.find_all(text=lambda text: text and '%' in text and any(char.isdigit() for char in text))
                    logger.info(f"✅ Hinze Dam page accessible, found {len(hinze_capacity)} capacity elements")
                    self.results['seqwater'] = {'status': 'accessible', 'main_page': True, 'specific_dams': True}
                else:
                    logger.warning(f"⚠️ Seqwater main page OK but specific dam pages returned {hinze_response.status_code}")
                    self.results['seqwater'] = {'status': 'partial', 'main_page': True, 'specific_dams': False}
            else:
                logger.error(f"❌ Seqwater returned status {response.status_code}")
                self.results['seqwater'] = {'status': 'inaccessible', 'error': f'HTTP {response.status_code}'}
                
        except Exception as e:
            logger.error(f"❌ Seqwater test failed: {e}")
            self.results['seqwater'] = {'status': 'error', 'error': str(e)}
    
    def test_waternsw_data(self):
        """Test WaterNSW data access"""
        logger.info("Testing WaterNSW data access...")
        
        try:
            # Test main water data page
            url = "https://www.waternsw.com.au/water-services/water-data"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for API or data links
                api_links = soup.find_all('a', href=True)
                api_found = any('api' in link.get('href', '').lower() for link in api_links)
                
                logger.info(f"✅ WaterNSW accessible, API links found: {api_found}")
                self.results['waternsw'] = {'status': 'accessible', 'api_available': api_found}
            else:
                logger.error(f"❌ WaterNSW returned status {response.status_code}")
                self.results['waternsw'] = {'status': 'inaccessible', 'error': f'HTTP {response.status_code}'}
                
        except Exception as e:
            logger.error(f"❌ WaterNSW test failed: {e}")
            self.results['waternsw'] = {'status': 'error', 'error': str(e)}
    
    def test_melbourne_water_data(self):
        """Test Melbourne Water data access"""
        logger.info("Testing Melbourne Water data access...")
        
        try:
            url = "https://www.melbournewater.com.au/water/water-storage-levels"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for storage level data
                storage_elements = soup.find_all(text=lambda text: text and '%' in text and any(char.isdigit() for char in text))
                logger.info(f"✅ Melbourne Water accessible, found {len(storage_elements)} storage elements")
                self.results['melbourne_water'] = {'status': 'accessible', 'storage_data': len(storage_elements)}
            else:
                logger.error(f"❌ Melbourne Water returned status {response.status_code}")
                self.results['melbourne_water'] = {'status': 'inaccessible', 'error': f'HTTP {response.status_code}'}
                
        except Exception as e:
            logger.error(f"❌ Melbourne Water test failed: {e}")
            self.results['melbourne_water'] = {'status': 'error', 'error': str(e)}
    
    def test_sa_water_data(self):
        """Test SA Water data access"""
        logger.info("Testing SA Water data access...")
        
        try:
            url = "https://www.waterconnect.sa.gov.au/Systems/RTWD/SitePages/Available%20Data.aspx"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for data tables or elements
                data_elements = soup.find_all(['table', 'div'], class_=lambda x: x and any(keyword in x.lower() for keyword in ['data', 'level', 'storage']))
                logger.info(f"✅ SA Water accessible, found {len(data_elements)} data elements")
                self.results['sa_water'] = {'status': 'accessible', 'data_elements': len(data_elements)}
            else:
                logger.error(f"❌ SA Water returned status {response.status_code}")
                self.results['sa_water'] = {'status': 'inaccessible', 'error': f'HTTP {response.status_code}'}
                
        except Exception as e:
            logger.error(f"❌ SA Water test failed: {e}")
            self.results['sa_water'] = {'status': 'error', 'error': str(e)}
    
    def test_hydro_tasmania_data(self):
        """Test Hydro Tasmania data access"""
        logger.info("Testing Hydro Tasmania data access...")
        
        try:
            url = "https://www.hydro.com.au/water/lake-levels"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for lake level data
                table = soup.find('table')
                if table:
                    rows = table.find_all('tr')
                    logger.info(f"✅ Hydro Tasmania accessible, found table with {len(rows)} rows")
                    self.results['hydro_tasmania'] = {'status': 'accessible', 'table_rows': len(rows)}
                else:
                    logger.warning("⚠️ Hydro Tasmania accessible but no table found")
                    self.results['hydro_tasmania'] = {'status': 'accessible_no_table', 'table_rows': 0}
            else:
                logger.error(f"❌ Hydro Tasmania returned status {response.status_code}")
                self.results['hydro_tasmania'] = {'status': 'inaccessible', 'error': f'HTTP {response.status_code}'}
                
        except Exception as e:
            logger.error(f"❌ Hydro Tasmania test failed: {e}")
            self.results['hydro_tasmania'] = {'status': 'error', 'error': str(e)}
    
    def run_all_tests(self):
        """Run all data source tests"""
        logger.info("🔍 Starting comprehensive data source investigation...")
        logger.info("=" * 60)
        
        # Test electricity sources
        self.test_aemo_data()
        time.sleep(1)
        self.test_opennem_data()
        time.sleep(1)
        
        # Test dam sources
        self.test_seqwater_data()
        time.sleep(1)
        self.test_waternsw_data()
        time.sleep(1)
        self.test_melbourne_water_data()
        time.sleep(1)
        self.test_sa_water_data()
        time.sleep(1)
        self.test_hydro_tasmania_data()
        
        # Print summary
        logger.info("=" * 60)
        logger.info("📊 DATA SOURCE INVESTIGATION SUMMARY")
        logger.info("=" * 60)
        
        for source, result in self.results.items():
            status = result['status']
            if status == 'accessible':
                logger.info(f"✅ {source.upper()}: REAL DATA AVAILABLE")
            elif status == 'partial':
                logger.info(f"⚠️ {source.upper()}: PARTIAL DATA AVAILABLE")
            else:
                logger.info(f"❌ {source.upper()}: NO REAL DATA AVAILABLE")
        
        return self.results

def main():
    tester = DataSourceTester()
    results = tester.run_all_tests()
    
    # Save results to file
    with open('data_source_test_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    logger.info(f"\n📄 Results saved to data_source_test_results.json")
    
    return results

if __name__ == "__main__":
    main()
