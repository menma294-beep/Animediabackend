import uuid
from datetime import datetime
from app.services.neo4j_service import get_driver
from app.services.neo4j_service import run_query
import uuid
import cloudinary.uploader
from fastapi import UploadFile

def create_post(content: str, user_id: str):
    query = """
    MATCH (u:User {id: $user_id})
    CREATE (p:Post {
        id: randomUUID(),
        content: $content,
        created_at: datetime()
    })
    CREATE (u)-[:AUTHORED]->(p)
    RETURN p AS post, u AS user
    """
    record = run_query(query, {"content": content, "user_id": user_id}, single=True)

    if not record:
        return None

    return {
        "post": {
            "id": record["post"]["id"],
            "content": record["post"]["content"],
            "created_at": str(record["post"]["created_at"]),
        },
        "user": {
            "id": record["user"]["id"],
            "username": record["user"]["username"],
        }
    }
def get_all_posts():
    driver = get_driver()
    query = """
    MATCH (u:User)-[:AUTHORED]->(p:Post)
    RETURN p AS post, u AS user
    ORDER BY p.created_at DESC
    """
    with driver.session() as session:
        results = session.run(query)
        return [
            {
                "id": r["post"]["id"],
                "content": r["post"].get("content", None),
                "media_url": r["post"].get("media_url", None),
                "media_type": r["post"].get("media_type", None),
                "created_at": r["post"]["created_at"],
                "author_id": r["user"]["id"],
                "author_username": r["user"]["username"]
            }
            for r in results
        ]


def get_posts_by_user(user_id: str):
    driver = get_driver()
    query = """
    MATCH (u:User {id: $user_id})-[:AUTHORED]->(p:Post)
    RETURN p AS post, u AS user
    ORDER BY p.created_at DESC
    """
    with driver.session() as session:
        results = session.run(query, user_id=user_id)
        return [
            {
                "id": r["post"]["id"],
                "content": r["post"].get("content", None),
                "media_url": r["post"].get("media_url", None),
                "media_type": r["post"].get("media_type", None),
                "created_at": r["post"]["created_at"],
                "author_id": r["user"]["id"],
                "author_username": r["user"]["username"]
            }
            for r in results
        ]

def create_media_post(user_id: str, file: UploadFile, content: str = None):
    # Upload to Cloudinary
    upload_result = cloudinary.uploader.upload(file.file, resource_type="auto")

    media_url = upload_result.get("secure_url")
    media_type = "image" if upload_result.get("resource_type") == "image" else "video"

    query = """
    MATCH (u:User {id: $user_id})
    CREATE (p:Post {
        id: randomUUID(),
        content: $content,
        media_url: $media_url,
        media_type: $media_type,
        created_at: datetime()
    })
    CREATE (u)-[:AUTHORED]->(p)
    RETURN p AS post, u AS user
    """

    record = run_query(query, {
        "user_id": user_id,
        "content": content,
        "media_url": media_url,
        "media_type": media_type
    }, single=True)

    return {
        "post": {
            "id": record["post"]["id"],
            "content": record["post"]["content"],
            "media_url": record["post"]["media_url"],
            "media_type": record["post"]["media_type"],
            "created_at": str(record["post"]["created_at"])
        },
        "user": {
            "id": record["user"]["id"],
            "username": record["user"]["username"]
        }
    }