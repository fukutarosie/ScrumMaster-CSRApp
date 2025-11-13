"""Quick check if both servers are running"""
import requests

print("=" * 60)
print("SERVER STATUS CHECK")
print("=" * 60)

# Check backend
try:
    response = requests.get('http://localhost:5000/api/roles/public', timeout=2)
    if response.status_code == 200:
        print("[OK] Backend (Flask) is running on http://localhost:5000")
    else:
        print(f"[WARN] Backend responded with status {response.status_code}")
except requests.exceptions.ConnectionError:
    print("[ERROR] Backend is NOT running on http://localhost:5000")
except Exception as e:
    print(f"[ERROR] Backend check failed: {e}")

# Check frontend
try:
    response = requests.get('http://localhost:3000', timeout=2)
    if response.status_code == 200:
        print("[OK] Frontend (Next.js) is running on http://localhost:3000")
    else:
        print(f"[WARN] Frontend responded with status {response.status_code}")
except requests.exceptions.ConnectionError:
    print("[ERROR] Frontend is NOT running on http://localhost:3000")
except Exception as e:
    print(f"[ERROR] Frontend check failed: {e}")

print("=" * 60)
print("\nYour app is ready at: http://localhost:3000")
print("=" * 60)





