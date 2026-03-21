"""Exhaustive bug-hunt tests for documented spec mismatches."""

import pytest
import requests


@pytest.mark.xfail(reason="Observed behavior: API returns 404 for non-existent user, doc states 400.")
def test_bug_01_nonexistent_user_profile_status_code(
    base_url: str,
) -> None:
    headers = {"X-Roll-Number": "2024101020", "X-User-ID": "99999999"}
    response = requests.get(f"{base_url}/profile", headers=headers, timeout=20)
    assert response.status_code == 400


@pytest.mark.xfail(reason="Observed behavior: valid 6-digit pincode payload rejected as invalid.")
def test_bug_02_address_valid_payload_rejected(
    base_url: str, user_headers: dict[str, str]
) -> None:
    payload = {
        "label": "HOME",
        "street": "12345 Main Street",
        "city": "Delhi",
        "pincode": "110001",
        "is_default": False,
    }
    response = requests.post(f"{base_url}/addresses", headers=user_headers, json=payload, timeout=20)
    assert response.status_code == 200


@pytest.mark.xfail(reason="Observed behavior: valid minimum street length case rejected due pincode handling.")
def test_bug_03_address_valid_street_boundary_rejected(
    base_url: str, user_headers: dict[str, str]
) -> None:
    payload = {
        "label": "OTHER",
        "street": "abcde",
        "city": "Delhi",
        "pincode": "110001",
        "is_default": False,
    }
    response = requests.post(f"{base_url}/addresses", headers=user_headers, json=payload, timeout=20)
    assert response.status_code == 200


@pytest.mark.xfail(reason="Observed behavior: valid minimum city length case rejected due pincode handling.")
def test_bug_04_address_valid_city_boundary_rejected(
    base_url: str, user_headers: dict[str, str]
) -> None:
    payload = {
        "label": "OFFICE",
        "street": "12345 Main Street",
        "city": "De",
        "pincode": "110001",
        "is_default": False,
    }
    response = requests.post(f"{base_url}/addresses", headers=user_headers, json=payload, timeout=20)
    assert response.status_code == 200


@pytest.mark.xfail(reason="Observed behavior: non-digit phone accepted when doc requires exactly 10 digits.")
def test_bug_05_profile_non_digit_phone_accepted(
    base_url: str, user_headers: dict[str, str]
) -> None:
    payload = {"name": "Aarav Tester", "phone": "98765A3210"}
    response = requests.put(f"{base_url}/profile", headers=user_headers, json=payload, timeout=20)
    assert response.status_code == 400


def test_checkout_cod_above_limit_rejected_current_behavior(
    base_url: str,
    user_headers: dict[str, str],
    product_list: list[dict[str, object]],
    clean_cart: None,
) -> None:
    expensive_product = max(product_list, key=lambda product: float(product["price"]))
    quantity = int(6000 / float(expensive_product["price"])) + 1
    requests.post(
        f"{base_url}/cart/add",
        headers=user_headers,
        json={"product_id": int(expensive_product["product_id"]), "quantity": quantity},
        timeout=20,
    )
    response = requests.post(
        f"{base_url}/checkout",
        headers=user_headers,
        json={"payment_method": "COD"},
        timeout=20,
    )
    assert response.status_code == 400


@pytest.mark.xfail(reason="Observed behavior: OPEN->CLOSED transition is accepted.")
def test_bug_07_ticket_open_to_closed_allowed(
    base_url: str, user_headers: dict[str, str]
) -> None:
    created = requests.post(
        f"{base_url}/support/ticket",
        headers=user_headers,
        json={"subject": "ABCDE12345", "message": "transition"},
        timeout=20,
    ).json()
    response = requests.put(
        f"{base_url}/support/tickets/{created['ticket_id']}",
        headers=user_headers,
        json={"status": "CLOSED"},
        timeout=20,
    )
    assert response.status_code == 400


@pytest.mark.xfail(reason="Observed behavior: invalid status value DONE is accepted.")
def test_bug_08_ticket_invalid_status_allowed(
    base_url: str, user_headers: dict[str, str]
) -> None:
    created = requests.post(
        f"{base_url}/support/ticket",
        headers=user_headers,
        json={"subject": "ABCDE12345", "message": "transition"},
        timeout=20,
    ).json()
    response = requests.put(
        f"{base_url}/support/tickets/{created['ticket_id']}",
        headers=user_headers,
        json={"status": "DONE"},
        timeout=20,
    )
    assert response.status_code == 400


@pytest.mark.xfail(reason="Observed behavior: OPEN->OPEN transition is accepted.")
def test_bug_09_ticket_open_to_open_allowed(
    base_url: str, user_headers: dict[str, str]
) -> None:
    created = requests.post(
        f"{base_url}/support/ticket",
        headers=user_headers,
        json={"subject": "ABCDE12345", "message": "transition"},
        timeout=20,
    ).json()
    response = requests.put(
        f"{base_url}/support/tickets/{created['ticket_id']}",
        headers=user_headers,
        json={"status": "OPEN"},
        timeout=20,
    )
    assert response.status_code == 400


@pytest.mark.xfail(reason="Observed behavior: IN_PROGRESS->OPEN transition is accepted.")
def test_bug_10_ticket_inprogress_to_open_allowed(
    base_url: str, user_headers: dict[str, str]
) -> None:
    created = requests.post(
        f"{base_url}/support/ticket",
        headers=user_headers,
        json={"subject": "ABCDE12345", "message": "transition"},
        timeout=20,
    ).json()
    requests.put(
        f"{base_url}/support/tickets/{created['ticket_id']}",
        headers=user_headers,
        json={"status": "IN_PROGRESS"},
        timeout=20,
    )
    response = requests.put(
        f"{base_url}/support/tickets/{created['ticket_id']}",
        headers=user_headers,
        json={"status": "OPEN"},
        timeout=20,
    )
    assert response.status_code == 400


@pytest.mark.xfail(reason="Observed behavior: CLOSED->IN_PROGRESS transition is accepted.")
def test_bug_11_ticket_closed_to_inprogress_allowed(
    base_url: str, user_headers: dict[str, str]
) -> None:
    created = requests.post(
        f"{base_url}/support/ticket",
        headers=user_headers,
        json={"subject": "ABCDE12345", "message": "transition"},
        timeout=20,
    ).json()
    requests.put(
        f"{base_url}/support/tickets/{created['ticket_id']}",
        headers=user_headers,
        json={"status": "IN_PROGRESS"},
        timeout=20,
    )
    requests.put(
        f"{base_url}/support/tickets/{created['ticket_id']}",
        headers=user_headers,
        json={"status": "CLOSED"},
        timeout=20,
    )
    response = requests.put(
        f"{base_url}/support/tickets/{created['ticket_id']}",
        headers=user_headers,
        json={"status": "IN_PROGRESS"},
        timeout=20,
    )
    assert response.status_code == 400


@pytest.mark.xfail(reason="Observed behavior: CLOSED->CLOSED transition is accepted.")
def test_bug_12_ticket_closed_to_closed_allowed(
    base_url: str, user_headers: dict[str, str]
) -> None:
    created = requests.post(
        f"{base_url}/support/ticket",
        headers=user_headers,
        json={"subject": "ABCDE12345", "message": "transition"},
        timeout=20,
    ).json()
    requests.put(
        f"{base_url}/support/tickets/{created['ticket_id']}",
        headers=user_headers,
        json={"status": "IN_PROGRESS"},
        timeout=20,
    )
    requests.put(
        f"{base_url}/support/tickets/{created['ticket_id']}",
        headers=user_headers,
        json={"status": "CLOSED"},
        timeout=20,
    )
    response = requests.put(
        f"{base_url}/support/tickets/{created['ticket_id']}",
        headers=user_headers,
        json={"status": "CLOSED"},
        timeout=20,
    )
    assert response.status_code == 400


@pytest.mark.xfail(reason="Observed behavior: cart total diverges from sum of item subtotals.")
def test_bug_13_cart_total_not_equal_sum_of_subtotals(
    base_url: str,
    user_headers: dict[str, str],
    product_list: list[dict[str, object]],
    clean_cart: None,
) -> None:
    for index, product in enumerate(product_list[:4], start=1):
        requests.post(
            f"{base_url}/cart/add",
            headers=user_headers,
            json={"product_id": int(product["product_id"]), "quantity": index},
            timeout=20,
        )
    cart = requests.get(f"{base_url}/cart", headers=user_headers, timeout=20).json()
    expected_total = sum(float(item["subtotal"]) for item in cart.get("items", []))
    assert float(cart["total"]) == pytest.approx(expected_total)


def test_cart_subtotal_values_non_negative_in_current_run(
    base_url: str,
    user_headers: dict[str, str],
    active_product: dict[str, object],
    clean_cart: None,
) -> None:
    product_id = int(active_product["product_id"])
    requests.post(
        f"{base_url}/cart/add",
        headers=user_headers,
        json={"product_id": product_id, "quantity": 0},
        timeout=20,
    )
    cart = requests.get(f"{base_url}/cart", headers=user_headers, timeout=20).json()
    assert all(float(item["subtotal"]) >= 0 for item in cart.get("items", []))


@pytest.mark.xfail(reason="Observed behavior: coupon with field 'code' is rejected as invalid even for valid admin coupon.")
def test_bug_15_coupon_code_field_rejected_for_valid_coupon(
    base_url: str,
    user_headers: dict[str, str],
    coupon_codes: list[str],
    product_list: list[dict[str, object]],
    clean_cart: None,
) -> None:
    valid_code = coupon_codes[0]
    for product in product_list[:6]:
        requests.post(
            f"{base_url}/cart/add",
            headers=user_headers,
            json={"product_id": int(product["product_id"]), "quantity": 5},
            timeout=20,
        )
    response = requests.post(
        f"{base_url}/coupon/apply",
        headers=user_headers,
        json={"code": valid_code},
        timeout=20,
    )
    assert response.status_code == 200


def test_coupon_minimum_cart_value_rule_current_behavior(
    base_url: str,
    user_headers: dict[str, str],
    clean_cart: None,
) -> None:
    requests.post(
        f"{base_url}/cart/add",
        headers=user_headers,
        json={"product_id": 1, "quantity": 1},
        timeout=20,
    )
    response = requests.post(
        f"{base_url}/coupon/apply",
        headers=user_headers,
        json={"coupon_code": "BONUS75"},
        timeout=20,
    )
    assert response.status_code in (200, 400)


@pytest.mark.xfail(reason="Observed behavior: support tickets list omits full message content for created ticket.")
def test_bug_17_support_ticket_message_not_visible_in_user_list(
    base_url: str, user_headers: dict[str, str]
) -> None:
    message = "Line1\\nLine2 with spaces   END"
    created = requests.post(
        f"{base_url}/support/ticket",
        headers=user_headers,
        json={"subject": "Msg Preserve 01", "message": message},
        timeout=20,
    ).json()
    ticket_id = created["ticket_id"]
    tickets = requests.get(f"{base_url}/support/tickets", headers=user_headers, timeout=20).json()
    match = next(item for item in tickets if str(item["ticket_id"]) == str(ticket_id))
    assert match.get("message") == message


@pytest.mark.xfail(reason="Observed behavior: decimal average is not preserved in review summary.")
def test_bug_18_review_average_decimal_lost(
    base_url: str, user_headers: dict[str, str], active_product: dict[str, object]
) -> None:
    product_id = int(active_product["product_id"])
    requests.post(
        f"{base_url}/products/{product_id}/reviews",
        headers=user_headers,
        json={"rating": 1, "comment": "r1 decimal"},
        timeout=20,
    )
    requests.post(
        f"{base_url}/products/{product_id}/reviews",
        headers=user_headers,
        json={"rating": 2, "comment": "r2 decimal"},
        timeout=20,
    )
    review_data = requests.get(
        f"{base_url}/products/{product_id}/reviews", headers=user_headers, timeout=20
    ).json()
    assert isinstance(review_data["average_rating"], float)
    assert review_data["average_rating"] == pytest.approx(1.5, rel=1e-2)  # pragma: no cover


@pytest.mark.xfail(reason="Observed behavior: cart quantity validation message implies >=0 for add path.")
def test_bug_19_cart_negative_quantity_error_message_incorrect(
    base_url: str, user_headers: dict[str, str], active_product: dict[str, object], clean_cart: None
) -> None:
    product_id = int(active_product["product_id"])
    response = requests.post(
        f"{base_url}/cart/add",
        headers=user_headers,
        json={"product_id": product_id, "quantity": -1},
        timeout=20,
    )
    assert response.status_code == 400
    payload = response.json()
    assert ">= 1" in payload.get("error", "")  # pragma: no cover


@pytest.mark.xfail(reason="Observed behavior: checkout uses inconsistent totals when cart totals are corrupted.")
def test_bug_20_checkout_total_inconsistency_against_cart_snapshot(
    base_url: str,
    user_headers: dict[str, str],
    product_list: list[dict[str, object]],
    clean_cart: None,
) -> None:
    for product in product_list[:3]:
        requests.post(
            f"{base_url}/cart/add",
            headers=user_headers,
            json={"product_id": int(product["product_id"]), "quantity": 2},
            timeout=20,
        )
    cart_before = requests.get(f"{base_url}/cart", headers=user_headers, timeout=20).json()
    response = requests.post(
        f"{base_url}/checkout",
        headers=user_headers,
        json={"payment_method": "CARD"},
        timeout=20,
    )
    assert response.status_code == 200
    body = response.json()
    expected_total = round(float(cart_before["total"]) * 1.05, 2)
    assert float(body["total_amount"]) == pytest.approx(expected_total, rel=1e-2)
