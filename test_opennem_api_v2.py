#!/usr/bin/env python3
"""
Test script for OpenNEM/OpenElectricity API - Alternative approaches
"""

import requests
import json

API_KEY = "oe_3ZHgEpYF2VgLP832QfpkrG8H"

def test_api_version(version):
    """Test different API versions"""
    base_urls = [
        f"https://api.openelectricity.org.au/{version}",
        f"https://api.opennem.org.au/{version}",
        f"https://opennem.org.au/api/{version}",
        f"https://api.opennem.org.au/{version}",
    ]
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    for base_url in base_urls:
        try:
            # Test /me endpoint first
            me_url = f"{base_url}/me"
            response = requests.get(me_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ Found working API: {base_url}")
                data = response.json()
                print(f"   Response: {json.dumps(data, indent=2)[:200]}...")
                
                # Now test some common endpoints
                test_endpoints = [
                    "price",
                    "prices", 
                    "electricity",
                    "nem",
                    "data",
                    "stats",
                    "summary",
                    "current",
                    "latest",
                    "recent"
                ]
                
                for endpoint in test_endpoints:
                    try:
                        test_url = f"{base_url}/{endpoint}"
                        test_response = requests.get(test_url, headers=headers, timeout=5)
                        if test_response.status_code == 200:
                            print(f"   ✅ Working endpoint: {endpoint}")
                        elif test_response.status_code == 401:
                            print(f"   🔒 Auth required: {endpoint}")
                        elif test_response.status_code == 403:
                            print(f"   🚫 Forbidden: {endpoint}")
                        elif test_response.status_code == 404:
                            print(f"   ❌ Not found: {endpoint}")
                        else:
                            print(f"   ⚠️  Status {test_response.status_code}: {endpoint}")
                    except:
                        pass
                
                return base_url
            else:
                print(f"❌ {base_url}: Status {response.status_code}")
        except Exception as e:
            print(f"❌ {base_url}: {e}")
    
    return None

def main():
    print("🔍 Testing OpenNEM/OpenElectricity API versions...")
    
    versions = ["v4", "v3", "v2", "v1", ""]
    
    for version in versions:
        print(f"\n📡 Testing version: {version if version else 'no version'}")
        working_api = test_api_version(version)
        if working_api:
            print(f"🎉 Found working API: {working_api}")
            break
    
    # Also try some alternative approaches
    print(f"\n🔍 Testing alternative approaches...")
    
    # Try without authentication
    try:
        response = requests.get("https://api.openelectricity.org.au/v4/", timeout=10)
        print(f"Public API status: {response.status_code}")
        if response.status_code == 200:
            print(f"Public API response: {response.text[:200]}...")
    except Exception as e:
        print(f"Public API error: {e}")
    
    # Try the old OpenNEM API
    try:
        response = requests.get("https://api.opennem.org.au/", timeout=10)
        print(f"Old OpenNEM API status: {response.status_code}")
        if response.status_code == 200:
            print(f"Old OpenNEM API response: {response.text[:200]}...")
    except Exception as e:
        print(f"Old OpenNEM API error: {e}")

if __name__ == "__main__":
    main()
