#!/usr/bin/env python3
"""
Real-time data collection script for the Australian Electricity Market Dashboard
Uses actual web scraping to get current data from official sources
"""

import sys
import os
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

def main():
    """Main function to collect real-time data"""
    try:
        from backend.data.collectors.real_time_scrapers import RealTimeScrapers
        from backend.database.database import SessionLocal, ElectricityPrice, DamLevel
        from datetime import datetime, timedelta
        import logging
        
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        print("Starting REAL-TIME data collection...")
        print("This will collect:")
        print("   - Real-time dam levels from Seqwater (Queensland)")
        print("   - Real-time lake levels from Hydro Tasmania")
        print("   - Data will be stored in the database")
        print()
        
        # Create real-time data scraper
        scraper = RealTimeScrapers()
        
        # Get database session
        db = SessionLocal()
        
        try:
            # Collect real-time data
            print("Collecting real-time data...")
            real_time_data = scraper.scrape_all_real_time_data()
            
            # Store real-time dam data
            if real_time_data['dam_levels']:
                stored_count = 0
                for data in real_time_data['dam_levels']:
                    # Check if record already exists (same timestamp, dam, state)
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
                print(f"SUCCESS: Stored {stored_count} new real-time dam level records")
                
                # Show what we collected
                for data in real_time_data['dam_levels']:
                    print(f"   - {data['dam_name']} ({data['state']}): {data['capacity_percentage']}%")
            else:
                print("WARNING: No real-time dam data collected")
            
            # Get current database stats
            electricity_count = db.query(ElectricityPrice).count()
            dam_count = db.query(DamLevel).count()
            
            # Get latest records
            latest_electricity = db.query(ElectricityPrice.timestamp).order_by(ElectricityPrice.timestamp.desc()).first()
            latest_dam = db.query(DamLevel.timestamp).order_by(DamLevel.timestamp.desc()).first()
            
            print("\nREAL-TIME data collection completed!")
            print(f"Total electricity records: {electricity_count:,}")
            print(f"Total dam level records: {dam_count:,}")
            print(f"Latest electricity update: {latest_electricity[0] if latest_electricity else 'N/A'}")
            print(f"Latest dam update: {latest_dam[0] if latest_dam else 'N/A'}")
            
            print("\nYour dashboard now has real-time data!")
            print("   - Frontend: http://localhost:3000")
            print("   - API: http://localhost:8000")
            print("   - API Docs: http://localhost:8000/docs")
            
            print("\nReal-time data sources:")
            print("   - Seqwater (Queensland dams)")
            print("   - Hydro Tasmania (Tasmania lakes)")
            
        except Exception as e:
            db.rollback()
            print(f"ERROR: Database error: {e}")
            raise
        finally:
            db.close()
            
    except ImportError as e:
        print(f"ERROR: Error importing modules: {e}")
        print("Make sure you've installed the requirements:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Error collecting real-time data: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
