def test_get_users(api_client):
    """Test GET /users endpoint"""
    response = api_client.get_users()
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) > 0
    assert "name" in data[0]

def test_get_single_user(api_client):
    """Test GET /users/<id> endpoint"""
    response = api_client.get_user(2)
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == 2
    assert "email" in data

def test_create_user(api_client):
    """Test POST /users endpoint"""
    response = api_client.create_user("morpheus", "leader")
    assert response.status_code == 201
    
    data = response.json()
    assert data["name"] == "morpheus"
    assert data["job"] == "leader"
    assert "id" in data

def test_update_user(api_client):
    """Test PUT /users/<id> endpoint"""
    response = api_client.update_user(2, "morpheus", "zion resident")
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == "morpheus"
    assert data["job"] == "zion resident"

def test_delete_user(api_client):
    """Test DELETE /users/<id> endpoint"""
    response = api_client.delete_user(2)
    assert response.status_code == 200
