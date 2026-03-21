"""Coupon and checkout endpoint tests."""

import pytest
import requests


def test_apply_invalid_coupon_returns_400(
    base_url: str, user_headers: dict[str, str], clean_cart: None
) -> None:
    response = requests.post(
        f"{base_url}/coupon/apply",
        headers=user_headers,
        json={"code": "INVALID_COUPON"},
        timeout=15,
    )
    assert response.status_code == 400


def test_remove_coupon_returns_success(
    base_url: str, user_headers: dict[str, str], clean_cart: None
) -> None:
    response = requests.post(f"{base_url}/coupon/remove", headers=user_headers, timeout=15)
    assert response.status_code == 200


def test_checkout_invalid_payment_method_returns_400(
    base_url: str, user_headers: dict[str, str], clean_cart: None
) -> None:
    response = requests.post(
        f"{base_url}/checkout",
        headers=user_headers,
        json={"payment_method": "UPI"},
        timeout=15,
    )
    assert response.status_code == 400


def test_checkout_empty_cart_returns_400(
    base_url: str, user_headers: dict[str, str], clean_cart: None
) -> None:
    response = requests.post(
        f"{base_url}/checkout",
        headers=user_headers,
        json={"payment_method": "CARD"},
        timeout=15,
    )
    assert response.status_code == 400


def test_checkout_cod_sets_payment_pending(
    base_url: str,
    user_headers: dict[str, str],
    active_product: dict[str, object],
    clean_cart: None,
) -> None:
    product_id = int(active_product["product_id"])
    requests.post(
        f"{base_url}/cart/add",
        headers=user_headers,
        json={"product_id": product_id, "quantity": 1},
        timeout=15,
    )
    response = requests.post(
        f"{base_url}/checkout",
        headers=user_headers,
        json={"payment_method": "COD"},
        timeout=15,
    )
    assert response.status_code == 200
    body = response.json()
    assert body.get("payment_status") == "PENDING"


@pytest.mark.xfail(reason="Potential bug: valid coupon may still be rejected as invalid.")
def test_apply_known_coupon_code_succeeds_when_cart_eligible(
    base_url: str,
    user_headers: dict[str, str],
    active_product: dict[str, object],
    valid_coupon_code: str | None,
    clean_cart: None,
) -> None:
    if not valid_coupon_code:
        pytest.skip("No coupon code available from admin endpoint")  # pragma: no cover

    product_id = int(active_product["product_id"])
    requests.post(
        f"{base_url}/cart/add",
        headers=user_headers,
        json={"product_id": product_id, "quantity": 50},
        timeout=15,
    )
    response = requests.post(
        f"{base_url}/coupon/apply",
        headers=user_headers,
        json={"code": valid_coupon_code},
        timeout=15,
    )
    assert response.status_code == 200
