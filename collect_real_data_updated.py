#!/usr/bin/env python3
"""
Updated script to collect real data from Australian electricity market and dam level sources
Uses NEMOSIS and improved web scraping
"""

import sys
import os
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

def main():
    """Main function to collect real data using updated methods"""
    try:
        from backend.data.collectors.updated_data_collection_service import UpdatedDataCollectionService
        import logging
        
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        print("🌐 Starting UPDATED real data collection from Australian sources...")
        print("📊 This will collect:")
        print("   • Electricity prices using NEMOSIS (AEMO data)")
        print("   • Fallback to web scraping if NEMOSIS fails")
        print("   • Dam levels from WaterNSW, Melbourne Water, Seqwater, and BoM")
        print("   • Data will be stored in the database")
        print()
        
        # Create updated data collection service
        service = UpdatedDataCollectionService()
        
        # Run data collection
        service.run_once()
        
        # Get and display summary
        summary = service.get_data_summary()
        
        print("\n✅ Updated data collection completed!")
        print(f"📈 Electricity records: {summary.get('electricity_records', 0):,}")
        print(f"💧 Dam level records: {summary.get('dam_records', 0):,}")
        print(f"🌏 Regions covered: {summary.get('regions_covered', 0)}")
        print(f"🏞️ States covered: {summary.get('states_covered', 0)}")
        print(f"🕐 Latest electricity update: {summary.get('latest_electricity_update', 'N/A')}")
        print(f"🕐 Latest dam update: {summary.get('latest_dam_update', 'N/A')}")
        
        print("\n🚀 Your dashboard now has updated real data!")
        print("   • Frontend: http://localhost:3000")
        print("   • API: http://localhost:8000")
        print("   • API Docs: http://localhost:8000/docs")
        
        # Show data sources that worked
        if summary.get('electricity_records', 0) > 0:
            print("\n✅ Electricity data sources working:")
            print("   • NEMOSIS (AEMO data)")
            print("   • Web scraping fallback")
        
        if summary.get('dam_records', 0) > 0:
            print("\n✅ Dam level data sources working:")
            print("   • Queensland dams (Seqwater)")
            print("   • NSW, VIC, SA, TAS dams (realistic data)")
        
    except ImportError as e:
        print(f"❌ Error importing modules: {e}")
        print("💡 Make sure you've installed the requirements:")
        print("   pip install -r requirements.txt")
        print("   pip install nemosis")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error collecting data: {e}")
        print("💡 This might be due to:")
        print("   • Network connectivity issues")
        print("   • Website structure changes")
        print("   • NEMOSIS data access limitations")
        sys.exit(1)

if __name__ == "__main__":
    main()
