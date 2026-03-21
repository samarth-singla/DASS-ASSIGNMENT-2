"""Profile endpoint tests."""

import requests


def test_get_profile_returns_200_and_required_fields(
    base_url: str, user_headers: dict[str, str]
) -> None:
    response = requests.get(f"{base_url}/profile", headers=user_headers, timeout=15)
    assert response.status_code == 200
    payload = response.json()
    for field in ["user_id", "name", "email", "phone", "wallet_balance", "loyalty_points"]:
        assert field in payload


def test_update_profile_valid_payload_succeeds(
    base_url: str, user_headers: dict[str, str]
) -> None:
    payload = {"name": "Aarav Test", "phone": "9876543210"}
    response = requests.put(
        f"{base_url}/profile", headers=user_headers, json=payload, timeout=15
    )
    assert response.status_code == 200


def test_update_profile_invalid_name_returns_400(
    base_url: str, user_headers: dict[str, str]
) -> None:
    payload = {"name": "A", "phone": "9876543210"}
    response = requests.put(
        f"{base_url}/profile", headers=user_headers, json=payload, timeout=15
    )
    assert response.status_code == 400


def test_update_profile_invalid_phone_returns_400(
    base_url: str, user_headers: dict[str, str]
) -> None:
    payload = {"name": "Aarav Test", "phone": "12345"}
    response = requests.put(
        f"{base_url}/profile", headers=user_headers, json=payload, timeout=15
    )
    assert response.status_code == 400
