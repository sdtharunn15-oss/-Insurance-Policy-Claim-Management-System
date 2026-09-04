def admin_headers(token):
    return {
        "Authorization": f"Bearer {token}"
    }


def create_customer(client, admin_token, create_users):

    response = client.post(
        f"/customers?user_id={create_users['customer'].id}",
        headers=admin_headers(admin_token),
        json={
            "name": "Report Customer",
            "email": "reportcustomer@test.com",
            "phone": "9999999999",
            "address": "Chennai"
        }
    )

    return response.json()



def create_policy(client, admin_token, customer_id):

    response = client.post(
        "/policies",
        headers=admin_headers(admin_token),
        json={
            "customer_id": customer_id,
            "policy_number": "REPORTPOL001",
            "policy_type": "Life Insurance",
            "premium_amount": 10000,
            "coverage_amount": 1000000,
            "policy_start_date": "2026-01-01",
            "policy_end_date": "2027-01-01",
            "status": "Active"
        }
    )

    return response.json()



def create_claim(
    client,
    customer_token,
    policy_id
):

    response = client.post(
        "/claims",
        headers={
            "Authorization": f"Bearer {customer_token}"
        },
        json={
            "policy_id": policy_id,
            "claim_amount": 50000,
            "claim_reason": "Hospital bill",
            "claim_date": "2026-02-01"
        }
    )

    return response.json()



def test_search_policy_report(
    client,
    admin_token,
    create_users
):

    customer = create_customer(
        client,
        admin_token,
        create_users
    )

    create_policy(
        client,
        admin_token,
        customer["id"]
    )


    response = client.get(
        "/reports/policies/search",
        params={
            "policy_number": "REPORTPOL001"
        },
        headers=admin_headers(admin_token)
    )


    assert response.status_code == 200

    assert (
        response.json()["policy_number"]
        ==
        "REPORTPOL001"
    )



def test_filter_claims_by_status(
    client,
    admin_token,
    customer_token,
    create_users
):

    customer = create_customer(
        client,
        admin_token,
        create_users
    )

    policy = create_policy(
        client,
        admin_token,
        customer["id"]
    )


    create_claim(
        client,
        customer_token,
        policy["id"]
    )


    response = client.get(
        "/reports/claims/status",
        params={
            "status": "Submitted"
        },
        headers=admin_headers(admin_token)
    )


    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )



def test_customer_claim_history(
    client,
    admin_token,
    customer_token,
    create_users
):

    customer = create_customer(
        client,
        admin_token,
        create_users
    )

    policy = create_policy(
        client,
        admin_token,
        customer["id"]
    )


    create_claim(
        client,
        customer_token,
        policy["id"]
    )


    response = client.get(
        f"/reports/customers/{customer['id']}/claims",
        headers=admin_headers(admin_token)
    )


    assert response.status_code == 200

    data = response.json()

    assert data["customer_id"] == customer["id"]

    assert data["total_claims"] >= 1



def test_customer_claim_history_not_found(
    client,
    admin_token
):

    response = client.get(
        "/reports/customers/999/claims",
        headers=admin_headers(admin_token)
    )


    assert response.status_code == 404



def test_summary_report(
    client,
    admin_token
):

    response = client.get(
        "/reports/summary",
        headers=admin_headers(admin_token)
    )


    assert response.status_code == 200

    data = response.json()

    assert "total_customers" in data

    assert "total_policies" in data

    assert "total_claims" in data



def test_claim_filter_pagination(
    client,
    admin_token
):

    response = client.get(
        "/reports/claims/status",
        params={
            "status": "Submitted",
            "page": 1,
            "limit": 5
        },
        headers=admin_headers(admin_token)
    )


    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )