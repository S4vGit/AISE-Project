import requests

BASE_URL = "http://127.0.0.1:8000"

def get_auth_token(role: str):
    if role == "A":
        login_data = {
            "user_id": "admin",
            "password": "admin"
        }
    elif role == "J":
        login_data = {
            "user_id": "claudia",
            "password": "claudia"
        }
    elif role == "R": 
        login_data = {
            "user_id": "sav",
            "password": "sav"
        }
    response = requests.post(f"{BASE_URL}/users/login", json=login_data)
    assert response.status_code == 200, f"Login failed: {response.text}"
    return response.json().get("token")

def test_generate_fake_news():
    token = get_auth_token("J")
    headers = {"Authorization": f"Bearer {token}"}

    with open(r"tests\utils\test9.jpeg", "rb") as img:
        files = {"file": img}
        response = requests.post(f"{BASE_URL}/fake-news/generate-fake-news", files=files, headers=headers)

    assert response.status_code == 200, f"Expected 200, but got {response.status_code}: {response.text}"
    data = response.json()
    assert "description" in data
    assert "fake_news" in data

def test_detect_fake_news():
    token = get_auth_token("R")
    headers = {"Authorization": f"Bearer {token}"}

    with open(r"tests\utils\test10.jpeg", "rb") as img:
        files = {"file": img}
        response = requests.post(f"{BASE_URL}/detection/detect-fake-news", files=files, headers=headers)

    assert response.status_code == 200, f"Expected 200, but got {response.status_code}: {response.text}"
    data = response.json()
    assert "description" in data
    assert "fake_news" in data
    assert "fake_probability" in data

def test_login():
    login_data = {
        "user_id": "sav",
        "password": "sav"
    }
    response = requests.post(f"{BASE_URL}/users/login", json=login_data)

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    data = response.json()
    assert "token" in data, "Missing 'token' in response"
    assert isinstance(data["token"], str), f"Expected 'token' to be a string, but got {type(data['token'])}"

def test_get_all_fake_news():
    token = get_auth_token("A")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/admin/overview", headers=headers)

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    data = response.json()
    assert isinstance(data, list), f"Expected response to be a list, but got {type(data)}"
    if data:
        for item in data:
            assert "description" in item, "Missing 'description' in fake news item"
            assert "generated_text" in item, "Missing 'generated_text' in fake news item"
            assert "fake_probability" in item, "Missing 'fake_probability' in fake news item"
            assert "image_path" in item, "Missing 'image_path' in fake news item"
            
def test_register():
    register_data = {
        "user_id": "test",
        "password": "test",
        "role": "J"
    }
    response = requests.post(f"{BASE_URL}/users/register", json=register_data)

    assert response.status_code in [200, 201], f"Expected 200 or 201, but got {response.status_code}: {response.text}"
    data = response.json()
    assert "user_id" in data, "Missing 'user_id' in response"
    assert data["user_id"] == register_data["user_id"], f"Expected 'user_id' to be {register_data['user_id']}, but got {data['user_id']}"
    assert "role" in data, "Missing 'role' in response"
    assert data["role"] == register_data["role"], f"Expected 'role' to be {register_data['role']}, but got {data['role']}"
