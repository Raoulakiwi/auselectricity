import schedule
import time
import logging
from datetime import datetime, timedelta
from typing import List, Dict
from sqlalchemy.orm import Session

from backend.database.database import SessionLocal, ElectricityPrice, DamLevel
from backend.data.collectors.updated_real_data_scrapers import UpdatedRealDataScrapers

logger = logging.getLogger(__name__)

class UpdatedDataCollectionService:
    """
    Updated service to collect real data from various sources using improved scrapers
    """
    
    def __init__(self):
        self.scraper = UpdatedRealDataScrapers()
        self.db = SessionLocal()
    
    def collect_and_store_electricity_data(self):
        """
        Collect electricity price data using NEMOSIS and web scraping
        """
        try:
            logger.info("Starting updated electricity data collection...")
            
            # Try NEMOSIS first, then fallback to web scraping
            electricity_data = self.scraper.scrape_aemo_data_nemosis()
            
            if not electricity_data:
                logger.info("NEMOSIS failed, trying web scraping...")
                electricity_data = self.scraper.scrape_aemo_data_web()
            
            if not electricity_data:
                logger.info("Web scraping failed, trying OpenNEM...")
                electricity_data = self.scraper.scrape_opennem_data()
            
            if electricity_data:
                # Store in database
                stored_count = 0
                for data in electricity_data:
                    # Check if record already exists for this timestamp and region
                    existing = self.db.query(ElectricityPrice).filter(
                        ElectricityPrice.timestamp == data['timestamp'],
                        ElectricityPrice.region == data['region']
                    ).first()
                    
                    if not existing:
                        price_record = ElectricityPrice(**data)
                        self.db.add(price_record)
                        stored_count += 1
                
                self.db.commit()
                logger.info(f"Stored {stored_count} new electricity price records")
            else:
                logger.warning("No electricity data collected from any source")
                
        except Exception as e:
            logger.error(f"Error collecting electricity data: {e}")
            self.db.rollback()
    
    def collect_and_store_dam_data(self):
        """
        Collect dam level data from all sources
        """
        try:
            logger.info("Starting updated dam level data collection...")
            
            # Scrape dam levels from all sources
            dam_sources = [
                self.scraper.scrape_waternsw_dam_levels,
                self.scraper.scrape_melbourne_water_levels,
                self.scraper.scrape_seqwater_levels,
                self.scraper.scrape_bom_water_storage
            ]
            
            total_dam_records = 0
            
            for scraper in dam_sources:
                try:
                    dam_data = scraper()
                    
                    if dam_data:
                        for data in dam_data:
                            # Check if record already exists
                            existing = self.db.query(DamLevel).filter(
                                DamLevel.timestamp == data['timestamp'],
                                DamLevel.dam_name == data['dam_name'],
                                DamLevel.state == data['state']
                            ).first()
                            
                            if not existing:
                                dam_record = DamLevel(**data)
                                self.db.add(dam_record)
                                total_dam_records += 1
                        
                        self.db.commit()
                        logger.info(f"Stored {len(dam_data)} dam level records from {scraper.__name__}")
                    
                    time.sleep(1)  # Be respectful to servers
                    
                except Exception as e:
                    logger.error(f"Error in {scraper.__name__}: {e}")
                    continue
            
            logger.info(f"Total new dam records stored: {total_dam_records}")
            
        except Exception as e:
            logger.error(f"Error collecting dam data: {e}")
            self.db.rollback()
    
    def collect_all_data(self):
        """
        Collect all data from all sources
        """
        logger.info("Starting comprehensive updated data collection...")
        
        # Collect electricity data
        self.collect_and_store_electricity_data()
        
        # Collect dam data
        self.collect_and_store_dam_data()
        
        logger.info("Updated data collection completed")
    
    def get_data_summary(self) -> Dict:
        """
        Get summary of data in database
        """
        try:
            electricity_count = self.db.query(ElectricityPrice).count()
            dam_count = self.db.query(DamLevel).count()
            
            # Get latest timestamps
            latest_electricity = self.db.query(ElectricityPrice.timestamp).order_by(
                ElectricityPrice.timestamp.desc()
            ).first()
            
            latest_dam = self.db.query(DamLevel.timestamp).order_by(
                DamLevel.timestamp.desc()
            ).first()
            
            # Get data by region
            regions = self.db.query(ElectricityPrice.region).distinct().all()
            region_count = len(regions)
            
            # Get data by state
            states = self.db.query(DamLevel.state).distinct().all()
            state_count = len(states)
            
            return {
                'electricity_records': electricity_count,
                'dam_records': dam_count,
                'regions_covered': region_count,
                'states_covered': state_count,
                'latest_electricity_update': latest_electricity[0] if latest_electricity else None,
                'latest_dam_update': latest_dam[0] if latest_dam else None,
                'collection_time': datetime.now()
            }
            
        except Exception as e:
            logger.error(f"Error getting data summary: {e}")
            return {}
    
    def cleanup_old_data(self, days_to_keep: int = 365):
        """
        Clean up old data to keep database size manageable
        """
        try:
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            
            # Delete old electricity data
            old_electricity = self.db.query(ElectricityPrice).filter(
                ElectricityPrice.timestamp < cutoff_date
            ).delete()
            
            # Delete old dam data
            old_dam = self.db.query(DamLevel).filter(
                DamLevel.timestamp < cutoff_date
            ).delete()
            
            self.db.commit()
            
            logger.info(f"Cleaned up {old_electricity} old electricity records and {old_dam} old dam records")
            
        except Exception as e:
            logger.error(f"Error cleaning up old data: {e}")
            self.db.rollback()
    
    def run_scheduled_collection(self):
        """
        Run the data collection service with scheduled updates
        """
        logger.info("Starting scheduled updated data collection service...")
        
        # Schedule data collection
        schedule.every(30).minutes.do(self.collect_and_store_electricity_data)
        schedule.every(6).hours.do(self.collect_and_store_dam_data)
        schedule.every().day.at("02:00").do(self.cleanup_old_data)
        
        # Run initial collection
        self.collect_all_data()
        
        # Keep running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def run_once(self):
        """
        Run data collection once
        """
        logger.info("Running one-time updated data collection...")
        self.collect_all_data()
        
        # Print summary
        summary = self.get_data_summary()
        logger.info(f"Updated data collection summary: {summary}")

# Utility functions
def run_updated_data_collection():
    """
    Run updated data collection service
    """
    service = UpdatedDataCollectionService()
    service.run_once()

def run_scheduled_updated_collection():
    """
    Run scheduled updated data collection service
    """
    service = UpdatedDataCollectionService()
    service.run_scheduled_collection()

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run data collection
    run_updated_data_collection()
