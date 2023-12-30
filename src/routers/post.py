from typing import List, Union

from fastapi import APIRouter, HTTPException

from src.models.post import (
    Comment,
    CommentIn,
    UserPost,
    UserPostIn,
    UserPostWithComments,
)

post_router = APIRouter()


post_db = {}


@post_router.post("/post", status_code=201)
def create_post(post: UserPostIn) -> UserPost:
    data = post.model_dump()
    id = len(post_db)
    new_post = {"id": id, **data}
    post_db[id] = new_post
    return new_post


@post_router.get("/post/{id}")
def get_post(id: int) -> Union[None, UserPost]:
    return post_db.get(id)


@post_router.get("/posts")
def get_posts() -> List[UserPost]:
    return list(post_db.values())


comment_db = {}


@post_router.post("/comment", status_code=201)
def create_comment(comment: CommentIn) -> Comment:
    post = get_post(comment.post_id)
    if not post:
        raise HTTPException(404, "can not find the post.")
    data = comment.model_dump()
    comment_id = len(comment_db)
    new_comment = {"id": comment_id, **data}
    comment_db[comment_id] = new_comment
    return new_comment


@post_router.get("/post/{post_id}/comment")
def get_comments_by_post_id(post_id: int) -> List[Comment]:
    comments = [
        comment for comment in comment_db.values() if comment["post_id"] == post_id
    ]
    return comments


@post_router.get("/post_with_comments/{post_id}")
def get_post_with_comments(post_id: int) -> UserPostWithComments:
    post = get_post(post_id)
    if not post:
        raise HTTPException(404, "can not find the post.")
    comments = get_comments_by_post_id(post_id)
    return {"post": post, "comments": comments}
