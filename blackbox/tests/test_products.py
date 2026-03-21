"""Product listing and lookup tests."""

import requests


def test_products_list_returns_only_active_products(
    base_url: str, user_headers: dict[str, str]
) -> None:
    response = requests.get(f"{base_url}/products", headers=user_headers, timeout=15)
    assert response.status_code == 200
    products = response.json()
    assert isinstance(products, list)
    assert products
    assert all(product.get("is_active") is True for product in products)


def test_products_list_contains_required_fields(
    base_url: str, user_headers: dict[str, str]
) -> None:
    products = requests.get(f"{base_url}/products", headers=user_headers, timeout=15).json()
    sample = products[0]
    for field in ["product_id", "name", "category", "price", "stock_quantity", "is_active"]:
        assert field in sample


def test_product_lookup_by_valid_id(
    base_url: str, user_headers: dict[str, str], active_product: dict[str, object]
) -> None:
    product_id = int(active_product["product_id"])
    response = requests.get(f"{base_url}/products/{product_id}", headers=user_headers, timeout=15)
    assert response.status_code == 200
    payload = response.json()
    assert int(payload["product_id"]) == product_id


def test_product_lookup_nonexistent_id_returns_404(
    base_url: str, user_headers: dict[str, str]
) -> None:
    response = requests.get(f"{base_url}/products/99999999", headers=user_headers, timeout=15)
    assert response.status_code == 404


def test_products_filter_and_sort_are_accepted(
    base_url: str, user_headers: dict[str, str]
) -> None:
    response = requests.get(
        f"{base_url}/products",
        params={"category": "fruits", "search": "apple", "sort": "price_asc"},
        headers=user_headers,
        timeout=15,
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
