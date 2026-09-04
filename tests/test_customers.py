from app.models.customer import Customer


def get_admin_headers(admin_token):
    return {
        "Authorization": f"Bearer {admin_token}"
    }


def test_create_customer(client, admin_token, create_users):

    response = client.post(
        "/customers?user_id=" + str(create_users["customer"].id),
        headers=get_admin_headers(admin_token),
        json={
            "name": "John Customer",
            "email": "johncustomer@test.com",
            "phone": "9876543210",
            "address": "Chennai"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "John Customer"
    assert data["email"] == "johncustomer@test.com"



def test_create_customer_invalid_user(client, admin_token):

    response = client.post(
        "/customers?user_id=999",
        headers=get_admin_headers(admin_token),
        json={
            "name": "Invalid Customer",
            "email": "invalidcustomer@test.com",
            "phone": "9876543210",
            "address": "Chennai"
        }
    )

    assert response.status_code == 404

    assert response.json()["detail"] == "User not found"



def test_get_customers(client, admin_token):

    response = client.get(
        "/customers",
        headers=get_admin_headers(admin_token)
    )

    assert response.status_code == 200

    assert isinstance(response.json(), list)



def test_get_customer_not_found(client, admin_token):

    response = client.get(
        "/customers/999",
        headers=get_admin_headers(admin_token)
    )

    assert response.status_code == 404

    assert response.json()["detail"] == "Customer not found"



def test_update_customer(client, admin_token, create_users):

    create_response = client.post(
        "/customers?user_id=" + str(create_users["customer"].id),
        headers=get_admin_headers(admin_token),
        json={
            "name": "Old Name",
            "email": "oldcustomer@test.com",
            "phone": "9000000000",
            "address": "Old Address"
        }
    )

    customer_id = create_response.json()["id"]


    response = client.put(
        f"/customers/{customer_id}",
        headers=get_admin_headers(admin_token),
        json={
            "name": "Updated Name",
            "email": "updatedcustomer@test.com",
            "phone": "9999999999",
            "address": "Updated Address"
        }
    )


    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Updated Name"



def test_delete_customer(client, admin_token, create_users):

    create_response = client.post(
        "/customers?user_id=" + str(create_users["customer"].id),
        headers=get_admin_headers(admin_token),
        json={
            "name": "Delete Customer",
            "email": "deletecustomer@test.com",
            "phone": "8888888888",
            "address": "Chennai"
        }
    )

    customer_id = create_response.json()["id"]


    response = client.delete(
        f"/customers/{customer_id}",
        headers=get_admin_headers(admin_token)
    )


    assert response.status_code == 200

    assert (
        response.json()["message"]
        ==
        "Customer deleted successfully"
    )