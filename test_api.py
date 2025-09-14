#!/usr/bin/env python3
"""
Test script for the Schedule Builder API endpoints
"""
import requests
import json

# Base URL for the API (using port 8002 as specified in project memory)
BASE_URL = "http://localhost:8002"

def test_root_endpoint():
    """Test the root endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Root endpoint test: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error testing root endpoint: {e}")
        return False

def test_update_lecture():
    """Test the update lecture endpoint"""
    # Sample lecture data
    lecture_data = {
        "id": "lec_0",
        "lenda_e_rreg": "Mikroekonomia (MK)",
        "dep_reale_rreg": "Kon",
        "sem_rreg": "Semestri i parë (I)",
        "niveli_rreg": "Baçelor",
        "viti_rreg": "VITI I",
        "prof_rreg": "Ramiz Livoreka",
        "grup_rreg": "Gr. 1",
        "status_lende_rreg": "L",
        "qasja_lende_rreg": "O",
        "mesimdhe_lende_rreg": "P",
        "time_per_lec_rreg": 135
    }
    
    try:
        response = requests.put(f"{BASE_URL}/api/lectures/lec_0", json=lecture_data)
        print(f"Update lecture test: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Error testing update lecture endpoint: {e}")
        return False

def test_delete_lecture():
    """Test the delete lecture endpoint"""
    try:
        response = requests.delete(f"{BASE_URL}/api/lectures/lec_test")
        print(f"Delete lecture test: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Error testing delete lecture endpoint: {e}")
        return False

def main():
    """Main test function"""
    print("Testing Schedule Builder API endpoints")
    print("=" * 40)
    
    # Test root endpoint
    print("\n1. Testing root endpoint...")
    test_root_endpoint()
    
    # Test update lecture endpoint
    print("\n2. Testing update lecture endpoint...")
    test_update_lecture()
    
    # Test delete lecture endpoint
    print("\n3. Testing delete lecture endpoint...")
    test_delete_lecture()
    
    print("\n" + "=" * 40)
    print("API testing completed")

if __name__ == "__main__":
    main()