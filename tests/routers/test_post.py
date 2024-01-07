from typing import AsyncGenerator

import pytest
from requests import Response


class TestPost:
    @pytest.mark.anyio
    async def test_create_post(self, async_client: AsyncGenerator) -> None:
        response = await async_client.post("/post", json={"body": "test post"})
        assert response.status_code == 201
        assert {"id": 1, "body": "test post"}.items() <= response.json().items()

    @pytest.mark.anyio
    async def test_get_post(
        self, async_client: AsyncGenerator, _create_post: Response
    ) -> None:
        response = await async_client.get(
            "/post/1",
        )
        assert response.status_code == 200
        assert response.json() == _create_post.json()

    @pytest.mark.anyio
    async def test_get_post_id_not_in_db(self, async_client: AsyncGenerator) -> None:
        response = await async_client.get("/post/1")
        assert response.status_code == 200
        assert response.json() is None

    @pytest.mark.anyio
    async def test_get_posts(
        self, async_client: AsyncGenerator, _create_post: Response
    ) -> None:
        response = await async_client.get("/posts")
        assert response.status_code == 200
        assert response.json() == [_create_post.json()]

    @pytest.mark.anyio
    async def test_create_comment(
        self, async_client: AsyncGenerator, _create_post: Response
    ) -> None:
        response = await async_client.post(
            "/comment", json={"body": "test comment", "post_id": 1}
        )
        assert response.status_code == 201
        assert {
            "id": 1,
            "body": "test comment",
            "post_id": _create_post.json()["id"],
        }.items() <= response.json().items()

    @pytest.mark.anyio
    async def test_create_comment_no_post_id(
        self, async_client: AsyncGenerator
    ) -> None:
        response = await async_client.post(
            "/comment", json={"body": "test comment", "post_id": 1}
        )
        assert response.status_code == 404

    @pytest.mark.anyio
    async def test_get_comments_by_post_id(
        self,
        async_client: AsyncGenerator,
        _create_post: Response,
        _create_comment: Response,
    ) -> None:
        response = await async_client.get("/post/1/comment")
        assert response.status_code == 200
        assert {
            "post_id": _create_post.json()["id"],
            "id": _create_comment.json()["id"],
            "body": "test comment",
        } in response.json()

    @pytest.mark.anyio
    async def test_get_post_with_comments(
        self,
        async_client: AsyncGenerator,
        _create_post: Response,
        _create_comment: Response,
    ) -> None:
        response = await async_client.get("/post_with_comments/1")
        assert response.status_code == 200
        assert {
            "post": _create_post.json(),
            "comments": [_create_comment.json()],
        }.items() <= response.json().items()

    @pytest.mark.anyio
    async def test_get_post_with_comments_no_post_id(
        self, async_client: AsyncGenerator
    ) -> None:
        response = await async_client.get("/post_with_comments/1")
        assert response.status_code == 404

    @pytest.fixture()
    async def _create_post(self, async_client: AsyncGenerator) -> Response:
        response = await async_client.post("/post", json={"body": "test post"})
        return response

    @pytest.fixture()
    async def _create_comment(self, async_client: AsyncGenerator) -> Response:
        response = await async_client.post(
            "/comment", json={"body": "test comment", "post_id": 1}
        )
        return response
