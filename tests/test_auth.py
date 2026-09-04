from app.models.user import User


def test_register_success(client):
    response = client.post(
        "/auth/register",
        json={
            "name": "New User",
            "email": "newuser@test.com",
            "password": "password123",
            "role": "Customer"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == "newuser@test.com"
    assert data["role"] == "Customer"



def test_register_duplicate_email(client):
    client.post(
        "/auth/register",
        json={
            "name": "User One",
            "email": "duplicate@test.com",
            "password": "password123",
            "role": "Customer"
        }
    )


    response = client.post(
        "/auth/register",
        json={
            "name": "User Two",
            "email": "duplicate@test.com",
            "password": "password123",
            "role": "Customer"
        }
    )


    assert response.status_code == 400

    assert response.json()["detail"] == "Email already registered"



def test_register_invalid_role(client):

    response = client.post(
        "/auth/register",
        json={
            "name": "Invalid Role",
            "email": "invalid@test.com",
            "password": "password123",
            "role": "Manager"
        }
    )


    assert response.status_code == 400

    assert response.json()["detail"] == "Invalid role"



def test_login_success(client):

    client.post(
        "/auth/register",
        json={
            "name": "Login User",
            "email": "login@test.com",
            "password": "password123",
            "role": "Customer"
        }
    )


    response = client.post(
        "/auth/login",
        json={
            "email": "login@test.com",
            "password": "password123"
        }
    )


    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"



def test_login_wrong_password(client):

    client.post(
        "/auth/register",
        json={
            "name": "Wrong Password",
            "email": "wrong@test.com",
            "password": "password123",
            "role": "Customer"
        }
    )


    response = client.post(
        "/auth/login",
        json={
            "email": "wrong@test.com",
            "password": "wrongpassword"
        }
    )


    assert response.status_code == 401

    assert response.json()["detail"] == "Invalid email or password"



def test_login_invalid_email(client):

    response = client.post(
        "/auth/login",
        json={
            "email": "notfound@test.com",
            "password": "password123"
        }
    )


    assert response.status_code == 401

    assert response.json()["detail"] == "Invalid email or password"