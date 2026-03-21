"""Review endpoint tests."""

import pytest
import requests


def test_get_reviews_returns_structure(
    base_url: str, user_headers: dict[str, str], active_product: dict[str, object]
) -> None:
    product_id = int(active_product["product_id"])
    response = requests.get(
        f"{base_url}/products/{product_id}/reviews", headers=user_headers, timeout=15
    )
    assert response.status_code == 200
    payload = response.json()
    assert "average_rating" in payload
    assert "reviews" in payload


def test_post_review_invalid_rating_returns_400(
    base_url: str, user_headers: dict[str, str], active_product: dict[str, object]
) -> None:
    product_id = int(active_product["product_id"])
    response = requests.post(
        f"{base_url}/products/{product_id}/reviews",
        headers=user_headers,
        json={"rating": 6, "comment": "bad"},
        timeout=15,
    )
    assert response.status_code == 400


def test_post_review_invalid_comment_length_returns_400(
    base_url: str, user_headers: dict[str, str], active_product: dict[str, object]
) -> None:
    product_id = int(active_product["product_id"])
    response = requests.post(
        f"{base_url}/products/{product_id}/reviews",
        headers=user_headers,
        json={"rating": 5, "comment": ""},
        timeout=15,
    )
    assert response.status_code == 400


def test_post_review_valid_payload_succeeds(
    base_url: str, user_headers: dict[str, str], active_product: dict[str, object]
) -> None:
    product_id = int(active_product["product_id"])
    response = requests.post(
        f"{base_url}/products/{product_id}/reviews",
        headers=user_headers,
        json={"rating": 5, "comment": "Very good product"},
        timeout=15,
    )
    assert response.status_code == 200


@pytest.mark.xfail(reason="Potential bug: average rating appears truncated to integer.")
def test_average_rating_supports_decimal_value(
    base_url: str, user_headers: dict[str, str], active_product: dict[str, object]
) -> None:
    product_id = int(active_product["product_id"])
    response = requests.get(
        f"{base_url}/products/{product_id}/reviews", headers=user_headers, timeout=15
    )
    payload = response.json()
    avg = payload["average_rating"]
    if payload.get("reviews"):
        assert isinstance(avg, float)
