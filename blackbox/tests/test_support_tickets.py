"""Support ticket endpoint tests."""

import pytest
import requests


def test_create_ticket_invalid_subject_returns_400(
    base_url: str, user_headers: dict[str, str]
) -> None:
    response = requests.post(
        f"{base_url}/support/ticket",
        headers=user_headers,
        json={"subject": "abc", "message": "Need help"},
        timeout=15,
    )
    assert response.status_code == 400


def test_create_ticket_invalid_message_returns_400(
    base_url: str, user_headers: dict[str, str]
) -> None:
    response = requests.post(
        f"{base_url}/support/ticket",
        headers=user_headers,
        json={"subject": "Valid Subject", "message": ""},
        timeout=15,
    )
    assert response.status_code == 400


def test_create_ticket_valid_payload_starts_open(
    base_url: str, user_headers: dict[str, str]
) -> None:
    response = requests.post(
        f"{base_url}/support/ticket",
        headers=user_headers,
        json={"subject": "Order Query", "message": "Need support for order"},
        timeout=15,
    )
    assert response.status_code == 200
    body = response.json()
    assert body.get("status") == "OPEN"


def test_get_support_tickets_returns_list(
    base_url: str, user_headers: dict[str, str]
) -> None:
    response = requests.get(f"{base_url}/support/tickets", headers=user_headers, timeout=15)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_ticket_status_forward_transitions_are_allowed(
    base_url: str, user_headers: dict[str, str]
) -> None:
    create = requests.post(
        f"{base_url}/support/ticket",
        headers=user_headers,
        json={"subject": "Flow Check", "message": "Track transitions"},
        timeout=15,
    ).json()
    ticket_id = create["ticket_id"]

    step1 = requests.put(
        f"{base_url}/support/tickets/{ticket_id}",
        headers=user_headers,
        json={"status": "IN_PROGRESS"},
        timeout=15,
    )
    step2 = requests.put(
        f"{base_url}/support/tickets/{ticket_id}",
        headers=user_headers,
        json={"status": "CLOSED"},
        timeout=15,
    )
    assert step1.status_code == 200
    assert step2.status_code == 200


@pytest.mark.xfail(reason="Potential bug: reverse status transition is accepted.")
def test_ticket_status_reverse_transition_rejected_per_spec(
    base_url: str, user_headers: dict[str, str]
) -> None:
    create = requests.post(
        f"{base_url}/support/ticket",
        headers=user_headers,
        json={"subject": "Reverse Flow", "message": "Should not reopen"},
        timeout=15,
    ).json()
    ticket_id = create["ticket_id"]

    requests.put(
        f"{base_url}/support/tickets/{ticket_id}",
        headers=user_headers,
        json={"status": "IN_PROGRESS"},
        timeout=15,
    )
    requests.put(
        f"{base_url}/support/tickets/{ticket_id}",
        headers=user_headers,
        json={"status": "CLOSED"},
        timeout=15,
    )
    reopen = requests.put(
        f"{base_url}/support/tickets/{ticket_id}",
        headers=user_headers,
        json={"status": "OPEN"},
        timeout=15,
    )
    assert reopen.status_code == 400
