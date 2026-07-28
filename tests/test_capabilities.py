import sys
from pathlib import Path

from fastapi.testclient import TestClient

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.app import app, capabilities


client = TestClient(app)


def test_capability_filter_implementation():
    response = client.get("/capabilities", params={"practice_area": "Technology"})

    assert response.status_code == 200
    data = response.json()
    assert data
    assert "Digital Strategy" not in data

    for capability in data.values():
        assert capability["practice_area"] == "Technology"


def test_capabilities_endpoint_returns_all_capabilities_without_filters():
    response = client.get("/capabilities")

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, dict)
    assert set(data.keys()) == set(capabilities.keys())

    sample_capability = data["Cloud Architecture"]
    assert "description" in sample_capability
    assert "practice_area" in sample_capability
    assert "skill_levels" in sample_capability
    assert "certifications" in sample_capability
    assert "industry_verticals" in sample_capability
    assert "capacity" in sample_capability
    assert "consultants" in sample_capability