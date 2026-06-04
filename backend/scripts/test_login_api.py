import requests

def test_login():
    url = "http://127.0.0.1:8000/api/auth/login/"
    data = {
        "username": "EST-001",
        "password": "password123"
    }
    try:
        response = requests.post(url, json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_login()
