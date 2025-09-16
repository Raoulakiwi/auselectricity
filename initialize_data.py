#!/usr/bin/env python3
"""
Initialize the database with sample data for the Australian Electricity Market Dashboard
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

# Add the backend directory to Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

def initialize_database():
    """Initialize the database with sample data"""
    try:
        from backend.database.database import create_tables, SessionLocal, ElectricityPrice, DamLevel
        from backend.data.collectors.aemo_collector import get_sample_electricity_data
        from backend.data.collectors.dam_collector import get_sample_dam_data
        
        print("🗄️  Creating database tables...")
        create_tables()
        
        print("📊 Generating sample electricity data...")
        electricity_data = get_sample_electricity_data()
        
        print("💧 Generating sample dam level data...")
        dam_data = get_sample_dam_data()
        
        print("💾 Inserting data into database...")
        db = SessionLocal()
        
        try:
            # Check if data already exists
            if db.query(ElectricityPrice).count() > 0:
                print("⚠️  Electricity price data already exists, skipping...")
            else:
                # Insert electricity data in batches
                batch_size = 1000
                for i in range(0, len(electricity_data), batch_size):
                    batch = electricity_data[i:i + batch_size]
                    for data in batch:
                        price_record = ElectricityPrice(**data)
                        db.add(price_record)
                    db.commit()
                    print(f"✅ Inserted electricity batch {i//batch_size + 1}/{(len(electricity_data) + batch_size - 1)//batch_size}")
            
            if db.query(DamLevel).count() > 0:
                print("⚠️  Dam level data already exists, skipping...")
            else:
                # Insert dam data in batches
                batch_size = 1000
                for i in range(0, len(dam_data), batch_size):
                    batch = dam_data[i:i + batch_size]
                    for data in batch:
                        dam_record = DamLevel(**data)
                        db.add(dam_record)
                    db.commit()
                    print(f"✅ Inserted dam level batch {i//batch_size + 1}/{(len(dam_data) + batch_size - 1)//batch_size}")
            
            # Print summary
            electricity_count = db.query(ElectricityPrice).count()
            dam_count = db.query(DamLevel).count()
            
            print(f"\n📈 Database Summary:")
            print(f"   • Electricity price records: {electricity_count:,}")
            print(f"   • Dam level records: {dam_count:,}")
            print(f"   • Date range: {datetime.now() - timedelta(days=365)} to {datetime.now()}")
            
        finally:
            db.close()
            
        print("\n🎉 Database initialization completed successfully!")
        print("🚀 You can now start the backend server with: python start_backend.py")
        
    except ImportError as e:
        print(f"❌ Error importing modules: {e}")
        print("💡 Make sure you've installed the requirements:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    initialize_database()
