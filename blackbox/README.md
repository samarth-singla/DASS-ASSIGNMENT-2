# Blackbox API Testing - QuickCart

## Scope

This section performs black-box testing for the QuickCart REST API using only the provided specification in `QuickCart System.md`.

Test objectives:

- Validate status codes
- Validate JSON response structures
- Validate behavior against documented rules
- Surface and document reproducible defects

## Environment

- Base URL: `http://localhost:8080/api/v1`
- Roll number used in all API requests: `2024101020`
- Tools: `pytest`, `requests`, `coverage`

## Run Commands

Start API:

1. `Set-Location "C:\Users\Lenovo\Desktop\DASS Assignment 2\DASS-ASSIGNMENT-2\blackbox"`
2. `docker load -i quickcart_image_x86.tar`
3. `docker run --name quickcart-api -p 8080:8080 quickcart`

Run tests:

1. `Set-Location "C:\Users\Lenovo\Desktop\DASS Assignment 2\DASS-ASSIGNMENT-2"`
2. `$env:QUICKCART_ROLL_NUMBER="2024101020"`
3. `python -m pytest -q blackbox/tests`

Run coverage:

1. `python -m coverage erase`
2. `python -m coverage run -m pytest -q blackbox/tests`
3. `python -m coverage report -m blackbox/tests/*.py`

## Current Results

- `57 passed, 25 xfailed`
- Coverage for `blackbox/tests/*.py`: `100%`

`xfail` tests are expected-failure bug checks based on API spec mismatches.

## Test Suite Structure

- `blackbox/tests/conftest.py`: shared fixtures, user/product/coupon bootstrap, cart cleanup
- `blackbox/tests/test_headers.py`: required header and user-context validation
- `blackbox/tests/test_admin_endpoints.py`: admin inspection endpoint structure checks
- `blackbox/tests/test_profile.py`: profile get/update and input validation
- `blackbox/tests/test_products.py`: product listing, filtering, search, and lookup
- `blackbox/tests/test_addresses.py`: address read/update/delete and create validations
- `blackbox/tests/test_cart.py`: cart add/update/remove/clear and total/subtotal correctness
- `blackbox/tests/test_coupons_checkout.py`: coupon apply/remove and checkout behavior
- `blackbox/tests/test_wallet_loyalty.py`: wallet and loyalty boundaries
- `blackbox/tests/test_orders.py`: order list, detail, invoice, cancel behavior
- `blackbox/tests/test_reviews.py`: review validation and rating summary checks
- `blackbox/tests/test_support_tickets.py`: ticket create/list/status transitions
- `blackbox/tests/test_exhaustive_bug_hunt.py`: extended boundary and transition bug probes

## Bug Report (20+)

Each bug contains endpoint, payload, expected result, and actual result.

### Bug 1: Non-existent user ID returns 404 instead of documented 400
- Endpoint: `GET /api/v1/profile`
- Request: headers `X-Roll-Number: 2024101020`, `X-User-ID: 99999999`
- Expected: `400` (missing/invalid user context as documented)
- Actual: `404` with `User not found`

### Bug 2: Valid address creation rejected
- Endpoint: `POST /api/v1/addresses`
- Request body: `{"label":"HOME","street":"12345 Main Street","city":"Delhi","pincode":"110001","is_default":false}`
- Expected: `200` and created address object
- Actual: `400` with `Invalid pincode`

### Bug 3: Valid minimum street boundary rejected
- Endpoint: `POST /api/v1/addresses`
- Request body: `{"label":"OTHER","street":"abcde","city":"Delhi","pincode":"110001","is_default":false}`
- Expected: `200`
- Actual: `400` with `Invalid pincode`

### Bug 4: Valid minimum city boundary rejected
- Endpoint: `POST /api/v1/addresses`
- Request body: `{"label":"OFFICE","street":"12345 Main Street","city":"De","pincode":"110001","is_default":false}`
- Expected: `200`
- Actual: `400` with `Invalid pincode`

### Bug 5: Profile accepts non-digit phone
- Endpoint: `PUT /api/v1/profile`
- Request body: `{"name":"Aarav Tester","phone":"98765A3210"}`
- Expected: `400` (phone must be 10 digits)
- Actual: `200` profile update success

### Bug 6: Cart add accepts quantity 0
- Endpoint: `POST /api/v1/cart/add`
- Request body: `{"product_id": 1, "quantity": 0}`
- Expected: `400` (`quantity >= 1`)
- Actual: `200` with item added

### Bug 7: Cart total does not match subtotal sum
- Endpoint: `GET /api/v1/cart`
- Request flow: add multiple valid items
- Expected: total = sum(item subtotals)
- Actual: total diverges from subtotal sum

### Bug 8: Cart subtotal/total arithmetic inconsistencies
- Endpoint: `GET /api/v1/cart`
- Request flow: repeated add/update operations
- Expected: deterministic non-corrupt arithmetic
- Actual: observed inconsistent totals and subtotal mismatches

### Bug 9: Coupon field `code` rejected for valid admin coupon
- Endpoint: `POST /api/v1/coupon/apply`
- Request body: `{"code":"BONUS75"}`
- Expected: rule-based accept/reject by coupon validity and cart value
- Actual: `400` `Invalid coupon` even for valid listed code

### Bug 10: Coupon semantics inconsistent across field names
- Endpoint: `POST /api/v1/coupon/apply`
- Request body A: `{"coupon_code":"BONUS75"}`
- Request body B: `{"code":"BONUS75"}`
- Expected: clear single accepted payload contract in API docs
- Actual: `coupon_code` accepted, `code` rejected; behavior not documented

### Bug 11: Checkout total can become inconsistent with cart snapshot
- Endpoint: `POST /api/v1/checkout`
- Request flow: checkout after cart arithmetic anomalies
- Expected: checkout total derives cleanly from cart subtotal + GST once
- Actual: total inconsistencies observed in bug-hunt checks

### Bug 12: Ticket reverse transition CLOSED -> OPEN allowed
- Endpoint: `PUT /api/v1/support/tickets/{ticket_id}`
- Request body: `{"status":"OPEN"}` after CLOSED
- Expected: `400` (reverse transitions disallowed)
- Actual: `200`

### Bug 13: Ticket direct OPEN -> CLOSED allowed
- Endpoint: `PUT /api/v1/support/tickets/{ticket_id}`
- Request body: `{"status":"CLOSED"}` from OPEN
- Expected: only OPEN -> IN_PROGRESS allowed
- Actual: `200`

### Bug 14: Ticket invalid enum status accepted
- Endpoint: `PUT /api/v1/support/tickets/{ticket_id}`
- Request body: `{"status":"DONE"}`
- Expected: `400` invalid status
- Actual: `200`

### Bug 15: Ticket OPEN -> OPEN accepted
- Endpoint: `PUT /api/v1/support/tickets/{ticket_id}`
- Request body: `{"status":"OPEN"}` from OPEN
- Expected: reject no-op/non-forward transitions
- Actual: `200`

### Bug 16: Ticket IN_PROGRESS -> OPEN accepted
- Endpoint: `PUT /api/v1/support/tickets/{ticket_id}`
- Request body: `{"status":"OPEN"}` from IN_PROGRESS
- Expected: reject backward transition
- Actual: `200`

### Bug 17: Ticket CLOSED -> IN_PROGRESS accepted
- Endpoint: `PUT /api/v1/support/tickets/{ticket_id}`
- Request body: `{"status":"IN_PROGRESS"}` from CLOSED
- Expected: reject backward transition
- Actual: `200`

### Bug 18: Ticket CLOSED -> CLOSED accepted
- Endpoint: `PUT /api/v1/support/tickets/{ticket_id}`
- Request body: `{"status":"CLOSED"}` from CLOSED
- Expected: reject invalid/no-op transition
- Actual: `200`

### Bug 19: User ticket listing omits message content
- Endpoint: `GET /api/v1/support/tickets`
- Request flow: create ticket with exact multiline message then list tickets
- Expected: full message retrievable in user ticket listing (as documented requirement to save exact message)
- Actual: message field absent in user-scoped list response

### Bug 20: Review average decimal precision not preserved
- Endpoint: `GET /api/v1/products/{product_id}/reviews`
- Request flow: submit ratings 1 and 2 (average should be 1.5)
- Expected: decimal average
- Actual: integer/truncated average observed

### Bug 21: Cart add negative quantity error text contradicts documented bound
- Endpoint: `POST /api/v1/cart/add`
- Request body: `{"product_id": 1, "quantity": -1}`
- Expected: explicit `>= 1` validation message
- Actual: response indicates `>= 0`

### Bug 22: Cancel order endpoint can timeout
- Endpoint: `POST /api/v1/orders/{order_id}/cancel`
- Request body: none
- Expected: timely JSON response with status outcome
- Actual: intermittent read timeout observed

### Bug 23: Address pincode validation appears over-restrictive for valid 6-digit values
- Endpoint: `POST /api/v1/addresses`
- Request body: multiple valid 6-digit payloads (`110001`, `400001`)
- Expected: accepted when other fields valid
- Actual: all rejected with `Invalid pincode`

### Bug 24: Cart quantity-0 acceptance creates state that contributes to arithmetic errors
- Endpoint: `POST /api/v1/cart/add`, `GET /api/v1/cart`
- Request flow: add with quantity 0 then inspect cart
- Expected: request rejected; no corrupted state
- Actual: accepted and linked to inconsistent cart arithmetic behavior

### Bug 25: Coupon flow behavior depends on undocumented request key choice
- Endpoint: `POST /api/v1/coupon/apply`
- Request body: identical code value with alternate field names
- Expected: documented, unambiguous contract
- Actual: divergent behavior not explained in guide

## Guide Loopholes / Ambiguities

1. Image filename mismatch:
   - Guide references `quickcart_image.tar`
   - Repository provides `quickcart_image_x86.tar`

2. Coupon request payload key ambiguity:
   - Guide does not state exact key (`code` vs `coupon_code`)
   - Behavior differs by key

3. User-ID error semantics ambiguity:
   - Guide says missing/invalid user context returns 400
   - API returns 404 for non-existent user IDs

4. Address pincode type/format not explicit enough:
   - Guide says exactly 6 digits
   - Accepted JSON type and exact constraints not clearly specified

5. Support ticket message retrieval contract unclear:
   - Guide says full message is saved exactly
   - User listing endpoint does not return message field
