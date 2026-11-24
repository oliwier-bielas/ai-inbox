from fastapi.testclient import TestClient
from pydantic import TypeAdapter

from app.email.exceptions import EmailNotFoundError
from app.email.schemas import EmailRead
from app.main import app

client = TestClient(app)


def test_get_emails() -> None:
    res = client.get("/emails")
    assert res.status_code == 200
    assert len(res.json()) == 3
    assert TypeAdapter(list[EmailRead]).validate_python(res.json())


def test_get_email_by_existing_id() -> None:
    email_id = 1
    res = client.get(f"/emails/{email_id}")

    assert res.status_code == 200

    assert res.json() == {
        "id": 1,
        "sender": "billing@example.com",
        "subject": "Invoice #TEST-001",
        "body": "Please pay the attached invoice of $100 by Friday.",
        "is_read": False,
    }


def test_get_email_by_fake_id() -> None:
    email_id = 99
    res = client.get(f"/emails/{email_id}")
    assert res.status_code == 404
    assert res.json() == {"detail": EmailNotFoundError(email_id).message}
