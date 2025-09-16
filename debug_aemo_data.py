#!/usr/bin/env python3
"""
Debug AEMO data structure to fix parsing
"""

import requests
import zipfile
import io
import csv
import json
from datetime import datetime

def debug_aemo_data():
    """Debug the AEMO data structure"""
    
    url = "https://nemweb.com.au/Reports/Current/DispatchIS_Reports/PUBLIC_DISPATCHIS_202509111655_0000000480215212.zip"
    
    print("🔍 Downloading and analyzing AEMO data structure...")
    
    try:
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
                csv_files = [f for f in zip_file.namelist() if f.upper().endswith('.CSV')]
                
                if csv_files:
                    csv_file = csv_files[0]
                    with zip_file.open(csv_file) as csv_data:
                        content = csv_data.read().decode('utf-8', errors='ignore')
                        
                        # Parse CSV
                        csv_reader = csv.reader(io.StringIO(content))
                        rows = list(csv_reader)
                        
                        print(f"📊 Total rows: {len(rows)}")
                        
                        # Find the PRICE table
                        price_header_row = None
                        price_data_rows = []
                        
                        for i, row in enumerate(rows):
                            if row and len(row) > 2:
                                # Look for PRICE table header
                                if (row[1] == 'DISPATCH' and 
                                    row[2] == 'PRICE' and 
                                    row[0] == 'I'):
                                    price_header_row = i
                                    print(f"📋 Found PRICE header at row {i}: {row}")
                                    break
                        
                        if price_header_row is not None:
                            # Look for data rows after the header
                            for i in range(price_header_row + 1, len(rows)):
                                row = rows[i]
                                if row and len(row) > 0:
                                    if row[0] == 'D' and len(row) > 9:
                                        # This is a data row
                                        print(f"📊 Price data row {i}: {row}")
                                        price_data_rows.append(row)
                                        
                                        # Show first few data rows
                                        if len(price_data_rows) <= 10:
                                            region = row[7] if len(row) > 7 else "N/A"
                                            price = row[9] if len(row) > 9 else "N/A"
                                            print(f"   Region: {region}, Price: {price}")
                                    elif row[0] == 'I':
                                        # New table started
                                        break
                        
                        print(f"📊 Found {len(price_data_rows)} price data rows")
                        
                        # Extract prices by region
                        prices = {}
                        for row in price_data_rows:
                            if len(row) > 9:
                                region = row[7]
                                price = row[9]
                                
                                if region in ['NSW1', 'VIC1', 'QLD1', 'SA1', 'TAS1']:
                                    try:
                                        price_value = float(price)
                                        prices[region] = price_value
                                        print(f"✅ {region}: ${price_value}/MWh")
                                    except ValueError:
                                        print(f"❌ Invalid price for {region}: {price}")
                        
                        return prices
                        
    except Exception as e:
        print(f"❌ Error: {e}")
        return {}

if __name__ == "__main__":
    prices = debug_aemo_data()
    print(f"\n📊 Final prices: {json.dumps(prices, indent=2)}")
