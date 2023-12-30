from typing import Generator

import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.routers.post import comment_db, post_db


@pytest.fixture(scope="session")
def client() -> Generator:
    yield TestClient(app)


@pytest.fixture(autouse=True)
def db() -> Generator:
    post_db.clear()
    comment_db.clear()
    yield
