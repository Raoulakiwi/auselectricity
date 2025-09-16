#!/usr/bin/env python3
"""
Test script to extract real electricity price data from NEMWeb files
"""

import requests
import zipfile
import io
import csv
import json
from datetime import datetime, timedelta
import time

def download_and_extract_nemweb_file(url):
    """Download and extract a NEMWeb ZIP file"""
    
    print(f"\n🔍 Downloading: {url}")
    
    try:
        response = requests.get(url, timeout=30)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   ✅ Downloaded {len(response.content)} bytes")
            
            # Try to extract the ZIP file
            try:
                with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
                    print(f"   📁 ZIP file contains {len(zip_file.namelist())} files:")
                    
                    for file_name in zip_file.namelist()[:10]:  # Show first 10 files
                        print(f"      - {file_name}")
                    
                    # Look for CSV files
                    csv_files = [f for f in zip_file.namelist() if f.endswith('.csv')]
                    print(f"   📊 Found {len(csv_files)} CSV files")
                    
                    if csv_files:
                        # Try to read the first CSV file
                        csv_file = csv_files[0]
                        print(f"   📖 Reading: {csv_file}")
                        
                        with zip_file.open(csv_file) as csv_data:
                            # Read first few lines
                            content = csv_data.read().decode('utf-8', errors='ignore')
                            lines = content.split('\n')[:10]
                            
                            print(f"   📄 First 10 lines:")
                            for i, line in enumerate(lines):
                                if line.strip():
                                    print(f"      {i+1}: {line[:100]}...")
                            
                            return content
                    
                    return None
                    
            except zipfile.BadZipFile:
                print(f"   ❌ Not a valid ZIP file")
                return None
                
        else:
            print(f"   ❌ Download failed: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def test_recent_dispatch_files():
    """Test downloading recent dispatch files to find price data"""
    
    print("🔍 Testing recent NEMWeb dispatch files...")
    
    # Get the most recent dispatch files (from the output we saw)
    recent_files = [
        "https://nemweb.com.au/Reports/Current/DispatchIS_Reports/PUBLIC_DISPATCHIS_202509111655_0000000480215212.zip",
        "https://nemweb.com.au/Reports/Current/DispatchIS_Reports/PUBLIC_DISPATCHIS_202509111650_0000000480214720.zip",
        "https://nemweb.com.au/Reports/Current/DispatchIS_Reports/PUBLIC_DISPATCHIS_202509111645_0000000480214202.zip",
        "https://nemweb.com.au/Reports/Current/DispatchIS_Reports/PUBLIC_DISPATCHIS_202509111640_0000000480213749.zip",
        "https://nemweb.com.au/Reports/Current/DispatchIS_Reports/PUBLIC_DISPATCHIS_202509111635_0000000480213198.zip",
    ]
    
    successful_extractions = []
    
    for file_url in recent_files:
        content = download_and_extract_nemweb_file(file_url)
        if content:
            successful_extractions.append((file_url, content))
            
        # Don't overwhelm the server
        time.sleep(1)
    
    return successful_extractions

def analyze_dispatch_data(content):
    """Analyze dispatch data to extract price information"""
    
    print(f"\n🔍 Analyzing dispatch data...")
    
    if not content:
        return None
    
    lines = content.split('\n')
    print(f"   📄 Total lines: {len(lines)}")
    
    # Look for price-related data
    price_data = []
    
    for line in lines:
        if line.strip():
            # Look for common price indicators
            if any(keyword in line.upper() for keyword in [
                'PRICE', 'DISPATCH', 'REGION', 'NSW', 'VIC', 'QLD', 'SA', 'TAS',
                'SPOT', 'MARKET', 'ENERGY', 'MWH', '$'
            ]):
                price_data.append(line)
    
    print(f"   📊 Found {len(price_data)} price-related lines")
    
    if price_data:
        print(f"   📄 Sample price data:")
        for i, line in enumerate(price_data[:10]):  # Show first 10
            print(f"      {i+1}: {line[:100]}...")
    
    return price_data

def test_price_and_demand_files():
    """Test accessing price and demand files directly"""
    
    print(f"\n🔍 Testing direct price and demand file access...")
    
    # Try different date formats and regions
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    
    regions = ['NSW1', 'VIC1', 'QLD1', 'SA1', 'TAS1']
    
    for date in [today, yesterday]:
        date_str = date.strftime('%Y%m%d')
        
        for region in regions:
            # Try different URL patterns
            url_patterns = [
                f"https://www.aemo.com.au/aemo/data/nem/priceanddemand/PRICE_AND_DEMAND_{date_str}_{region}.csv",
                f"https://nemweb.com.au/Reports/Current/Price_And_Demand/PRICE_AND_DEMAND_{date_str}_{region}.csv",
                f"https://www.aemo.com.au/aemo/data/nem/priceanddemand/PRICE_AND_DEMAND_{date_str}_{region}.zip",
                f"https://nemweb.com.au/Reports/Current/Price_And_Demand/PRICE_AND_DEMAND_{date_str}_{region}.zip",
            ]
            
            for url in url_patterns:
                try:
                    print(f"\n🔍 Testing: {url}")
                    response = requests.get(url, timeout=10)
                    print(f"   Status: {response.status_code}")
                    
                    if response.status_code == 200:
                        print(f"   ✅ Found data!")
                        
                        # Check if it's CSV or ZIP
                        if url.endswith('.csv'):
                            content = response.text
                            print(f"   📄 CSV content preview:")
                            lines = content.split('\n')[:5]
                            for line in lines:
                                if line.strip():
                                    print(f"      {line}")
                        else:
                            # It's a ZIP file
                            content = download_and_extract_nemweb_file(url)
                        
                        return url, content
                        
                except Exception as e:
                    print(f"   ❌ Error: {e}")
    
    return None, None

def main():
    print("🚀 NEMWeb Data Extraction Test")
    print("=" * 50)
    
    # Test recent dispatch files
    successful_extractions = test_recent_dispatch_files()
    
    # Analyze the data
    if successful_extractions:
        print(f"\n📊 Analyzing extracted data...")
        for url, content in successful_extractions:
            price_data = analyze_dispatch_data(content)
            if price_data:
                print(f"   ✅ Found price data in: {url}")
                break
    
    # Test direct price and demand files
    price_url, price_content = test_price_and_demand_files()
    
    print(f"\n📊 SUMMARY:")
    print(f"Successful dispatch extractions: {len(successful_extractions)}")
    print(f"Direct price file access: {'✅' if price_url else '❌'}")
    
    if successful_extractions or price_url:
        print(f"\n✅ SUCCESS: Found real electricity data sources!")
        print(f"   - NEMWeb dispatch files contain real-time data")
        print(f"   - Can extract price information from these files")
        print(f"   - Ready to integrate into the dashboard")
    else:
        print(f"\n❌ No accessible price data found")
        print(f"   - May need different approach or authentication")

if __name__ == "__main__":
    main()
