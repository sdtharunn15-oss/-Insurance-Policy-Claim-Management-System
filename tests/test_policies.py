from datetime import date


def admin_headers(token):
    return {
        "Authorization": f"Bearer {token}"
    }


def customer_headers(token):
    return {
        "Authorization": f"Bearer {token}"
    }


def create_test_customer(client, admin_token, create_users):

    response = client.post(
        f"/customers?user_id={create_users['customer'].id}",
        headers=admin_headers(admin_token),
        json={
            "name": "Test Customer",
            "email": "policycustomer@test.com",
            "phone": "9876543210",
            "address": "Chennai"
        }
    )

    return response.json()



def create_test_policy(client, admin_token, customer_id):

    response = client.post(
        "/policies",
        headers=admin_headers(admin_token),
        json={
            "customer_id": customer_id,
            "policy_number": "POL1001",
            "policy_type": "Health Insurance",
            "premium_amount": 5000,
            "coverage_amount": 500000,
            "policy_start_date": "2026-01-01",
            "policy_end_date": "2027-01-01",
            "status": "Active"
        }
    )

    return response



def test_create_policy(
    client,
    admin_token,
    create_users
):

    customer = create_test_customer(
        client,
        admin_token,
        create_users
    )

    response = create_test_policy(
        client,
        admin_token,
        customer["id"]
    )

    assert response.status_code == 201

    data = response.json()

    assert data["policy_number"] == "POL1001"
    assert data["status"] == "Active"



def test_duplicate_policy_number(
    client,
    admin_token,
    create_users
):

    customer = create_test_customer(
        client,
        admin_token,
        create_users
    )


    create_test_policy(
        client,
        admin_token,
        customer["id"]
    )


    response = create_test_policy(
        client,
        admin_token,
        customer["id"]
    )


    assert response.status_code == 400

    assert (
        response.json()["detail"]
        ==
        "Policy number already exists"
    )



def test_invalid_premium(
    client,
    admin_token,
    create_users
):

    customer = create_test_customer(
        client,
        admin_token,
        create_users
    )


    response = client.post(
        "/policies",
        headers=admin_headers(admin_token),
        json={
            "customer_id": customer["id"],
            "policy_number": "POL2001",
            "policy_type": "Life",
            "premium_amount": -100,
            "coverage_amount": 500000,
            "policy_start_date": "2026-01-01",
            "policy_end_date": "2027-01-01",
            "status": "Active"
        }
    )


    assert response.status_code == 422



def test_get_policies(
    client,
    admin_token
):

    response = client.get(
        "/policies",
        headers=admin_headers(admin_token)
    )


    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )



def test_search_policy(
    client,
    admin_token,
    create_users
):

    customer = create_test_customer(
        client,
        admin_token,
        create_users
    )


    create_test_policy(
        client,
        admin_token,
        customer["id"]
    )


    response = client.get(
        "/policies/search",
        params={
            "policy_number": "POL1001"
        },
        headers=admin_headers(admin_token)
    )


    assert response.status_code == 200

    assert (
        response.json()["policy_number"]
        ==
        "POL1001"
    )



def test_get_policy_not_found(
    client,
    admin_token
):

    response = client.get(
        "/policies/999",
        headers=admin_headers(admin_token)
    )


    assert response.status_code == 404



def test_update_policy(
    client,
    admin_token,
    create_users
):

    customer = create_test_customer(
        client,
        admin_token,
        create_users
    )


    policy_response = create_test_policy(
        client,
        admin_token,
        customer["id"]
    )

    policy_id = policy_response.json()["id"]


    response = client.put(
        f"/policies/{policy_id}",
        headers=admin_headers(admin_token),
        json={
            "policy_type": "Updated Health",
            "premium_amount": 7000,
            "coverage_amount": 800000,
            "policy_start_date": "2026-01-01",
            "policy_end_date": "2027-01-01",
            "status": "Active"
        }
    )


    assert response.status_code == 200

    assert (
        response.json()["policy_type"]
        ==
        "Updated Health"
    )