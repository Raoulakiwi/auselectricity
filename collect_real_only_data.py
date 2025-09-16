#!/usr/bin/env python3
"""
Real-only data collection script for the Australian Electricity Market Dashboard
Uses only sources that can provide actual real data, returns 0 for unavailable sources
"""

import sys
import os
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

def main():
    """Main function to collect real-only data"""
    try:
        from backend.data.collectors.real_only_scrapers import RealOnlyScrapers
        from backend.database.database import SessionLocal, ElectricityPrice, DamLevel
        from datetime import datetime, timedelta
        import logging
        
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        print("Starting REAL-ONLY data collection...")
        print("This will collect:")
        print("   - Electricity data: 0 for all regions (no real sources available)")
        print("   - Dam data: Real data from Seqwater, WaterNSW, SA Water, Hydro Tasmania")
        print("   - Dam data: 0 for Melbourne Water (not accessible)")
        print("   - Dam data: 0 for any dams that cannot be scraped")
        print("   - Data will be stored in the database")
        print()
        
        # Create real-only data scraper
        scraper = RealOnlyScrapers()
        
        # Get database session
        db = SessionLocal()
        
        try:
            # Collect real-only data
            print("Collecting real-only data...")
            real_data = scraper.scrape_all_real_data()
            
            # Store electricity data (all 0 since no real sources available)
            if real_data['electricity_prices']:
                stored_count = 0
                for data in real_data['electricity_prices']:
                    # Check if record already exists (same timestamp, region)
                    existing = db.query(ElectricityPrice).filter(
                        ElectricityPrice.timestamp == data['timestamp'],
                        ElectricityPrice.region == data['region']
                    ).first()
                    
                    if not existing:
                        electricity_record = ElectricityPrice(**data)
                        db.add(electricity_record)
                        stored_count += 1
                
                db.commit()
                print(f"SUCCESS: Stored {stored_count} new electricity price records (all 0 - no real sources available)")
                
                # Show what we collected
                for data in real_data['electricity_prices']:
                    print(f"   - {data['region']}: Price=${data['price']}, Demand={data['demand']}, Supply={data['supply']}")
            else:
                print("WARNING: No electricity data collected")
            
            # Store dam data
            if real_data['dam_levels']:
                stored_count = 0
                for data in real_data['dam_levels']:
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
                print(f"SUCCESS: Stored {stored_count} new dam level records")
                
                # Show what we collected
                real_dams = [d for d in real_data['dam_levels'] if d['capacity_percentage'] > 0]
                zero_dams = [d for d in real_data['dam_levels'] if d['capacity_percentage'] == 0]
                
                if real_dams:
                    print(f"   Real data found for {len(real_dams)} dams:")
                    for data in real_dams:
                        print(f"     - {data['dam_name']} ({data['state']}): {data['capacity_percentage']}%")
                
                if zero_dams:
                    print(f"   No real data available for {len(zero_dams)} dams (set to 0%):")
                    for data in zero_dams:
                        print(f"     - {data['dam_name']} ({data['state']}): 0%")
            else:
                print("WARNING: No dam data collected")
            
            # Get current database stats
            electricity_count = db.query(ElectricityPrice).count()
            dam_count = db.query(DamLevel).count()
            
            # Get latest records
            latest_electricity = db.query(ElectricityPrice.timestamp).order_by(ElectricityPrice.timestamp.desc()).first()
            latest_dam = db.query(DamLevel.timestamp).order_by(DamLevel.timestamp.desc()).first()
            
            print("\nREAL-ONLY data collection completed!")
            print(f"Total electricity records: {electricity_count:,}")
            print(f"Total dam level records: {dam_count:,}")
            print(f"Latest electricity update: {latest_electricity[0] if latest_electricity else 'N/A'}")
            print(f"Latest dam update: {latest_dam[0] if latest_dam else 'N/A'}")
            
            print("\nYour dashboard now has REAL-ONLY data!")
            print("   - Frontend: http://localhost:3000")
            print("   - API: http://localhost:8000")
            print("   - API Docs: http://localhost:8000/docs")
            
            print("\nData sources status:")
            print("   - Electricity: 0 for all regions (no real sources available)")
            print("   - Seqwater (QLD): Real data where available, 0 otherwise")
            print("   - WaterNSW (NSW): Real data where available, 0 otherwise")
            print("   - SA Water (SA): Real data where available, 0 otherwise")
            print("   - Hydro Tasmania (TAS): Real data where available, 0 otherwise")
            print("   - Melbourne Water (VIC): 0 (not accessible)")
            
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
        print(f"ERROR: Error collecting real-only data: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
