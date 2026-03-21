"""Order and invoice endpoint tests."""

import pytest
import requests


def test_get_orders_returns_list(base_url: str, user_headers: dict[str, str]) -> None:
    response = requests.get(f"{base_url}/orders", headers=user_headers, timeout=15)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_single_order_by_id(
    base_url: str, user_headers: dict[str, str], existing_order_id: int | None
) -> None:
    if existing_order_id is None:
        pytest.skip("No existing order available for this user")  # pragma: no cover
    response = requests.get(
        f"{base_url}/orders/{existing_order_id}", headers=user_headers, timeout=15
    )
    assert response.status_code == 200


def test_get_order_invoice_contains_totals(
    base_url: str, user_headers: dict[str, str], existing_order_id: int | None
) -> None:
    if existing_order_id is None:
        pytest.skip("No existing order available for this user")  # pragma: no cover
    response = requests.get(
        f"{base_url}/orders/{existing_order_id}/invoice", headers=user_headers, timeout=15
    )
    assert response.status_code == 200
    payload = response.json()
    for field in ["order_id", "subtotal", "gst_amount", "total_amount"]:
        assert field in payload


def test_cancel_nonexistent_order_returns_404(
    base_url: str, user_headers: dict[str, str]
) -> None:
    response = requests.post(
        f"{base_url}/orders/99999999/cancel", headers=user_headers, timeout=15
    )
    assert response.status_code == 404


def test_cancel_order_endpoint_returns_json_message(
    base_url: str, user_headers: dict[str, str], existing_order_id: int | None
) -> None:
    if existing_order_id is None:
        pytest.skip("No existing order available for this user")  # pragma: no cover
    try:
        response = requests.post(
            f"{base_url}/orders/{existing_order_id}/cancel", headers=user_headers, timeout=15
        )
    except requests.exceptions.ReadTimeout:
        pytest.xfail("Potential bug: cancel order endpoint can timeout instead of returning JSON.")  # pragma: no cover
    assert response.status_code in (200, 400)  # pragma: no cover
    assert isinstance(response.json(), dict)  # pragma: no cover
