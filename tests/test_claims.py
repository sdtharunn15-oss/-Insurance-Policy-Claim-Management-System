def admin_headers(token):
    return {
        "Authorization": f"Bearer {token}"
    }


def agent_headers(token):
    return {
        "Authorization": f"Bearer {token}"
    }


def create_customer(client, admin_token, create_users):

    response = client.post(
        f"/customers?user_id={create_users['customer'].id}",
        headers=admin_headers(admin_token),
        json={
            "name": "Claim Customer",
            "email": "claimcustomer@test.com",
            "phone": "9876543210",
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
            "policy_number": "CLAIMPOL001",
            "policy_type": "Health",
            "premium_amount": 5000,
            "coverage_amount": 500000,
            "policy_start_date": "2026-01-01",
            "policy_end_date": "2027-01-01",
            "status": "Active"
        }
    )

    return response.json()



def create_claim(client, customer_token, policy_id):

    response = client.post(
        "/claims",
        headers=agent_headers(customer_token),
        json={
            "policy_id": policy_id,
            "claim_amount": 100000,
            "claim_reason": "Medical expenses",
            "claim_date": "2026-02-01"
        }
    )

    return response



def test_create_claim(
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


    response = create_claim(
        client,
        customer_token,
        policy["id"]
    )


    assert response.status_code == 201

    assert (
        response.json()["claim_status"]
        ==
        "Submitted"
    )



def test_claim_amount_exceeds_coverage(
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


    response = client.post(
        "/claims",
        headers=agent_headers(customer_token),
        json={
            "policy_id": policy["id"],
            "claim_amount": 9999999,
            "claim_reason": "High amount",
            "claim_date": "2026-02-01"
        }
    )


    assert response.status_code == 400

    assert (
        response.json()["detail"]
        ==
        "Claim amount exceeds policy coverage"
    )



def test_get_claims(
    client,
    customer_token
):

    response = client.get(
        "/claims",
        headers=agent_headers(customer_token)
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )



def test_verify_claim(
    client,
    admin_token,
    agent_token,
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


    claim = create_claim(
        client,
        customer_token,
        policy["id"]
    ).json()


    response = client.post(
        f"/claims/{claim['id']}/verify",
        headers=agent_headers(agent_token)
    )


    assert response.status_code == 200

    assert (
        response.json()["message"]
        ==
        "Claim verified successfully"
    )



def test_approve_claim(
    client,
    admin_token,
    agent_token,
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


    claim = create_claim(
        client,
        customer_token,
        policy["id"]
    ).json()


    client.post(
        f"/claims/{claim['id']}/verify",
        headers=agent_headers(agent_token)
    )


    response = client.post(
        f"/claims/{claim['id']}/approve",
        headers=agent_headers(agent_token)
    )


    assert response.status_code == 200

    assert (
        response.json()["message"]
        ==
        "Claim approved successfully"
    )



def test_reject_claim(
    client,
    admin_token,
    agent_token,
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


    claim = create_claim(
        client,
        customer_token,
        policy["id"]
    ).json()


    client.post(
        f"/claims/{claim['id']}/verify",
        headers=agent_headers(agent_token)
    )


    response = client.post(
        f"/claims/{claim['id']}/reject",
        headers=agent_headers(agent_token)
    )


    assert response.status_code == 200

    assert (
        response.json()["message"]
        ==
        "Claim rejected successfully"
    )