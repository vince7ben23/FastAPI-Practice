from fastapi.testclient import TestClient
from requests import Response


class TestPost:
    def test_create_post(self, client: TestClient) -> None:
        response = self._create_post(client)

        assert response.status_code == 201
        assert {"id": 0, "body": "test post"}.items() <= response.json().items()

    def test_get_post(self, client: TestClient) -> None:
        self._create_post(client)

        response = client.get("/post/0")
        assert response.status_code == 200
        assert response.json() == {"id": 0, "body": "test post"}

    def test_get_post_id_not_in_db(self, client: TestClient) -> None:
        response = client.get("/post/0")
        assert response.status_code == 200
        assert response.json() is None

    def test_get_posts(self, client: TestClient) -> None:
        self._create_post(client)
        response = client.get("/posts")
        assert response.status_code == 200
        assert response.json() == [{"id": 0, "body": "test post"}]

    def test_create_comment(self, client: TestClient) -> None:
        self._create_post(client)
        response = self._create_comment(client)
        assert response.status_code == 201
        assert {
            "id": 0,
            "body": "test comment",
            "post_id": 0,
        }.items() <= response.json().items()

    def test_create_comment_no_post_id(self, client: TestClient) -> None:
        response = self._create_comment(client)
        assert response.status_code == 404

    def test_get_comments_by_post_id(self, client: TestClient):
        self._create_post(client)
        self._create_comment(client)
        response = client.get("/post/0/comment")
        assert response.status_code == 200
        assert {"post_id": 0, "id": 0, "body": "test comment"} in response.json()

    def test_get_post_with_comments(self, client: TestClient):
        self._create_post(client)
        self._create_comment(client)
        response = client.get("/post_with_comments/0")
        assert response.status_code == 200
        assert {
            "post": {"id": 0, "body": "test post"},
            "comments": [{"post_id": 0, "id": 0, "body": "test comment"}],
        }.items() <= response.json().items()

    def test_get_post_with_comments_no_post_id(self, client: TestClient):
        response = client.get("/post_with_comments/0")
        assert response.status_code == 404

    def _create_post(self, client: TestClient) -> Response:
        response = client.post("/post", json={"body": "test post"})
        return response

    def _create_comment(self, client: TestClient) -> Response:
        response = client.post("/comment", json={"body": "test comment", "post_id": 0})
        return response
