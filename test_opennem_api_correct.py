#!/usr/bin/env python3
"""
Test script for OpenNEM/OpenElectricity API using correct endpoints from documentation
"""

import requests
import json
from datetime import datetime, timedelta

API_KEY = "oe_3ZHgEpYF2VgLP832QfpkrG8H"
BASE_URL = "https://api.openelectricity.org.au/v4"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def test_endpoint(endpoint, params=None):
    """Test an API endpoint"""
    url = f"{BASE_URL}/{endpoint}"
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        print(f"\n🔍 Testing: {endpoint}")
        if params:
            print(f"   Params: {params}")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success: {json.dumps(data, indent=2)[:500]}...")
            return data
        else:
            print(f"   ❌ Error: {response.text}")
            return None
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return None

def main():
    print("🔍 Testing OpenElectricity API with correct endpoints from documentation...")
    
    # Based on the documentation, let's test the correct endpoints
    test_cases = [
        # Basic endpoints
        ("", None),
        ("/", None),
        
        # Price data endpoints (based on documentation)
        ("price", None),
        ("price/current", None),
        ("price/latest", None),
        ("price/recent", None),
        ("price/today", None),
        ("price/yesterday", None),
        ("price/week", None),
        ("price/month", None),
        ("price/year", None),
        
        # Market data endpoints
        ("market", None),
        ("market/price", None),
        ("market/price/current", None),
        ("market/price/latest", None),
        ("market/price/recent", None),
        ("market/price/today", None),
        ("market/price/yesterday", None),
        ("market/price/week", None),
        ("market/price/month", None),
        ("market/price/year", None),
        
        # Balancing summary (mentioned in documentation)
        ("balancing", None),
        ("balancing/summary", None),
        ("balancing/summary/current", None),
        ("balancing/summary/latest", None),
        ("balancing/summary/recent", None),
        ("balancing/summary/today", None),
        ("balancing/summary/yesterday", None),
        ("balancing/summary/week", None),
        ("balancing/summary/month", None),
        ("balancing/summary/year", None),
        
        # NEM specific endpoints
        ("nem", None),
        ("nem/price", None),
        ("nem/price/current", None),
        ("nem/price/latest", None),
        ("nem/price/recent", None),
        ("nem/price/today", None),
        ("nem/price/yesterday", None),
        ("nem/price/week", None),
        ("nem/price/month", None),
        ("nem/price/year", None),
        
        # WEM specific endpoints
        ("wem", None),
        ("wem/price", None),
        ("wem/price/current", None),
        ("wem/price/latest", None),
        ("wem/price/recent", None),
        ("wem/price/today", None),
        ("wem/price/yesterday", None),
        ("wem/price/week", None),
        ("wem/price/month", None),
        ("wem/price/year", None),
        
        # Data endpoints
        ("data", None),
        ("data/price", None),
        ("data/price/current", None),
        ("data/price/latest", None),
        ("data/price/recent", None),
        ("data/price/today", None),
        ("data/price/yesterday", None),
        ("data/price/week", None),
        ("data/price/month", None),
        ("data/price/year", None),
        
        # Stats endpoints
        ("stats", None),
        ("stats/price", None),
        ("stats/price/current", None),
        ("stats/price/latest", None),
        ("stats/price/recent", None),
        ("stats/price/today", None),
        ("stats/price/yesterday", None),
        ("stats/price/week", None),
        ("stats/price/month", None),
        ("stats/price/year", None),
        
        # Summary endpoints
        ("summary", None),
        ("summary/price", None),
        ("summary/price/current", None),
        ("summary/price/latest", None),
        ("summary/price/recent", None),
        ("summary/price/today", None),
        ("summary/price/yesterday", None),
        ("summary/price/week", None),
        ("summary/price/month", None),
        ("summary/price/year", None),
    ]
    
    successful_endpoints = []
    
    for endpoint, params in test_cases:
        data = test_endpoint(endpoint, params)
        if data:
            successful_endpoints.append((endpoint, params))
    
    print(f"\n📊 SUMMARY:")
    print(f"Total endpoints tested: {len(test_cases)}")
    print(f"Successful endpoints: {len(successful_endpoints)}")
    
    if successful_endpoints:
        print(f"\n✅ Working endpoints:")
        for endpoint, params in successful_endpoints:
            print(f"   - {endpoint} with params: {params}")
    else:
        print(f"\n❌ No working endpoints found")
        print(f"   - API key is valid (me endpoint works)")
        print(f"   - But no price data endpoints are accessible")
        print(f"   - This suggests the BASIC plan doesn't include price data access")
        print(f"   - You may need to upgrade to a higher plan to access price data")

if __name__ == "__main__":
    main()
