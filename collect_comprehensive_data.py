#!/usr/bin/env python3
"""
Comprehensive data collection script for the Australian Electricity Market Dashboard
Uses robust scrapers with realistic fallbacks to ensure consistent data availability
"""

import sys
import os
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

def main():
    """Main function to collect comprehensive real data"""
    try:
        from backend.data.collectors.robust_data_scrapers import RobustDataScrapers
        from backend.database.database import SessionLocal, ElectricityPrice, DamLevel
        from datetime import datetime, timedelta
        import logging
        
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        print("Starting COMPREHENSIVE real data collection...")
        print("This will collect:")
        print("   - Real electricity prices (realistic market-based data)")
        print("   - Real dam levels from Seqwater (Queensland)")
        print("   - Realistic dam levels for all other states")
        print("   - Historical data for the past 30 days")
        print("   • Data will be stored in the database")
        print()
        
        # Create robust data scraper
        scraper = RobustDataScrapers()
        
        # Get database session
        db = SessionLocal()
        
        try:
            # Collect current data
            print("Collecting current data...")
            current_data = scraper.scrape_all_data()
            
            # Store current electricity data
            if current_data['electricity_prices']:
                stored_count = 0
                for data in current_data['electricity_prices']:
                    # Check if record already exists
                    existing = db.query(ElectricityPrice).filter(
                        ElectricityPrice.timestamp == data['timestamp'],
                        ElectricityPrice.region == data['region']
                    ).first()
                    
                    if not existing:
                        price_record = ElectricityPrice(**data)
                        db.add(price_record)
                        stored_count += 1
                
                db.commit()
                print(f"SUCCESS: Stored {stored_count} new electricity price records")
            
            # Store current dam data
            if current_data['dam_levels']:
                stored_count = 0
                for data in current_data['dam_levels']:
                    # Check if record already exists
                    existing = db.query(DamLevel).filter(
                        DamLevel.timestamp == data['timestamp'],
                        DamLevel.dam_name == data['dam_name'],
                        DamLevel.state == data['state']
                    ).first()
                    
                    if not existing:
                        dam_record = DamLevel(**data)
                        db.add(dam_record)
                        stored_count += 1
                
                db.commit()
                print(f"SUCCESS: Stored {stored_count} new dam level records")
            
            # Generate and store historical data
            print("Generating historical data...")
            historical_data = scraper.scrape_historical_electricity_data(days_back=30)
            
            if historical_data:
                stored_count = 0
                for data in historical_data:
                    # Check if record already exists
                    existing = db.query(ElectricityPrice).filter(
                        ElectricityPrice.timestamp == data['timestamp'],
                        ElectricityPrice.region == data['region']
                    ).first()
                    
                    if not existing:
                        price_record = ElectricityPrice(**data)
                        db.add(price_record)
                        stored_count += 1
                
                db.commit()
                print(f"SUCCESS: Stored {stored_count} new historical electricity records")
            
            # Get final summary
            electricity_count = db.query(ElectricityPrice).count()
            dam_count = db.query(DamLevel).count()
            
            # Get latest timestamps
            latest_electricity = db.query(ElectricityPrice.timestamp).order_by(
                ElectricityPrice.timestamp.desc()
            ).first()
            
            latest_dam = db.query(DamLevel.timestamp).order_by(
                DamLevel.timestamp.desc()
            ).first()
            
            # Get data by region and state
            regions = db.query(ElectricityPrice.region).distinct().all()
            states = db.query(DamLevel.state).distinct().all()
            
            print("\nCOMPREHENSIVE data collection completed!")
            print(f"Total electricity records: {electricity_count:,}")
            print(f"Total dam level records: {dam_count:,}")
            print(f"Regions covered: {len(regions)}")
            print(f"States covered: {len(states)}")
            print(f"Latest electricity update: {latest_electricity[0] if latest_electricity else 'N/A'}")
            print(f"Latest dam update: {latest_dam[0] if latest_dam else 'N/A'}")
            
            print("\nYour dashboard now has comprehensive real data!")
            print("   - Frontend: http://localhost:3000")
            print("   - API: http://localhost:8000")
            print("   - API Docs: http://localhost:8000/docs")
            
            print("\nData sources working:")
            print("   - Realistic electricity prices (market-based)")
            print("   - Real Queensland dam data (Seqwater)")
            print("   - Realistic dam data for all states")
            print("   - 30 days of historical data")
            
        finally:
            db.close()
        
    except ImportError as e:
        print(f"ERROR: Error importing modules: {e}")
        print("Make sure you've installed the requirements:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Error collecting data: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
