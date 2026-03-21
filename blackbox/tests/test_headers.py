"""Header validation tests for QuickCart API."""

import requests


def test_missing_roll_number_returns_401(base_url: str) -> None:
    response = requests.get(f"{base_url}/admin/users", timeout=15)
    assert response.status_code == 401


def test_invalid_roll_number_returns_400(base_url: str) -> None:
    response = requests.get(
        f"{base_url}/admin/users", headers={"X-Roll-Number": "abc"}, timeout=15
    )
    assert response.status_code == 400


def test_admin_endpoint_does_not_require_user_id(
    base_url: str, admin_headers: dict[str, str]
) -> None:
    response = requests.get(f"{base_url}/admin/products", headers=admin_headers, timeout=15)
    assert response.status_code == 200


def test_user_endpoint_missing_user_id_returns_400(
    base_url: str, admin_headers: dict[str, str]
) -> None:
    response = requests.get(f"{base_url}/profile", headers=admin_headers, timeout=15)
    assert response.status_code == 400


def test_user_endpoint_invalid_user_id_returns_400(
    base_url: str, admin_headers: dict[str, str]
) -> None:
    headers = dict(admin_headers)
    headers["X-User-ID"] = "xyz"
    response = requests.get(f"{base_url}/profile", headers=headers, timeout=15)
    assert response.status_code == 400


def test_user_endpoint_nonexistent_user_id_returns_400(
    base_url: str, admin_headers: dict[str, str]
) -> None:
    headers = dict(admin_headers)
    headers["X-User-ID"] = "99999999"
    response = requests.get(f"{base_url}/profile", headers=headers, timeout=15)
    assert response.status_code == 404
