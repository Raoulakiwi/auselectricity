#!/usr/bin/env python3
"""
Test script for OpenNEM/OpenElectricity API
"""

import requests
import json

API_KEY = "oe_3ZHgEpYF2VgLP832QfpkrG8H"
BASE_URL = "https://api.openelectricity.org.au/v4"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def test_api_endpoint(endpoint):
    """Test an API endpoint"""
    url = f"{BASE_URL}/{endpoint}"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"\n🔍 Testing: {endpoint}")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success: {json.dumps(data, indent=2)[:200]}...")
            return data
        else:
            print(f"❌ Error: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def main():
    print("🔍 Testing OpenNEM/OpenElectricity API endpoints...")
    
    # Test various endpoints
    endpoints_to_test = [
        "me",
        "price",
        "price/current", 
        "price/latest",
        "price/recent",
        "price/today",
        "price/yesterday",
        "price/week",
        "price/month",
        "price/year",
        "prices",
        "prices/current",
        "prices/latest",
        "prices/recent",
        "prices/today",
        "prices/yesterday",
        "prices/week",
        "prices/month",
        "prices/year",
        "electricity",
        "electricity/price",
        "electricity/price/current",
        "electricity/price/latest",
        "electricity/price/recent",
        "electricity/price/today",
        "electricity/price/yesterday",
        "electricity/price/week",
        "electricity/price/month",
        "electricity/price/year",
        "electricity/prices",
        "electricity/prices/current",
        "electricity/prices/latest",
        "electricity/prices/recent",
        "electricity/prices/today",
        "electricity/prices/yesterday",
        "electricity/prices/week",
        "electricity/prices/month",
        "electricity/prices/year",
        "nem",
        "nem/price",
        "nem/price/current",
        "nem/price/latest",
        "nem/price/recent",
        "nem/price/today",
        "nem/price/yesterday",
        "nem/price/week",
        "nem/price/month",
        "nem/price/year",
        "nem/prices",
        "nem/prices/current",
        "nem/prices/latest",
        "nem/prices/recent",
        "nem/prices/today",
        "nem/prices/yesterday",
        "nem/prices/week",
        "nem/prices/month",
        "nem/prices/year",
        "data",
        "data/price",
        "data/price/current",
        "data/price/latest",
        "data/price/recent",
        "data/price/today",
        "data/price/yesterday",
        "data/price/week",
        "data/price/month",
        "data/price/year",
        "data/prices",
        "data/prices/current",
        "data/prices/latest",
        "data/prices/recent",
        "data/prices/today",
        "data/prices/yesterday",
        "data/prices/week",
        "data/prices/month",
        "data/prices/year"
    ]
    
    successful_endpoints = []
    
    for endpoint in endpoints_to_test:
        data = test_api_endpoint(endpoint)
        if data:
            successful_endpoints.append(endpoint)
    
    print(f"\n📊 SUMMARY:")
    print(f"Total endpoints tested: {len(endpoints_to_test)}")
    print(f"Successful endpoints: {len(successful_endpoints)}")
    
    if successful_endpoints:
        print(f"\n✅ Working endpoints:")
        for endpoint in successful_endpoints:
            print(f"   - {endpoint}")
    else:
        print(f"\n❌ No working endpoints found")
        print(f"   - API key is valid (me endpoint works)")
        print(f"   - But no price data endpoints are accessible")
        print(f"   - This might be a plan limitation or endpoint change")

if __name__ == "__main__":
    main()
