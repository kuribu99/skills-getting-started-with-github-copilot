from urllib.parse import quote


def test_get_activities(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Should have at least a couple of predefined activities
    assert "Chess Club" in data
    assert "Programming Class" in data
    # Each activity should have participants list
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_success_and_reflected_in_get(client):
    activity = "Art Club"
    email = "newstudent@mergington.edu"

    # Sign up
    resp = client.post(f"/activities/{quote(activity)}/signup?email={quote(email)}")
    assert resp.status_code == 200
    assert email in resp.json()["message"]

    # Verify via GET
    get_resp = client.get("/activities")
    assert get_resp.status_code == 200
    participants = get_resp.json()[activity]["participants"]
    assert email in participants


def test_signup_duplicate_returns_400(client):
    activity = "Programming Class"
    email = "emma@mergington.edu"  # already present in seed data

    # Try duplicate signup
    resp = client.post(f"/activities/{quote(activity)}/signup?email={quote(email)}")
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Student already signed up for this activity"


def test_signup_unknown_activity_returns_404(client):
    resp = client.post("/activities/Unknown%20Activity/signup?email=test@example.com")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Activity not found"


def test_unregister_success(client):
    activity = "Programming Class"
    email = "temp@mergington.edu"

    # Add first
    add = client.post(f"/activities/{quote(activity)}/signup?email={quote(email)}")
    assert add.status_code == 200

    # Remove
    remove = client.delete(
        f"/activities/{quote(activity)}/participants?email={quote(email)}"
    )
    assert remove.status_code == 200
    assert email in remove.json()["message"]

    # Verify removal
    get_resp = client.get("/activities")
    assert get_resp.status_code == 200
    participants = get_resp.json()[activity]["participants"]
    assert email not in participants


def test_unregister_not_registered_returns_404(client):
    activity = "Science Olympiad"
    email = "notjoined@mergington.edu"

    resp = client.delete(
        f"/activities/{quote(activity)}/participants?email={quote(email)}"
    )
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Student not registered for this activity"


def test_unregister_unknown_activity_returns_404(client):
    resp = client.delete(
        "/activities/Unknown%20Activity/participants?email=someone@example.com"
    )
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Activity not found"
