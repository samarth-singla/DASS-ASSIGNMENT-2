"""Cart endpoint tests, including bug-focused assertions."""

import pytest
import requests


def test_get_cart_returns_required_structure(
    base_url: str, user_headers: dict[str, str]
) -> None:
    response = requests.get(f"{base_url}/cart", headers=user_headers, timeout=15)
    assert response.status_code == 200
    payload = response.json()
    for field in ["cart_id", "items", "total"]:
        assert field in payload


def test_add_nonexistent_product_returns_404(
    base_url: str, user_headers: dict[str, str], clean_cart: None
) -> None:
    response = requests.post(
        f"{base_url}/cart/add",
        headers=user_headers,
        json={"product_id": 99999999, "quantity": 1},
        timeout=15,
    )
    assert response.status_code == 404


def test_add_and_update_cart_item_success(
    base_url: str,
    user_headers: dict[str, str],
    active_product: dict[str, object],
    clean_cart: None,
) -> None:
    product_id = int(active_product["product_id"])
    add_response = requests.post(
        f"{base_url}/cart/add",
        headers=user_headers,
        json={"product_id": product_id, "quantity": 1},
        timeout=15,
    )
    assert add_response.status_code == 200

    update_response = requests.post(
        f"{base_url}/cart/update",
        headers=user_headers,
        json={"product_id": product_id, "quantity": 2},
        timeout=15,
    )
    assert update_response.status_code == 200


def test_update_cart_with_quantity_below_one_returns_400(
    base_url: str,
    user_headers: dict[str, str],
    active_product: dict[str, object],
    clean_cart: None,
) -> None:
    product_id = int(active_product["product_id"])
    response = requests.post(
        f"{base_url}/cart/update",
        headers=user_headers,
        json={"product_id": product_id, "quantity": 0},
        timeout=15,
    )
    assert response.status_code == 400


def test_remove_product_not_in_cart_returns_404(
    base_url: str, user_headers: dict[str, str], clean_cart: None
) -> None:
    response = requests.post(
        f"{base_url}/cart/remove",
        headers=user_headers,
        json={"product_id": 99999999},
        timeout=15,
    )
    assert response.status_code == 404


def test_clear_cart_empties_items(
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
    clear_response = requests.delete(f"{base_url}/cart/clear", headers=user_headers, timeout=15)
    assert clear_response.status_code == 200

    cart_response = requests.get(f"{base_url}/cart", headers=user_headers, timeout=15)
    assert cart_response.status_code == 200
    assert cart_response.json().get("items") == []


@pytest.mark.xfail(reason="Potential bug: quantity 0 add should be rejected with 400.")
def test_add_item_with_zero_quantity_rejected_per_spec(
    base_url: str,
    user_headers: dict[str, str],
    active_product: dict[str, object],
    clean_cart: None,
) -> None:
    product_id = int(active_product["product_id"])
    response = requests.post(
        f"{base_url}/cart/add",
        headers=user_headers,
        json={"product_id": product_id, "quantity": 0},
        timeout=15,
    )
    assert response.status_code == 400


@pytest.mark.xfail(reason="Potential bug: cart subtotal and total calculations are incorrect.")
def test_cart_subtotals_and_total_match_price_times_quantity(
    base_url: str,
    user_headers: dict[str, str],
    active_product: dict[str, object],
    clean_cart: None,
) -> None:
    product_id = int(active_product["product_id"])
    quantity = 2
    requests.post(
        f"{base_url}/cart/add",
        headers=user_headers,
        json={"product_id": product_id, "quantity": quantity},
        timeout=15,
    )
    cart = requests.get(f"{base_url}/cart", headers=user_headers, timeout=15).json()
    assert cart["items"], "Expected at least one cart item"
    item = cart["items"][0]
    expected_subtotal = item["unit_price"] * item["quantity"]
    assert item["subtotal"] == expected_subtotal
    expected_total = sum(entry["subtotal"] for entry in cart["items"])  # pragma: no cover
    assert cart["total"] == expected_total  # pragma: no cover
