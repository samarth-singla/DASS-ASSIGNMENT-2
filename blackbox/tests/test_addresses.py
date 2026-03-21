"""Address endpoint tests including expected bug behavior markers."""

import pytest
import requests


def test_get_addresses_returns_list(base_url: str, user_headers: dict[str, str]) -> None:
    response = requests.get(f"{base_url}/addresses", headers=user_headers, timeout=15)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_delete_nonexistent_address_returns_404(
    base_url: str, user_headers: dict[str, str]
) -> None:
    response = requests.delete(f"{base_url}/addresses/9999999", headers=user_headers, timeout=15)
    assert response.status_code == 404


def test_update_address_allowed_fields_reflected_in_response(
    base_url: str, user_headers: dict[str, str], first_address_id: int
) -> None:
    payload = {"street": "888 QA Street", "is_default": False}
    response = requests.put(
        f"{base_url}/addresses/{first_address_id}", headers=user_headers, json=payload, timeout=15
    )
    assert response.status_code == 200
    body = response.json()
    assert body["address"]["street"] == "888 QA Street"
    assert body["address"]["is_default"] is False


def test_update_address_disallowed_fields_do_not_change(
    base_url: str, user_headers: dict[str, str], first_address_id: int
) -> None:
    before = requests.get(f"{base_url}/addresses", headers=user_headers, timeout=15).json()
    original = next(item for item in before if int(item["address_id"]) == first_address_id)

    response = requests.put(
        f"{base_url}/addresses/{first_address_id}",
        headers=user_headers,
        json={"label": "OFFICE", "city": "Delhi", "pincode": "123456"},
        timeout=15,
    )
    assert response.status_code == 200

    after = requests.get(f"{base_url}/addresses", headers=user_headers, timeout=15).json()
    updated = next(item for item in after if int(item["address_id"]) == first_address_id)
    assert updated["label"] == original["label"]
    assert updated["city"] == original["city"]
    assert updated["pincode"] == original["pincode"]


@pytest.mark.xfail(reason="Potential bug: valid 6-digit pincode is rejected by API.")
def test_create_address_with_valid_payload_succeeds_per_spec(
    base_url: str, user_headers: dict[str, str]
) -> None:
    payload = {
        "label": "OTHER",
        "street": "123 Main Street Sector 9",
        "city": "Mumbai",
        "pincode": "400001",
        "is_default": False,
    }
    response = requests.post(f"{base_url}/addresses", headers=user_headers, json=payload, timeout=15)
    assert response.status_code == 200


def test_create_address_with_invalid_label_returns_400(
    base_url: str, user_headers: dict[str, str]
) -> None:
    payload = {
        "label": "HOME2",
        "street": "123 Main Street Sector 9",
        "city": "Mumbai",
        "pincode": "400001",
        "is_default": False,
    }
    response = requests.post(f"{base_url}/addresses", headers=user_headers, json=payload, timeout=15)
    assert response.status_code == 400
