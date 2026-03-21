"""Wallet and loyalty endpoint tests."""

import pytest
import requests


def test_get_wallet_returns_balance_field(
    base_url: str, user_headers: dict[str, str]
) -> None:
    response = requests.get(f"{base_url}/wallet", headers=user_headers, timeout=15)
    assert response.status_code == 200
    payload = response.json()
    assert "wallet_balance" in payload


def test_wallet_add_invalid_amount_returns_400(
    base_url: str, user_headers: dict[str, str]
) -> None:
    response = requests.post(
        f"{base_url}/wallet/add", headers=user_headers, json={"amount": 0}, timeout=15
    )
    assert response.status_code == 400


def test_wallet_add_valid_amount_succeeds(
    base_url: str, user_headers: dict[str, str]
) -> None:
    response = requests.post(
        f"{base_url}/wallet/add", headers=user_headers, json={"amount": 10}, timeout=15
    )
    assert response.status_code == 200


def test_wallet_pay_invalid_amount_returns_400(
    base_url: str, user_headers: dict[str, str]
) -> None:
    response = requests.post(
        f"{base_url}/wallet/pay", headers=user_headers, json={"amount": 0}, timeout=15
    )
    assert response.status_code == 400


def test_get_loyalty_returns_points_field(
    base_url: str, user_headers: dict[str, str]
) -> None:
    response = requests.get(f"{base_url}/loyalty", headers=user_headers, timeout=15)
    assert response.status_code == 200
    payload = response.json()
    assert "loyalty_points" in payload


def test_loyalty_redeem_zero_points_returns_400(
    base_url: str, user_headers: dict[str, str]
) -> None:
    response = requests.post(
        f"{base_url}/loyalty/redeem", headers=user_headers, json={"points": 0}, timeout=15
    )
    assert response.status_code == 400


@pytest.mark.xfail(reason="Potential bug: wallet may deduct incorrect amount in some flows.")
def test_wallet_pay_deducts_exact_amount(
    base_url: str, user_headers: dict[str, str]
) -> None:
    before = requests.get(f"{base_url}/wallet", headers=user_headers, timeout=15).json()[
        "wallet_balance"
    ]
    amount = 1
    pay_response = requests.post(
        f"{base_url}/wallet/pay",
        headers=user_headers,
        json={"amount": amount},
        timeout=15,
    )
    assert pay_response.status_code == 200
    after = requests.get(f"{base_url}/wallet", headers=user_headers, timeout=15).json()[
        "wallet_balance"
    ]
    assert round(before - amount, 2) == round(after, 2)
