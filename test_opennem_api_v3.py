#!/usr/bin/env python3
"""
Test script for OpenNEM/OpenElectricity API - Final attempt with different approaches
"""

import requests
import json

API_KEY = "oe_3ZHgEpYF2VgLP832QfpkrG8H"
BASE_URL = "https://api.openelectricity.org.au/v4"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def test_endpoint_with_params(endpoint, params=None):
    """Test an endpoint with optional parameters"""
    url = f"{BASE_URL}/{endpoint}"
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        print(f"\n🔍 Testing: {endpoint}")
        if params:
            print(f"   Params: {params}")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success: {json.dumps(data, indent=2)[:300]}...")
            return data
        else:
            print(f"   ❌ Error: {response.text}")
            return None
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return None

def main():
    print("🔍 Testing OpenNEM/OpenElectricity API with different approaches...")
    
    # Test with different parameter combinations
    test_cases = [
        # Basic endpoints
        ("", None),
        ("/", None),
        ("docs", None),
        ("api", None),
        ("endpoints", None),
        ("help", None),
        
        # Price endpoints with different parameters
        ("price", {"region": "NSW"}),
        ("price", {"region": "VIC"}),
        ("price", {"region": "QLD"}),
        ("price", {"region": "SA"}),
        ("price", {"region": "TAS"}),
        ("price", {"region": "ALL"}),
        ("price", {"date": "2025-09-11"}),
        ("price", {"date": "today"}),
        ("price", {"date": "yesterday"}),
        ("price", {"period": "day"}),
        ("price", {"period": "week"}),
        ("price", {"period": "month"}),
        ("price", {"period": "year"}),
        ("price", {"format": "json"}),
        ("price", {"limit": 10}),
        ("price", {"limit": 100}),
        ("price", {"limit": 1000}),
        
        # Alternative endpoint names
        ("prices", {"region": "NSW"}),
        ("prices", {"region": "VIC"}),
        ("prices", {"region": "QLD"}),
        ("prices", {"region": "SA"}),
        ("prices", {"region": "TAS"}),
        ("prices", {"date": "2025-09-11"}),
        ("prices", {"date": "today"}),
        ("prices", {"date": "yesterday"}),
        ("prices", {"period": "day"}),
        ("prices", {"period": "week"}),
        ("prices", {"period": "month"}),
        ("prices", {"period": "year"}),
        ("prices", {"format": "json"}),
        ("prices", {"limit": 10}),
        ("prices", {"limit": 100}),
        ("prices", {"limit": 1000}),
        
        # Alternative endpoint names
        ("electricity", {"region": "NSW"}),
        ("electricity", {"region": "VIC"}),
        ("electricity", {"region": "QLD"}),
        ("electricity", {"region": "SA"}),
        ("electricity", {"region": "TAS"}),
        ("electricity", {"date": "2025-09-11"}),
        ("electricity", {"date": "today"}),
        ("electricity", {"date": "yesterday"}),
        ("electricity", {"period": "day"}),
        ("electricity", {"period": "week"}),
        ("electricity", {"period": "month"}),
        ("electricity", {"period": "year"}),
        ("electricity", {"format": "json"}),
        ("electricity", {"limit": 10}),
        ("electricity", {"limit": 100}),
        ("electricity", {"limit": 1000}),
        
        # Alternative endpoint names
        ("nem", {"region": "NSW"}),
        ("nem", {"region": "VIC"}),
        ("nem", {"region": "QLD"}),
        ("nem", {"region": "SA"}),
        ("nem", {"region": "TAS"}),
        ("nem", {"date": "2025-09-11"}),
        ("nem", {"date": "today"}),
        ("nem", {"date": "yesterday"}),
        ("nem", {"period": "day"}),
        ("nem", {"period": "week"}),
        ("nem", {"period": "month"}),
        ("nem", {"period": "year"}),
        ("nem", {"format": "json"}),
        ("nem", {"limit": 10}),
        ("nem", {"limit": 100}),
        ("nem", {"limit": 1000}),
        
        # Alternative endpoint names
        ("data", {"region": "NSW"}),
        ("data", {"region": "VIC"}),
        ("data", {"region": "QLD"}),
        ("data", {"region": "SA"}),
        ("data", {"region": "TAS"}),
        ("data", {"date": "2025-09-11"}),
        ("data", {"date": "today"}),
        ("data", {"date": "yesterday"}),
        ("data", {"period": "day"}),
        ("data", {"period": "week"}),
        ("data", {"period": "month"}),
        ("data", {"period": "year"}),
        ("data", {"format": "json"}),
        ("data", {"limit": 10}),
        ("data", {"limit": 100}),
        ("data", {"limit": 1000}),
    ]
    
    successful_endpoints = []
    
    for endpoint, params in test_cases:
        data = test_endpoint_with_params(endpoint, params)
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
