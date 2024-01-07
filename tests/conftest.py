from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from src.database.database import database
from src.main import app


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture()
def client() -> Generator:
    yield TestClient(app)


@pytest.fixture(autouse=True)
async def db() -> AsyncGenerator:
    await database.connect()
    await reset_increment_seq()
    yield
    await database.disconnect()


@pytest.fixture()
async def async_client(client) -> AsyncGenerator:
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        yield ac


async def reset_increment_seq():
    # await database.execute("TRUNCATE TABLE posts, comments RESTART IDENTITY;")
    await database.execute("ALTER SEQUENCE posts_id_seq RESTART WITH 1;")
    await database.execute("ALTER SEQUENCE comments_id_seq RESTART WITH 1;")
