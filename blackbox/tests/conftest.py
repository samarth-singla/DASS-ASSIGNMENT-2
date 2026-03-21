"""Shared fixtures for QuickCart black-box API tests."""

import os
from typing import Any, Dict, List

import pytest
import requests


BASE_URL = os.getenv("QUICKCART_BASE_URL", "http://localhost:8080/api/v1")
ROLL_NUMBER = os.getenv("QUICKCART_ROLL_NUMBER", "2024101020")
REQUEST_TIMEOUT = 15


@pytest.fixture(scope="session")
def base_url() -> str:
    return BASE_URL.rstrip("/")


@pytest.fixture(scope="session")
def admin_headers() -> Dict[str, str]:
    return {"X-Roll-Number": ROLL_NUMBER}


@pytest.fixture(scope="session")
def users(base_url: str, admin_headers: Dict[str, str]) -> List[Dict[str, Any]]:
    response = requests.get(
        f"{base_url}/admin/users", headers=admin_headers, timeout=REQUEST_TIMEOUT
    )
    response.raise_for_status()
    data = response.json()
    assert isinstance(data, list) and data, "Admin users endpoint returned no users."
    return data


@pytest.fixture(scope="session")
def valid_user_id(users: List[Dict[str, Any]]) -> int:
    return int(users[0]["user_id"])


@pytest.fixture(scope="session")
def user_headers(valid_user_id: int) -> Dict[str, str]:
    return {"X-Roll-Number": ROLL_NUMBER, "X-User-ID": str(valid_user_id)}


@pytest.fixture(scope="session")
def product_list(base_url: str, user_headers: Dict[str, str]) -> List[Dict[str, Any]]:
    response = requests.get(
        f"{base_url}/products", headers=user_headers, timeout=REQUEST_TIMEOUT
    )
    response.raise_for_status()
    data = response.json()
    assert isinstance(data, list) and data, "Products endpoint returned no active products."
    return data


@pytest.fixture(scope="session")
def active_product(product_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    for product in product_list:
        if int(product.get("stock_quantity", 0)) > 2:
            return product
    return product_list[0]  # pragma: no cover


@pytest.fixture(scope="session")
def coupon_codes(base_url: str, admin_headers: Dict[str, str]) -> List[str]:
    response = requests.get(
        f"{base_url}/admin/coupons", headers=admin_headers, timeout=REQUEST_TIMEOUT
    )
    response.raise_for_status()
    data = response.json()
    if not isinstance(data, list):
        return []  # pragma: no cover
    return [coupon.get("coupon_code") for coupon in data if coupon.get("coupon_code")]


@pytest.fixture(scope="session")
def valid_coupon_code(base_url: str, admin_headers: Dict[str, str]) -> str | None:
    response = requests.get(
        f"{base_url}/admin/coupons", headers=admin_headers, timeout=REQUEST_TIMEOUT
    )
    response.raise_for_status()
    coupons = response.json()
    if not isinstance(coupons, list):
        return None  # pragma: no cover
    for coupon in coupons:
        code = coupon.get("coupon_code")
        if code:
            return code
    return None  # pragma: no cover


@pytest.fixture(scope="function")
def clean_cart(base_url: str, user_headers: Dict[str, str]) -> None:
    requests.delete(f"{base_url}/cart/clear", headers=user_headers, timeout=REQUEST_TIMEOUT)
    yield
    requests.delete(f"{base_url}/cart/clear", headers=user_headers, timeout=REQUEST_TIMEOUT)


@pytest.fixture(scope="session")
def first_address_id(base_url: str, user_headers: Dict[str, str]) -> int:
    response = requests.get(
        f"{base_url}/addresses", headers=user_headers, timeout=REQUEST_TIMEOUT
    )
    response.raise_for_status()
    addresses = response.json()
    assert isinstance(addresses, list) and addresses, "No existing addresses available for tests."
    return int(addresses[0]["address_id"])


@pytest.fixture(scope="session")
def existing_order_id(base_url: str, user_headers: Dict[str, str]) -> int | None:
    response = requests.get(f"{base_url}/orders", headers=user_headers, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    orders = response.json()
    if isinstance(orders, list) and orders:
        return int(orders[0]["order_id"])
    return None  # pragma: no cover
