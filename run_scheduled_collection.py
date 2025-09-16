#!/usr/bin/env python3
"""
Scheduled data collection service for the Australian Electricity Market Dashboard
Runs continuously and collects data at regular intervals
"""

import sys
import os
from pathlib import Path
import logging
import signal
import time

# Add the backend directory to Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print('\n🛑 Stopping scheduled data collection...')
    sys.exit(0)

def main():
    """Main function to run scheduled data collection"""
    try:
        from backend.data.collectors.updated_data_collection_service import UpdatedDataCollectionService
        import schedule
        
        # Set up signal handler for graceful shutdown
        signal.signal(signal.SIGINT, signal_handler)
        
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('data_collection.log'),
                logging.StreamHandler()
            ]
        )
        
        print("🔄 Starting scheduled data collection service...")
        print("📊 This will collect data at regular intervals:")
        print("   • Electricity prices: Every 30 minutes")
        print("   • Dam levels: Every 6 hours")
        print("   • Data cleanup: Daily at 2:00 AM")
        print("🛑 Press Ctrl+C to stop")
        print()
        
        # Create data collection service
        service = UpdatedDataCollectionService()
        
        # Schedule data collection
        schedule.every(30).minutes.do(service.collect_and_store_electricity_data)
        schedule.every(6).hours.do(service.collect_and_store_dam_data)
        schedule.every().day.at("02:00").do(service.cleanup_old_data)
        
        # Run initial collection
        print("🚀 Running initial data collection...")
        service.collect_all_data()
        
        # Get and display initial summary
        summary = service.get_data_summary()
        print(f"\n✅ Initial collection completed!")
        print(f"📈 Electricity records: {summary.get('electricity_records', 0):,}")
        print(f"💧 Dam level records: {summary.get('dam_records', 0):,}")
        print(f"🌏 Regions covered: {summary.get('regions_covered', 0)}")
        print(f"🏞️ States covered: {summary.get('states_covered', 0)}")
        
        print("\n⏰ Scheduled collection is now running...")
        print("   • Next electricity collection: 30 minutes")
        print("   • Next dam collection: 6 hours")
        print("   • Next cleanup: 2:00 AM daily")
        
        # Keep running and check for scheduled tasks
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
            
    except ImportError as e:
        print(f"❌ Error importing modules: {e}")
        print("💡 Make sure you've installed the requirements:")
        print("   pip install -r requirements.txt")
        print("   pip install nemosis schedule")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error in scheduled collection: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
