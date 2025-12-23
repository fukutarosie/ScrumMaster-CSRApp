"""Test login API endpoint directly"""
import requests
import json

url = "http://localhost:5000/api/auth/login"

payload = {
    "username": "admin1",
    "password": "password123",
    "role_name": "User Admin"
}

print("\nTesting login API endpoint...")
print(f"URL: {url}")
print(f"Payload: {json.dumps(payload, indent=2)}")
print("\nSending request...\n")

try:
    response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"ERROR: {e}")


