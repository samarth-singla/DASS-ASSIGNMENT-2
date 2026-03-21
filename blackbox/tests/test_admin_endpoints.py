"""Admin endpoint structure and status tests."""

import requests


ADMIN_ENDPOINTS = [
    "/admin/users",
    "/admin/carts",
    "/admin/orders",
    "/admin/products",
    "/admin/coupons",
    "/admin/tickets",
    "/admin/addresses",
]


def test_admin_endpoints_return_200_and_json_array(
    base_url: str, admin_headers: dict[str, str]
) -> None:
    for endpoint in ADMIN_ENDPOINTS:
        response = requests.get(f"{base_url}{endpoint}", headers=admin_headers, timeout=15)
        assert response.status_code == 200
        assert isinstance(response.json(), list)


def test_admin_users_contains_required_fields(
    base_url: str, admin_headers: dict[str, str]
) -> None:
    response = requests.get(f"{base_url}/admin/users", headers=admin_headers, timeout=15)
    users = response.json()
    assert users and isinstance(users, list)
    user = users[0]
    for field in ["user_id", "name", "email", "phone", "wallet_balance", "loyalty_points"]:
        assert field in user


def test_admin_products_includes_inactive_products(
    base_url: str, admin_headers: dict[str, str]
) -> None:
    response = requests.get(f"{base_url}/admin/products", headers=admin_headers, timeout=15)
    products = response.json()
    assert products and isinstance(products, list)
    assert any(product.get("is_active") is False for product in products)


def test_admin_single_user_lookup_returns_correct_user(
    base_url: str, admin_headers: dict[str, str], valid_user_id: int
) -> None:
    response = requests.get(
        f"{base_url}/admin/users/{valid_user_id}", headers=admin_headers, timeout=15
    )
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, dict)
    assert int(payload["user_id"]) == valid_user_id
