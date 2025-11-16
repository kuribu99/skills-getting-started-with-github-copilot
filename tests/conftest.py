import sys
from pathlib import Path
import copy
import pytest

# Ensure the 'src' directory is on the path so we can import the app module
SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from fastapi.testclient import TestClient  # noqa: E402
import app as appmodule  # noqa: E402


@pytest.fixture()
def client():
    """Provide a TestClient for the FastAPI app."""
    return TestClient(appmodule.app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset in-memory activities before and after each test to ensure isolation."""
    snapshot = copy.deepcopy(appmodule.activities)
    try:
        yield
    finally:
        appmodule.activities.clear()
        appmodule.activities.update(snapshot)
