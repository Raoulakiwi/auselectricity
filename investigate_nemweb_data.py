#!/usr/bin/env python3
"""
Investigate NEMWeb data structure and find electricity price data
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime, timedelta
import re

def investigate_nemweb_directory(url, max_depth=2, current_depth=0):
    """Recursively investigate NEMWeb directory structure"""
    
    if current_depth >= max_depth:
        return []
    
    print(f"\n🔍 Investigating: {url} (depth: {current_depth})")
    
    try:
        response = requests.get(url, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for links
            links = soup.find_all('a')
            print(f"   Found {len(links)} links")
            
            interesting_links = []
            
            for link in links:
                href = link.get('href', '')
                text = link.get_text(strip=True)
                
                if href and not href.startswith('..') and not href.startswith('#'):
                    # Look for interesting patterns
                    if any(keyword in href.lower() or keyword in text.lower() for keyword in [
                        'price', 'dispatch', 'offer', 'bid', 'energy', 'demand', 'generation',
                        'trading', 'settlement', 'forecast', 'actual', 'current', 'realtime'
                    ]):
                        full_url = url.rstrip('/') + '/' + href.lstrip('/')
                        interesting_links.append({
                            'url': full_url,
                            'text': text,
                            'href': href
                        })
                        print(f"   📊 Interesting: {text} -> {href}")
            
            return interesting_links
            
        else:
            print(f"   ❌ Not accessible: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return []

def test_nemweb_data_access():
    """Test access to NEMWeb data directories"""
    
    print("🔍 Testing NEMWeb data access...")
    
    # Start with the working URLs we found
    base_urls = [
        "https://nemweb.com.au/Reports/Current/",
        "https://nemweb.com.au/Reports/Current/DispatchIS_Reports/",
    ]
    
    all_interesting_links = []
    
    for base_url in base_urls:
        print(f"\n📁 Exploring: {base_url}")
        interesting_links = investigate_nemweb_directory(base_url, max_depth=1)
        all_interesting_links.extend(interesting_links)
    
    return all_interesting_links

def test_aemo_dashboard_alternative():
    """Test alternative approaches to access AEMO dashboard data"""
    
    print(f"\n🔍 Testing alternative AEMO dashboard access...")
    
    # Try different user agents and headers
    headers_list = [
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        },
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
        },
        {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    ]
    
    dashboard_url = "https://www.aemo.com.au/energy-systems/electricity/national-electricity-market-nem/data-nem/data-dashboard-nem"
    
    for i, headers in enumerate(headers_list):
        try:
            print(f"\n🔍 Testing with headers {i+1}: {headers['User-Agent'][:50]}...")
            response = requests.get(dashboard_url, headers=headers, timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ Success with these headers!")
                return response
            else:
                print(f"   ❌ Still blocked: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return None

def search_for_public_aemo_data():
    """Search for publicly accessible AEMO data sources"""
    
    print(f"\n🔍 Searching for public AEMO data sources...")
    
    # Common public data endpoints
    public_endpoints = [
        "https://www.aemo.com.au/aemo/data/nem/priceanddemand/",
        "https://www.aemo.com.au/aemo/data/nem/priceanddemand/PRICE_AND_DEMAND_20250911_NSW1.csv",
        "https://www.aemo.com.au/aemo/data/nem/priceanddemand/PRICE_AND_DEMAND_20250911_VIC1.csv",
        "https://www.aemo.com.au/aemo/data/nem/priceanddemand/PRICE_AND_DEMAND_20250911_QLD1.csv",
        "https://www.aemo.com.au/aemo/data/nem/priceanddemand/PRICE_AND_DEMAND_20250911_SA1.csv",
        "https://www.aemo.com.au/aemo/data/nem/priceanddemand/PRICE_AND_DEMAND_20250911_TAS1.csv",
        "https://www.aemo.com.au/aemo/data/nem/priceanddemand/PRICE_AND_DEMAND_20250910_NSW1.csv",
        "https://www.aemo.com.au/aemo/data/nem/priceanddemand/PRICE_AND_DEMAND_20250910_VIC1.csv",
        "https://www.aemo.com.au/aemo/data/nem/priceanddemand/PRICE_AND_DEMAND_20250910_QLD1.csv",
        "https://www.aemo.com.au/aemo/data/nem/priceanddemand/PRICE_AND_DEMAND_20250910_SA1.csv",
        "https://www.aemo.com.au/aemo/data/nem/priceanddemand/PRICE_AND_DEMAND_20250910_TAS1.csv",
    ]
    
    working_endpoints = []
    
    for endpoint in public_endpoints:
        try:
            print(f"\n🔍 Testing: {endpoint}")
            response = requests.get(endpoint, timeout=5)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ Accessible!")
                working_endpoints.append(endpoint)
                
                # Check if it's CSV data
                if 'text/csv' in response.headers.get('content-type', '') or endpoint.endswith('.csv'):
                    print(f"   📊 CSV data found!")
                    # Show first few lines
                    lines = response.text.split('\n')[:5]
                    for line in lines:
                        if line.strip():
                            print(f"   - {line}")
                            
            elif response.status_code == 404:
                print(f"   ❌ Not found")
            else:
                print(f"   ⚠️  Status: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return working_endpoints

def main():
    print("🚀 AEMO Data Source Investigation")
    print("=" * 50)
    
    # Test NEMWeb data access
    interesting_links = test_nemweb_data_access()
    
    # Test alternative dashboard access
    dashboard_response = test_aemo_dashboard_alternative()
    
    # Search for public data endpoints
    working_endpoints = search_for_public_aemo_data()
    
    print(f"\n📊 SUMMARY:")
    print(f"Interesting NEMWeb links found: {len(interesting_links)}")
    print(f"Dashboard accessible: {'✅' if dashboard_response else '❌'}")
    print(f"Working public endpoints: {len(working_endpoints)}")
    
    if interesting_links:
        print(f"\n📊 Interesting NEMWeb links:")
        for link in interesting_links[:10]:  # Show first 10
            print(f"   - {link['text']} -> {link['url']}")
    
    if working_endpoints:
        print(f"\n✅ Working public data endpoints:")
        for endpoint in working_endpoints:
            print(f"   - {endpoint}")
    
    if not working_endpoints and not interesting_links:
        print(f"\n❌ No direct data access found")
        print(f"   - AEMO data may require authentication or registration")
        print(f"   - Consider using third-party tools like NEMED or NEMSEER")
        print(f"   - May need to scrape the dashboard with proper headers")

if __name__ == "__main__":
    main()
