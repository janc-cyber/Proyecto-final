import pytest
import json
from app import app, get_system_info, get_pipeline_stages


@pytest.fixture
def client():
    """Creates a test client for the Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ─── Route Tests ──────────────────────────────────────────────────────────────

class TestRoutes:
    def test_home_returns_200(self, client):
        """Home page should return HTTP 200."""
        response = client.get("/")
        assert response.status_code == 200

    def test_health_endpoint(self, client):
        """Health endpoint should return status ok."""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "ok"

    def test_info_endpoint(self, client):
        """Info endpoint should return app metadata."""
        response = client.get("/api/info")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "app_name" in data
        assert "version" in data
        assert "python_version" in data

    def test_pipeline_endpoint(self, client):
        """Pipeline endpoint should return list of stages."""
        response = client.get("/api/pipeline")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 6

    def test_invalid_route_returns_404(self, client):
        """Unknown routes should return 404."""
        response = client.get("/this-does-not-exist")
        assert response.status_code == 404


# ─── Logic Tests ──────────────────────────────────────────────────────────────

class TestBusinessLogic:
    def test_system_info_has_required_keys(self):
        """get_system_info() must contain all required fields."""
        info = get_system_info()
        required_keys = ["app_name", "version", "environment", "python_version", "platform", "timestamp"]
        for key in required_keys:
            assert key in info, f"Missing key: {key}"

    def test_system_info_app_name(self):
        """App name should be the expected value."""
        info = get_system_info()
        assert info["app_name"] == "DevOps CI/CD Dashboard"

    def test_pipeline_stages_count(self):
        """Pipeline must have exactly 6 stages."""
        stages = get_pipeline_stages()
        assert len(stages) == 6

    def test_pipeline_stages_have_required_fields(self):
        """Each pipeline stage must have id, name, icon, status, description."""
        stages = get_pipeline_stages()
        for stage in stages:
            assert "id" in stage
            assert "name" in stage
            assert "icon" in stage
            assert "status" in stage
            assert "description" in stage

    def test_pipeline_ids_are_sequential(self):
        """Pipeline stage IDs must be sequential starting from 1."""
        stages = get_pipeline_stages()
        ids = [s["id"] for s in stages]
        assert ids == list(range(1, len(stages) + 1))

    def test_pipeline_last_stage_is_deploy(self):
        """The final pipeline stage should be Deploy."""
        stages = get_pipeline_stages()
        assert stages[-1]["name"] == "Deploy"
