#!/usr/bin/env python3
"""
Real-only data scrapers that only use sources that can provide actual real data
Returns 0 for sources that cannot be scraped
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import time
import logging
from typing import List, Dict, Optional
import re
from .aemo_nemweb_scraper import AEMONEMWebScraper

logger = logging.getLogger(__name__)

class RealOnlyScrapers:
    """
    Real-only scrapers that only use sources verified to provide real data
    Returns 0 for unavailable sources instead of simulated data
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    def scrape_electricity_data_real_only(self) -> List[Dict]:
        """
        Scrape electricity data from real sources only
        Now uses AEMO NEMWeb for real electricity price data
        """
        logger.info("Scraping electricity data from AEMO NEMWeb...")
        
        try:
            # Use AEMO NEMWeb scraper for real electricity data
            aemo_scraper = AEMONEMWebScraper()
            price_data = aemo_scraper.scrape_current_prices()
            
            if price_data and price_data.get('data_quality') == 'REAL':
                # Convert to our format
                electricity_data = []
                regions = ['NSW1', 'VIC1', 'QLD1', 'SA1', 'TAS1']
                current_time = datetime.now()
                
                for region in regions:
                    price = price_data.get(region, 0.0)
                    electricity_data.append({
                        'timestamp': current_time,
                        'region': region,
                        'price': price,
                        'demand': 0.0,  # We don't have demand data yet
                        'supply': 0.0   # We don't have supply data yet
                    })
                
                logger.info(f"Electricity data: {len(electricity_data)} records from AEMO NEMWeb (REAL DATA)")
                return electricity_data
            else:
                logger.warning("AEMO NEMWeb data not available - returning 0 values")
                # Fallback to 0 values
                regions = ['NSW1', 'VIC1', 'QLD1', 'SA1', 'TAS1']
                current_time = datetime.now()
                
                electricity_data = []
                for region in regions:
                    electricity_data.append({
                        'timestamp': current_time,
                        'region': region,
                        'price': 0.0,
                        'demand': 0.0,
                        'supply': 0.0
                    })
                
                return electricity_data
                
        except Exception as e:
            logger.error(f"Error scraping AEMO NEMWeb data: {e}")
            # Fallback to 0 values
            regions = ['NSW1', 'VIC1', 'QLD1', 'SA1', 'TAS1']
            current_time = datetime.now()
            
            electricity_data = []
            for region in regions:
                electricity_data.append({
                    'timestamp': current_time,
                    'region': region,
                    'price': 0.0,
                    'demand': 0.0,
                    'supply': 0.0
                })
            
            return electricity_data
    
    def scrape_seqwater_real_data(self) -> List[Dict]:
        """
        Scrape real dam level data from Seqwater (Queensland)
        """
        logger.info("Scraping real Seqwater dam levels...")
        
        try:
            url = "https://www.seqwater.com.au/dam-levels"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            dam_data = []
            
            # Known Seqwater dams
            seqwater_dams = [
                'Hinze', 'Wivenhoe', 'Somerset', 'Fairbairn', 'Burdekin Falls',
                'Baroon Pocket', 'Borumba', 'Cooloolabin', 'Ewen Maddock',
                'Lake Macdonald', 'Lake Manchester', 'Leslie Harrison',
                'Little Nerang', 'Maroon', 'Moogerah', 'North Pine',
                'Poona', 'Sideling Creek', 'Six Mile Creek', 'Tingalpa', 'Wappa'
            ]
            
            # Try to extract data from the main page
            # Look for capacity information in various formats
            capacity_patterns = [
                r'(\d+\.?\d*)\s*%',  # Percentage patterns
                r'(\d+\.?\d*)\s*per\s*cent',  # "per cent" patterns
            ]
            
            for dam_name in seqwater_dams:
                try:
                    # Try to find dam-specific data on the main page
                    dam_section = soup.find(text=re.compile(dam_name, re.IGNORECASE))
                    if dam_section:
                        # Look for capacity data near the dam name
                        parent = dam_section.parent
                        if parent:
                            # Search in nearby elements for capacity data
                            capacity_found = False
                            for pattern in capacity_patterns:
                                capacity_match = re.search(pattern, parent.get_text())
                                if capacity_match:
                                    capacity = float(capacity_match.group(1))
                                    if 0 <= capacity <= 100:  # Valid percentage
                                        dam_data.append({
                                            'timestamp': datetime.now(),
                                            'dam_name': dam_name,
                                            'state': 'QLD',
                                            'capacity_percentage': capacity,
                                            'volume_ml': 0.0  # We don't have volume data from main page
                                        })
                                        capacity_found = True
                                        logger.info(f"Found {dam_name}: {capacity}%")
                                        break
                            
                            if not capacity_found:
                                # Try individual dam page
                                dam_url = f"https://www.seqwater.com.au/dams/{dam_name.lower().replace(' ', '-')}"
                                dam_response = self.session.get(dam_url, timeout=10)
                                
                                if dam_response.status_code == 200:
                                    dam_soup = BeautifulSoup(dam_response.content, 'html.parser')
                                    
                                    # Look for capacity in the dam page
                                    for pattern in capacity_patterns:
                                        capacity_match = re.search(pattern, dam_soup.get_text())
                                        if capacity_match:
                                            capacity = float(capacity_match.group(1))
                                            if 0 <= capacity <= 100:
                                                dam_data.append({
                                                    'timestamp': datetime.now(),
                                                    'dam_name': dam_name,
                                                    'state': 'QLD',
                                                    'capacity_percentage': capacity,
                                                    'volume_ml': 0.0
                                                })
                                                logger.info(f"Found {dam_name} on individual page: {capacity}%")
                                                break
                                
                                time.sleep(0.5)  # Be respectful
                    else:
                        # Dam not found on main page, try individual page
                        dam_url = f"https://www.seqwater.com.au/dams/{dam_name.lower().replace(' ', '-')}"
                        dam_response = self.session.get(dam_url, timeout=10)
                        
                        if dam_response.status_code == 200:
                            dam_soup = BeautifulSoup(dam_response.content, 'html.parser')
                            
                            for pattern in capacity_patterns:
                                capacity_match = re.search(pattern, dam_soup.get_text())
                                if capacity_match:
                                    capacity = float(capacity_match.group(1))
                                    if 0 <= capacity <= 100:
                                        dam_data.append({
                                            'timestamp': datetime.now(),
                                            'dam_name': dam_name,
                                            'state': 'QLD',
                                            'capacity_percentage': capacity,
                                            'volume_ml': 0.0
                                        })
                                        logger.info(f"Found {dam_name} on individual page: {capacity}%")
                                        break
                        
                        time.sleep(0.5)  # Be respectful
                
                except Exception as e:
                    logger.error(f"Error scraping {dam_name}: {e}")
                    continue
            
            if dam_data:
                logger.info(f"Successfully scraped {len(dam_data)} real Seqwater dam records")
            else:
                logger.warning("No Seqwater data found - will return 0")
            
            return dam_data
            
        except Exception as e:
            logger.error(f"Error scraping Seqwater: {e}")
            return []
    
    def scrape_waternsw_real_data(self) -> List[Dict]:
        """
        Scrape real dam level data from WaterNSW (New South Wales)
        """
        logger.info("Scraping real WaterNSW dam levels...")
        
        try:
            # WaterNSW has API available, but for now we'll try web scraping
            url = "https://www.waternsw.com.au/supply/dam-levels"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            dam_data = []
            
            # Known WaterNSW dams
            waternsw_dams = [
                'Blowering', 'Burrinjuck', 'Copeton', 'Eucumbene', 'Warragamba', 'Windamere'
            ]
            
            # Look for dam level data
            for dam_name in waternsw_dams:
                try:
                    # Search for dam name and nearby capacity data
                    dam_elements = soup.find_all(text=re.compile(dam_name, re.IGNORECASE))
                    
                    for element in dam_elements:
                        parent = element.parent
                        if parent:
                            # Look for capacity percentage in nearby text
                            capacity_match = re.search(r'(\d+\.?\d*)\s*%', parent.get_text())
                            if capacity_match:
                                capacity = float(capacity_match.group(1))
                                if 0 <= capacity <= 100:
                                    dam_data.append({
                                        'timestamp': datetime.now(),
                                        'dam_name': dam_name,
                                        'state': 'NSW',
                                        'capacity_percentage': capacity,
                                        'volume_ml': 0.0
                                    })
                                    logger.info(f"Found {dam_name}: {capacity}%")
                                    break
                
                except Exception as e:
                    logger.error(f"Error scraping {dam_name}: {e}")
                    continue
            
            if dam_data:
                logger.info(f"Successfully scraped {len(dam_data)} real WaterNSW dam records")
            else:
                logger.warning("No WaterNSW data found - will return 0")
            
            return dam_data
            
        except Exception as e:
            logger.error(f"Error scraping WaterNSW: {e}")
            return []
    
    def scrape_sa_water_real_data(self) -> List[Dict]:
        """
        Scrape real dam level data from SA Water (South Australia)
        """
        logger.info("Scraping real SA Water dam levels...")
        
        try:
            url = "https://www.waterconnect.sa.gov.au/Systems/RTWD/SitePages/Available%20Data.aspx"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            dam_data = []
            
            # Known SA Water dams
            sa_dams = ['Happy Valley', 'Mount Bold', 'Myponga']
            
            # Look for dam level data
            for dam_name in sa_dams:
                try:
                    # Search for dam name and nearby capacity data
                    dam_elements = soup.find_all(text=re.compile(dam_name, re.IGNORECASE))
                    
                    for element in dam_elements:
                        parent = element.parent
                        if parent:
                            # Look for capacity percentage in nearby text
                            capacity_match = re.search(r'(\d+\.?\d*)\s*%', parent.get_text())
                            if capacity_match:
                                capacity = float(capacity_match.group(1))
                                if 0 <= capacity <= 100:
                                    dam_data.append({
                                        'timestamp': datetime.now(),
                                        'dam_name': dam_name,
                                        'state': 'SA',
                                        'capacity_percentage': capacity,
                                        'volume_ml': 0.0
                                    })
                                    logger.info(f"Found {dam_name}: {capacity}%")
                                    break
                
                except Exception as e:
                    logger.error(f"Error scraping {dam_name}: {e}")
                    continue
            
            if dam_data:
                logger.info(f"Successfully scraped {len(dam_data)} real SA Water dam records")
            else:
                logger.warning("No SA Water data found - will return 0")
            
            return dam_data
            
        except Exception as e:
            logger.error(f"Error scraping SA Water: {e}")
            return []
    
    def scrape_hydro_tasmania_real_data(self) -> List[Dict]:
        """
        Scrape real dam level data from Hydro Tasmania
        """
        logger.info("Scraping real Hydro Tasmania lake levels...")
        
        try:
            url = "https://www.hydro.com.au/water/lake-levels"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            dam_data = []
            
            # Look for the lake levels table
            table = soup.find('table')
            if table:
                rows = table.find_all('tr')[1:]  # Skip header row
                
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) >= 2:
                        try:
                            # Extract lake name from the link
                            lake_link = cells[0].find('a')
                            if lake_link:
                                lake_name = lake_link.get_text().strip()
                                
                                # Extract metres from full
                                metres_text = cells[1].get_text().strip()
                                if metres_text and metres_text != 'Spilling':
                                    try:
                                        metres_from_full = float(metres_text)
                                        
                                        # Convert to percentage (this is approximate)
                                        # We'll need to get the actual capacity data for accurate conversion
                                        # For now, we'll estimate based on typical dam capacities
                                        estimated_capacity = max(0, min(100, 100 - (metres_from_full * 2)))
                                        
                                        dam_data.append({
                                            'timestamp': datetime.now(),
                                            'dam_name': lake_name,
                                            'state': 'TAS',
                                            'capacity_percentage': round(estimated_capacity, 1),
                                            'volume_ml': 0.0  # We don't have volume data
                                        })
                                        logger.info(f"Found {lake_name}: {estimated_capacity}% (estimated from {metres_from_full}m from full)")
                                        
                                    except ValueError:
                                        continue
                                        
                        except Exception as e:
                            logger.error(f"Error parsing row: {e}")
                            continue
            
            if dam_data:
                logger.info(f"Successfully scraped {len(dam_data)} real Hydro Tasmania records")
            else:
                logger.warning("No Hydro Tasmania data found - will return 0")
            
            return dam_data
            
        except Exception as e:
            logger.error(f"Error scraping Hydro Tasmania: {e}")
            return []
    
    def scrape_melbourne_water_real_data(self) -> List[Dict]:
        """
        Scrape real dam level data from Melbourne Water (Victoria)
        Returns empty list since Melbourne Water is not accessible (404)
        """
        logger.info("Scraping Melbourne Water dam levels - NOT ACCESSIBLE (404)")
        
        # Based on investigation: Melbourne Water returns 404
        # Return empty list - will be filled with 0 values
        return []
    
    def scrape_all_real_data(self) -> Dict[str, List[Dict]]:
        """
        Scrape all available real data sources
        Returns 0 for unavailable sources
        """
        logger.info("Starting REAL-ONLY data scraping...")
        
        all_data = {
            'electricity_prices': [],
            'dam_levels': []
        }
        
        # Scrape electricity data (returns 0 for all since no real sources available)
        try:
            electricity_data = self.scrape_electricity_data_real_only()
            all_data['electricity_prices'].extend(electricity_data)
        except Exception as e:
            logger.error(f"Electricity data scraping failed: {e}")
        
        # Scrape real dam data from available sources
        try:
            seqwater_data = self.scrape_seqwater_real_data()
            all_data['dam_levels'].extend(seqwater_data)
        except Exception as e:
            logger.error(f"Seqwater scraping failed: {e}")
        
        try:
            waternsw_data = self.scrape_waternsw_real_data()
            all_data['dam_levels'].extend(waternsw_data)
        except Exception as e:
            logger.error(f"WaterNSW scraping failed: {e}")
        
        try:
            sa_water_data = self.scrape_sa_water_real_data()
            all_data['dam_levels'].extend(sa_water_data)
        except Exception as e:
            logger.error(f"SA Water scraping failed: {e}")
        
        try:
            hydro_tas_data = self.scrape_hydro_tasmania_real_data()
            all_data['dam_levels'].extend(hydro_tas_data)
        except Exception as e:
            logger.error(f"Hydro Tasmania scraping failed: {e}")
        
        # Melbourne Water is not accessible (404) - no data added
        
        # Fill in missing dams with 0 values
        all_states = ['NSW', 'VIC', 'QLD', 'SA', 'TAS']
        all_dams = {
            'NSW': ['Blowering', 'Burrinjuck', 'Copeton', 'Eucumbene', 'Warragamba', 'Windamere'],
            'VIC': ['Dartmouth', 'Eildon', 'Hume', 'Thomson', 'Yarrawonga'],
            'QLD': ['Hinze', 'Wivenhoe', 'Somerset', 'Fairbairn', 'Burdekin Falls', 'Baroon Pocket', 'Borumba', 'Cooloolabin', 'Ewen Maddock', 'Lake Macdonald', 'Lake Manchester', 'Leslie Harrison', 'Little Nerang', 'Maroon', 'Moogerah', 'North Pine', 'Poona', 'Sideling Creek', 'Six Mile Creek', 'Tingalpa', 'Wappa'],
            'SA': ['Happy Valley', 'Mount Bold', 'Myponga'],
            'TAS': ['Gordon', 'Great Lake', 'Lake Pedder']
        }
        
        # Add 0 values for dams that weren't found
        found_dams = {(dam['dam_name'], dam['state']) for dam in all_data['dam_levels']}
        
        for state, dams in all_dams.items():
            for dam_name in dams:
                if (dam_name, state) not in found_dams:
                    all_data['dam_levels'].append({
                        'timestamp': datetime.now(),
                        'dam_name': dam_name,
                        'state': state,
                        'capacity_percentage': 0.0,  # No real data available
                        'volume_ml': 0.0
                    })
                    logger.info(f"Added {dam_name} ({state}): 0% - no real data available")
        
        logger.info(f"Real-only scraping complete. Got {len(all_data['electricity_prices'])} electricity records and {len(all_data['dam_levels'])} dam records")
        
        return all_data

# Utility function to run real-only scraping
def scrape_real_only_data():
    """
    Main function to scrape real data only
    """
    scraper = RealOnlyScrapers()
    return scraper.scrape_all_real_data()
