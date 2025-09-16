#!/usr/bin/env python3
"""
Script to collect real data from Australian electricity market and dam level sources
"""

import sys
import os
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

def main():
    """Main function to collect real data"""
    try:
        from backend.data.collectors.data_collection_service import DataCollectionService
        import logging
        
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        print("🌐 Starting real data collection from Australian sources...")
        print("📊 This will collect:")
        print("   • Electricity prices from AEMO")
        print("   • Dam levels from WaterNSW, Melbourne Water, Seqwater, and BoM")
        print("   • Data will be stored in the database")
        print()
        
        # Create data collection service
        service = DataCollectionService()
        
        # Run data collection
        service.run_once()
        
        # Get and display summary
        summary = service.get_data_summary()
        
        print("\n✅ Data collection completed!")
        print(f"📈 Electricity records: {summary.get('electricity_records', 0):,}")
        print(f"💧 Dam level records: {summary.get('dam_records', 0):,}")
        print(f"🕐 Latest electricity update: {summary.get('latest_electricity_update', 'N/A')}")
        print(f"🕐 Latest dam update: {summary.get('latest_dam_update', 'N/A')}")
        
        print("\n🚀 Your dashboard now has real data!")
        print("   • Frontend: http://localhost:3000")
        print("   • API: http://localhost:8000")
        print("   • API Docs: http://localhost:8000/docs")
        
    except ImportError as e:
        print(f"❌ Error importing modules: {e}")
        print("💡 Make sure you've installed the requirements:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error collecting data: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
