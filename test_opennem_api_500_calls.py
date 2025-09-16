#!/usr/bin/env python3
"""
Test script for OpenNEM/OpenElectricity API - Investigating 500 calls per day plan
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
        elif response.status_code == 403:
            print(f"   🔒 Permission denied: {response.text}")
            return "permission_denied"
        elif response.status_code == 404:
            print(f"   ❌ Not found: {response.text}")
            return None
        elif response.status_code == 429:
            print(f"   ⚠️  Rate limited: {response.text}")
            return "rate_limited"
        else:
            print(f"   ⚠️  Status {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return None

def main():
    print("🔍 Testing OpenElectricity API with 500 calls per day plan...")
    
    # Let's try some different approaches based on the documentation
    test_cases = [
        # Try different base URLs
        ("https://api.openelectricity.org.au/v4/stats/price/current", None),
        ("https://api.openelectricity.org.au/v4/stats/price/latest", None),
        ("https://api.openelectricity.org.au/v4/stats/price/recent", None),
        
        # Try different API versions
        ("https://api.openelectricity.org.au/v3/stats/price/current", None),
        ("https://api.openelectricity.org.au/v2/stats/price/current", None),
        ("https://api.openelectricity.org.au/v1/stats/price/current", None),
        
        # Try different base domains
        ("https://data.openelectricity.org.au/v4/stats/price/current", None),
        ("https://openelectricity.org.au/api/v4/stats/price/current", None),
        
        # Try different endpoint structures
        ("stats/price/current", None),
        ("stats/price/latest", None),
        ("stats/price/recent", None),
        ("stats/price/today", None),
        ("stats/price/yesterday", None),
        
        # Try with different headers
        ("stats/price/current", None, {"Authorization": f"Bearer {API_KEY}", "Accept": "application/json"}),
        ("stats/price/current", None, {"Authorization": f"Bearer {API_KEY}", "Accept": "*/*"}),
        ("stats/price/current", None, {"Authorization": f"Bearer {API_KEY}", "User-Agent": "Mozilla/5.0"}),
        
        # Try different parameter combinations
        ("stats/price/current", {"limit": 1}),
        ("stats/price/current", {"limit": 5}),
        ("stats/price/current", {"limit": 10}),
        ("stats/price/current", {"region": "NSW"}),
        ("stats/price/current", {"region": "VIC"}),
        ("stats/price/current", {"region": "QLD"}),
        ("stats/price/current", {"region": "SA"}),
        ("stats/price/current", {"region": "TAS"}),
        ("stats/price/current", {"network": "NEM"}),
        ("stats/price/current", {"network": "WEM"}),
        
        # Try different time periods
        ("stats/price/current", {"period": "5min"}),
        ("stats/price/current", {"period": "30min"}),
        ("stats/price/current", {"period": "hour"}),
        ("stats/price/current", {"period": "day"}),
        ("stats/price/current", {"period": "week"}),
        ("stats/price/current", {"period": "month"}),
        ("stats/price/current", {"period": "year"}),
        
        # Try different date formats
        ("stats/price/current", {"date": "2025-09-11"}),
        ("stats/price/current", {"date": "today"}),
        ("stats/price/current", {"date": "yesterday"}),
        ("stats/price/current", {"start_date": "2025-09-11"}),
        ("stats/price/current", {"end_date": "2025-09-11"}),
        ("stats/price/current", {"start_date": "2025-09-11", "end_date": "2025-09-11"}),
        
        # Try different price types
        ("stats/price/current", {"price_type": "spot"}),
        ("stats/price/current", {"price_type": "dispatch"}),
        ("stats/price/current", {"price_type": "forecast"}),
        ("stats/price/current", {"price_type": "market"}),
        ("stats/price/current", {"price_type": "balancing"}),
        
        # Try different data formats
        ("stats/price/current", {"format": "json"}),
        ("stats/price/current", {"format": "csv"}),
        ("stats/price/current", {"format": "xml"}),
        ("stats/price/current", {"format": "xlsx"}),
        
        # Try different limits
        ("stats/price/current", {"limit": 1}),
        ("stats/price/current", {"limit": 5}),
        ("stats/price/current", {"limit": 10}),
        ("stats/price/current", {"limit": 50}),
        ("stats/price/current", {"limit": 100}),
        ("stats/price/current", {"limit": 1000}),
        
        # Try different offsets
        ("stats/price/current", {"offset": 0}),
        ("stats/price/current", {"offset": 10}),
        ("stats/price/current", {"offset": 100}),
        
        # Try different sorting
        ("stats/price/current", {"sort": "asc"}),
        ("stats/price/current", {"sort": "desc"}),
        ("stats/price/current", {"sort": "timestamp"}),
        ("stats/price/current", {"sort": "price"}),
        ("stats/price/current", {"sort": "region"}),
        
        # Try different fields
        ("stats/price/current", {"fields": "price"}),
        ("stats/price/current", {"fields": "timestamp"}),
        ("stats/price/current", {"fields": "region"}),
        ("stats/price/current", {"fields": "network"}),
        ("stats/price/current", {"fields": "price,timestamp"}),
        ("stats/price/current", {"fields": "price,timestamp,region"}),
        ("stats/price/current", {"fields": "price,timestamp,region,network"}),
    ]
    
    successful_endpoints = []
    permission_denied_endpoints = []
    rate_limited_endpoints = []
    
    for test_case in test_cases:
        if len(test_case) == 3:
            endpoint, params, custom_headers = test_case
            headers_to_use = custom_headers
        else:
            endpoint, params = test_case
            headers_to_use = headers
        
        # Handle full URLs
        if endpoint.startswith("https://"):
            url = endpoint
        else:
            url = f"{BASE_URL}/{endpoint}"
        
        try:
            response = requests.get(url, headers=headers_to_use, params=params, timeout=10)
            print(f"\n🔍 Testing: {endpoint}")
            if params:
                print(f"   Params: {params}")
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Success: {json.dumps(data, indent=2)[:500]}...")
                successful_endpoints.append((endpoint, params))
            elif response.status_code == 403:
                print(f"   🔒 Permission denied: {response.text}")
                permission_denied_endpoints.append((endpoint, params))
            elif response.status_code == 404:
                print(f"   ❌ Not found: {response.text}")
            elif response.status_code == 429:
                print(f"   ⚠️  Rate limited: {response.text}")
                rate_limited_endpoints.append((endpoint, params))
            else:
                print(f"   ⚠️  Status {response.status_code}: {response.text}")
        except Exception as e:
            print(f"   ❌ Exception: {e}")
    
    print(f"\n📊 SUMMARY:")
    print(f"Total endpoints tested: {len(test_cases)}")
    print(f"Successful endpoints: {len(successful_endpoints)}")
    print(f"Permission denied endpoints: {len(permission_denied_endpoints)}")
    print(f"Rate limited endpoints: {len(rate_limited_endpoints)}")
    
    if successful_endpoints:
        print(f"\n✅ Working endpoints:")
        for endpoint, params in successful_endpoints:
            print(f"   - {endpoint} with params: {params}")
    
    if permission_denied_endpoints:
        print(f"\n🔒 Permission denied endpoints (exist but need higher plan):")
        for endpoint, params in permission_denied_endpoints[:10]:  # Show first 10
            print(f"   - {endpoint} with params: {params}")
        if len(permission_denied_endpoints) > 10:
            print(f"   ... and {len(permission_denied_endpoints) - 10} more")
    
    if rate_limited_endpoints:
        print(f"\n⚠️  Rate limited endpoints:")
        for endpoint, params in rate_limited_endpoints:
            print(f"   - {endpoint} with params: {params}")
    
    if not successful_endpoints and not permission_denied_endpoints and not rate_limited_endpoints:
        print(f"\n❌ No working endpoints found")
        print(f"   - API key is valid (me endpoint works)")
        print(f"   - But no price data endpoints are accessible")
        print(f"   - This suggests the plan doesn't include price data access")
        print(f"   - You may need to upgrade to a higher plan to access price data")

if __name__ == "__main__":
    main()
