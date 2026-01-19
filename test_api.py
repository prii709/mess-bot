#!/usr/bin/env python3
"""
Test script for the Mess Bot API
Demonstrates all available endpoints and intents
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def print_response(endpoint, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"Endpoint: {endpoint}")
    print(f"Status: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2))
    print('='*60)

def test_api():
    """Test all API endpoints"""
    
    # Test root endpoint
    print("\n🔍 Testing Root Endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print_response("GET /", response)
    
    # Test health endpoint
    print("\n🏥 Testing Health Endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print_response("GET /health", response)
    
    # Test scheduler jobs endpoint
    print("\n⏰ Testing Scheduler Jobs Endpoint...")
    response = requests.get(f"{BASE_URL}/scheduler/jobs")
    print_response("GET /scheduler/jobs", response)
    
    # Test config endpoint
    print("\n⚙️  Testing Config Endpoint...")
    response = requests.get(f"{BASE_URL}/config")
    print_response("GET /config", response)
    
    # Test chat endpoint with different intents
    test_messages = [
        ("Show me the inventory", "Inventory Query"),
        ("Any low stock items?", "Low Stock Alert"),
        ("Show attendance statistics", "Attendance Stats"),
        ("Predict tomorrow's attendance", "Attendance Prediction"),
        ("What is the average feedback?", "Feedback Average"),
        ("Show low rating alerts", "Low Rating Alert"),
        ("Check inventory for rice", "Inventory Query for Item"),
        ("Hello, what can you do?", "General Query"),
    ]
    
    print("\n💬 Testing Chat Endpoint with Various Intents...")
    for message, description in test_messages:
        print(f"\n📝 {description}: '{message}'")
        response = requests.post(
            f"{BASE_URL}/chat",
            json={"message": message}
        )
        print_response("POST /chat", response)

if __name__ == "__main__":
    print("🤖 Mess Bot API Test Suite")
    print("="*60)
    
    try:
        test_api()
        print("\n✅ All tests completed successfully!")
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to the API server.")
        print("Please make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"\n❌ Error: {e}")
