from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_create_and_list_habit():
    r = client.post("/habits", json={"name": "Read 20 minutes"})
    assert r.status_code == 200
    hid = r.json()["id"]
    r2 = client.get("/habits")
    assert r2.status_code == 200
    assert any(h["id"] == hid for h in r2.json())


def test_checkin_flow():
    hid = client.post("/habits", json={"name": "Stretch"}).json()["id"]
    r = client.post(f"/habits/{hid}/checkin", json={"day": "2026-09-22"})
    assert r.status_code == 200
    r2 = client.get(f"/habits/{hid}/checkins")
    assert r2.json() == ["2026-09-22"]


def test_checkin_unknown_habit_404():
    r = client.post("/habits/99999/checkin", json={"day": "2026-09-22"})
    assert r.status_code == 404


def test_validation_empty_habit_name_422():
    for bad_name in ["", "   ", "\t\n", "\u200b", "​"]:
        r = client.post("/habits", json={"name": bad_name})
        assert r.status_code == 422


def test_validation_malformed_day_422():
    hid = client.post("/habits", json={"name": "Meditate"}).json()["id"]
    invalid_days = [
        "not-a-date",
        "2026-02-30",  # Invalid date in February
        "2026-13-45",  # Invalid month
        "20260922",  # Missing hyphens
        "2026-9-22",  # Missing leading zero
        "2026/09/22",  # Slashes instead of hyphens
        "yesterday",
        "",
    ]
    for bad_day in invalid_days:
        r = client.post(f"/habits/{hid}/checkin", json={"day": bad_day})
        assert r.status_code == 422
