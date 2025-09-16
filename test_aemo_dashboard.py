#!/usr/bin/env python3
"""
Test script to investigate AEMO NEM data dashboard structure and data sources
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime, timedelta

def test_aemo_dashboard():
    """Test AEMO NEM data dashboard access and structure"""
    
    print("🔍 Testing AEMO NEM Data Dashboard...")
    
    # AEMO NEM Data Dashboard URL
    dashboard_url = "https://www.aemo.com.au/energy-systems/electricity/national-electricity-market-nem/data-nem/data-dashboard-nem"
    
    try:
        # Test basic access to the dashboard
        print(f"\n📊 Testing dashboard access: {dashboard_url}")
        response = requests.get(dashboard_url, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Dashboard accessible")
            
            # Parse the HTML to understand the structure
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for data sources, APIs, or embedded data
            print(f"\n🔍 Analyzing dashboard structure...")
            
            # Check for embedded JavaScript data
            scripts = soup.find_all('script')
            data_sources = []
            
            for script in scripts:
                if script.string:
                    script_content = script.string
                    # Look for API endpoints, data URLs, or configuration
                    if any(keyword in script_content.lower() for keyword in ['api', 'data', 'price', 'nem', 'dashboard']):
                        data_sources.append(script_content[:200] + "..." if len(script_content) > 200 else script_content)
            
            print(f"   Found {len(data_sources)} potential data sources in scripts")
            
            # Look for iframe or embedded content
            iframes = soup.find_all('iframe')
            print(f"   Found {len(iframes)} iframes")
            
            for iframe in iframes:
                src = iframe.get('src', '')
                if src:
                    print(f"   - iframe src: {src}")
            
            # Look for data attributes or configuration
            elements_with_data = soup.find_all(attrs={'data-': True})
            print(f"   Found {len(elements_with_data)} elements with data attributes")
            
            # Look for specific dashboard elements
            dashboard_elements = soup.find_all(['div', 'section'], class_=lambda x: x and any(keyword in x.lower() for keyword in ['dashboard', 'price', 'data', 'chart']))
            print(f"   Found {len(dashboard_elements)} potential dashboard elements")
            
            return True
            
        else:
            print(f"   ❌ Dashboard not accessible: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error accessing dashboard: {e}")
        return False

def test_aemo_api_endpoints():
    """Test potential AEMO API endpoints"""
    
    print(f"\n🔍 Testing potential AEMO API endpoints...")
    
    # Common AEMO API patterns
    api_endpoints = [
        "https://api.aemo.com.au/v1/",
        "https://api.aemo.com.au/v2/",
        "https://data.aemo.com.au/",
        "https://nemweb.com.au/",
        "https://www.aemo.com.au/api/",
        "https://www.aemo.com.au/data/",
        "https://www.aemo.com.au/energy-systems/electricity/national-electricity-market-nem/data-nem/data-dashboard-nem/api/",
        "https://www.aemo.com.au/energy-systems/electricity/national-electricity-market-nem/data-nem/data-dashboard-nem/data/",
    ]
    
    working_endpoints = []
    
    for endpoint in api_endpoints:
        try:
            print(f"\n🔍 Testing: {endpoint}")
            response = requests.get(endpoint, timeout=5)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ Accessible")
                working_endpoints.append(endpoint)
            elif response.status_code == 404:
                print(f"   ❌ Not found")
            else:
                print(f"   ⚠️  Status: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return working_endpoints

def test_nemweb_access():
    """Test NEMWeb access (AEMO's data portal)"""
    
    print(f"\n🔍 Testing NEMWeb access...")
    
    # NEMWeb is AEMO's main data portal
    nemweb_urls = [
        "https://nemweb.com.au/",
        "https://nemweb.com.au/Reports/Current/",
        "https://nemweb.com.au/Reports/Current/DispatchIS_Reports/",
        "https://nemweb.com.au/Reports/Current/DispatchIS_Reports/Next_Day_Offer_Energy/",
        "https://nemweb.com.au/Reports/Current/DispatchIS_Reports/Next_Day_Offer_Energy/Next_Day_Offer_Energy_20250911/",
    ]
    
    working_urls = []
    
    for url in nemweb_urls:
        try:
            print(f"\n🔍 Testing: {url}")
            response = requests.get(url, timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ Accessible")
                working_urls.append(url)
                
                # Check if it's a directory listing
                if "Index of" in response.text or "Directory listing" in response.text:
                    print(f"   📁 Directory listing found")
                    
                    # Parse directory listing
                    soup = BeautifulSoup(response.content, 'html.parser')
                    links = soup.find_all('a')
                    print(f"   Found {len(links)} links in directory")
                    
                    # Look for recent data files
                    for link in links[:10]:  # Show first 10 links
                        href = link.get('href', '')
                        if href and not href.startswith('..'):
                            print(f"   - {href}")
                            
            elif response.status_code == 404:
                print(f"   ❌ Not found")
            else:
                print(f"   ⚠️  Status: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return working_urls

def main():
    print("🚀 AEMO NEM Data Dashboard Investigation")
    print("=" * 50)
    
    # Test dashboard access
    dashboard_accessible = test_aemo_dashboard()
    
    # Test API endpoints
    working_apis = test_aemo_api_endpoints()
    
    # Test NEMWeb access
    working_nemweb = test_nemweb_access()
    
    print(f"\n📊 SUMMARY:")
    print(f"Dashboard accessible: {'✅' if dashboard_accessible else '❌'}")
    print(f"Working API endpoints: {len(working_apis)}")
    print(f"Working NEMWeb URLs: {len(working_nemweb)}")
    
    if working_apis:
        print(f"\n✅ Working API endpoints:")
        for endpoint in working_apis:
            print(f"   - {endpoint}")
    
    if working_nemweb:
        print(f"\n✅ Working NEMWeb URLs:")
        for url in working_nemweb:
            print(f"   - {url}")
    
    if not working_apis and not working_nemweb:
        print(f"\n❌ No direct API access found")
        print(f"   - Dashboard may use embedded data or require authentication")
        print(f"   - May need to scrape the dashboard directly")
        print(f"   - Consider using third-party tools like NEMED or NEMSEER")

if __name__ == "__main__":
    main()
