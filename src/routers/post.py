from typing import List, Union

from fastapi import APIRouter, HTTPException

from src.database.database import database
from src.models.post import (
    Comment,
    CommentIn,
    UserPost,
    UserPostIn,
    UserPostWithComments,
)

post_router = APIRouter()


@post_router.post("/post", status_code=201)
async def create_post(post: UserPostIn) -> UserPost:
    data = post.model_dump()
    query = f"INSERT INTO posts(body) VALUES('{data['body']}') RETURNING id;"
    last_post_id = await database.execute(query)
    return {"id": last_post_id, **data}


@post_router.get("/post/{id}")
async def get_post(id: int) -> Union[None, UserPost]:
    query = f"SELECT * FROM posts WHERE id={id};"
    res = await database.fetch_one(query)
    return res


@post_router.get("/posts")
async def get_posts() -> List[UserPost]:
    query = "SELECT id, body FROM posts;"
    res = await database.fetch_all(query)
    return res


@post_router.post("/comment", status_code=201)
async def create_comment(comment: CommentIn) -> Comment:
    post = await get_post(comment.post_id)
    if not post:
        raise HTTPException(404, "can not find the post.")
    data = comment.model_dump()
    query = f"""
            INSERT INTO comments(body, post_id) 
            VALUES('{data['body']}', {data['post_id']})
            RETURNING id
            ;
        """
    last_comment_id = await database.execute(query)
    return {"id": last_comment_id, **data}


@post_router.get("/post/{post_id}/comment")
async def get_comments_by_post_id(post_id: int) -> List[Comment]:
    query = f"""
        SELECT id, post_id, body 
        FROM comments 
        WHERE post_id={post_id}
        ;
    """
    res = await database.fetch_all(query)
    return res


@post_router.get("/post_with_comments/{post_id}")
async def get_post_with_comments(post_id: int) -> UserPostWithComments:
    post = await get_post(post_id)
    if not post:
        raise HTTPException(404, "can not find the post.")
    comments = await get_comments_by_post_id(post_id)
    return {"post": post, "comments": comments}
