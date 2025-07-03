from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_count_reps():
    response = client.post(
        "/count-reps",
        json={"data": [{"x": 1, "y": 2, "z": 3}, {"x": 4, "y": 5, "z": 6}]},
    )
    assert response.status_code == 200
    assert response.json() == {"rep_count": 42}
