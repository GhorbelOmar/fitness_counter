from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_count_reps():
    # A simple dataset representing one rep (e.g., a single up-down motion in y-axis)
    test_data = [
        {"x": 0, "y": 0, "z": 0},
        {"x": 0, "y": 1, "z": 0},
        {"x": 0, "y": 0, "z": 0},
        {"x": 0, "y": -1, "z": 0},
        {"x": 0, "y": 0, "z": 0},
    ]
    response = client.post(
        "/count-reps",
        json={"data": test_data},
    )
    assert response.status_code == 200
    assert response.json() == {"rep_count": 1}
